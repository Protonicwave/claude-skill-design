# Bench round seven: web-ui-craft against Taste Skill

Scope note: run on 24 November 2026. Arm `taste-skill` is the `skills/taste-skill` folder of github.com/Leonxlnx/taste-skill (version 2.5.1, MIT) at commit 6c0b5c78f5d31776e2210305abaa210cdc0030bf, copied whole. It built restaurant and profiler twice each. Arm `web-ui-craft` had no new builds: round six's restaurant builds and round five's profiler builds were recaptured. Run i was paired with run i in each subject: four pairs, eight verdicts, one voter on all four. Builders ran on Sonnet and judges on Opus, both at medium effort; the model behind the older profiler builds was not checked. Run data stays in `bench/runs/round-7/`, which git ignores.

## 1. Outcome

### Takeaway
A tie by the rule settled before the round, under which a vote decides its pair. Judges chose web-ui-craft on every criterion; the voter split 2 to 2, choosing Taste Skill on both profiler pairs. No further competitor round until a competitor ships a major version.

### Findings
- Judges, web-ui-craft against Taste Skill: first screen, whole page, imagery, type, motion, fit and overall each 4 wins, 0 ties, 0 losses. Both orders agreed on every pair and page A was chosen in 4 of 8 overall choices.
- Judges and voter agreed on two of four pairs:

  | Pair | Subject | Judges | Vote |
  |---|---|---|---|
  | p01 | restaurant, run 1 | web-ui-craft | web-ui-craft |
  | p02 | restaurant, run 2 | web-ui-craft | web-ui-craft |
  | p03 | profiler, run 2 | web-ui-craft | Taste Skill |
  | p04 | profiler, run 1 | web-ui-craft | Taste Skill |

- The tie is by votes. Taken alone, the judges give web-ui-craft 4 to 0. A vote carries no reason or criterion, so why the voter preferred Taste Skill's profiler pages is not known.

## 2. What the judges named

### Takeaway
Taste Skill lost on imagery and a still first screen. It covered more of the profiler's case, which is the one strength judges conceded and may be what the voter saw.

### Findings
- Restaurant: both Taste Skill pages had no photographs and a half-empty hero. Judges: "reads as a template with its pictures missing". They also named invented prices and closing times, which the pages marked as assumed in code only.
- Profiler: judges said Taste Skill's button "only leads further down", its first screen does not change over the four frames, and its phone panels are cut off.
- Conceded to Taste Skill: "has more content, notably the killed run against the named test", "A is fuller but padded", "covers more (install steps, history chart, pricing, FAQ)", "good" history chart and pull request comment. Against that, judges named repetition and large empty gaps.
- Faults named on web-ui-craft: profiler has a thin ending and sparse middle, a "Pause animation" button at an awkward edge, a chart label over the bars and misaligned plan headings. Restaurant keeps the faults listed in `bench-round-6.md`, section 4.

## 3. Function and cost

### Takeaway
web-ui-craft has fewer serious function faults. On restaurant, the only subject where both costs are known, Taste Skill cost a third more.

### Findings
- Serious axe violations: three of four Taste Skill builds (`aria-prohibited-attr` on both restaurants, `color-contrast` on 32 nodes of restaurant 1, `nested-interactive` on profiler 2), none of web-ui-craft's. Clipped phone text: both Taste Skill profilers. Missing `og:image`: one Taste Skill build, all four of web-ui-craft's. Hidden or covered focus, phone overflow, console errors and failed requests: none. Captures took 14.3 to 16.5 s. Lighthouse was not run.
- Cost per build:

  | Build | Taste Skill tokens | web-ui-craft tokens |
  |---|---|---|
  | Restaurant 1 | 149,824 | 141,278 |
  | Restaurant 2 | 215,864 | 130,732 |
  | Profiler 1 | 242,829 | not recorded |
  | Profiler 2 | 327,250 | not recorded |

- Restaurant medians are 182,844 against 136,005. The arm medians in `results.md` (229,346.5 against 136,005) compare different subjects and should not be read as a ratio. Taste Skill's four builds cost 935,767 tokens and took 15 to 44 minutes each. The eight judges cost 828,418.

## 4. Limits

### Takeaway
The restaurant result is not a clean comparison of the two skills, and four pairs judged by one model and one voter cannot separate them finely.

### Findings
- Both Taste Skill restaurant builders read the subject's "no external images" as a ban and used the skill's no-photograph route. web-ui-craft had the same reading in round six's first attempt and was then changed to read it as no hotlinking (`bench-round-6.md`, section 2). Taste Skill had no such tuning to this bench, so its restaurant pages understate it: it normally leads a place page with 12 to 20 photographs.
- web-ui-craft was developed against these four subjects and judged by this rubric in earlier rounds. Taste Skill was not.
- Taste Skill's finish hook did not run, because builders read its `SKILL.md` rather than loading it as a skill; each builder ran the gate by hand. Three ended `GATE: PASS`, two restaurants and profiler 2 with waivers. Profiler 1 ended `GATE: OPEN 6` with its rounds used up, then fixed some without a fourth gate run.
- Builders read some required references only in part. Restaurant 2 did not run `perf.mjs` and listed a shared scratch folder once without opening another builder's file. Its notice said background work was still running; it did not resume, and its files had not changed for 28 minutes when captures began.
- The four builders ran at once on one machine, which lengthens the durations.
- Judges were pointed at their brief file rather than given it verbatim, as in round six. Their summaries appeared in the session before the vote, so whether the voter saw them is not known.
