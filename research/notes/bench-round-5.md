# Bench round five: web-ui-craft with placeholders kept out of sight

Scope note: run on 13 November 2026 with the bench in `bench/` unchanged since commit 1879f88. Only the web-ui-craft arm was rebuilt, at commit 1e53857. That commit revises the copy rule after round four: write around a missing fact first, give the primary action the value the subject makes obvious and report it as an assumption, and keep any remaining placeholder off the first screen and out of the closing section. Everything else round four measured (72d1541, d51efab, adafb54, a8af4f1, cfb9c3c) is unchanged. The 16 bare and frontend-design builds are round one's, recaptured with the current capture. Eight new builds were paired with run i of each other arm in the same subject: 16 pairs, each judged once in each order, 32 verdicts. No person voted. Five of the eight builders stopped part-way through on a usage limit and were resumed from where they stopped. Run data stays in `bench/runs/round-5/`, which git ignores.

## 1. Overall result

### Takeaway
web-ui-craft won 15 of 16 pairs and tied 1, losing none, and the round passes the plan's rule. Whole page against frontend-design is now level, not lost, but round one's lead on it has not come back.

### Findings
- Overall verdicts, with rounds one, two, three and four in brackets:

  | Arm pair | Wins | Ties | Losses |
  |---|---|---|---|
  | web-ui-craft against bare | 8 (7, 8, 8, 7) | 0 (1, 0, 0, 1) | 0 (0, 0, 0, 0) |
  | web-ui-craft against frontend-design | 7 (5, 8, 7, 7) | 1 (2, 0, 1, 1) | 0 (1, 0, 0, 0) |

- Pass rule: wins are at least round one's against each arm (8 against 7, 7 against 5), and no criterion that round one led is lost. Whole page against frontend-design went 2 to web-ui-craft, 4 ties and 2 to frontend-design, against 3 to 5 in round four and round one's lead of 5 to 0. A level criterion is not lost under the rule as written, but the lead round one had is gone. Every other criterion round one led is still led against both arms.
- The tie is charity run 2 against frontend-design (p18). The order that chose frontend-design named one thing: the line "Dates for each Saturday: [session dates]" in the section where volunteers pick a session.

## 2. Copy truth

### Takeaway
The revision did what it was for: only one page out of eight showed a placeholder, no primary action was blank, and no judge found an invented fact on a web-ui-craft page.

### Findings
- Seven builders left no placeholder on the page. Both profiler builders gave the install command as `pip install heapwise`, from the product's name, and reported it as an assumption; no judge called it invented. Charity run 1 numbered its sessions 1 to 12 along a March to June scale, which three verdicts named as better than the other pages' invented dates.
- Charity run 2 left `[session dates]` beside the session picker, which the revision meant to rule out. Its wording at 1e53857 kept placeholders off the first screen and out of the closing section, and said the primary action is never left blank, but did not name the controls that serve the action, so a builder could read the picker as outside it. Commit 1f34e70, after the round, names them. It is the only placeholder judges named (5 of 32 verdicts, all on this page), and it decided the tie.
- Judges named invented facts in 18 of 32 verdicts (23 in round four), every time on the other arm's page. Fit went to web-ui-craft 8 of 8 against bare and 6 to 1 with 1 tie against frontend-design.
- Charity run 1 added one claim the subject did not give, that balsam is invasive and crowds out native plants. It is general knowledge rather than a fact a visitor acts on, and no judge named it.

## 3. Whole page and the remaining faults

### Takeaway
Whole page is now lost on layout, not on copy. The faults are specific and each sits on one build.

### Findings
- Whole page went against web-ui-craft in both orders on five pairs: restaurant run 2 against both arms (p15, p16), profiler run 2 against bare (p07), dashboard run 2 against bare (p08) and charity run 2 against frontend-design (p18). Only p18 names a placeholder.
- Restaurant run 2: a tall gap under the hero, a bar card set low against the dining card, and an opening-days strip reading Closed, Open, Today with no day names.
- Profiler run 2: long empty gaps, pricing headings at different sizes and baselines, and a demo panel that runs past the right edge of the 1440 px screen. One judge also found its condensed display tracked so tight that word spaces close up, the fault adafb54 targets.
- Dashboard run 2: it hides low batteries and broken bikes behind tabs. Its face changes between captures because it uses `font-display: optional`, so a first visit shows the fallback. At 0.25 s its job list is still half faded and its vans start stacked in a corner of the map, reaching their places at about 3 s. That breaks the first-frame rule from 6442cf2 and 72d1541.
- Motion against frontend-design went 2, 4 ties and 2 (round four 4, 3, 1). The charity pages again stand still in the first-screen frames, and the two motion losses, each agreed in both orders, are dashboard run 2 (p19), whose vans arrive late, and restaurant run 1 (p13), where frontend-design's tipping-mug pour was rated above its loop.

## 4. Function and compliance

### Takeaway
The function checks are the cleanest of any round: no serious axe violation, no hidden focus and no phone overflow on any web-ui-craft build.

### Findings
- Serious axe violations 0 of 8 (1 in rounds three and four), hidden focus 0 (1), phone overflow 0 (0), clipped text 1 (dashboard run 2), console errors 0.
- Builders ran the static scan on 8 of 8, the phone check on 8 of 8, Lighthouse on 5 of 8 (every run within budget after fixes; dashboard run 1 first measured a layout shift of 0.473 and run 2 of 0.805, both fixed by reserving space) and the reference comparison on 0 of 8.
- Captures took 17.7 to 22.0 s against the 90 s budget. Three of the eight new builds exited 1 with an empty log on their first capture and passed on the retry, against one recapture in each of rounds three and four. A builder was still running Chrome during those captures.
- Restaurant run 1's builder wrote a stray `phone.html` to the repository root and deleted it; the root was clean when checked.

## 5. Method and its limits

### Takeaway
Both orders agreed on overall for 15 of 16 pairs and the first page shown was chosen in 17 of 32 verdicts. Each finding above rests on one or two builds, so the next revision should target the faults judges named rather than read the tallies alone.

### Findings
- Round five changed the arm by one commit against round four, so the change on whole page against frontend-design, from 3 to 5 in round four to 2 to 2, can be traced to it, though build-to-build variation is of the same size.
- Five builders were resumed after a usage limit stopped them. One (profiler run 1) had already finished its page and reported only; the other four finished their checks after resuming.
- Faults for a later revision: the placeholder gap above, closed in 1f34e70 but not yet measured; a run of identical dark bands still loses whole page on the restaurant subject; and one dashboard ignored the first-frame rule for its live layer.
