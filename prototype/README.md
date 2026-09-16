# HR Onboarding Automation Prototype

## Overview

This directory contains a small web-based prototype created for the
automation stage of the assignment.

The prototype is based on a repetitive workflow identified during the
analysis of Dataset B. The observed workflow involved using reference
information from Microsoft Word documents and entering the relevant
information into an HR onboarding system.

The prototype demonstrates how this repetitive note-entry step can be
assisted through a simple web interface while keeping a human review
step before completion.

---

## Automation Workflow

The workflow identified from Dataset B can be summarized as:

Reference document
        ↓
Review/reference information
        ↓
Prepare verification note
        ↓
Enter note into HR `ob-note` field
        ↓
Human review
        ↓
Complete verification

The prototype focuses mainly on the preparation and entry of the
verification note and the subsequent completion action.

---

## Why This Workflow Was Selected

During Dataset B analysis, repeated paste actions into the same HR
onboarding field were observed.

The logs contained:

- 89 explicit paste actions into the `ob-note` field
- Activity across 9 of 15 sessions
- 61 recovered segments containing at least one such paste
- Repeated reference activity in Microsoft Word before many of these
  paste actions

The browser events also identified the target field as:

- Field ID: `ob-note`
- Input type: `textarea`
- Input method: `paste`
- Label: `照合結果・特記事項を入力してください…`

The logs also showed a repeated verification action after the note was
entered.

These observations motivated the prototype.

---

## What the Prototype Does

The prototype provides a simplified HR onboarding interface.

A user can:

1. Select one of the observed reference documents.
2. Click **Prepare Note**.
3. Automatically populate the `ob-note` field with representative
   verification information.
4. Review and edit the generated note.
5. Click **照合完了** to complete the verification.
6. See the record status change from review to completed.

The three reference documents represented in the prototype are:

- `nyusha_checklist_shinsotsu_batch`
- `gyomu_itaku_ukeire_tetsuzuki`
- `gyomu_itaku_kyuuyo_kitei`

Each reference option produces a different representative note.

---

## Human Review

Human review is intentionally retained in the prototype.

After a note is prepared, the user can edit the text before completing
the verification.

The completion button is not available before a note has been prepared,
and an empty note cannot be submitted.

This reflects the intended automation scope: reduce repetitive data-entry
work without automatically making the underlying HR verification
decision.

---

## Prototype Structure

```text
prototype/
├── index.html
├── style.css
├── app.js
└── README.md