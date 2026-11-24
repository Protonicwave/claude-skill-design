# Named moves for editing an existing page

Scope note: gathered on 24 November 2026 for the rule in `skills/web-ui-craft/references/edits.md`. The idea of one small playbook per named move, pointed at one target, comes from Impeccable (github.com/pbakaus/impeccable, Apache-2.0), read at commit b49177d; it is restated here in our own words, and no text is copied into the skill. Quotations below are its words, for the record.

## Q1. How does Impeccable shape an edit?

### Takeaway
Each move has its own file, works on one named target and treats the rest of the page as fixed. Its moves amplify or reduce what the page already owns rather than adding new ideas.

### Cited findings
- "`/impeccable bolder the pricing cards` loads a playbook written for that one move and points it at one target": [Impeccable README](https://github.com/pbakaus/impeccable/blob/b49177d32788f2dc585c42831d845dacf1ebed2c/README.md). It groups `bolder`, `quieter` and `distill` under "Steer" and `polish` and `harden` under "Finish".
- Bolder: "Touch only the named target", and "do not add colors, fonts, radii, shadows, or system primitives the surface does not already own". It calls reaching for more effects "the opposite of bold", and asks to "Make the one decisive move completely, then quiet everything around it so the move is legible": [bolder.md](https://github.com/pbakaus/impeccable/blob/b49177d32788f2dc585c42831d845dacf1ebed2c/.claude/skills/impeccable/reference/bolder.md).
- Quieter: it looks for sources of intensity, "Color saturation", "Contrast extremes", "Visual weight", "Animation excess", "Complexity" and "Scale", and warns that "Quiet without intent collapses to generic": [quieter.md](https://github.com/pbakaus/impeccable/blob/b49177d32788f2dc585c42831d845dacf1ebed2c/.claude/skills/impeccable/reference/quieter.md).
- Distill: "Simplicity is not about removing features. It's about removing obstacles between users and their goals": [distill.md](https://github.com/pbakaus/impeccable/blob/b49177d32788f2dc585c42831d845dacf1ebed2c/.claude/skills/impeccable/reference/distill.md).
- Polish: "Polish is refinement, never concealed redesign", and it fixes broken tasks before states, hierarchy, visual inconsistency and code, in that order: [polish.md](https://github.com/pbakaus/impeccable/blob/b49177d32788f2dc585c42831d845dacf1ebed2c/.claude/skills/impeccable/reference/polish.md).
- Harden: "Designs that only work with perfect data aren't production-ready"; it tests extreme text, errors, translations ("German is often 30% longer than English") and item counts: [harden.md](https://github.com/pbakaus/impeccable/blob/b49177d32788f2dc585c42831d845dacf1ebed2c/.claude/skills/impeccable/reference/harden.md).

### Inferences
- One target and one decisive change is what makes an edit cheap: the identity decisions are already on the page, so the brief, the layout options and the reference site have nothing to decide.
- Five moves cover common follow-ups: bolder, quieter, simpler (its `distill`), polish and harden. Its other commands set up a project, review a page or repeat work web-ui-craft's steps already do.
- Harden's 40% text growth is our own margin above the 30% it quotes for German.

### Gaps
- Which follow-ups users phrase most was not measured; the five moves are a judgement.

## Q2. Which parts are our own?

### Takeaway
The limits on scope, the before and after screenshots and the reduced checks are ours, built from faults seen in earlier rounds and from this repository's checks.

### Inferences
- Searching for a token's other uses before changing it follows from building with tokens (SKILL.md step 4): a token is shared, so a change to it leaks out of the target.
- Enlarging a drawing shows its shortcuts, which is why a bolder hero goes back to the fidelity checklist: judges in round six called round five's drawn scenes crude (`bench-round-6.md`, section 3).
- Judges scored whether the action stayed on the first screen in every round, so bolder may not move it below the fold.
- Lighthouse cannot change much when an edit adds no script or media, so it runs only when one is added. This is untested.
