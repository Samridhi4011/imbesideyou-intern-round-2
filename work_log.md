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