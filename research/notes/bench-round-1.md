# Bench round one: web-ui-craft against frontend-design and no skill

Scope note: run on 11 November 2026 with the bench in `bench/`. Four subjects (`bench/subjects/`), three arms, two builds per subject and arm: 24 builds. Every build was made by the same worker model from the same brief, so the arms differ only in the instructions the builder read: none (`bare`), frontend-design 1.1.1, or web-ui-craft at commit 0069912. Each build was captured by `bench/capture.py`, and run i of each arm was paired with run i of every other arm within a subject: 24 pairs. A separate judge model scored each pair from screenshots alone, once in each order, so 48 verdicts. A choice counts only when both orders agree; otherwise it is a tie. No person voted in this round, so agreement between judges and a human is unmeasured. Run data stays in `bench/runs/round-1/`, which git ignores.

## 1. Overall result

### Takeaway
web-ui-craft won 7 of 8 pairs against no skill and 5 of 8 against frontend-design, losing one. frontend-design won 5 of 8 against no skill and lost none. The order is clear, but each arm pair rests on eight pairs that share builds, so the margins are indicative rather than settled.

### Findings
- Overall verdicts, wins against wins with ties between:

  | Arm pair | Wins | Ties | Wins |
  |---|---|---|---|
  | web-ui-craft against bare | 7 | 1 | 0 |
  | web-ui-craft against frontend-design | 5 | 2 | 1 |
  | frontend-design against bare | 5 | 3 | 0 |

- A sign test on the decided pairs alone gives two-sided p of 0.016 for 7 of 7, 0.22 for 5 of 6 and 0.063 for 5 of 5. Each build appears in two pairs, so the pairs are not independent and these figures overstate the confidence.
- By subject, web-ui-craft's overall record across its four pairs was: restaurant 4 wins; charity 3 wins and 1 tie; profiler 3 wins and 1 tie; dashboard 2 wins, 1 loss and 1 tie. Its only loss was dashboard run 1 against frontend-design.

## 2. Criteria

### Takeaway
web-ui-craft's lead comes from imagery, type and fit to the subject. Motion is where it gains least: most pages in every arm do not move.

### Findings
- Against bare, web-ui-craft won imagery 8 of 8, type 7, fit 7, whole page 6, first screen 5 and motion 3, with no criterion lost.
- Against frontend-design it won imagery 7, first screen 5, whole page 5, type 5 and fit 5. Motion was level at 2 wins each with 4 ties.
- frontend-design against bare won imagery 7 and fit 6, but lost first screen 1 to 4.
- Pages that moved did so where the subject offered a signature: a cider pour on the restaurant pages, bars growing on the profiler pages. No dashboard in any arm moved in its first 3 s.

## 3. What the judges marked down

### Takeaway
The judges' reasons point at a short list of faults. Several are things a capture script could check, and two are not checked yet.

### Findings
- Map labels drawn over station dots ("Redl●nd", "Ashtor.Court") on dashboard web-ui-craft run 1, and five identical "Assign van" buttons that name no van. Its sibling run named the van on the button ("Assign Van 4") and won both its pairs outright.
- Content the subject asks for shown only as a count. Dashboards that showed low-battery and broken bikes only as numbers were marked down for it on first screen or fit, in all three arms.
- A success state visible before submission: restaurant web-ui-craft run 1 shows "Booking received" under an empty form. Capture did not catch it.
- Text clipped at the edge with no scroll: restaurant frontend-design run 1 cuts its wordmark to "Sutond" at 375 px, and a web-ui-craft profiler page cuts its install command to "pip install". Capture reported 0 px overflow for both, because the content is clipped by `overflow: hidden` rather than widening the page.
- Invented facts: version support, licences, prices, session dates, meeting places and booking rules, in every arm. Judges counted them against fit when they would mislead a visitor.
- Condensed display type set so tight that word spaces nearly vanish (charity web-ui-craft run 2), and dates and figures breaking across lines ("Saturday 6 / March", "1 h / 49 min").
- Phone navigation wrapping onto two or three rows.

## 4. Function

### Takeaway
Function checks agree with the judges on direction: web-ui-craft builds had the fewest serious accessibility violations.

### Findings
- Builds with at least one serious or critical axe violation: bare 4 of 8, frontend-design 1 of 8, web-ui-craft 0 of 8.
- Builds with a focus stop that showed no visible focus: bare 1, frontend-design 0, web-ui-craft 1.
- Phone overflow: frontend-design profiler run 2 by 202 px, web-ui-craft profiler run 2 by 5 px. All others 0 px.
- No build logged a console error or a failed request. Every build lacks an Open Graph image, which the subjects' ban on external images makes hard to supply.
- Every capture finished inside the 90 s budget, at 18.0 to 35.6 s. The two bare dashboards took longest because their keyboard walks reached the 200-stop limit across 180 focusable map stations.

## 5. Method and its limits

### Takeaway
The two-order rule held: it turned a strong position preference in the first batch into ties rather than wrong winners. The largest gaps in the method are the missing human vote and three capture faults.

### Findings
- In the first 16 verdicts the page shown second won overall 13 times, and only 3 of those 8 pairs agreed across orders. The later 32 verdicts showed no such preference. Over all 48 the first page was chosen 18 times, and 18 of 24 pairs agreed on overall.
- The first builder brief told builders to read no repository file but SKILL.md, so a web-ui-craft builder skipped the skill's references while frontend-design, which has none, lost nothing. All eight web-ui-craft builds were discarded and rebuilt from the corrected brief (commit d52ea0b). The 16 bare and frontend-design builds kept the old brief, which differs from the new one only for arms with reference files.
- The first 16 builders shared one scratch folder and sometimes overwrote each other's check scripts. That affected their own checks, not their output.
- Builders following web-ui-craft skipped steps it asks for: only the two dashboard builders ran Lighthouse, and none compared the page against a reference site.
- Capture faults: a date input ends the keyboard walk early as a false "repeat", because Tab moves between its day, month and year fields while focus stays on the input, which affected all six restaurant builds; clipped content reads as 0 px overflow; and full-page phone images over about 10,000 px tall reach the judge downscaled to roughly a quarter of their width, so they can be judged only on layout.
- Builds ran on the worker model. The result says how web-ui-craft guides that model, not the stronger main model.
- One builder force-stopped every Python process on the machine during the round. Every capture still completed and printed its time, so none was cut short.
