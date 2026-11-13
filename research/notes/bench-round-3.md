# Bench round three: web-ui-craft with motion that carries the subject

Scope note: run on 13 November 2026 with the bench in `bench/` unchanged since commit 1879f88. Only the web-ui-craft arm was rebuilt, at commit 6442cf2. That commit asks every page for one movement the subject makes, a first screen complete in its first frame and at rest by 1.5 s, and a looping piece that opens on a finished frame. The 16 bare and frontend-design builds are round one's, recaptured with the current capture. Eight new builds, made by the same worker model from the same builder brief as rounds one and two, were paired with run i of each other arm in the same subject: 16 pairs, each judged once in each order, so 32 verdicts. The eight pairs of bare against frontend-design were not judged again. No person voted. Run data stays in `bench/runs/round-3/`, which git ignores.

## 1. Overall result

### Takeaway
web-ui-craft won 15 of 16 pairs and tied the other: 8 of 8 against no skill and 7 of 8 against frontend-design. Round one won 7 and 5. The revision passes the plan's rule, but it does not beat round two's 16 of 16.

### Findings
- Overall verdicts, with round one and then round two in brackets:

  | Arm pair | Wins | Ties | Losses |
  |---|---|---|---|
  | web-ui-craft against bare | 8 (7, 8) | 0 (1, 0) | 0 (0, 0) |
  | web-ui-craft against frontend-design | 7 (5, 8) | 1 (2, 0) | 0 (1, 0) |

- Pass rule: at least as many wins as round one against each arm (8 against 7, 7 against 5), and no criterion lost that round one led on. web-ui-craft still leads every criterion against both arms.
- The tie is restaurant run 1 against frontend-design (p15). The first order chose web-ui-craft, the second frontend-design. Both judges found the web-ui-craft hero's copy and booking button still faint at 0.25 s, and both gave fit to frontend-design for invented pintxos and a booking rule for parties of nine or more.

## 2. Motion

### Takeaway
Motion did not improve on round two. Against frontend-design it went from 4 wins, 3 ties and 1 loss to 5 wins, 1 tie and 2 losses, and against bare from 8 wins to 7 and a tie. Each loss traces to a gap in the revision's own wording, not to builders ignoring it.

### Findings
- Every web-ui-craft build drew its signature movement from the subject, as the revision asks: a cider pour on both restaurant pages, a trolley hauled onto the bank on both charity pages, growth bars or a memory trace on the profiler pages, and vans travelling with stations changing state on both dashboards. Round two's builds did the same without the rule, so this part shows no change.
- Restaurant run 1 lost motion to frontend-design in both orders. Its hero copy and booking button fade in from opacity 0 and are still faint at 0.25 s. Both restaurant builds copied the entrance snippet in `references/interaction.md`, which fades every follower from opacity 0, and that snippet contradicts the new rule that the first screen reads in its first frame.
- Profiler run 1 lost motion to frontend-design and tied with bare. It opens on a finished report, as asked, but its 10 s loop holds that frame for 5.2 s before the first bar retracts, so all four frames in the first 3 s are identical. The revision said how a loop should open, not how soon it should first move.
- Round two's profiler fault, a hero report still filling at 1.5 s, did not recur: no judge found a web-ui-craft page still assembling at 1.5 s.
- Both gaps were fixed after the round in commit 72d1541. The entrance snippet now moves followers without fading them, and a looping piece makes its first change within about 1 s. Round four measures that commit together with the next revision.

## 3. Other criteria

### Takeaway
Imagery and type went to web-ui-craft in all 16 pairs. Whole page is still the weakest criterion against frontend-design.

### Findings
- Against bare, web-ui-craft won imagery 8, type 8, fit 8, overall 8, first screen 7, motion 7 and whole page 6. It lost first screen once and tied whole page twice.
- Against frontend-design it won imagery 8, type 8, overall 7, first screen 6, whole page 6, fit 6 and motion 5. It lost whole page twice (restaurant runs 1 and 2) and fit once (restaurant run 1).
- Judges named invented facts, on either page, in 22 of 32 verdicts, against 17 in round two. On web-ui-craft pages they named session meeting places and places-left counts on both charity pages, command-line flags, defaults and version support on both profiler pages, pintxos and booking rules on the restaurant pages.

## 4. Function

### Takeaway
Phone overflow returned on two web-ui-craft builds, against none in round two.

### Findings
- Phone overflow: charity run 2 (24 px) and profiler run 2 (68 px). Judges saw both: the charity page's header "Sign up" button clips and wraps, and the profiler page's install band runs past the column. Neither builder saw the fault: profiler run 2's builder viewed only the top 3,100 px of its phone page, and charity run 2's builder changed the phone header after its last screenshot.
- Clipped text at 375 px: profiler run 2 truncates 6 test names and paths in its report rows, against 9 on each profiler build in round two.
- Serious axe violations: 1 build of 8, as in round two. Charity run 2 breaks `definition-list`, and one of its focus stops has no visible focus.
- No console errors or failed requests in any web-ui-craft build. Captures took 18.7 to 23.2 s against the 90 s budget. One capture of dashboard run 2 exited without output and passed when rerun.

## 5. Method and its limits

### Takeaway
Both orders agreed on 15 of 16 pairs, and the first page shown was chosen in 15 of 32 verdicts, so position bias did not show. As in round two, one round cannot separate the revision from build-to-build variation.

### Findings
- Each judge received a two-line prompt, its task type and the path of its brief, and read the brief from disk. At most 20 judges ran at once.
- Builders still skipped the verification steps: 2 of 8 ran Lighthouse (both dashboards, both within every budget) and none compared the page with a reference site. Only the two dashboard builders read `app-screens.md`, which is correct, since only the dashboard is a tool.
- The fixes in 72d1541 were made after reading this round's verdicts, so round four is the first round to test them on builds the fixes did not see.
