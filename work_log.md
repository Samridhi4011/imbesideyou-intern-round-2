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

