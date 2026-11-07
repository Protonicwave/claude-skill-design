---
name: web-ui-craft
description: Design and build web interfaces that look deliberate rather than generated. Use whenever creating or restyling a website, landing page, web app screen, dashboard, component, HTML or CSS page, or React, Vue or Svelte UI, and whenever the user asks for something beautiful, polished, distinctive, modern or not AI-looking. Forces a written design brief derived from the subject, applies evidence-based defaults for type, colour, spacing, depth, motion, navigation, states, performance and accessibility, and ends with a critique pass that removes generic AI tells.
---

# Web UI craft

Generic UI is not a style. It is what fills every decision nobody made: the model, the template or the framework supplies its most common answer, and the result could belong to any product. The best-looking sites (Linear, Vercel, Stripe, Family, the Awwwards winners) leave almost nothing to default. They compute a small system, commit to one idea, and hold functional details to measurable standards.

So the job is to make decisions, write them down, and trace each one to the subject, the user or the physics of perception. Follow the five steps below in order. Scale them to the task: a single button gets a sentence of brief and a quick critique, a landing page gets the full treatment.

## 1. Read the subject

Before any visual choice, establish:

- **Subject**: what the product, organisation or content actually is, and the world it belongs to (its industry, materials, vocabulary, artefacts).
- **Audience**: who arrives, what they already know, which device they are likely on.
- **Primary job**: the one thing the page or screen must get done. Everything else is subordinate to it.
- **Existing constraints**: brand assets, an existing design system, tokens, component library or framework in the repository. If tokens exist, use them and apply this skill within them. Do not impose a new identity on an established product unless asked.

If the user gave little to go on, infer from the subject and state your assumptions in the brief rather than asking a list of questions.

## 2. Write the design brief

Write a compact brief in your response before writing code. It is the design, so it must be specific enough that someone else could build the same thing from it.

```
Direction:    a named aesthetic and why it fits this subject (one or two lines)
Signature:    the one idea this page is remembered for, and where it lives
Palette:      neutral (tinted toward ...), one accent (role), semantic colours; OKLCH values
Type:         family and role for each (display, text, mono if needed); scale ratio; body size
Layout:       grid, measure, density, section rhythm; a rough wireframe of the first screen
Depth:        how surfaces separate (tone steps, hairlines, shadows) and why
Motion:       what moves, how long, and what deliberately does not
Imagery:      photography, illustration, 3D, product UI or type-only; art direction in one line
Copy:         the headline and primary action, written for this audience
```

Rules for the brief:

- **Derive, do not decorate.** Each line answers "why this, for this subject?". A palette taken from the product's materials, a typeface from its vernacular, a hero that opens with the most characteristic thing in its world.
- **One signature, everything else quiet.** Stripe has its gradient wave, Apple its scroll-scrubbed product shots, Family its flying trays. Spend boldness once. Restraint around it is what makes it read.
- **Restraint is a valid direction.** A calm, type-led, monochrome system with one accent is as deliberate as a WebGL hero, and usually the right call for tools and documentation.
- **Quiet is not bare.** Restraint limits how many ideas a page has, not how rich each one is. The signature should reward a long look: an illustration drawn for this subject, real data set out with care, texture, type at true display scale. Food, culture, consumer and brand subjects usually need imagery or illustration to carry warmth, so a type-only page for one of them needs a stated reason.
- **Claim, proof, action.** Most pages need one clear statement, one piece of real evidence (product view, live number, customer, demo) and one primary action. Structure follows content, not a template.

Read `references/exemplars.md` when choosing a direction or signature, and `references/visual-system.md` when setting palette, type, layout and depth.

## 3. Challenge the brief

Before building, attack it:

- **Swap test.** Could a competitor's name replace this one without anyone noticing? If yes, the brief has not made its decisions yet.
- **Per-choice test.** For every line, ask whether it could belong to any product. If it could, it must be a deliberate, well-tuned default from the build sheet below, or it must change.
- **Tell check.** Compare against `references/slop-tells.md`. Do not swap one default for the next most common one (Inter for Space Grotesk, purple for teal). Replace it with a choice that has a reason.

Revise the brief, then build.

## 4. Build

- **Tokens first.** Write the palette, type scale, spacing, radii, shadows and motion as CSS custom properties (or the project's token system) before any component. Components use token names only, never raw values like `bg-indigo-500` or `#6366f1`.
- **Structure second.** Semantic HTML, real links for navigation, headings in order, then style.
- **Apply the build sheet** below and the detail in `references/visual-system.md` and `references/interaction.md`.
- **Design every state.** Hover, active, focus-visible, disabled, loading, empty, error, success, long content and short content. Generated UI is weakest here, and the fixes are cheapest here.
- **Keep spectacle cheap and optional.** Heavy effects (WebGL, video, large blur) live in one isolated layer, have a static fallback, and sit behind `prefers-reduced-motion: no-preference`.

## 5. Critique and cut

Treat the first build as a draft.

1. Run the static checker over the files you wrote, using the skill's own directory for the script path. It needs Python 3.11 or later and no packages:

   ```
   python <skill-dir>/scripts/check_slop.py <files or folders you changed>
   ```

   Fix every `defect` (exit code 1 means at least one remains). For every `tell`, change it or say in your report why it stays. The checker reads source text only, so a clean result is necessary, not sufficient.
2. Render the page and look at it at 1440 px and 375 px wide, in both colour schemes if it has two. Use a browser tool if the session has one. Otherwise most machines have headless Chrome or Edge; write screenshots and the browser profile to a temporary folder, then read the images:

   ```
   chrome --headless=new --hide-scrollbars --user-data-dir=<temp>/profile --window-size=1440,2600 --virtual-time-budget=4000 --screenshot=<temp>/desktop.png <file or http URL>
   ```

   Headless Chrome will not make a window narrower than about 500 px, so a 390 px screenshot is silently cropped from a wider layout. For the phone check, screenshot a small wrapper page that holds the site in an `<iframe>` 375 px wide. Sections that stay blank in a full-page screenshot are hidden until a scroll reveal fires, which is itself a defect (see `references/interaction.md`). With a real browser tool, also tab through every flow.
3. Ask whether the first screen gives the eye something worth looking at. A page that is correct but forgettable has a timid signature: strengthen the signature rather than adding more elements.
4. Walk the checklist in `references/interaction.md` (states, focus, targets, forms, performance).
5. Re-run the tell check in `references/slop-tells.md` against the built page, not the brief. It covers structural tells the checker cannot see, such as the centred badge hero and three identical cards.
6. Remove anything that does not serve the subject or the user: decorative dividers, labels above self-explanatory content, badges, glows, icons that repeat their text, a second accent colour. Deleting is usually the biggest improvement available.
7. Report the brief, what the critique changed, and anything you could not verify (for example rendered contrast without a browser).

## Build sheet

Well-sourced starting values. They protect good decisions; they do not replace the identity decisions in the brief.

| Dimension | Default |
|---|---|
| Body text | 16 to 20 px, line height about 1.5, measure 45 to 90 characters (aim for about 65) |
| Headings | Line height 1.0 to 1.2, tracking about -0.02em from 24 px up, `text-wrap: balance` |
| Paragraphs | `text-wrap: pretty`; bold and italic never together |
| Type scale | Fluid via `clamp()`, ratio about 1.2 on small screens to 1.25 on large |
| All caps | Rare, under one line, letter-spacing 0.05em to 0.12em |
| Colour | OKLCH; one tinted neutral scale, one accent, three or four semantic colours, each with role-based steps |
| Contrast | WCAG 4.5:1 body, 3:1 large text and UI parts; aim for APCA Lc 75 or more on body text |
| Dark mode | A separate palette: dark grey base (about `oklch(0.18 0.01 h)`), lighter surfaces for elevation, desaturated accent |
| Gradients | Interpolate `in oklch`; adjacent hues; optional fine grain; at most one deliberate gradient |
| Spacing | 4 px base: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128; gap between groups at least double the gap within |
| Depth | Tone steps and hairline borders first; shadows layered, one light source, tinted with the surface hue |
| Radii | Two or three values; nested radius = outer radius minus padding |
| Icons | One family, one grid, one stroke width; no emoji as interface icons |
| Motion | Under 300 ms, strong ease-out, `transform` and `opacity` only, from the trigger, none on keyboard or high-frequency actions |
| Navigation | Visible top-level links on desktop, up to four visible on mobile, UI state in the URL |
| Loading | Nothing under about 1 s; delay indicators 150 to 300 ms, then show for at least 300 to 500 ms |
| Performance | LCP at most 2.5 s, INP at most 200 ms, CLS at most 0.1; visible response to input within 100 ms |
| Targets and focus | At least 24 px (44 px on touch); visible `:focus-visible` ring never hidden by sticky elements |

## References

- `references/visual-system.md`: colour, typography, layout, depth, radii, icons and imagery, with CSS.
- `references/interaction.md`: navigation, motion, states, forms, performance, accessibility and the critique checklist.
- `references/slop-tells.md`: the catalogue of generic tells, why they appear and what to do instead.
- `references/exemplars.md`: aesthetic directions and what to learn from specific acclaimed sites.
- `scripts/check_slop.py`: static scan for craft defects and generic tells, used in step 5.

The evidence behind every rule is in the `research/` folder of the repository this skill is published from.
