# Edits to an existing page

Read this when the page exists and the request is to change part of it. The page already holds its decisions, so this path reads them instead of making new ones. It replaces the five steps of `SKILL.md`: no new brief, no layout options, no reference site.

## When it applies

All three must hold. Otherwise use the five steps.

- The page exists and its identity stays: no new direction, palette, typeface or brand.
- The request names a move or a target (one section, component or screen), or both.
- The work fits one target. "Make the whole site bolder" is a redesign; "polish the page" is not, because polish adds nothing new.

Match the request to a move by what it asks for, not by the word. A plain change ("move the form up", "swap the image") has no move: do it under the rules in "Every edit".

| Move | Also asked for as |
|---|---|
| Bolder | flat, boring, safe, more impact, stand out |
| Quieter | too much, loud, busy colours, calm it down |
| Simpler | cluttered, confusing, too much going on, cut it down |
| Polish | tidy, finish, tighten, make it feel right |
| Harden | edge cases, long text, empty or error states, make it production-ready |

When two moves fit, take the one that changes less and say which in the report. When the request names no target, take the section it plainly describes; for "bolder" and "quieter" alone, take the first screen.

## Every edit

1. **Read** the target's markup, style and script, the token block and the project's DESIGN.md if it has one. Screenshot the target at 1440 px and 375 px, before changing anything, and look: several moves cannot be planned from source.
2. **Write two lines** in the response before editing: `Change:` what is wrong with the target and the one thing that will fix it; `Keep:` what the target must still do afterwards (its claim, its action, its behaviour).
3. **Edit** inside the target only. Use existing tokens, typefaces and motifs. A new token is allowed when it extends a scale the page has (a larger display step); a new colour or typeface is not, so say what is missing and stop short of it. Leave facts as they are: the rule in `SKILL.md` step 2 on facts nobody supplied applies to every word added.
4. **Check** as below, then report.

A shared token or class changes every place that uses it. Search for its other uses before editing it. If there are any outside the target, scope the new value to the target instead.

## Moves

### Bolder

A flat section is usually one that stops short of what the rest of the page does. Find the strongest thing the page owns (its display type, its signature piece, its accent, its density) and let the target use it at full strength.

- Make one decisive change and quieten what surrounds it. If every element gets louder, nothing is.
- Pick the change from the target's own weakness: type that does not act in the composition (scale, width, line breaks, what it sits against); a hero piece that is small, floating or lost in empty space (bring it up in scale, crop it on purpose, let it meet the page edge); a composition with no tension; a ground that gives the light nothing to fall on.
- Work on the hero piece is work on its fidelity as well as its size: an enlarged drawing shows every shortcut. Run the fidelity checklist in `references/artefacts.md` on it afterwards.
- Glows, gradients, extra accents, badges and more motion are not boldness.
- Larger type keeps clear of the hero piece: no letter over it and nothing of it through a letter. It stays inside the content edge the rest of the page keeps and clear of the text below, and breaks by sense at both widths.
- Whatever the hero piece shows on the first screen, its moving part included, still shows there at both widths.
- The primary action stays on the first screen at both widths, and at least as prominent as it was.

### Quieter

Find the two or three things that compete, and decide which one the target is for. That one keeps its strength; the others give it up.

- Take away in this order: motion that says nothing, effects (glow, blur, stacked shadow), extra accents, weight, then size. Stop as soon as one thing leads.
- Lower chroma before lightness, so contrast holds. Recheck contrast on every text colour touched.
- Keep the signature. A section with no focal point is not quiet, it is empty.

### Simpler

Name the target's one job, then take each element in turn and ask what is lost without it.

- Remove what repeats, decorates or explains something self-evident; merge what is said twice; move what is needed only sometimes behind a visible control.
- Never remove a fact, an option, a label a control needs, a state or a path the visitor uses. List everything taken out in the report, so it can be put back.
- Close the space left behind: regroup, rather than leave a hole in the old layout.

### Polish

Nothing new appears: the same design, finished. If the idea itself is weak, say so in the report and stop at finishing it.

- Work in this order: what is broken or unreachable, missing states, alignment and spacing off the scale, type (breaks, measure, orphans, figures), colour off the tokens, motion timing, then untidy source.
- Compare like with like. The same role takes the same size, weight, radius and gap everywhere in the target.
- Walk the checklist in `references/interaction.md` and fix each failure inside the target.

### Harden

Make the target survive what it will meet. The normal case must look the same afterwards.

- **Content**: a name three times as long, one word that will not break, none, one, and a thousand; a missing image; figures at their widest; text 40% longer in translation.
- **State**: loading, empty, error, offline, success, disabled and no permission, each with what to do next. The detail is in "States and feedback" in `references/interaction.md`.
- **Use**: a double submit, Back and refresh mid-flow, keyboard only, 200% text size, reduced motion, script failing to load.

Force each case by temporarily editing the page, look at it, then undo the forcing. Write no state for a case the target cannot reach.

## Check

Run these, not the five checks in `SKILL.md`, whose step 5 holds the commands:

- The static scan on the whole front-end source. Fix every defect the edit introduced; list the ones that were already there without fixing them.
- `scripts/check_phone.py` on the page, with the same rule for breaches.
- Screenshots of the target again at 1440 px and 375 px, looked at beside the ones from before. Say what is better. If the difference is hard to see, the move was too small; polish and harden are meant to be small.
- The parts of the page just above and below the target, which must look as they did.
- Lighthouse only when the edit adds script or media.

Report:

```
Edit:          the move, the target, and what changed
Kept:          what was deliberately left as it was
Checks:        static scan, phone and screenshots; Lighthouse, or why it did not apply
Already there: defects found outside the edit, not fixed
```
