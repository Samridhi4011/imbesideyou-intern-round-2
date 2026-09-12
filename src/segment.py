import json
import sys
from datetime import datetime, timezone
from pathlib import Path


MIN_SEGMENT_SECONDS = 15


def parse_timestamp(event):
    value = event.get("timestamp_iso") or event.get("ts_utc")

    if not value:
        return None

    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_events(session_dir):
    events = []

    for path in sorted(session_dir.glob("chunk_*/events.jsonl")):
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    event = json.loads(line)
                    timestamp = parse_timestamp(event)

                    if timestamp:
                        events.append((timestamp, event))

                except json.JSONDecodeError:
                    continue

    events.sort(key=lambda x: x[0])
    return events


def app_identity(event):
    app = event.get("context", {}).get("active_app") or {}

    return (
        app.get("process_name"),
        app.get("app_name"),
        app.get("window_title"),
    )


def is_boundary_candidate(previous_event, current_event):
    current_type = current_event.get("event_type")

    # Browser navigation is a strong process-change candidate,
    # but it is not treated as a boundary by itself without
    # the minimum-segment safeguard below.
    if current_type == "browser_navigation":
        return True

    # Only treat app_switch as meaningful when the application
    # or window actually changes.
    if current_type == "app_switch":
        previous_app = app_identity(previous_event)
        current_app = app_identity(current_event)

        previous_process, previous_name, previous_title = previous_app
        current_process, current_name, current_title = current_app

        if previous_process != current_process:
            return True

        if previous_name != current_name:
            return True

        if previous_title != current_title:
            return True

    # Window changes are weaker candidates.
    if current_type in {
        "window_title_change",
        "window_state_change",
    }:
        return True

    return False


def segment_events(events):
    if not events:
        return []

    segments = []

    start = events[0][0]
    previous_timestamp, previous_event = events[0]

    for timestamp, event in events[1:]:

        candidate = is_boundary_candidate(
            previous_event,
            event
        )

        current_duration = (
            previous_timestamp - start
        ).total_seconds()

        # Do not create very short segments.
        if candidate and current_duration >= MIN_SEGMENT_SECONDS:
            segments.append((start, previous_timestamp))
            start = timestamp

        previous_timestamp = timestamp
        previous_event = event

    segments.append((start, previous_timestamp))

    # Merge any short segments produced near boundaries.
    merged = []

    for segment in segments:

        duration = segment[1] - segment[0]

        if merged and duration.total_seconds() < MIN_SEGMENT_SECONDS:
            merged[-1] = (
                merged[-1][0],
                segment[1]
            )
        else:
            merged.append(segment)

    return merged


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python src/segment.py "
            "<dataset_dir> <output_file>"
        )
        sys.exit(1)

    dataset_dir = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    all_segments = []

    for session_dir in sorted(dataset_dir.glob("ses_*")):

        events = load_events(session_dir)
        segments = segment_events(events)

        for start, end in segments:
            all_segments.append({
                "session_id": session_dir.name,
                "start": start.astimezone(timezone.utc)
                    .isoformat()
                    .replace("+00:00", "Z"),
                "end": end.astimezone(timezone.utc)
                    .isoformat()
                    .replace("+00:00", "Z"),
                "label": "unknown_process"
            })

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_file.open("w", encoding="utf-8") as f:
        for segment in all_segments:
            f.write(
                json.dumps(
                    segment,
                    ensure_ascii=False
                ) + "\n"
            )

    print(f"Created {len(all_segments)} segments")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()