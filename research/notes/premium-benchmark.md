# Premium benchmark: acclaimed sites and the built-in frontend-design skill

Scope note: gathered on 8 November 2026 to test whether web-ui-craft produces pages that hold up beside acclaimed sites. Three sources of evidence: Anthropic's `frontend-design` skill (plugin version 1.1.1) as shipped in the official Claude Code plugin marketplace, headless Chrome screenshots of twelve sites at 1440 by 1800 px, and counts of motion techniques in the page source and linked bundles of four of them. Screenshots show the first 1800 px only, after an 8 s virtual time budget, so scroll-triggered and WebGL content may be missing (Lusion and Arc rendered almost blank and are excluded). Bundle counts are text matches: they show what ships, not what runs, and short names such as "three" also match ordinary words, so only distinctive identifiers are reported.

## 1. The built-in frontend-design skill

### Takeaway
frontend-design is about 90 lines of art direction. It is newer than web-ui-craft on what generated pages now look like and stronger at pushing the model to take a position. It gives one sentence to the functional quality floor that web-ui-craft spends most of its length on.

### Findings
- Frames the model as the design lead of a studio whose client "has already rejected proposals that felt cliché or templated", and asks it to "take aesthetic risk if justified". [frontend-design SKILL.md](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design)
- Lists five clusters that generated design "right now" falls into: cream near #F4F1EA with a high-contrast serif and a terracotta accent near #D97757; near-black with one acid-green or vermilion accent; a broadsheet layout with hairline rules and zero radius; the SaaS card kit (identical rounded cards, one radius, one soft grey shadow, gradient washes); and template chrome (tracked all-caps eyebrows, "A · B · C" meta strings, labels built as a word, a spaced em dash and a fragment, near-black standing in for black, a monospace face for small data labels, a "→" appended to links and buttons). [frontend-design](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design)
- Several web-ui-craft remedies lead into those clusters: the Editorial and Swiss directions, warm paper tints, hairlines as the first depth tool, grain, and mono for data.
- Asks for layout concepts as one-sentence descriptions plus ASCII wireframes "to ideate and compare", and for a convergence test: "work through a similar prompt to see if you arrive somewhere similar". [frontend-design](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design)
- Treats type as "an active part of the design, not a neutral delivery vehicle". [frontend-design](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design)
- Copy rule: "An action keeps the same name through the whole flow, so the button that says 'Publish' produces a toast that says 'Published.'" Errors do not apologise. [frontend-design](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design)
- Quality floor in one sentence: responsive, visible focus, reduced motion, accessible, harmonious palette. No tokens, states, forms, performance figures or checker.

## 2. What the acclaimed sites show

### Takeaway
None of these sites is premium because it avoids generated-UI tells: most use one or more. What they share is a hero piece made to a very high standard, very large sparse type set against tiny dense believable detail, and light treated as a material.

### Tells they use anyway
- [Stripe](https://stripe.com): indigo primary button, a two-tone headline (statement in ink, continuation in slate), a logo row directly under the hero.
- [Linear](https://linear.app): Inter, a logo row under the hero, a monospace all-caps caption under the logos, a two-tone second statement.
- [Mercury](https://mercury.com), [Raycast](https://www.raycast.com) and [Family](https://family.co): centred heroes. Raycast's hero is a blurred light effect.

### The hero piece
- Linear: a product screen at native fidelity with believable data (issue DRV-8852, a comment that a spinner "makes it look like the car disappeared", labels, cycle number, release version), lit by a soft pool of light under the frame.
- Stripe: a payment terminal and a checkout drawn with real line items, tax and totals, in a grid whose cells differ in size; a live percentage of global GDP above the headline.
- Teenage Engineering: one studio-lit product render on a dark field, a long cast shadow, then a price and one button.
- Mercury: a full-bleed cinematic photograph of a desk on a misty hillside.
- Family: an owned cast of illustrated characters around the headline.
- Lando Norris: a real-time 3D helmet over a portrait.
- PostHog: the whole site is a desktop operating system with icons, windows and a demo panel that plays itself behind a pause button. The metaphor reaches the cookie banner.

### Scale and density
- Linear's hero headline is roughly 64 px; the product screen beneath it uses 12 to 13 px interface text. The contrast between the two is a large part of the effect.
- Teenage Engineering's navigation is set large with small sub-links beside illustrated line icons; the price is the only text over the product.

## 3. Motion in shipped code

### Takeaway
Two kinds of premium motion. Product sites are fast and quiet and spend motion on the product demo and on elements moving between states. Brand sites choreograph the scroll with GSAP, smooth scrolling and WebGL. web-ui-craft's curves and durations already match the product sites.

### Findings
- Linear: 168 `@keyframes` rules, Framer Motion shared layout (`layoutId`), durations mostly 0.2 to 0.5 s, the Vaul sheet curve `cubic-bezier(0.32, 0.72, 0, 1)`. No GSAP or smooth-scroll library found.
- Raycast: Framer Motion shared layout (18 matches), View Transitions (11), CSS `linear()` easing (6), `cubic-bezier(0.23, 1, 0.32, 1)` as its most common strong ease-out, durations mostly 0.15 to 0.3 s, ten `prefers-reduced-motion` rules.
- Stripe: little CSS motion; the WebGL gradient carries it.
- Lando Norris (Awwwards Site of the Year 2025): GSAP with ScrollTrigger, Lenis smooth scrolling, WebGL, Rive, `linear()` easing and expo curves such as `cubic-bezier(0.19, 1, 0.22, 1)`.
- web-ui-craft's ease-out token is `cubic-bezier(0.22, 1, 0.36, 1)` and its routine durations are 120 to 300 ms, within the range Linear and Raycast ship.

## 4. Speed

- The engineer skill sets measured budgets for code in general (write the figure down, commit a script that measures it) but has nothing specific to the front end: no Web Vitals, frame rate, script weight or perceived speed.
- web-ui-craft lists LCP, INP and CLS targets but never measures them; its checker reads source text only.
- Lighthouse (13.6.0 on npm at the time of writing) applies 4x CPU throttling in its mobile profile and reports LCP, CLS, total blocking time, script weight and non-composited animations. It does not report the frame rate of a given animation.

## 5. Implications for web-ui-craft

- A method for building the hero piece in code when no assets exist, with a fidelity checklist.
- Light from a believable source allowed as a material; decorative glow stays a tell.
- The two-tone headline separated from the single accent word.
- Motion taught by site tier, with choreography, springs, shared-element motion, scroll-linked animation and a hero piece that plays itself.
- Speed measured in the critique step, with a weight budget for the spectacle.
- The giveaway list reframed as defaults versus decisions and updated with frontend-design's clusters.
- From frontend-design: compared layout sketches, the convergence test, type as an active element, the copy consistency rule.
- A premium bar in the critique: compare the build with a reference site in the same direction.

## Gaps

- Single 1440 px viewport per site; no mobile screenshots, no scroll or interaction recorded.
- Motion evidence is from source text, not traces.
- The frontend-design file is plugin version 1.1.1, as installed on 8 November 2026.
