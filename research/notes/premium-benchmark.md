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

### Platform support for the techniques these sites use
Checked on 8 November 2026 against the web-features data set (fetched from unpkg) and MDN's browser-compat-data, which agreed on every version below.

- `linear()` easing: "allows the approximation of complex animations and transitions by interpolating linearly between the specified points". Baseline since 11 December 2023 (Chrome 113, Firefox 112, Safari 17.2), widely available since 11 June 2026. [MDN, linear()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function/linear) A generator with spring and bounce presets exists at [linear-easing-generator.netlify.app](https://linear-easing-generator.netlify.app/).
- Scroll-driven animations (`animation-timeline: scroll()` and `view()`, `animation-range`): Chrome and Edge 115, Firefox 159, Safari 26; Baseline only since 27 October 2026, so older browsers in use still lack them. [MDN, animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline) Chrome's guide lists "the ability to have scroll-driven animations run off the main thread". [Chrome for Developers, scroll-driven animations](https://developer.chrome.com/docs/css-ui/scroll-driven-animations) MDN warns that `animation-timeline` "is included in the animation shorthand as a reset-only value", so it must be declared after the shorthand.
- Same-document View Transitions (`document.startViewTransition`): Baseline since 14 October 2025 (Chrome 111, Firefox 144, Safari 18). `view-transition-class` reached Baseline on the same date. [MDN, startViewTransition()](https://developer.mozilla.org/en-US/docs/Web/API/Document/startViewTransition)
- Cross-document View Transitions (`@view-transition { navigation: auto; }`): Chrome and Edge 126 and Safari 18.2; not in Firefox (browser-compat-data lists it as "preview"), so not Baseline. [Chrome for Developers, cross-document view transitions](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document)
- Duplicate names: "If two rendered elements have the same `view-transition-name` at the same time, ViewTransition.ready will reject and the transition will be skipped." [MDN, Using the View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using) Starting a transition while one is running skips the first: "If document's active view transition is not null, then skip that view transition". [CSS View Transitions Module Level 1](https://drafts.csswg.org/css-view-transitions-1/)
- FLIP (Paul Lewis, 2015): "First: the initial state of the element(s) involved in the transition. Last: the final state of the element(s)." Play is to "switch on transitions for any of the properties you changed, and then remove the inversion changes". [Aerotwist, FLIP your animations](https://aerotwist.com/blog/flip-your-animations/)
- GSAP ScrollTrigger: `pin` makes an element "appear to 'stick' in its starting position while the rest of the content continues scrolling underneath it"; `scrub`: "Links the progress of the animation directly to the scrollbar so it acts like a scrubber." [GSAP, ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger) All of GSAP, plugins included, "can be used in commercial projects at no charge". [GSAP licensing](https://gsap.com/licensing/)
- Pointer media features: `pointer: fine`: "The primary input mechanism includes an accurate pointing device, such as a mouse." `hover: hover`: "The primary input mechanism can conveniently hover over elements." [MDN, pointer](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/pointer); [MDN, hover](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/hover)
- Among the elements Chromium excludes from Largest Contentful Paint: "Elements with an opacity of 0, that are invisible to the user". A headline held at opacity 0 by an animation delay is not yet counted. [web.dev, Largest Contentful Paint](https://web.dev/articles/lcp)

### Spring tokens
No source examined gives spring constants (the gap noted in `interaction-navigation-performance.md`), so web-ui-craft's two spring tokens are derived rather than cited. Each is the step response of a damped spring with mass 1, x(t) = 1 - e^(-ζωt)(cos ω_d t + (ζω/ω_d) sin ω_d t), with ω chosen so the response stays within 0.1% of its end value after the stated duration, sampled at 400 points and simplified with the Ramer-Douglas-Peucker algorithm to within 0.002.

| Token | Damping ratio ζ | Duration | Stiffness | Damping | Overshoot | 95% reached |
|---|---|---|---|---|---|---|
| `--spring-settle` | 0.9 | 500 ms | 281 | 30.2 | 0.15% | 240 ms |
| `--spring-bounce` | 0.6 | 800 ms | 161 | 15.2 | 9.5% | about 200 ms |

The settling spring reaches 95% of its travel in about the time of a 250 ms ease-out, which keeps it inside the product sites' 150 to 300 ms range while ending without a hard stop.

## 4. Speed

- The engineer skill sets measured budgets for code in general (write the figure down, commit a script that measures it) but has nothing specific to the front end: no Web Vitals, frame rate, script weight or perceived speed.
- web-ui-craft lists LCP, INP and CLS targets but never measures them; its checker reads source text only.
- Lighthouse (13.6.0 on npm at the time of writing) applies 4x CPU throttling in its mobile profile and reports LCP, CLS, total blocking time, script weight and non-composited animations. It does not report the frame rate of a given animation.
- Lighthouse colours total blocking time on mobile green ("fast") from 0 to 200 ms, orange ("moderate") from 200 to 600 ms and red ("slow") above 600 ms; the desktop bands are 0 to 150 and 150 to 350 ms. [Chrome for Developers, Total Blocking Time](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time)
- Alex Russell's 2024 budget for a first load interactive within 3 s on 75th-percentile devices and networks: about 730 KiB compressed in total with up to 365 KiB of compressed JavaScript for a JavaScript-heavy site; 75 KiB of JavaScript for a markup-based one. The 5 s budget doubles these. [Infrequently Noted, The Performance Inequality Gap, 2024](https://infrequently.org/2024/01/performance-inequality-gap-2024/)

Observed by running Lighthouse 13.6.0 (mobile, simulated throttling: 150 ms RTT, 1.6 Mbps, 4x CPU) against two local pages on 8 November 2026:

- A navigation report has no `interaction-to-next-paint` audit, because nothing is clicked. Total blocking time is the lab measure of main-thread responsiveness.
- `non-composited-animations` keeps a score of 1 and a display mode of "informative" while listing elements, for example `body > div#bar` with "Unsupported CSS Properties: width, box-shadow". A reader has to count the listed elements; the score never fails. With no animations the mode is "notApplicable".
- `resource-summary` gives transfer size per resource type. Python's `http.server` sends files uncompressed, so script weight measured through it reads higher than a production server would deliver: a 196 KiB file was reported at its full size.
- The baseline brand page (Kestrel S-16, built with the skill at 409a764) scored LCP 1.4 s, CLS 0.092, total blocking time 0 ms and 96 KiB in total. Its CLS sits just under the 0.1 budget, which no reading of the source had shown.

## 5. Defaults from component libraries and from the skill itself

### Takeaway
frontend-design's list misses two sources of default. Some effects arrive ready-made from component libraries and get attached whatever the subject. Others come from web-ui-craft itself: both baseline pages took the same typeface from its candidate list.

### Findings
- The cursor-following spotlight card ships ready-made in several libraries, checked on 8 November 2026. Aceternity UI's "card spotlight" installs through the shadcn CLI and depends on framer-motion. [Aceternity UI, card spotlight](https://ui.aceternity.com/components/card-spotlight) Magic UI's Magic Card is "A spotlight effect that follows your mouse cursor and highlights borders on hover." [Magic UI, Magic Card](https://v3.magicui.design/docs/components/magic-card) An account named @claude-ai on 21st.dev publishes "Interactive cards with a radial mouse-following spotlight glow". [21st.dev, Spotlight Cards](https://21st.dev/@claude-ai/components/spotlight)
- Geometric grain (a dot pattern, a hairline grid or noise over the whole dark surface) is the fifth of Brainy Papers' SaaS tells; see `ai-slop-and-distinctiveness.md`.
- Two baseline pages were built with web-ui-craft at 409a764 from separate prompts (a database-branching tool and a hardware sequencer). Both picked Schibsted Grotesk from the "contemporary grotesk" row of the candidate list in `visual-system.md`, and both paired it with a mono face from the same list (Spline Sans Mono, Martian Mono) used for every label and figure. Both tinted their neutrals cool (hues 240 and 250) and separated sections with hairlines. The checker reported no tells on either page.

### Inferences
- A named list of recommended fonts becomes the default for a model that reads it, as Anthropic's 2025 list did for Space Grotesk. Two builds show convergence; they do not measure how often it happens.
- No source examined calls the spotlight card a tell. It is treated as a default here because it is installed whole and attached to cards whatever the subject, which is the same mechanism that spread the three-card grid.

## 6. Implications for web-ui-craft

- A method for building the hero piece in code when no assets exist, with a fidelity checklist.
- Light from a believable source allowed as a material; decorative glow stays a tell.
- The two-tone headline separated from the single accent word.
- Motion taught by site tier, with choreography, springs, shared-element motion, scroll-linked animation and a hero piece that plays itself.
- Speed measured in the critique step, with a weight budget for the spectacle.
- The giveaway list reframed as defaults versus decisions and updated with frontend-design's clusters.
- The font candidate list replaced by a method for finding a face, since the list itself became the default.
- From frontend-design: compared layout sketches, the convergence test, type as an active element, the copy consistency rule.
- A premium bar in the critique: compare the build with a reference site in the same direction.

## 7. Before and after

### Takeaway
With the same two prompts, the revised skill produced hero pieces that hold a long look: a lit object with modelled pads and sockets, and a product screen with a sidebar, a log and a loop that plays itself. Speed did not suffer. The two pages no longer share a typeface or a mono label system. The static checker found no tells on any of the four pages, so the difference shows only in the screenshots. The rebuilds also exposed a new source of default: examples in the skill that matched the test subjects were copied into the pages.

### Method
Both pages were built on 8 November 2026 by a subagent given the verbatim prompt and the skill folder, with no access to the baseline pages or notes. The baselines used the skill at 409a764; the rebuilds used it at da61a11. Figures come from Lighthouse 13.6.0 in its default mobile profile against `python -m http.server`, read with `check_budgets.py`.

| Page | LCP | CLS | Total blocking time | Script | Non-composited animations |
|---|---|---|---|---|---|
| Brand, before | 1392 ms | 0.092 | 0 ms | 4 KiB | 0 |
| Brand, after | 996 ms | 0.000 | 0 ms | 5 KiB | 0 |
| Product, before | 1396 ms | 0.015 | 0 ms | 7 KiB | 0 |
| Product, after | 1542 ms | 0.047 | 0 ms | 5 KiB | 0 |

Budgets: LCP 2500 ms, CLS 0.1, total blocking time 200 ms, script 75 KiB. All eight runs pass.

### Findings
- Brand page (Kestrel S-16). Before: a flat dark panel of amber squares, mono on every label, hairlines between sections, Schibsted Grotesk. After: the sequencer drawn as an object lit from the upper left, with bevelled pads, light leaking round the lit ones, corner screws, and a rear panel of hex-nut jacks and a five-pin MIDI socket. The headline is Archivo at 68% width and weight 800, 128 px against 11 px legends. There is no mono face, and rules appear only inside the specification table. The ground is still a pale cool grey (hue 245 against the baseline's 250), now traced to bead-blasted aluminium. Below the hero, the specification table and pre-order band carry little to look at. The builder compared the page with Teenage Engineering and named photographic light and parts detail as the largest gap, which code alone could only partly close.
- Product page (Forkline). Before: an abstract block map in a hairline card, then a plain terminal. After: a dark product screen that bleeds off the right edge, with a pull-request sidebar, a map of 144 heap pages for production and the branch, a command log and a progress bar, playing a 10 s loop. A second piece is a bot comment on the pull request with a table of checks. Type is IBM Plex Sans at 85% width, with Plex Mono for code only, on a pale green ground taken from greenbar printer paper. The builder compared the page with Linear, named the density of detail around the hero as the largest gap, and added the sidebar to close part of it. A dark panel with a yellow accent sits near the near-black and acid cluster; the builder kept it because the page around it is light and the yellow has one meaning.
- Self-hosting the font with a `size-adjust` fallback face gave CLS 0.000. Linking Google Fonts without a fallback face gave 0.047. Requested without a browser User-Agent, the Google Fonts stylesheet lists only TrueType files.
- The product page used `PR #4127` and branch ids ending `7f3c`, the identifiers in `artefacts.md`. Those examples, and the motion and font-reason examples in other references, described the test subjects themselves, so the rebuilds were partly guided by them. Five such examples were replaced with unrelated subjects after these builds.
- Builders reported four instructions they could not follow as written: the screenshot of a self-playing piece caught a random frame; the fidelity checklist required an operable hero to leave the tab order; the light guidance described only dark pages; and the convergence test did not say whether a line may stay when the two subjects share the fact behind it. Each was revised.

### Inferences
- The largest change is in the hero piece, which is where the revised skill put its effort. It came from building a piece in code to a checklist, not from new libraries or more script: both rebuilds ship 5 KiB of script.
- Some of the gain on the product page may come from the leaked examples rather than the method, so a fresh subject would test the method more fairly.

## Gaps

- Single 1440 px viewport per site; no mobile screenshots, no scroll or interaction recorded.
- Motion evidence is from source text, not traces.
- Russell's budgets assume a P75 device and network; no source examined splits a page's script budget between its base and a spectacle layer, so the split in web-ui-craft's brief is a judgement per page.
- The frontend-design file is plugin version 1.1.1, as installed on 8 November 2026.
- The before and after comparison is one build per subject per version, so the variation between runs of the same skill is unmeasured. The screenshots were judged by the skill's author, not by blind raters.
- Neither rebuild had a browser tool, so the frame rate of each loop, keyboard walks and the brand page's sound were not checked.
