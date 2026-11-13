# Slop tells

A tell is a default: a choice that turns up whatever the subject. The same pattern made for a stated reason is a decision. This file lists the defaults generated and template-built interfaces fall into, why they appear, and what to do instead.

## Why it happens

- **Distributional convergence.** Safe choices that "work universally and offend no one" dominate web training data, so a model left without direction samples from that centre. Anthropic's own team found unguided landing pages "almost always" converge on Inter, purple gradients on white and minimal animation.
- **Path dependence.** A few influential defaults were copied until they read as "modern": Tailwind UI's `bg-indigo-500` buttons, the three-column icon feature section from countless tutorials, the Stripe look around 2020 and the Linear look from 2022.
- **Ready-made components.** Effects such as the cursor-following spotlight card ship whole in component libraries and get installed onto any card on any subject.
- **Feedback loop.** Generated sites are published, crawled and learned from, so variance shrinks.
- **Static training data.** Models learn from code, not from use, so functional states (validation, errors, empty screens, focus) are routinely missing.

Measured scale: Adrian Krebs ran deterministic checks over about 1,500 recent Show HN sites in April 2026. 22% triggered four or more of these patterns, 32% two or three, 46% one or none.

## Default or decision

Acclaimed sites use these patterns. Stripe has an indigo button and a logo row under the hero, Linear sets everything in Inter, and Mercury, Raycast and Family centre their heroes. They still look expensive, because each pattern was chosen inside a system and executed to a high standard. So the question for every pattern below is not "is it on the list?" but "would it be here on any other subject?".

- **A pattern is a decision when the brief traces it to a fact about this subject** and the build carries it out properly. Inter in Linear's computed system is a decision; Inter because nothing else was considered is a default.
- **The reason has to be specific.** "Clean", "modern", "readable" and "professional" justify anything on any page, so they do not count. "The ferry company's timetables have been set in the same slab serif since 1962" does.
- **Do not swap a default for its nearest neighbour** (Inter for Space Grotesk, indigo for teal, a purple glow for a cyan one). Telling a model to avoid a default moves it to the next most probable choice: Anthropic's model drifted to Space Grotesk when told to avoid common fonts, and by 2026 Space Grotesk, Instrument Serif and Geist were themselves listed as "LLM font combos".
- **Any suggestion can become a default, this skill's included.** Two pages built from the same version of this skill both took the same typeface from its list of candidates, and a later product page copied the identifiers from its mock-up examples. Treat everything here as examples of the principle. New defaults will appear.
- **Every tell the checker reports needs a decision**: change it, or say in the report what about the subject it came from.

## Whole-look clusters

Generated pages tend to arrive as one of a few complete looks, where every choice pulls in the next. A page can be free of single tells and still be one of these. If the brief's direction is heading toward one, the subject has to be the reason.

| Cluster | Recognised by | Usually reached from |
|---|---|---|
| Cream and clay | Warm cream ground near `#F4F1EA`, high-contrast serif display, terracotta accent near `#D97757` (Claude's own accent) | An editorial direction, or "warm paper" as the tint |
| Near-black and acid | Near-black ground (`#0B0B0B`, `#111`), one acid-green or vermilion accent, everything else grey | A calm tool or utilitarian direction |
| Dark SaaS template | Dark slate with white type and a faint cyan or violet accent, blurred colour mesh across the top, mono accent word in the headline, a Cmd+K pill, a dot grid or noise over the surface | Copying the Linear look without its system |
| Broadsheet | Hairline rules between everything, zero radius, dense newspaper columns, small caps labels | An editorial or Swiss direction, or hairlines as the default depth tool |
| SaaS card kit | Content chopped into identical rounded cards, one radius everywhere, the same soft grey shadow (`rgba(0,0,0,.1)`) under each, gradient washes | A feature list with nothing to show |
| Template chrome | Tracked all-caps eyebrows, "A · B · C" meta strings, labels built as a word, a spaced dash and a fragment, mono for small labels, an arrow on every link and button | Any direction; it appears whatever the subject |

## The tells, by layer

Fixing one layer leaves the others intact. Check all five. `scripts/check_slop.py` catches the ones that show up in source text (default fonts, indigo, gradient text, glow shadows, emoji icons, filler copy, "trusted by", eyebrow labels, the italic accent word, appended arrows written as text or a lucide or heroicons icon, and the cream and clay colours in hex, rgb() or oklch()). Structural ones, such as the centred badge hero or three identical cards, need a look at the rendered page.

### Type

| Default | Instead |
|---|---|
| Inter, Roboto, Open Sans, Lato, Arial, Poppins or the system stack everywhere | A family found for the subject's voice (see `visual-system.md`) |
| Second-wave substitutes: Space Grotesk, Instrument Serif, Geist, Playfair Display, JetBrains Mono as display | Same: choose by voice, not by "not Inter" |
| The face every recent build used, or one taken from a list of recommendations | A face found through the subject, with the reason in the brief |
| One italic serif, monospace or gradient accent word inside an otherwise plain sans headline | Let the whole headline carry the voice through size, weight and setting |
| Mono for every small label, spec and figure | Mono for code, identifiers and figures read character by character; labels in the text face |
| Timid hierarchy: 400 against 600, headings 1.5x body | Decisive steps in size and weight |
| All-caps eyebrow labels above every section | Remove the label, or make the heading say it |

A two-tone headline (a statement in full ink and its continuation dimmed, as on Stripe and Linear) is not the accent-word tell: the split follows the sentence, not one word picked out for decoration.

### Colour

| Default | Instead |
|---|---|
| Indigo, violet or purple primary (`indigo-500`, `#6366f1`, `violet-600`) | An accent taken from the subject |
| Cream `#F4F1EA` with terracotta `#D97757` | A ground and accent sampled from a real material in the subject's world |
| Near-black (`#0B0B0B`, `#111`) with one acid accent | A dark ground tinted toward the subject, if dark suits the subject at all |
| Purple-to-blue or coral-to-violet-to-cyan gradients, gradient text in headlines | At most one gradient, in adjacent hues, modelling something real |
| Aurora glow or blurred mesh behind the hero, coloured glow shadows | Tone steps and a neutral, physically plausible shadow; for drama, light from one source falling on something real (see `artefacts.md`) |
| Five or more neon colours with no hierarchy | One accent with a job; neutrals for everything else |
| Permanent dark slate with medium-grey body text that barely passes contrast | Light or dark chosen for the subject; body text passing comfortably |
| Pure black and pure white neutrals | Neutrals tinted toward the subject |

### Structure

| Default | Instead |
|---|---|
| Centred hero with a pill badge above the H1, gradient headline, two buttons | Open with the most characteristic thing in the subject's world |
| Hero formula of big number, small label, supporting stats, gradient accent | Claim, proof, action with real evidence |
| Three identical icon-topped feature cards | Layout derived from content: unequal sizes for unequal importance, real product views |
| Bento grid whose cells are the same weight and each hold an icon and two lines | Cells sized by importance, each showing something real, or no grid |
| Numbered 1, 2, 3 steps for things that are not a sequence | Numbers only for real sequences |
| Stat banner row of round numbers | One live or specific number, sourced |
| "Trusted by" logo row at 60% opacity directly under the hero | Proof where it supports a claim, or a named customer story |
| Cards nested inside cards | Flatten; use space and type for grouping |
| A hairline rule between every section | Space and a change of content mark a new section; rules only where space cannot |
| Every section revealed on scroll | Motion only where it paces a story |

### Micro-ornament

| Default | Instead |
|---|---|
| Emoji as icons in navigation, features or headings | One icon family, or no icons |
| A spotlight or glow that follows the cursor across cards | Pointer response only on the hero piece, as the object reacting (see `interaction.md`) |
| A dot grid, hairline grid or noise laid over the whole surface | Texture only where it models a material, such as paper or print |
| Status dots on everything, detached from real status | Dots only for live state |
| Meta strings joined with middle dots ("Berlin · 2026 · 4 min") | Say the one fact that matters, or set the facts in a table |
| Labels built as a word, a spaced dash and a fragment | A plain label or a heading that says it |
| An arrow appended to link and button text | A label that says where it goes; an arrow only where it shows direction |
| Coloured top or left border on every card | Borders only where they carry information |
| Decorative dividers, sparkle icons, floating blurred blobs | Delete them |
| Glassmorphism on every surface | Glass only where content scrolls beneath, if at all |
| `rounded-2xl` on everything, soft shadow on everything | Radii and depth chosen once for the voice |
| A Cmd+K pill on a marketing site with nothing to command | Real navigation |

### Copy and function

| Default | Instead |
|---|---|
| "Build faster. Ship smarter.", "Unlock the power of", "Supercharge your", "seamless", "revolutionise" | Plain, specific copy that names the audience and what is different |
| Lorem-like filler, invented testimonials, and plausible facts nobody supplied (dates, places, prices, counts, versions, options, rules) | Facts from the subject only: copy that does not need the missing fact, or a visible placeholder such as `[start date]`, listed in the report |
| A button that says one thing and a confirmation that says another ("Publish", then "Saved") | One name per action through the whole flow |
| Errors that apologise or stay vague ("Oops, something went wrong") | What happened and how to fix it, in the interface's voice |
| Forms with no validation, error, empty or loading states | Every state designed (see `interaction.md`) |
| No focus rings, `outline: none` | Visible `:focus-visible` rings |
| No reduced-motion handling | Movement behind `prefers-reduced-motion: no-preference` |

## Remedies that last

1. **Provenance.** Derive the palette, typeface, imagery and layout from something true about the subject. A choice that could belong to any product is not yet a choice.
2. **A named direction.** Naming a concrete aesthetic (Swiss editorial, 1970s ski lodge, laboratory notebook, municipal signage, parchment and leather) forces many correlated decisions at once, which is why it steers so strongly. Check which cluster above the direction slides into, and make the subject pull it somewhere else.
3. **Tokens.** Write the system as tokens and use only those names. This removes the chance to reach for `bg-indigo-500`.
4. **Pick a fight with one or two tells**, not all of them. Keep the useful parts of convention: clear type, strong hierarchy, visible navigation.
5. **Carry the identity everywhere**: loading states, empty states, errors, onboarding, the dashboard. Generic interiors behind a distinctive hero are still generic.
6. **Restraint reads as confidence.** One gradient at most, one accent, dots only for real status, motion only where it explains.
7. **The swap test.** Replace the wordmark with a competitor's. If nobody would notice, the design has not been made yet.

The sceptical view is fair: no source links any aesthetic to conversion, and Krebs calls the generic look "uninspired" rather than bad. The case for distinctiveness rests on trust and brand. Generic output makes a product "easy to dismiss".
