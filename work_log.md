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