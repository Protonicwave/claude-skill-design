# Edit check: the short path against the skill before it

Scope note: run on 24 November 2026. Two round-five web-ui-craft pages, `restaurant-web-ui-craft-1` and `profiler-web-ui-craft-2`, were each given the request "Make the hero bolder." twice: once under the skill at 8ef348f, which has the edit path (arm `edit-path`), and once under the skill at 016062f, which does not (arm `full-process`). Two pairs, one judge in each order, four verdicts. No votes were cast. Run data stays in `bench/runs/edit-check/`, which git ignores.

## 1. Result

### Takeaway
The edit path fails the check, and a rerun after a fix (section 4) fails too. It beat the earlier skill on the profiler page at a lower cost, and lost to it on the restaurant page at a higher cost.

### Findings
- The pass rule, written before any build: on both pages the edit path costs fewer tokens, loses neither overall nor first screen, and leaves everything outside the hero unchanged.

  | Page | Overall | First screen | Edit-path tokens | Earlier skill's tokens |
  |---|---|---|---|---|
  | Profiler | Edit path, both orders | Edit path, both orders | 81,582 | 92,460 |
  | Restaurant | Earlier skill, both orders | Earlier skill, both orders | 82,555 | 77,153 |

- Medians: 82,068.5 tokens on the edit path, 84,806.5 under the earlier skill, 3% less. With one build per page and arm, that is no evidence of a saving.
- Both arms cost well under round six's median of 142,579.5 for a whole page, which is a different task.
- Scope: with the hero hidden, both profiler edits matched the unedited page pixel for pixel at 1,440 and 375 px, as did both restaurant edits at 375 px. Both restaurant edits differed slightly at 1,440 px in the bar section (21 pixels for the edit path by greyscale, 0 for the other arm, which differed only in colour); neither edit's source touches that section, so the cause is unidentified and is taken as rendering. Judges saw nothing different below either hero.

## 2. What the judges named

### Takeaway
Scale helped where the type broke by sense and the proof stayed on screen, and hurt where the larger type ran into the signature piece.

### Findings
- Profiler: both judges preferred the edit path's two-line headline because the whole report, with its moving bar, stayed on the first screen. The earlier skill's three lines pushed the bar below the fold, so its first three seconds looked still.
- Restaurant: both judges faulted the edit path's headline for running across the cider stream, passing the 1,320 px content edge to about 1,380, and crowding the lede. They preferred the headline broken by phrase in its own column, and faulted that page's hard-edged glow less.

### Inferences
- `edits.md` invites the collision: it tells the builder to let the hero piece "meet the type", and says nothing about legibility, the content edge or line breaks by sense.
- The profiler result suggests a second rule the file lacks: what the hero piece shows on the first screen, its moving part included, stays there.

## 3. Cost and method

### Takeaway
The comparison measures the path against a skill that already shortened itself, and it is small.

### Findings
- The skill already said to scale its steps to the task, and the earlier skill's builders did. On restaurant the builder skipped the brief, both scripts and the reference. On profiler it read three references and skipped Lighthouse and the reference site. The edit path's builders ran the static scan and the phone check on both pages, which the restaurant builder of the other arm did not.
- So the edit path did not make an edit much cheaper. It made its checks consistent: its two edits ran the same set.
- Function: no serious axe violation, hidden focus, phone overflow, clipped text or console error in any build. Every build lacks `og:image`, as before. Lighthouse did not run in any build.
- Judges: 405,374 tokens for four. Builders: 333,750 for four.

### Limits
- One build per page and arm, one move of the five, and one model for each role: builders on Sonnet, judges on Opus, both at medium effort. Quieter, simpler, polish and harden are untested.
- Judges saw the original prompt, not the request, so they chose the better page rather than the bolder one. Whether each edit was bolder than its unedited page is the author's look, not blind: all four were, the restaurant edit path most.
- Judges were pointed at their brief files rather than given them verbatim.

## 4. The rerun on restaurant

### Takeaway
Three rules removed the collision, and the edit path still lost. The edit became timid, where the other arm used colour the page already owned.

### Findings
- Commit 1db83c6 keeps larger type clear of the hero piece, inside the content edge and broken by sense, and keeps the piece's first-screen content on screen. One new edit-path build was paired with the same earlier-skill build, and one judge took each order. Run data is in `bench/runs/edit-check-2/`.
- The cost clause was loosened after the first result, with the user's approval: costs within 10% tie. The rerun cost 85,057 tokens against 77,153, 10.2% more, so it fails that clause by a hair, and it fails the original clause too.
- Judges, both orders: overall, first screen, type and fit to the earlier skill. Whole page, motion and imagery tied; imagery because one order chose the earlier skill.
- The whole edit was one token and a letter-spacing value. The headline kept clear of the pour but crowded the fold, where the table and pause label are cut, and on the phone it still breaks across its two clauses, which the rule forbids. That page had the same phone break before the edit.
- Judges credited the earlier skill for setting "poured from height." in the cider gold of the button and pour, and for breaking the headline by clause.
- Scope: as in section 1, with 21 pixels differing in the bar section at 1,440 px and none at 375 px. Function: the same faults, only `og:image` missing.
- The two judges cost 204,500 tokens, so the check cost about 1.03 million in all: 418,807 for five builds and 609,874 for six judges.

### Inferences
- The playbook's limits cost it here. "One decisive change" and the line against extra accents steer away from giving the headline an accent the page already owns, which is the change both judges preferred.
- Over three builds the edit path cost 83,065 tokens on average against 84,807 for the earlier skill's two. The short path is not cheaper for this move.

## 5. Outcome

### Takeaway
The edit path was removed. The skill scales its five steps down for an edit, as it did before.

### Findings
- Commits 8ef348f and 1db83c6 were reverted with the user's agreement, after two failed checks and no measured saving.
- Only bolder was tested, on two pages, so this is no evidence about the other four moves.
