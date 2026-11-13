# Bench round four: web-ui-craft with copy truth, type setting and reported checks

Scope note: run on 13 November 2026 with the bench in `bench/` unchanged since commit 1879f88. Only the web-ui-craft arm was rebuilt, at commit cfb9c3c. This round measures two sets of changes together: commit 72d1541, made after round three, which keeps the first screen readable in its first frame and starts a loop within about 1 s; and four commits after it. Those keep copy to supplied facts and hide confirmations until their action (d51efab), stop figures breaking across lines, condensed type closing its word spaces and phone headers wrapping (adafb54), add `scripts/check_phone.py` (a8af4f1), and recast step 5 as five checks that each get a report line (cfb9c3c). The 16 bare and frontend-design builds are round one's, recaptured with the current capture. Eight new builds were paired with run i of each other arm in the same subject: 16 pairs, each judged once in each order, 32 verdicts. No person voted. Run data stays in `bench/runs/round-4/`, which git ignores.

## 1. Overall result

### Takeaway
web-ui-craft won 14 of 16 pairs and tied 2, losing none, but the round fails the plan's rule: it lost whole page to frontend-design, a criterion round one led. The cause is the copy rule's visible placeholders.

### Findings
- Overall verdicts, with rounds one, two and three in brackets:

  | Arm pair | Wins | Ties | Losses |
  |---|---|---|---|
  | web-ui-craft against bare | 7 (7, 8, 8) | 1 (1, 0, 0) | 0 (0, 0, 0) |
  | web-ui-craft against frontend-design | 7 (5, 8, 7) | 1 (2, 0, 1) | 0 (1, 0, 0) |

- Pass rule: wins are at least round one's against each arm (7 against 7, 7 against 5). Whole page against frontend-design went 3 to web-ui-craft and 5 to frontend-design; round one led it 5 to 0 with 3 ties. Every other criterion still leads against both arms.
- Both ties are profiler pairs whose orders split: run 2 against bare (p08) and run 2 against frontend-design (p21). In each, the order that went against web-ui-craft named the same thing: the install section shows `[install command]` where the primary action should be, so the page could not ship.

## 2. Copy truth

### Takeaway
The copy rule worked as written: no judge found an invented fact on a web-ui-craft page. It moved the cost from fit to whole page, because a placeholder in a late section reads as an unfinished page.

### Findings
- Judges named invented facts in 23 of 32 verdicts (22 in round three), and every one found them on the other arm's page. Round three found them on both charity, both profiler and both restaurant web-ui-craft pages. Fit went to web-ui-craft 8 of 8 against bare (as in round three) and 7 of 8 against frontend-design (5, 6 and 6 in rounds one to three).
- Placeholders were named in 27 of 32 verdicts. Builders left between 3 and 6 per page: `[date]` on every charity session, `[meeting point]`, `[set menu price]`, `[postcode]`, `[licence]`, `[price]`, and `[install command]` or `[package name]` on both profiler pages.
- Four of the five whole-page losses to frontend-design name placeholders in a later section: the visit block and footer of both restaurant pages (p13, p20), the charity footer (p14), and the profiler install band (p21). The fifth (p06) names a closing band of `pip install [package name]` and long empty gaps. Writing around missing facts also thinned sections: restaurant run 2's set menu is three dish names with no description.
- The rule let a builder leave the primary action as a placeholder. The subject gives no package name, so both profiler builders, following the rule, left the install command blank. Judges treated that as a page that cannot ship, and it decided both ties.
- Restaurant run 1's builder found its own booking confirmation visible before submit in a screenshot and fixed it. No judge named a confirmation shown early.

## 3. Type, phone and motion

### Takeaway
The phone faults of round three did not recur, and no judge named a broken figure or a closed word space on a web-ui-craft page. Motion held against bare and slipped against frontend-design.

### Findings
- Phone overflow: 0 of 8 web-ui-craft builds (2 in round three); clipped text 0 (1). Four builders report that `check_phone.py` found a breach they then fixed: 30, 39 and 4 px, and one page 455 px wide.
- Judges named split durations ("1 h 37 / min", "Saturday 6 / March") only on bare and frontend-design pages. On web-ui-craft pages they named "Aged / beef chop" wrapping in restaurant run 1's menu, a dish name rather than a figure, and a slashed zero in charity run 2's text face that makes "10 am" read as "1Ø am".
- Motion against bare: 6 wins, 2 ties. Against frontend-design: 4 wins, 3 ties, 1 loss (round three 5, 1, 2). Four of the five ties are charity pairs: their trolley signature plays when scrolled into view, so the first-screen frames stand still.
- Commit 72d1541 held: both restaurant pages had readable hero text at 0.25 s, and both profiler loops changed within the first 1.5 s (run 1 at 0.9 s). The one motion loss is restaurant run 1 against frontend-design (p13, both orders): the other page's pour played as one moment, while run 1's glass was already filling at 0.25 s.

## 4. Function and compliance

### Takeaway
Builders ran more of the checks than in any earlier round: Lighthouse on 6 of 8 pages against 2 of 8 in each of rounds one to three. The reference comparison is still skipped, and partly because of the bench's own builder brief.

### Findings
- Builders ran the static scan on 8 of 8, the phone check on 8 of 8, Lighthouse on 6 of 8 (every run within budget after fixes; dashboard run 1 first breached largest contentful paint (LCP) at 2,666 ms) and the reference comparison on 1 of 8 (dashboard run 2, against linear.app).
- Three builders said they skipped the reference because the builder brief says to read no file outside the arm's folder. The brief means repository files, but it reads as forbidding an outside site.
- Dashboard run 1 logged "Maximum call stack size exceeded" during the capture and hides focus on 15 keyboard stops, its map's station marks. Its builder had no browser tool and did not walk the keyboard.
- Serious axe violations: 1 of 8 (profiler run 2, `nested-interactive`), as in round three.
- Captures took 18.1 to 39.0 s against the 90 s budget. One recapture (profiler frontend-design run 1) exited 1 with an empty log and passed on rerun, the same fault round three met on another build.
- Dashboard run 1's builder listed the `builds/` folder names but opened none, so the build was kept.

## 5. Method and its limits

### Takeaway
Both orders agreed on overall for 14 of 16 pairs and the first page shown was chosen in 16 of 32 verdicts, so position bias did not show. The whole-page loss is consistent across orders, which makes it a property of the pages rather than of a judge.

### Findings
- Each of the five whole-page losses to frontend-design was agreed in both orders.
- Two changes sharing one round cannot be separated by the verdicts alone. The judges' reasons do separate them: no reason names a type, phone or check change as a fault, and the placeholder reasons trace to d51efab.
- Round five measures a revision of the copy rule that keeps placeholders off the first screen, out of the primary action and out of closing sections.
