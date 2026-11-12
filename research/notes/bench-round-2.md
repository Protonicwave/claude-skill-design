# Bench round two: web-ui-craft with app-screen guidance

Scope note: run on 12 November 2026 with the bench in `bench/` unchanged since commit 1879f88. Only the web-ui-craft arm was rebuilt, at commit cc7108e, which adds `references/app-screens.md` and sends builders to it when the page is a tool. The 16 bare and frontend-design builds are round one's, recaptured with the current capture. Eight new builds, made by the same worker model from the same builder brief as round one, were paired with run i of each other arm in the same subject: 16 pairs, each judged once in each order, so 32 verdicts. The eight pairs of bare against frontend-design were not judged again. No person voted. Run data stays in `bench/runs/round-2/`, which git ignores.

## 1. Overall result

### Takeaway
web-ui-craft won all 16 pairs: 8 of 8 against no skill and 8 of 8 against frontend-design, against 7 of 8 and 5 of 8 in round one. The revision passes the plan's rule. Only the dashboard gain can be traced to the change, because builders of the other three subjects did not read the new reference.

### Findings
- Overall verdicts, with round one in brackets:

  | Arm pair | Wins | Ties | Losses |
  |---|---|---|---|
  | web-ui-craft against bare | 8 (7) | 0 (1) | 0 (0) |
  | web-ui-craft against frontend-design | 8 (5) | 0 (2) | 0 (1) |

- Pass rule: at least as many wins as round one against each arm (8 against 7, 8 against 5), and no criterion lost that round one led on. Round one led every criterion against bare and every criterion but motion against frontend-design; round two still leads each one.
- Dashboard, round one's weakest subject at 2 wins, 1 loss and 1 tie, went to 4 wins of 4.
- Restaurant, charity and profiler also won 4 of 4 each. All six of those builders said they skipped `app-screens.md` because their page was not a tool, so their gain comes from sampling new builds, not from the change. Each arm pair still rests on eight pairs that share builds.

## 2. Criteria

### Takeaway
Motion, round one's weakest criterion, moved most: from 3 wins of 8 against bare to 8, and from level against frontend-design to 4 wins, 3 ties and 1 loss.

### Findings
- Against bare, web-ui-craft won imagery 8, motion 8, overall 8, first screen 7, type 7, fit 7 and whole page 6. It lost first screen, whole page and fit once each.
- Against frontend-design it won imagery 8, overall 8, first screen 7, type 7, fit 6, whole page 4 and motion 4. Whole page is the closest: 2 losses and 2 ties.
- Every web-ui-craft page moved in its first 3 s with its content present at 0.25 s: the cider pour on both restaurant pages, the river gauge filling on both charity pages, test rows streaming or bars growing on the profiler pages, and vans travelling with timers ticking on both dashboards. The skill's motion guidance is unchanged since round one, so this is sampling, not the revision.
- Both profiler builds play a hero report that is still filling at 1.5 s. Judges gave motion to the other page for that in 3 verdicts, the only motion losses in the round.

## 3. What the app-screen guidance changed

### Takeaway
On the dashboards, judges' reasons named each of the four rules the new reference sets, and none of round one's dashboard faults recurred.

### Findings
- Action named: both builds put one filled button on the longest-waiting job that names who goes ("Assign to Aisha", "Assign Van 2 (Callum)"), with the rest outlined. All 8 dashboard verdicts contrasted this with the other page's identical "Assign van" buttons.
- Items listed: both builds list low-battery e-bikes and broken bikes by identifier, place and time. Judges marked the frontend-design dashboards down for showing them as counts.
- Labels clear: no judge reported a label over a marker on a web-ui-craft dashboard. They reported collisions on the frontend-design dashboards ("Redl.nd", "Totterd.n", "Pick up" over "Drop off").
- Live state: in both builds a van moves along its route and counts tick between the 0.25 s and 3 s frames. Judges gave motion to them in 7 of 8 dashboard verdicts and a tie in the eighth.
- Run 2 merged empty and full stations into one queue, as the reference asks, and no judge reported a repeated list. Round one's run 1 was marked down for one.

## 4. Function

### Takeaway
Function checks regressed slightly on the dashboards and the profiler pages.

### Findings
- Serious axe violations: web-ui-craft 1 of 8 builds (0 in round one). Dashboard run 1 nests controls inside a job-card button (`nested-interactive`) and has two scroll boxes the keyboard cannot reach (`scrollable-region-focusable`).
- Focus stops with no visible focus: web-ui-craft 2 builds (1 in round one): an input on charity run 1 and one stop on dashboard run 1.
- Clipped text at 375 px: both profiler builds truncate test names in their report rows, 9 elements each. Profiler run 2 also reports its skip link, which is hidden with the standard 1 px `clip-path: inset(50%)` pattern. That one is a bench false positive.
- No phone overflow, console errors or failed requests in any web-ui-craft build. Captures took 18.2 to 22.9 s against the 90 s budget.

## 5. Method and its limits

### Takeaway
Both orders agreed on all 16 pairs, and the first page shown was chosen exactly half the time, so position bias did not show. The largest limit is that one round cannot separate the change from build-to-build variation.

### Findings
- Order agreement 16 of 16 on overall; page A chosen in 16 of 32 verdicts.
- Each judge received a one-line prompt naming its brief file, rather than the brief pasted in, and read the brief from disk. The brief itself was unchanged. At most 20 judges ran at once.
- Builders still skipped the verification steps: 2 of 8 ran Lighthouse (both passed every budget) and none compared the page with a reference site, as in round one.
- Invented facts persist in every arm: judges named them in 17 of 32 verdicts. Fit went against web-ui-craft in 4 verdicts, 3 of them for invented facts: command-line flags, defaults and a licence on profiler run 2, and places left per session on charity run 1.
- The bench's visually-hidden false positive should be fixed before a later bench change, not during the skill phases, so rounds stay comparable.
