# Work Log

## Day 1 — Project Setup & Understandings

### Objective
Today I went through the assignment and tried to understand what exactly
is expected in the second round.

I also read the `DATA_SCHEMA.md` and the `README.md` file to understand what kind of data is
provided and what information is available in the logs.

The task basically has three main parts as described in the readme:
1. Find individual work/process segments from the logs.
2. Analyze these processes and decide which ones are good candidates
   for automation.
3. Build a working automation for the process that seems to have the
   highest impact.

I also created the GitHub repository and set up the basic project
structure.

### What I understood so far

- Dataset A has ground truth, so I can use it to test whether my
  segmentation approach is working.
- Dataset B does not have ground truth and is the actual dataset that
  needs to be analyzed.
- A and B are from different departments and use different applications,
  so I should not make assumptions based only on Dataset A.

  ### Initial thoughts

For identifying different work units, I think some useful signals could
be the time between events, application switches, window/context
information, browser activity and user interactions.

Screen text and screenshots might also help when the other information
is not enough.

At this point these are only initial ideas. I have not tested them on
the actual data yet.

### Decision

I don't want to decide the final segmentation method before looking at
the actual events. I will first explore Dataset A and compare what I
observe with its ground truth.

### Next

Start exploring Dataset A and look at some actual sessions and events.

----------------------------------------------------------------------------------------------------------

## Day 2 — Dataset A Exploration

- Started exploring Dataset A using the ground truth in `gt.jsonl`.
- First looked at the `task_started` events to understand what individual tasks look like.
- Checked a few examples from processes K and A.
- Compared the ground-truth task timestamps with the raw events in `events.jsonl`.
- Observed that the same task can involve multiple actions such as clicking, typing, form input, clipboard operations and switching between applications.
- In some examples, Chrome was the main application while Notepad and clipboard operations were also involved.
- This made it clear that a business process cannot be identified only by looking at one application or one type of event.
- I also noticed that the raw events contain a lot of low-level activity, so I need to find useful signals rather than treating every event equally.

### Initial observation

The time gap between events, application changes and user activity seem like useful signals for finding process boundaries.

However, I do not want to rely only on time gaps because a user can switch to another application or temporarily stop working on a process and then return to it.

### Decision

I will start with a simple rule-based baseline and test it against Dataset A ground truth. Based on the results, I can improve the segmentation logic if needed.

### Next-

Implement the first segmentation script and evaluate it on Dataset A.

----------------------------------------------------------------------------------------------------------

## Segmentation Experiments — Dataset A

### Baseline V1

- I first tried a simple rule-based approach where a new segment was created whenever there was more than 60 seconds of inactivity.
- This produced 104 segments, while the GT reference had 1,696 clean process segments.
- Only 16 predicted segments had an IoU of at least 0.5, with an average best IoU of 0.29.
- This made it clear that the 60-second inactivity rule was too simple and was merging many separate processes together.

### V2 Experiment

- I then looked at the raw events around the GT process boundaries to understand which events might help identify a new process.
- `app_switch` appeared frequently around boundaries, but it was not reliable on its own because it could also happen when switching between windows of the same application.
- `screenshot_smart` was also not useful as a direct boundary signal since it is generated regularly as part of the recording process.
- One interesting pattern was `browser_navigation`: it appeared around 52.9% of GT boundaries, but only around 1.1% of the normal activity windows I checked.
- `app_switch` appeared around 53.6% of boundaries and 19.3% of normal windows, so I treated it as a supporting signal rather than a main boundary indicator.
- Based on these observations, I implemented a second rule-based version combining browser navigation, application/window changes, and inactivity.
- V2 produced 2,655 segments.
- 535 of these had an IoU of at least 0.5, but the average best IoU dropped to 0.262.
- So V2 improved the number of reasonably matching segments compared with V1, but it also created too many small segments. In other words, V1 was under-segmenting while V2 was over-segmenting.
- I am therefore treating V2 as an intermediate experiment rather than the final approach.

### Next Step

- I will look more closely at GT boundaries where `browser_navigation` is not present.
- The goal is to find additional reliable patterns that can help balance the segmentation instead of relying too heavily on any single event type.


### V3 Experiment

- V2 produced 2,655 segments, so it was clearly cutting the event stream too often.
- I looked more closely at the events around the GT process boundaries. This showed that `app_switch` by itself was too noisy, while browser navigation and actual application/window changes were more useful signals.
- Based on this, I tried a third rule-based version that treats these events as possible boundary points, but avoids creating very short segments by keeping a minimum segment duration.
- V3 produced 1,726 segments, which is much closer to the 1,696 GT reference segments.
- 844 predicted segments had an IoU of at least 0.5, with an average best IoU of 0.464.
- This was a clear improvement over both earlier attempts: V1 had an average best IoU of 0.290, while V2 had 0.262.
- For now, V3 looks like the most promising approach. I will do one more round of error analysis before deciding whether it is good enough to apply to Dataset B.

### Next Step

- Look at where V3 is still getting the boundaries wrong and see if a small adjustment can improve the results without bringing back the over-segmentation seen in V2.

----------------------------------------------------------------------------------------------------------

## Dataset B Exploration

- After getting a reasonably good result from V3 on Dataset A, I added Dataset B to the repository and applied the segmentation approach to it.
- Since Dataset B does not have ground truth, I could not directly calculate IoU or compare the boundaries in the same way as Dataset A.
- The initial recovery produced 343 segments across 15 sessions.
- I first checked the basic segment statistics such as duration, number of segments per session and the distribution of segment lengths.
- Most recovered segments were relatively short. The median duration was around 23 seconds and the average was around 28 seconds.
- I then looked at the event types inside the recovered segments to understand what kind of work was actually happening.

### Application Patterns

- I checked which applications commonly appeared together inside the recovered segments.
- The strongest combination was Microsoft Edge + Microsoft Word, appearing in 182 recovered segments.
- This combination was present across 9 different sessions, so it was not limited to just one user/session.
- I also looked at the window titles and found repeated combinations of specific business systems in Edge and specific Word documents.
- Some of the repeated Edge systems were the financial accounting system, HR/payroll system and order/inventory management system.
- The same Word documents also appeared repeatedly with these systems.

### Edge + Word Workflow

- I inspected actual event sequences from the Edge + Word segments instead of relying only on frequency counts.
- A repeated pattern was visible where the user worked in Edge, switched to Word for a short period, and then returned to Edge.
- After returning to Edge, clipboard changes were often followed by keyboard shortcuts, keystrokes and browser form input.
- This looks like a repeated reference/copy-and-enter type of workflow rather than random application switching.
- I also noticed that `screenshot_smart` appears regularly during active work, so I do not want to use it as a process boundary by itself.
- Similarly, `app_switch` is useful as a supporting signal but should not be treated as a boundary on its own.

### Current Understanding

At this point, the Dataset B analysis is showing that there are repeated workflows involving a business system in Edge and supporting work in Word/other applications.

The Edge + Word workflow looks particularly interesting because it occurs frequently and contains repetitive interactions such as clicking, typing, clipboard activity and browser form input.

However, I still need to understand what the user is actually accomplishing in these workflows before choosing the final automation candidate. Frequency alone is not enough to decide which process should be automated.

### Next Step

- Inspect the most frequent repeated workflows in more detail.
- Estimate which workflow has the highest combination of frequency, time spent and repetitive manual interaction.

### V3 Investigation — Missing Raw Event Capture 
- During V3 validation, I found some sessions where the ground-truth process timeline extends beyond the available raw event capture. For example, one session had a later chunk manifest but no corresponding events.jsonl, so the raw-event loader could only recover the events that were actually available. I treated this as missing capture rather than artificially creating process boundaries from ground truth.

### Decision on V4

- Initially, I was planning to build a V4 segmentation approach because V3 still had a significant number of low-IoU cases.
- Before changing the algorithm, I checked some of the cases where V3 had no overlap with the GT.
- This investigation showed that at least some of these cases were caused by missing raw event capture rather than incorrect segmentation logic. In one session, the GT timeline continued into a later chunk, but that chunk did not contain an `events.jsonl` file.
- Because there were no raw events available for that part of the session, changing the segmentation rules would not actually solve the problem.
- I therefore decided not to build V4 just for the sake of another iteration. Instead, I will keep V3 as the current segmentation approach and move forward with the recovered Dataset B processes for workflow analysis and automation candidate selection.

### Next Step

- Analyze the recovered Dataset B workflows in more detail.
- Compare their frequency, duration and amount of repetitive manual interaction.
- Use these observations to select the workflow with the strongest potential for automation.

----------------------------------------------------------------------------------------------------------
### DAY-5

### HR Onboarding Workflow Candidate

- While inspecting the repeated Edge + Word activity, I looked more closely at browser form input events in Dataset B.
- I found 89 explicit paste actions into the same HR onboarding form field (`ob-note`) across 9 of the 15 sessions.
- The field is a textarea labelled `照合結果・特記事項を入力してください…`, and the logs explicitly record the input method as `paste`.
- 61 of the 343 recovered Dataset B segments contain at least one paste into this field, which is about 17.8% of all recovered segments.
- The paste actions are repeated within individual sessions, with one session containing 23 such paste events.
- I also checked the activity before these paste events. In 53 of the 89 cases, a Microsoft Word clipboard change occurred within the previous 30 seconds.
- The average time between the Word clipboard change and the HR form paste was about 15.2 seconds.
- Repeated Word reference documents included onboarding checklists and procedure documents such as `nyusha_checklist_shinsotsu_batch`, `gyomu_itaku_ukeire_tetsuzuki` and `gyomu_itaku_kyuuyo_kitei`.
- The exact clipboard contents are not available in the logs, so I am not assuming what specific text is being transferred.
- Based on the frequency, repetition and clearly identifiable target field, I selected HR onboarding note entry as the main automation candidate for Step 3.

### Automation Scope

The prototype will focus on assisting with the repetitive entry of reference
information into the HR onboarding `ob-note` field.

The goal is not to fully automate the business decision itself. The prototype
will prepare or enter the information and leave the final review/confirmation
to the user.

### Workflow Interaction Analysis

- I inspected the events immediately following the `ob-note` paste actions to understand what the user does next.
- The logs showed that the paste is consistently followed by a mouse/browser click in the HR application within about half a second.
- The browser event identifies the clicked element as a button with the ID `btn-ob-ok` and class `btn success`.
- The corresponding screenshots show a completion notification such as `照合完了しました` after this interaction.
- This suggests that the repeated workflow is not only note entry, but also includes a specific verification/completion action after the note is entered.
- - I therefore refined the automation scope to focus on preparing/filling the identified `ob-note` field and supporting the corresponding verification action, while retaining human review before completion.
- I will keep the prototype generic rather than hard-coding a particular employee or record, since the logs contain multiple record IDs and local application instances.

**### Automation Prototype**

- I implemented a small web-based prototype for the selected HR onboarding workflow.
- The prototype was kept separate from the segmentation and analysis code under the `prototype/` directory.
- The interface was designed around the workflow observed in the logs, including the HR onboarding context, a reference-document selector, the `ob-note` textarea and the verification completion action.
- The prototype currently supports three reference documents that were repeatedly observed during the Dataset B analysis:
  - `nyusha_checklist_shinsotsu_batch`
  - `gyomu_itaku_ukeire_tetsuzuki`
  - `gyomu_itaku_kyuuyo_kitei`
- Selecting a reference document and clicking `Transfer Reference to HR Note` automatically prepares and inserts a corresponding note into the `ob-note` field.
- The generated note can be manually edited before completion.
- The `照合完了` action remains disabled until a note has been prepared, providing a basic safety check.
- After human review, the user can complete the verification and the prototype changes the record status to `完了`.

**### Prototype Testing**

I tested the prototype using the following cases:

- Prepared a note using the first reference document.
- Manually edited the generated note before completing the verification.
- Completed the verification successfully after review.
- Tested all three reference-document options and confirmed that each produced a different note.
- Confirmed that the completion action cannot be triggered before preparing a note.
- Tested the empty-note case and confirmed that verification is not completed when the note is empty.

All of the above test cases behaved as expected.

**### Implementation Decision**

- I chose a small deterministic web-based prototype rather than a more complex AI agent because the identified automation point is a repetitive and clearly defined form-entry interaction.
- The prototype focuses on reducing repetitive data-entry work rather than attempting to automate the underlying HR decision.
- Human review is intentionally retained before completion because the raw logs do not expose the actual clipboard text or enough business context to determine whether a particular note is correct.
- The original HR application used during data collection was not available in the current development environment, so the prototype reproduces the relevant observed interaction as a self-contained local demonstration rather than connecting to the original application.

----------------------------------------------------------------------------------------------------------

**### Level 1 — Working Browser Automation**

- After completing the initial prototype, I wanted to check whether the workflow could be automated through an actual browser interaction rather than only simulating the steps in the UI.
- I decided to start with a small Level 1 automation instead of immediately trying to integrate Microsoft Word or the original HR application. This keeps the scope manageable and also gives me a working baseline before adding more complexity.
- I added Playwright as a project dependency and used the locally installed Google Chrome browser for the automation.
- The automation script is kept separately under the `automation/` directory.
- The current automation opens the local HR onboarding prototype, selects a reference document, clicks the `Transfer Reference to HR Note` action, and checks whether the `ob-note` field has actually been populated.
- This means the browser interaction itself is automated rather than being performed manually by the user.
- I intentionally stop the automation after the note is populated and leave the record in the human-review stage. The final `照合完了` action is still performed by the user.

**### Automation Testing**

- I tested the automation on the local HR onboarding prototype using Google Chrome.
- The script successfully opened the HR application in the browser.
- It successfully selected the reference document and triggered the reference-to-HR transfer action.
- The `ob-note` field was populated successfully, and the script verified that the field was not empty.
- The automation then stopped and reported that human review was required.
- This confirmed that the basic browser automation works end-to-end for the selected interaction.

**### Current Limitation**

- The current Level 1 automation does not directly read content from a live Microsoft Word application.
- The reference information used by the prototype is still represented by predefined reference data, since the raw Dataset B logs do not expose the actual clipboard text.
- Therefore, I am treating this version as a working browser-automation baseline rather than claiming that it already performs full Word-to-HR data extraction.

**### Next Step**

- Since the basic browser automation is working, I can now consider extending the input side so that the automation can work with an actual reference file instead of predefined reference data.
- I will only add this extra layer if it can be done reliably within the remaining time, without making the current working prototype unstable.

**### Level 1 Update — Reference File Integration**

- I extended the Level 1 automation so that the reference information is no longer kept directly inside the automation script.
- I created a separate reference file under `automation/references/` and moved the onboarding reference information into it.
- The automation script now reads this reference file before opening the HR onboarding page.
- After reading the file, Playwright opens the HR prototype in Chrome and directly fills the `ob-note` field with the contents of the reference file.
- I tested this flow multiple times and confirmed that the reference file is read successfully and the HR note is populated automatically.
- The automation still stops at the human-review stage, so the final verification is not completed automatically.
- This makes the Level 1 prototype closer to the intended workflow while keeping the implementation simple and reliable.

**### Level 1 Status**

- The browser automation is now working end-to-end with an external reference file.
- The current implementation demonstrates automatic reference-file-to-HR-form transfer followed by human review.
- I will keep this working version as the baseline before deciding whether to attempt actual `.docx` / Microsoft Word integration.