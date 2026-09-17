# From Operation Logs to an Automation Proposal

## Candidate Information

- **Name:** Samridhi Singh
- **University:** Indian Institute of Technology Mandi
- **Department / Major:** Material Science Engineering
- **Email:** [Use the exact email address used in the Round 1 application]

---

## 1. Project Overview

This project analyzes desktop operation logs to identify coherent business
process executions, discover repetitive workflows, and build a working
automation prototype for a high-impact repetitive task.

The work was carried out in three stages:

1. **Process Recovery** — Recover meaningful work segments from continuous
   operation logs.
2. **Workflow Analysis** — Analyze the recovered Dataset B processes to
   identify repeated and automation-suitable workflows.
3. **Automation Prototype** — Build a working prototype for the selected
   automation opportunity.

Dataset A, which contains ground truth, was used to develop and validate
the segmentation approach. The resulting approach was then applied to
Dataset B, which does not contain ground truth.

---

## 2. Approach

### Step 1 — Process Segmentation

A rule-based segmentation approach was developed iteratively using
Dataset A.

Three versions were tested:

| Version | Approach | Result |
|---|---|---|
| V1 | 60-second inactivity rule | Under-segmented the activity |
| V2 | Browser navigation + application/window changes + inactivity | Over-segmented the activity |
| V3 | Browser/application/window signals with a 15-second minimum segment duration | Best balance among the tested approaches |

V3 produced **1,726 segments** compared with **1,696 GT reference
segments**.

The validation results for V3 included **844 predictions with IoU ≥ 0.5**
and an average best IoU of **0.464**.

V3 was then used to recover processes from Dataset B.

---

## 3. Dataset B Analysis

Applying the segmentation approach to Dataset B produced:

**343 recovered segments across 15 sessions.**

The recovered segments were analyzed using:

- Application usage
- Application co-occurrence
- Window titles
- Clipboard activity
- Keyboard and mouse interactions
- Browser form input
- Repeated patterns across sessions

One of the strongest repeated application combinations was:

**Microsoft Edge + Microsoft Word**

It appeared in **182 recovered segments across 9 of 15 sessions**.

Further event-level analysis revealed a more specific repeated workflow
within the HR onboarding system.

---

## 4. Selected Automation Candidate

The selected candidate is:

> **HR onboarding verification note preparation and entry**

The observed workflow can be summarized as:

```text
Reference information
        ↓
Prepare / copy information
        ↓
Paste into HR `ob-note` field
        ↓
Review
        ↓
Verification / completion action
```

The logs contained **89 explicit paste actions** into the same HR
onboarding field across **9 of 15 sessions**.

The browser events identified the target as:

```text
Field ID:       ob-note
Input type:     textarea
Input method:   paste
Label:          照合結果・特記事項を入力してください…
```

In **53 of the 89 cases**, Microsoft Word clipboard activity was observed
within the previous 30 seconds.

The logs also showed a repeated verification interaction after the note
was entered.

Because the actual clipboard contents are not available in the raw logs,
the analysis does not assume the exact text being transferred.

---

## 5. Automation Prototype

A self-contained web prototype was developed in:

```text
prototype/
```

The prototype demonstrates the identified workflow:

```text
Select reference document
        ↓
Prepare Note
        ↓
Note automatically populated
        ↓
Human review / editing
        ↓
照合完了
        ↓
Status → 完了
```

The prototype includes three representative reference documents observed
during Dataset B analysis:

- `nyusha_checklist_shinsotsu_batch`
- `gyomu_itaku_ukeire_tetsuzuki`
- `gyomu_itaku_kyuuyo_kitei`

The generated notes are representative demonstration content rather than
the actual production clipboard text.

### Human-in-the-loop

The final business decision is intentionally not automated.

The user can review and edit the prepared note before completing the
verification. Completion is also prevented when no note has been
prepared or when the note is empty.

This keeps the prototype focused on reducing repetitive data-entry work
while retaining human control over the final verification.

---

## 6. Why This Automation Approach

A deterministic web-based workflow was chosen because the identified
automation point is structured and repetitive.

A complex AI agent was not necessary for demonstrating the selected
automation opportunity.

The prototype focuses on:

- Reducing repetitive copy-paste/data-entry work
- Preparing information consistently
- Keeping the workflow understandable and controllable
- Retaining human review before completion

---

## 7. Expected Impact

The identified workflow involves repeated manual preparation and entry of
information into the same HR form field.

The analysis found:

- **89** explicit paste actions into `ob-note`
- **9/15 sessions** containing such activity
- **61/343 recovered segments** containing at least one such paste
- Repeated reference activity in Microsoft Word before many of the HR
  entries

The prototype demonstrates how the repetitive preparation and entry part
of this workflow could be reduced.

These numbers represent observed activity in the logs and should not be
interpreted as direct or guaranteed time savings.

---

## 8. Limitations

- The original HR application used during data collection was not
  available in the development environment.
- Its source code was not included in the repository.
- The raw logs do not expose the actual clipboard text.
- Therefore, the prototype is a self-contained demonstration rather than
  a direct integration with the original HR system.
- The current prototype uses representative note templates instead of
  production data.

A production implementation would require access to the actual HR system,
approved source documents and appropriate validation rules.
git 
---

## 9. Repository Structure

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
├── README.md
└── work_log.md
```

---

## 10. Running the Segmentation

From the repository root:

```bash
python src/segment.py
```

The generated segmentation outputs are stored under:

```text
outputs/
```

The Dataset B submission output is:

```text
outputs/dataset_b_segments.jsonl
```

Each segment follows the required format:

```json
{
  "session_id": "...",
  "start": "...Z",
  "end": "...Z",
  "label": "unknown_process"
}
```

---

## 11. Running the Prototype

From the repository root:

```bash
python -m http.server 8000 --directory prototype
```

Then open:

```text
http://localhost:8000
```

The prototype runs locally and does not require an external service.

For prototype-specific documentation, see:

```text
prototype/README.md
```

---

## 12. Documentation

### Work Log

`work_log.md` contains the detailed development history, including:

- Dataset exploration
- Segmentation experiments
- V1, V2 and V3 observations
- Dataset B workflow analysis
- Automation candidate selection
- Prototype development
- Prototype testing
- Major implementation decisions

### Prototype Documentation

`prototype/README.md` contains the prototype-specific workflow,
implementation details, testing steps and limitations.

---

## 13. Final Outcome

The project moves from raw desktop operation logs to a concrete,
working automation demonstration:

```text
Raw Operation Logs
        ↓
Process Segmentation
        ↓
Dataset B Workflow Analysis
        ↓
Repeated HR Onboarding Workflow
        ↓
Automation Candidate
        ↓
Working Prototype
```

The final prototype demonstrates a human-in-the-loop approach for
reducing repetitive HR onboarding note-entry work while keeping the final
verification decision under human control.