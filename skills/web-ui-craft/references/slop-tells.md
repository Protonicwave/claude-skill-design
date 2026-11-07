# Slop tells

The recognisable signs of AI-generated and template-built interfaces, why they appear, and what to do instead.

## Why it happens

- **Distributional convergence.** Safe choices that "work universally and offend no one" dominate web training data, so a model left without direction samples from that centre. Anthropic's own team found unguided landing pages "almost always" converge on Inter, purple gradients on white and minimal animation.
- **Path dependence.** A few influential defaults were copied until they read as "modern": Tailwind UI's `bg-indigo-500` buttons, the three-column icon feature section from countless tutorials, the Stripe look around 2020 and the Linear look from 2022.
- **Feedback loop.** Generated sites are published, crawled and learned from, so variance shrinks.
- **Static training data.** Models learn from code, not from use, so functional states (validation, errors, empty screens, focus) are routinely missing.

Measured scale: Adrian Krebs ran deterministic checks over about 1,500 recent Show HN sites in April 2026. 22% triggered four or more of these patterns, 32% two or three, 46% one or none.

## Banning is not enough

Telling a model to avoid a default moves it to the next most probable choice. Anthropic reported its model drifting to Space Grotesk when told to avoid common fonts; by 2026 Space Grotesk, Instrument Serif and Geist were themselves listed as "LLM font combos". So:

- Do not replace a tell with its nearest neighbour (Inter with Space Grotesk, indigo with teal, a purple glow with a cyan one).
- Replace it with a decision that has a reason rooted in the subject.
- Treat the lists below as examples of the principle, not as an exhaustive rule set. New tells will appear.
- A listed pattern is acceptable when it is a stated decision. Inter in Linear's computed system is a choice; Inter because nothing else was considered is a tell.

## The tells, by layer

Fixing one layer leaves the others intact. Check all five. `scripts/check_slop.py` catches the tells that show up in source text; structural ones, such as the centred badge hero or three identical cards, need a look at the rendered page.

### Type

| Tell | Instead |
|---|---|
| Inter, Roboto, Open Sans, Lato, Arial, Poppins or the system stack everywhere | A family chosen for the subject's voice (see `visual-system.md`) |
| Second-wave substitutes: Space Grotesk, Instrument Serif, Geist, Playfair Display, JetBrains Mono as display | Same: choose by voice, not by "not Inter" |
| One italic serif, monospace or gradient accent word inside an otherwise plain sans headline | Let the whole headline carry the voice through size, weight and setting |
| Timid hierarchy: 400 against 600, headings 1.5x body | Decisive steps in size and weight |
| All-caps eyebrow labels above every section | Remove the label, or make the heading say it |

### Colour

| Tell | Instead |
|---|---|
| Indigo, violet or purple primary (`indigo-500`, `#6366f1`, `violet-600`) | An accent taken from the subject |
| Purple-to-blue or coral-to-violet-to-cyan gradients, gradient text in headlines | At most one gradient, in adjacent hues, modelling something real |
| Aurora glow or blurred mesh behind the hero, coloured glow shadows | Tone steps and a neutral, physically plausible shadow |
| Five or more neon colours with no hierarchy | One accent with a job; neutrals for everything else |
| Permanent dark slate with medium-grey body text that barely passes contrast | Light or dark chosen for the subject; body text passing comfortably |
| Pure black and pure white neutrals | Neutrals tinted toward the subject |

### Structure

| Tell | Instead |
|---|---|
| Centred hero with a pill badge above the H1, gradient headline, two buttons | Open with the most characteristic thing in the subject's world |
| Hero formula of big number, small label, supporting stats, gradient accent | Claim, proof, action with real evidence |
| Three identical icon-topped feature cards | Layout derived from content: unequal sizes for unequal importance, real product views |
| Numbered 1, 2, 3 steps for things that are not a sequence | Numbers only for real sequences |
| Stat banner row of round numbers | One live or specific number, sourced |
| "Trusted by" logo row at 60% opacity directly under the hero | Proof where it supports a claim, or a named customer story |
| Cards nested inside cards | Flatten; use space and type for grouping |
| Every section revealed on scroll | Motion only where it paces a story |

### Micro-ornament

| Tell | Instead |
|---|---|
| Emoji as icons in navigation, features or headings | One icon family, or no icons |
| Status dots on everything, detached from real status | Dots only for live state |
| Coloured top or left border on every card | Borders only where they carry information |
| Decorative dividers, sparkle icons, floating blurred blobs | Delete them |
| Glassmorphism on every surface | Glass only where content scrolls beneath, if at all |
| `rounded-2xl` on everything, soft shadow on everything | Radii and depth chosen once for the voice |
| A Cmd+K pill on a marketing site with nothing to command | Real navigation |

### Copy and function

| Tell | Instead |
|---|---|
| "Build faster. Ship smarter.", "Unlock the power of", "Supercharge your", "seamless", "revolutionise" | Plain, specific copy that names the audience and what is different |
| Lorem-like filler and invented testimonials | Real content, or clearly marked placeholders the user will replace |
| Forms with no validation, error, empty or loading states | Every state designed (see `interaction.md`) |
| No focus rings, `outline: none` | Visible `:focus-visible` rings |
| No reduced-motion handling | Movement behind `prefers-reduced-motion: no-preference` |

## Remedies that last

1. **Provenance.** Derive the palette, typeface, imagery and layout from something true about the subject. A choice that could belong to any product is not yet a choice.
2. **A named direction.** Naming a concrete aesthetic (Swiss editorial, 1970s ski lodge, laboratory notebook, municipal signage, parchment and leather) forces many correlated decisions at once, which is why it steers so strongly.
3. **Tokens.** Write the system as tokens and use only those names. This removes the chance to reach for `bg-indigo-500`.
4. **Pick a fight with one or two tells**, not all of them. Keep the useful parts of convention: clear type, strong hierarchy, visible navigation.
5. **Carry the identity everywhere**: loading states, empty states, errors, onboarding, the dashboard. Generic interiors behind a distinctive hero are still generic.
6. **Restraint reads as confidence.** One gradient at most, one accent, dots only for real status, motion only where it explains.
7. **The swap test.** Replace the wordmark with a competitor's. If nobody would notice, the design has not been made yet.

The sceptical view is fair: no source links any aesthetic to conversion, and Krebs calls the generic look "uninspired" rather than bad. The case for distinctiveness rests on trust and brand. Generic output makes a product "easy to dismiss".
