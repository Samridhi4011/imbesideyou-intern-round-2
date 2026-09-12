import json
import sys
from datetime import datetime, timezone
from pathlib import Path


INACTIVITY_GAP_SECONDS = 10
BOUNDARY_SCORE_THRESHOLD = 3


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


def boundary_score(previous_event, current_event, gap):
    score = 0
    event_type = current_event.get("event_type")

    # Strong signal discovered during Dataset A exploration.
    if event_type == "browser_navigation":
        score += 3

    # app_switch happens frequently even within Chrome.
    # Only count it when the actual application/window changes.
    if event_type == "app_switch":
        previous_app = app_identity(previous_event)
        current_app = app_identity(current_event)

        if previous_app != current_app:
            score += 2

    if event_type == "window_title_change":
        score += 1

    if event_type == "window_state_change":
        score += 1

    # Keep inactivity as an additional signal, but lower the
    # threshold substantially compared with the baseline.
    if gap > INACTIVITY_GAP_SECONDS:
        score += 3

    return score


def segment_events(events):
    if not events:
        return []

    segments = []

    start = events[0][0]
    previous_timestamp, previous_event = events[0]

    for timestamp, event in events[1:]:
        gap = (timestamp - previous_timestamp).total_seconds()

        score = boundary_score(
            previous_event,
            event,
            gap
        )

        if score >= BOUNDARY_SCORE_THRESHOLD:
            segments.append((start, previous_timestamp))
            start = timestamp

        previous_timestamp = timestamp
        previous_event = event

    segments.append((start, previous_timestamp))

    return segments


def main():
    if len(sys.argv) != 3:
        print("Usage: python src/segment.py <dataset_dir> <output_file>")
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

    output_file.parent.mkdir(parents=True, exist_ok=True)

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