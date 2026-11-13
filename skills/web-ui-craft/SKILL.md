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
- **Page or tool**: whether the page tells people about something, or is the tool they work in (a dashboard, console, queue or admin screen). For a tool, read `references/app-screens.md` before the brief: it changes what the Signature, Copy and Motion lines mean.
- **Existing constraints**: brand assets, an existing design system, tokens, component library or framework in the repository. If tokens exist, use them and apply this skill within them. Do not impose a new identity on an established product unless asked.

If the user gave little to go on, infer from the subject and state your assumptions in the brief rather than asking a list of questions.

## 2. Write the design brief

Write a compact brief in your response before writing code. It is the design, so it must be specific enough that someone else could build the same thing from it.

```
Direction:    a named aesthetic and why it fits this subject (one or two lines)
Signature:    the one idea this page is remembered for, the hero piece that carries it, and how
              that piece will be made (supplied assets, a generated image, or built in code)
Palette:      neutral (tinted toward ...), one accent (role), semantic colours; OKLCH values
Type:         family and role for each (display, text, mono if needed) and what each shares with
              the subject; how the display type acts in the composition; scale ratio; body size
Layout:       two or three options for the first screen, each a one-line concept and an ASCII
              wireframe; the one chosen and why; grid, measure, density, section rhythm
Depth:        how surfaces separate (tone steps, hairlines, shadows), where the light comes from
              and what it falls on
Motion:       the tier (product or brand), the signature moment, its lead element and the
              movement of the subject it shows, the complete frame it opens on, what else
              moves and for how long, and what deliberately does not
Imagery:      photography, illustration, 3D, product UI or type-only; art direction in one line
Copy:         the headline and primary action, written for this audience; the action's name,
              kept from button to confirmation; each fact the page needs that was not supplied,
              and how the copy handles it
Budget:       compressed script for the whole page and the share the spectacle layer may take
              (365 KiB in total by default; 75 KiB for a page with no spectacle)
```

Rules for the brief:

- **Derive, do not decorate.** Each line answers "why this, for this subject?". A palette taken from the product's materials, a typeface from its vernacular, a hero that opens with the most characteristic thing in its world.
- **One signature, everything else quiet.** Stripe has its gradient wave, Apple its scroll-scrubbed product shots, Family its flying trays. Spend boldness once. Restraint around it is what makes it read.
- **Restraint is a valid direction.** A calm, type-led, monochrome system with one accent is as deliberate as a WebGL hero, and usually the right call for tools and documentation.
- **Quiet is not bare.** Restraint limits how many ideas a page has, not how rich each one is. The signature should reward a long look: an illustration drawn for this subject, real data set out with care, texture, type at true display scale. Food, culture, consumer and brand subjects usually need imagery or illustration to carry warmth, so a type-only page for one of them needs a stated reason.
- **The hero piece is where the effort goes.** Acclaimed sites break plenty of rules and still look expensive because one piece is made to a very high standard: a product screen with believable data, a lit object, an owned illustration. Choose and build it with `references/artefacts.md`. A rounded box with grey bars in it is not a product shot.
- **Type is part of the composition, not a carrier for it.** At display size the setting is the design: scale against the smallest text on the page, weight, width, case, where the lines break, what the headline sits against. Linear's 64 px headline over 12 px interface text is a large part of its effect.
- **Compare layouts before choosing one.** Sketch two or three genuinely different first screens (not one layout with the image moved) and pick by the subject's primary job. The first layout that comes to mind is usually the template.
- **Claim, proof, action.** Most pages need one clear statement, one piece of real evidence (product view, live number, customer, demo) and one primary action. Structure follows content, not a template.
- **One name per action.** The button that says "Publish" produces a confirmation that says "Published", not "Saved". The interface's vocabulary is how people find their way around it.
- **Only facts you were given.** Every fact a visitor could act on or repeat (a date, time, place, price, count, version, command, option, default, licence, rule or named person) comes from the subject, the user or the repository. A plausible invented fact misleads the visitor, and someone else has to find it and take it out. A visible gap costs too: a page that shows brackets reads as unfinished. So when the page wants a fact nobody supplied:
  - **Write around it first.** Most lines that seem to need a date, price or rule work without one: "every other Thursday, spring to autumn" rather than a list of dates the subject never gave. A section with nothing true left to say is cut, not padded.
  - **Never leave the primary action blank.** When it needs a value nobody supplied, such as the identifier an install or download takes, use the one the subject makes obvious (the product's own name) and list it in the report as an assumption to confirm.
  - **Otherwise mark the gap.** A fact the page cannot do without becomes a placeholder in square brackets, such as `[start date]`, kept off the first screen and out of the closing section, and listed in the report.

  A mock-up may invent the records it displays (names, identifiers, figures), but not the product's own commands, options, prices or limits, which a visitor would copy or rely on.

Read `references/exemplars.md` when choosing a direction or signature, `references/visual-system.md` when setting palette, type, layout and depth, and the motion section of `references/interaction.md` when writing the Motion line.

## 3. Challenge the brief

Before building, attack it:

- **Swap test.** Could a competitor's name replace this one without anyone noticing? If yes, the brief has not made its decisions yet.
- **Per-choice test.** For every line, ask whether it could belong to any product. If it could, it must be a deliberate, well-tuned default from the build sheet below, or it must change.
- **Convergence test.** Sketch in a few lines the brief you would write for a neighbouring subject: another tool in the same category, another maker in the same trade. Every line that comes out the same is a default, not a decision. Change it, and say in the brief what changed and why. A line may stay only when it follows from a fact the two subjects share (both products are hardware, both audiences read code); name the fact.
- **Tell check.** Compare against `references/slop-tells.md`, including the whole-look clusters. Do not swap one default for the next most common one (Inter for Space Grotesk, purple for teal). Replace it with a choice that has a reason.

Revise the brief, then build.

## 4. Build

- **Tokens first.** Write the palette, type scale, spacing, radii, shadows and motion as CSS custom properties (or the project's token system) before any component. Components use token names only, never raw values like `bg-indigo-500` or `#6366f1`.
- **Structure second.** Semantic HTML, real links for navigation, headings in order, then style.
- **Apply the build sheet** below and the detail in `references/visual-system.md` and `references/interaction.md`.
- **Design every state.** Hover, active, focus-visible, disabled, loading, empty, error, success, long content and short content. Generated UI is weakest here, and the fixes are cheapest here.
- **Keep spectacle cheap and optional.** Heavy effects (WebGL, video, large blur) live in one isolated layer within the brief's budget, start after first paint, have a static fallback, and sit behind `prefers-reduced-motion: no-preference`.

## 5. Check, critique and cut

Treat the first build as a draft. Run all five checks, fix what they find, and give each one a line in the report. A check that cannot run gets a line saying what stopped it; a missing line is a skipped check.

1. **Static scan** of the whole front-end source, not only the files you changed, since the focus and reduced-motion rules look for a global style anywhere in the scan. Fix every `defect` (exit code 1); change each `tell` or say why it stays. It needs Python 3.12 or later and no packages.

   ```
   python <skill-dir>/scripts/check_slop.py <front-end source folder>
   ```

2. **Phone overflow** over the whole page. Fix every `breach` (exit code 1) until it passes.

   ```
   python <skill-dir>/scripts/check_phone.py <page>.html
   ```

3. **Screenshots** at 1440 px and 375 px, in both colour schemes if there are two, then look at them. Use a browser tool if the session has one, and tab through every flow with it. Otherwise use headless Chrome or Edge, with the profile and images in a temporary folder:

   ```
   chrome --headless=new --hide-scrollbars --user-data-dir=<temp>/profile --window-size=1440,2600 --virtual-time-budget=4000 --screenshot=<temp>/desktop.png <file or http URL>
   ```

   The image is one window of the given size, so make it tall enough for what you need to see. Chrome will not make a window narrower than about 500 px: for the phone, screenshot a small page that holds the site in an `<iframe>` 375 px wide. A looping piece is caught mid-loop; add `--force-prefers-reduced-motion` for its finished frame. Content revealed on scroll may be missing, so check in the source that its hidden state is set by script (see `references/interaction.md`).

4. **Lighthouse** in its default mobile profile, over HTTP (for a static folder, `python -m http.server` in it), read by the budget reader:

   ```
   npx lighthouse@13.6.0 <http URL> --output=json --output-path=<temp>/report.json --quiet --chrome-flags="--headless=new --user-data-dir=<temp>/lh-profile"
   python <skill-dir>/scripts/check_budgets.py <temp>/report.json --script-kib <the brief's budget>
   ```

   Fix every `breach` (exit code 1). Exit code 2 means a figure is `unmeasured`: rerun once, then report it as unmeasured, never as passed. Set `CHROME_PATH` if Lighthouse cannot find Chrome. Lighthouse does not measure the signature moment's frame rate; record a trace if a browser tool can, and otherwise report it as unmeasured.

5. **Reference.** Screenshot the first screen of one acclaimed site in the chosen direction, one a designer in the subject's field would admire (`references/exemplars.md` names some), at 1440 px with the command in check 3, and look at it beside yours. Compare the hero piece's fidelity, the span from the largest type to the smallest detail, how much believable detail there is, and the light. Name the largest gap and close it, or say why it stays. Take the bar for craft from it, nothing from its surface.

Then critique by eye:

- Run the fidelity checklist in `references/artefacts.md` on the hero piece. If the first screen is correct but forgettable, strengthen the signature rather than adding elements.
- Walk the checklist in `references/interaction.md`, and for a tool the one at the end of `references/app-screens.md`.
- Re-run the tell check in `references/slop-tells.md` against the built page: it covers structural tells the scan cannot see, such as the centred badge hero, three identical cards and the whole-look clusters.
- Remove anything that does not serve the subject or the user: decorative dividers, labels above self-explanatory content, badges, glows, icons that repeat their text, a second accent colour. Deleting is usually the biggest improvement available.

Report the brief, what the critique changed, and these lines:

```
Static scan:  defects left, and each tell kept with its reason
Phone:        pass, or the overflow left and why
Screenshots:  the widths and colour schemes looked at
Lighthouse:   LCP, CLS, total blocking time and script KiB against budget, or what stopped it
Reference:    the site, the largest gap and what was done about it
Placeholders: each fact left for the user to supply, and each assumption to confirm
Unverified:   anything else not checked, such as rendered contrast without a browser
```

## Build sheet

Well-sourced starting values. They protect good decisions; they do not replace the identity decisions in the brief.

| Dimension | Default |
|---|---|
| Body text | 16 to 20 px, line height about 1.5, measure 45 to 90 characters (aim for about 65) |
| Headings | Line height 1.0 to 1.2, tracking about -0.02em from 24 px up (0 or more on condensed faces), `text-wrap: balance` |
| Paragraphs | `text-wrap: pretty`; bold and italic never together; no line break inside a figure, date, time or duration |
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
| Motion | Tier named in the brief; a signature movement taken from the subject; first screen complete in its first frame and its entrance at rest by 1.5 s, a looping signature piece excepted; routine motion under 300 ms (modals up to 400, large sheets up to 500), strong ease-out or a settling spring, `transform` and `opacity` only, from the trigger, none on keyboard or high-frequency actions |
| Navigation | Visible top-level links on desktop, up to four visible on mobile on one row at 375 px, UI state in the URL |
| Loading | Nothing under about 1 s; delay indicators 150 to 300 ms, then show for at least 300 to 500 ms |
| Performance | LCP at most 2.5 s, INP at most 200 ms, CLS at most 0.1; lab total blocking time at most 200 ms; script within the brief's budget; visible response to input within 100 ms |
| Targets and focus | At least 24 px (44 px on touch); visible `:focus-visible` ring never hidden by sticky elements |

## References

- `references/visual-system.md`: colour, typography, layout, depth, radii, icons and imagery, with CSS.
- `references/interaction.md`: navigation, motion, states, forms, performance, accessibility and the critique checklist.
- `references/slop-tells.md`: the catalogue of generic tells, why they appear and what to do instead.
- `references/exemplars.md`: aesthetic directions and what to learn from specific acclaimed sites.
- `references/artefacts.md`: choosing and building the hero piece, light as a material, and the fidelity checklist.
- `references/app-screens.md`: dashboards, consoles and queues: listing what was asked for, actions that name their object, map and chart labels, live state.
- `scripts/check_slop.py`: static scan for craft defects and generic tells, used in step 5.
- `scripts/check_phone.py`: measures how far the page runs past a 375 px screen and names the elements responsible, used in step 5.
- `scripts/check_budgets.py`: reads a Lighthouse report and compares it with the page budgets, used in step 5.

The evidence behind every rule is in the `research/` folder of the repository this skill is published from.
