import json
import sys
from datetime import datetime, timezone
from pathlib import Path


INACTIVITY_GAP_SECONDS = 60


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


def segment_events(events):
    if not events:
        return []

    segments = []
    start = events[0][0]
    previous = events[0][0]

    for timestamp, _ in events[1:]:
        gap = (timestamp - previous).total_seconds()

        if gap > INACTIVITY_GAP_SECONDS:
            segments.append((start, previous))
            start = timestamp

        previous = timestamp

    segments.append((start, previous))
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
            f.write(json.dumps(segment, ensure_ascii=False) + "\n")

    print(f"Created {len(all_segments)} segments")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()