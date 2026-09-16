# From Operation Logs to an Automation Proposal

This project was developed as part of the Round 2 assignment for analyzing desktop operation logs, recovering business-process executions, identifying repetitive workflows, and building a working automation prototype.

The project follows the three main steps given in the assignment:

1. Recover process segments from raw operation logs.
2. Analyze the recovered processes and identify a suitable automation candidate.
3. Build a working prototype for the selected workflow.

---

## Project Overview

The main challenge in this assignment is that the raw operation logs contain continuous low-level user activity such as:

- Mouse clicks
- Keyboard input
- Browser interactions
- Application switching
- Clipboard activity
- Window changes
- Screenshots

These events do not directly tell us where one business process starts or ends.

I therefore started by using **Dataset A**, which contains ground truth, to experiment with different rule-based segmentation approaches. After validating the approach, I applied the selected method to **Dataset B**, which does not contain ground truth, and analyzed the recovered workflows for possible automation opportunities.

The final automation candidate was an **HR onboarding verification workflow** involving repeated reference-document usage and manual entry into an HR system.

---

## Repository Structure

```text
.
├── analysis/
│   ├── gt_segments.tsv
│   └── task_starts.tsv
│
├── data/
│   ├── dataset_a/
│   └── dataset_b/
│
├── outputs/
│   ├── dataset_a_segments_baseline.jsonl
│   ├── dataset_a_segments_v2.jsonl
│   ├── dataset_a_segments_v3.jsonl
│   └── dataset_b_segments.jsonl
│
├── prototype/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── README.md
│
├── src/
│   └── segment.py
│
├── work_log.md
└── README.md