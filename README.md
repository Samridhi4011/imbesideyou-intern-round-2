# ImBesideYou Internship Round 2 — Operation Logs to Automation

## Candidate Information

- **Name:** Samridhi Singh
- **Institute:** Indian Institute of Technology Mandi
- **Department:** Material Science Engineering
- **Email:** b24382@students.iitmandi.ac.in
---

## 1. Project Overview

This project analyzes desktop operation logs to:

1. Recover coherent business-process executions from raw operation logs.
2. Analyze Dataset B to identify repetitive and automation-suitable workflows.
3. Build a working automation prototype for a selected workflow.

The approach was first developed and validated on **Dataset A**, which contains ground-truth annotations, and then applied to **Dataset B**.

---

## 2. Process Segmentation

### Dataset A

Dataset A was used to understand how business processes appear in continuous desktop activity and to validate segmentation approaches against the provided ground truth.

Three approaches were explored:

- **V1:** Inactivity-based segmentation.
- **V2:** Inactivity combined with browser and application/window changes.
- **V3:** Event-based segmentation using browser navigation, application/window changes, and minimum segment duration.

V1 significantly under-segmented the activity, while V2 produced too many small segments. V3 produced a segment count close to the ground-truth count and was therefore retained as the final baseline.

The main observation was that a business task is not necessarily restricted to one application or one continuous interaction pattern.

### Dataset A Validation Results

The segmentation approaches were compared against the ground-truth process segments provided with Dataset A.

- **V1:** Produced 104 segments and significantly under-segmented the activity. Only 16 predicted segments achieved IoU >= 0.5.
- **V2:** Produced 2,655 segments and showed strong over-segmentation, with many short segments.
- **V3:** Produced 1,726 segments compared with 1,696 ground-truth segments.

V3 was retained as the final baseline because its segmentation granularity was much closer to the provided ground truth than the earlier approaches.

During validation, some mismatches were also traced to missing raw event capture in certain sessions. The assignment data notes that missing raw capture can occur, so these cases were treated separately from segmentation errors.

### Dataset B

The V3 segmentation approach was applied to Dataset B, producing:

- **15 sessions**
- **343 recovered process segments**

The recovered segments were then analyzed using application usage, event patterns, clipboard activity, durations, and repeated workflow structures.

---

## 3. Dataset B Analysis

Repeated workflows involving **Microsoft Edge, Word, clipboard operations, and HR-related web forms** were identified.

A particularly repetitive pattern was:

**Reference document → Clipboard/Text transfer → HR onboarding form → Human verification**

The analysis found repeated interactions with the HR onboarding system, including form entries into the `ob-note` field.

Key observations:

- 89 explicit paste actions into the HR `ob-note` field.
- These occurred across 9 of the 15 Dataset B sessions.
- 61 of the 343 recovered segments contained at least one such paste action.
- In many cases, Word-based reference activity occurred shortly before the HR form entry.

Since the original clipboard text is not available for all events, the analysis does not assume the exact text being transferred.

---

## 4. Selected Automation Candidate

### HR Onboarding Reference-to-Form Entry

The selected workflow is the repetitive preparation and transfer of reference information into the HR onboarding form.

The prototype focuses on automating the repetitive **reference-to-form entry** step while keeping the final verification with a human.

### Candidate Selection

Other repeated Edge + Word workflows were also observed in Dataset B. The HR onboarding workflow was selected because the automation point was particularly clear in the logs:

- Repeated interaction with the HR onboarding system.
- Repeated paste actions into the same `ob-note` field.
- Reference/document activity occurring shortly before several of these entries.
- A clear human verification step following the data entry.

This made the workflow suitable for a small, deterministic automation prototype while keeping the final verification under human control.

### Scope

**Automated:**
- Read reference information.
- Prepare the relevant note.
- Transfer it into the HR `ob-note` field.
- Provide browser-level interaction.

**Manual:**
- Review the generated/prepared information.
- Perform the final verification/confirmation.

This keeps the prototype focused on the repetitive part of the workflow without attempting to automate the HR decision itself.

---

## 5. Automation Prototype

A lightweight local web prototype was created using:

- HTML
- CSS
- JavaScript

The prototype provides:

- HR onboarding form context.
- Reference document selection.
- Reference-to-note transfer.
- Human review status.
- Completion/verification action.

The workflow is represented as:

**Reference Document → Prepare & Transfer → HR Form → Human Review → Completion**

The prototype is intentionally deterministic and demonstrates the selected workflow without requiring a production HR system.

---

## 6. Expected Impact

The automation targets a repetitive reference-to-form entry step rather than the complete HR onboarding process.

The main expected benefits are:

- Reduced repetitive copying and typing.
- Fewer manual interactions required for repeated note preparation.
- More consistent transfer of reference information into the target form.
- Reduced opportunity for transcription errors during the repetitive entry step.

The available logs do not provide enough information to claim a precise production-wide time saving. Therefore, the prototype is evaluated primarily as a proof of the automation opportunity rather than as a measured production deployment.

## 7. Alternatives Considered

### Fully Autonomous HR Decision

A fully autonomous system was not selected because the logs do not provide sufficient information to reliably automate the final HR verification or approval decision.

### AI Agent-Based Automation

An AI agent was not necessary for the selected workflow because the observed interaction is structured and repetitive. A deterministic browser workflow is easier to test and provides more predictable behavior for this use case.

### Direct Production HR Integration

Direct integration with the original HR system was not attempted because the available assignment environment does not provide a production API or integration interface. The local prototype was therefore used to demonstrate the automation flow.

## 8. Browser Automation

The automation uses the installed Google Chrome browser to:

1. Open the local HR onboarding prototype.
2. Extract the relevant reference information from the DOCX file.
3. Populate the `ob-note` field automatically.
4. Verify that the field has been populated.
5. Stop at the human-review stage.

### Level 1 — Reference File Automation

The first browser automation version:

1. Reads a local reference file.
2. Opens the HR onboarding prototype.
3. Transfers the reference information into `#ob-note`.
4. Verifies that the field was populated.
5. Stops for human review.

This established a working browser automation flow.

### Level 2 — DOCX-Based Automation

The automation was then extended to work with a `.docx` reference document.

Flow:

**DOCX → Text Extraction → Relevant Notes → Playwright → HR `ob-note` → Human Review**

The DOCX content is extracted using **Mammoth**. The automation identifies the `Notes for HR` section and uses the relevant information to populate the HR form.

The final Level 2 flow is:

```text
onboarding_reference.docx
        ↓
Mammoth text extraction
        ↓
Notes for HR extraction
        ↓
Playwright browser automation
        ↓
HR onboarding #ob-note
        ↓
Human review
```

The Level 2 automation was tested end-to-end successfully. Final HR verification remains manual.

---

## 9. Why This Approach

A deterministic workflow was chosen because the identified task is repetitive and structured.

The prototype focuses on automating the clearly observable reference-to-form entry step while keeping the final HR verification with a human.

A fully autonomous HR decision-making system was not attempted because the available logs do not provide sufficient information to automate the final decision reliably.

---

## How to Run

### Install Dependencies

From the repository root, install the required Node.js dependencies:

```bash
npm install
```

### Run the HR Prototype

Start the local web server using:

```bash
python3 -m http.server 8000 -d prototype
```

Then open the following URL in your browser:

```text
http://localhost:8000
```

The prototype provides the HR onboarding interface and allows the reference information to be transferred into the `ob-note` field.

### Run the Browser Automation

Keep the prototype server running and open a second terminal in the repository root.

Run:

```bash
node automation/automate_hr.js
```

The automation uses the installed Google Chrome browser to:

1. Open the local HR onboarding prototype.
2. Extract the relevant reference information from the DOCX file.
3. Populate the `ob-note` field automatically.
4. Verify that the field has been populated.
5. Stop at the human-review stage.

The final HR verification remains a manual step.

### Dataset B Output

The generated Dataset B segmentation output is available at:

```text
outputs/dataset_b_segments.jsonl
```

## 10. Limitations

- Dataset B does not contain ground-truth segmentation.
- Some raw event information, including clipboard text, is unavailable.
- The prototype uses a controlled local HR interface rather than the original production system.
- DOCX extraction currently uses the `Notes for HR` section as the information source.
- The automation does not make HR decisions.
- Final verification remains manual.

---

## 11. Repository Structure

```text
.
├── analysis/
│   ├── gt_segments.tsv
│   └── task_starts.tsv
├── automation/
│   ├── references/
│   ├── automate_hr.js
│   └── extract_reference.js
├── data/
│   ├── dataset_a/
│   └── dataset_b/
├── docs/
├── outputs/
├── prototype/
│   ├── app.js
│   ├── index.html
│   ├── README.md
│   └── style.css
├── src/
│   └── segment.py
├── .gitignore
├── package.json
├── package-lock.json
├── README.md
└── work_log.md