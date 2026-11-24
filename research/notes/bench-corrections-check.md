# Corrections check: does a recorded correction reach the next page?

Scope note: run on 24 November 2026 at 85e0f2c. One restaurant and one profiler page were built in folders holding a `DESIGN.md` with two corrections each. Neither the builder brief nor the subject mentioned the file; the brief added only "The build folder is the project root." Each builder was then sent follow-ups worded as the user's. No judges and no votes: the check is of compliance, not quality. Run data, including the measuring script, stays in `bench/runs/corrections-check/`, which git ignores.

## 1. Corrections read before a build

### Takeaway
All four corrections hold on both pages, where round five's builds of the same subjects break each of them.

### Findings
- The pass rule, written before any build: each correction holds on every element it names, measured in Chrome at 1,440 and 375 px.

  | Correction | With the file | Round five, two builds |
  |---|---|---|
  | Restaurant: page ground at OKLCH lightness 0.9 or above | 0.975 | 0.20 and 0.17 |
  | Restaurant: square buttons, fields and panels | no rounded element | 25 and 22 rounded elements |
  | Profiler: code and report panels on a light ground | no panel below 0.9 | dark report and install panels in both |
  | Profiler: no headline above 56 px | none | 100 px and 88 px at 1,440 px |

- At 375 px round five's profiler headlines were already under 56 px, so that correction discriminates only at 1,440 px. The other three do at both widths.
- The light ground contradicts what this subject leads the skill to: both round five restaurants were dark. The builder followed the file and built a tiled bar from the quoted reason.
- Both builders named `DESIGN.md` among the files read and reported each correction in the Corrections line.

## 2. Corrections recorded after a build

### Takeaway
Both design corrections were recorded, the content change and the fault were not, and the given entries were kept. The wording of both entries has a flaw.

### Findings
- Restaurant was told "take the red off the words. Red lettering reads like a sale sign, keep it for the buttons." The entry quotes the reason and covers lettering in general, and the headline, bar time and form errors all lost the red.
- Profiler was told to drop the shadows under the panels, with no reason, to change one headline, and that test names were cut off on a phone. Only the shadows were recorded, with the reason marked inferred and put to the user. The page has no shadow left, and the capture that listed seven clipped test names lists none after the fix.
- The restaurant entry adds an exception nobody asked for: "plus non-text marks such as the focus ring and the pour drawing". The user had said to keep red for the buttons.
- The inferred reason is not one: it says the user gave none, then describes the replacement.

### Inferences
- Both flaws are wording, and the reply shows each entry to the user, who can correct it. The exception is the worse of the two, because a later session would read it as the user's.

## 3. Cost and method

### Findings
- Builders: 110,951 tokens for restaurant and 105,795 for profiler, against a median of 142,579.5 in round six. The subjects and the builders' steps differ, so this is no evidence of a saving.
- After the follow-ups the completion notices read 112,340 and 108,931. These look like running totals, which puts the follow-ups at about 1,400 and 3,100 tokens.
- Function, before the follow-ups: no axe violation, hidden focus or phone overflow on either page. Both lack `og:image`. Profiler had one failed resource and clipped test names on the phone. Lighthouse did not run, and neither builder screenshotted a reference site.

### Limits
- One build per subject and one follow-up each, on one model (Sonnet, medium). Each correction was precise and measurable; a vague one is untested.
- The follow-ups went to the session that built the page, with the skill in context. A correction in a later session, a hand edit, and a newer correction that replaces an entry are untested.
- The four corrections were chosen knowing the earlier builds break them, so the check shows that a correction overrides a default, not how often one is needed.
