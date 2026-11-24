# Bench round six: photographs from open archives

Scope note: run on 24 November 2026. Only the web-ui-craft arm was rebuilt, at commit 8897d6d, on the restaurant and charity subjects, two builds each. Round five's web-ui-craft builds (arm `web-ui-craft-r5`) and round one's frontend-design builds of those subjects were recaptured. Run i of each arm was paired with run i of every other arm in the same subject: 12 pairs. Judges took nine of them once in each order, 18 verdicts; p08, p11 and p12 were not judged. One person voted on all 12 pairs. Run data stays in `bench/runs/round-6/` and `bench/runs/round-6-attempt-1/`, which git ignores.

## 1. Overall result

### Takeaway
The photograph change passes on imagery by the judges' verdicts, 4 to 0 against round five. The voter preferred round five overall, 3 to 1, so the pass rests on setting those votes aside.

### Findings
- Judges, new web-ui-craft against each other arm; a choice counts only when both orders agree, and a tie includes orders that disagree:

  | Criterion | Against round five: win, tie, loss | Against frontend-design: win, tie, loss |
  |---|---|---|
  | Imagery | 4, 0, 0 | 2, 0, 0 |
  | Overall | 4, 0, 0 | 2, 0, 0 |
  | Whole page | 4, 0, 0 | 2, 0, 0 |
  | Fit | 4, 0, 0 | 2, 0, 0 |
  | Motion | 2, 2, 0 | 2, 0, 0 |
  | First screen | 2, 1, 1 | 2, 0, 0 |
  | Type | 0, 2, 2 | 2, 0, 0 |

- Votes, overall only: new 4 to 0 against frontend-design; round five 3 to 1 against new (p07, p09 and p10 to round five, p06 to new); round five 4 to 0 against frontend-design. Judges and voter agreed on 6 of 9 judged pairs.
- Pass rule: no loss to round five on the criterion the change targets, and no criterion lost to frontend-design that round five led. Neither happened in the judged pairs. The plan also said a vote decides its pair, but a vote carries no criterion and the rule does not map it to one. The outcome was settled after the results were known: the voter said to disregard their votes and accepted a pass on imagery. Read as overall votes deciding, the round fails.

## 2. The first attempt

### Takeaway
A reference alone did not change what builders did. They needed an explicit default in SKILL.md.

### Findings
- The first four builds, at 7456f9a, used no photographs. Three builders read "no external images" in the subject as a ban, and one preferred a drawing. Commit 8897d6d makes archive photographs the first choice for food, place and culture subjects and reads that wording as no hotlinking.
- After it, all four builds used credited photographs. The licence and author of each of the five photographs matched its Commons record.

## 3. What the judges named

### Takeaway
Photographs of the real place replaced round five's weakest drawings. Type and some controls did not improve.

### Findings
- Charity: judges called the Don photographs credible and round five's river crude, with floating balsam and hard water edges. A gauge marked at 4.2 t was credited for imagery and motion, though one judge called tonnes on a level scale a stretch.
- Restaurant: judges credited fish over coals and Call Lane against a round five page with no picture after its hero.
- Round five kept the better session picker on charity run 1 and the tidier form on charity run 2. Type went to it on both restaurant pairs.

## 4. Faults on the new pages

### Takeaway
Two pages state things nobody supplied, and each page has at least one layout fault.

### Findings
- Charity run 1: a caption says Himalayan balsam "grows thickly on the right bank", which nothing supplied supports, and sign-up is by month only.
- Charity run 2: the fold cuts the desktop button, two placeholders are visible and the radio labels are misaligned.
- Restaurant run 1: the hero glow ends in a hard edge, the headline breaks into five ragged lines and the phone header button touches the screen edge.
- Restaurant run 2: the Pause button covers the plank, the bottle is clipped and the booking email `bookings@sutondo.co.uk` is invented.

## 5. Function and cost

### Takeaway
The function checks do not separate new from round five. Judging cost more than three times the rebuild.

### Findings
- Serious axe violations, hidden focus, phone overflow and console errors: 0 of 12. Clipped text: one frontend-design build. Every build lacks `og:image`. Captures took 14.7 to 16.9 s.
- Lighthouse ran on one of the four rebuilds (LCP 1,600 ms, CLS 0.016, TBT 0); a hook blocked `npx` on the other three.

  | Work | Tokens |
  |---|---|
  | First attempt, four builds | 474,109 |
  | Rebuild, four builds (median 142,579.5) | 560,824 |
  | First 12 judges | about 1.24 million |
  | Six tie-break judges | 614,681 |

- Six of the first 12 judges compared round five with frontend-design (p01 to p03), which the pass rule does not use. The cost of the older arms' builds was not recorded.

## 6. Method and its limits

### Takeaway
The judges were blind and consistent, but they are one model on four pairs against round five, and several choices were made after results were seen.

### Findings
- Both orders agreed on overall for 9 of 9 judged pairs, and page A was chosen in 9 of 18 overall choices.
- p07, p09 and p10 were judged because the voter and the author of the change disagreed on them. The author's opinion was written before the votes were read, but was not blind and is not scored.
- All votes on p07 to p12 were recorded as "B", with the displayed order varying by pair. Whether that was deliberate was asked and not answered. The voter could have seen the results of p01 to p06 before voting, so agreement there is not independent.
- `votes.json` was found in a sibling project's folder and copied in, matched by its pair ids and time.
- Judges were pointed at their brief file rather than given it verbatim, as the README asks. Judges ran on Opus and builders on Sonnet, both at medium effort; the model behind round one's frontend-design builds is unverified.
- Archive test requests during research named this project in their User-Agent. Later requests used a generic one.
