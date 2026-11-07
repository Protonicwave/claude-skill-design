# What makes web UI feel great: interaction, navigation, motion, micro-interactions, performance and accessibility

Notes compiled November 2026. Every bullet carries an inline source. Where a fetch failed or only secondary sources were available, this is stated.

## 1. Navigation, information architecture, usability heuristics and Laws of UX

### Takeaway
Visible navigation beats hidden navigation on every measured metric. Show top-level links on desktop, show up to 4 links visibly on mobile, and use a hamburger or combo menu only beyond that. Sticky headers should be small, opaque and barely animated. Nielsen's 10 heuristics (unchanged since 1994) and a short list of laws (Fitts, Hick, Jakob, Doherty, Miller, Peak-End, Postel, Tesler) are the most directly actionable framing for web UI.

### Cited Findings

**Hidden versus visible navigation (NN/g, 179 participants, 6 sites)**
- Desktop: hidden menus were used in 27% of cases, visible navigation in 48%, combo navigation in 50%. Mobile: hidden navigation used in 57% of cases, combo in 86%. [NN/g, Hamburger Menus and Hidden Navigation Hurt UX Metrics](https://www.nngroup.com/articles/hamburger-menus/)
- Hidden navigation cut content discoverability by more than 20% versus visible or combo navigation on both desktop and mobile; the drop was larger on desktop. [NN/g](https://www.nngroup.com/articles/hamburger-menus/)
- Hidden navigation made desktop tasks at least 39% slower than visible or combo, and mobile tasks 15% slower than combo. Perceived difficulty (1 to 7, lower is better): hidden 2.6, combo 2.3, visible 2.1, so hidden was rated 21% harder than visible. [NN/g](https://www.nngroup.com/articles/hamburger-menus/)
- Recommendations: on desktop avoid hamburger icons and show top-level links across the top or down the left; on mobile with 4 or fewer top-level links, show them visibly; with more than 4, put some in an expandable menu and add in-page links to important content. [NN/g](https://www.nngroup.com/articles/hamburger-menus/)
- NN/g's mobile-first article concludes that hiding navigation under a menu significantly decreases navigation use and degrades the overall experience on desktop and mobile. [NN/g, Mobile First Is NOT Mobile Only](https://www.nngroup.com/articles/mobile-first-not-mobile-only/)

**Sticky headers (NN/g)**
- Five rules: keep it small (minimum height that gives readable text and tap targets of at least 1 cm by 1 cm); high contrast and opaque, not translucent; minimal motion, no delayed "stalker" menus that trail scroll; consider a partially persistent header that reappears on scroll-up; question whether you need one at all. [NN/g, Sticky Headers: 5 Ways to Make Them Better](https://www.nngroup.com/articles/sticky-headers/)
- Partially persistent headers should trigger after a few pixels of upward scroll and slide in over roughly 300 to 400 ms so they feel scrolled into view; let the animation complete even if scrolling stops. [NN/g](https://www.nngroup.com/articles/sticky-headers/)
- Start from the 1 cm tap target and roughly 16pt text minimums, then remove all extra vertical height; NN/g cites a 13:1 content-to-chrome ratio as a reasonable trade-off versus a wasteful 2:1. [NN/g](https://www.nngroup.com/articles/sticky-headers/)
- A frequently repeated claim that sticky headers save "22% of navigation time" is attributed to NN/g only by secondary blogs; the NN/g article itself contains no time-savings data. [Martin Koss blog (secondary)](https://martinkoss.com/sticky-headers-yes-or-no-what-users-actually-want/); contradicted by [NN/g](https://www.nngroup.com/articles/sticky-headers/)

**Breadcrumbs and local navigation**
- Breadcrumbs are considerably more compact (usually one line) than stacked local navigation but show no sibling pages; local navigation is a valuable orientation and wayfinding aid. [NN/g, Local Navigation](https://www.nngroup.com/articles/local-navigation/)

**Search and e-commerce navigation (Baymard, headline-level data only)**
- Search autocomplete is used on 90% of major e-commerce sites; a 2019 benchmark found 27% of sites had autocomplete implementations with several severe usability issues. [Baymard, autocomplete design](https://marketing-site-78zahjm59-baymard.vercel.app/blog/autocomplete-design)
- Baymard headlines: 69% of sites do not offer relevant autocomplete suggestions for closely misspelled queries; 58% do not copy the active autocomplete suggestion into the search field. [Baymard research archive](https://baymard.com/research-articles/archive)
- 2024 benchmark: 76% of leading US and European sites rated mediocre to poor for homepage and category navigation; 2025 headline: 67% of mobile sites mediocre to poor; only 24% offer a "View All" option at each level of the mobile product catalogue. [Baymard research archive](https://baymard.com/research-articles/archive)

**Command palettes (Cmd+K)** (practitioner sources only; no NN/g or Baymard research found)
- Cmd+K is the common trigger (Superhuman, Linear, Slack); VS Code and Sublime use Cmd+Shift+P. Superhuman's rule: the palette must be "the one place where users can find every command". In editors where Cmd+K inserts a link, Superhuman remaps it to do what people expect. [Superhuman, How to build a remarkable command palette](https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/)
- Fuzzy matching tuned for prefix/substring typing (cmdk uses `command-score`), searchable keywords/synonyms per command, and showing each command's keyboard shortcut so the palette teaches shortcuts. [Superhuman](https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/)
- Escape closes; arrows and Enter navigate and select; when focus is in a text field, only an explicit Cmd/Ctrl+K should open the palette; recent commands first when repeat speed matters more than discovery. [Playbooks web-ux-command-palette (practitioner)](https://playbooks.com/skills/gwenwindflower/.charmschool/web-ux-command-palette); [Chameleon, CMD+K search](https://www.chameleon.io/patterns/cmd-k-search)
- Rauno Freiberg reports that animating a command menu used hundreds of times a day made it feel sluggish; frequent, low-novelty actions should skip animation. [Rauno, Invisible Details of Interaction Design](https://rauno.me/craft/interaction-design)

**URL and navigation mechanics (Vercel Web Interface Guidelines)**
- Store UI state in the URL so share, refresh and Back/Forward work; filters, tabs, pagination, expanded panels and `useState` values should be deep-linkable. [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines)
- Use real `<a>`/`<Link>` for navigation so Cmd/Ctrl+Click, middle-click and right-click work; Back/Forward must restore scroll position; `<title>` reflects current context; set `scroll-margin-top` on anchored headings so sticky headers do not cover them. [Vercel](https://vercel.com/design/guidelines)

**Nielsen's 10 usability heuristics** (last reviewed 30 January 2024; heuristics unchanged since 1994)
1. Visibility of system status. 2. Match between system and real world. 3. User control and freedom (clear exits, undo). 4. Consistency and standards. 5. Error prevention. 6. Recognition rather than recall. 7. Flexibility and efficiency of use (shortcuts for experts). 8. Aesthetic and minimalist design. 9. Help users recognise, diagnose and recover from errors. 10. Help and documentation. [NN/g, 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)

**Laws of UX most relevant to web UI** ([lawsofux.com](https://lawsofux.com/) lists 30)
- Fitts's Law: pointing time grows with distance and shrinks with target size. [Laws of UX](https://lawsofux.com/) Screen corners act as effectively infinite targets; radial menus hold distance and size constant. [Rauno](https://rauno.me/craft/interaction-design)
- Hick's Law: decision time rises with number and complexity of choices. Choice Overload: too many options impair choosing. [Laws of UX](https://lawsofux.com/)
- Jakob's Law: users expect your site to work like the sites they already use. [Laws of UX](https://lawsofux.com/)
- Doherty Threshold: productivity peaks when system and user respond within about 400 ms; from Doherty and Thadani, IBM Systems Journal 1982, which lowered the previous 2-second standard. Takeaways: feedback within 400 ms, use perceived-performance techniques, progress bars help even when imprecise. [Laws of UX, Doherty Threshold](https://lawsofux.com/doherty-threshold/)
- Miller's Law (7 plus or minus 2 items in working memory), Chunking, Serial Position Effect (first and last items recalled best), Von Restorff (the distinct item is remembered), Peak-End Rule (experiences judged by peak and ending), Postel's Law (lenient input, strict output), Tesler's Law (complexity cannot be removed, only moved), Aesthetic-Usability Effect (attractive designs judged easier to use), Goal-Gradient, Zeigarnik, Gestalt laws (Proximity, Common Region, Similarity, Uniform Connectedness, Pragnanz). [Laws of UX](https://lawsofux.com/)

### Inferences
- For product apps, a visible primary nav plus a Cmd+K palette satisfies both heuristic 6 (recognition) and heuristic 7 (expert accelerators); the palette should not animate, or should animate minimally, given its frequency.
- Postel's Law and the Vercel form rules converge: trim whitespace, accept paste, accept varied formats.
- Peak-End implies investing polish in completion states (success toasts, confirmations) and in the end of flows, not only first impressions.

### Gaps
- No primary NN/g or Baymard study on command palettes was found; guidance is practitioner-level.
- Baymard's full 2025 benchmark numbers (mega menus, autocomplete scores) are paywalled; only headline figures are cited.
- NN/g breadcrumb article was not fetched directly; breadcrumb guidance here is limited.

## 2. Motion: easing, durations, springs, interruptibility, reduced motion

### Takeaway
Most UI motion should be under 300 ms, use a strong ease-out for entering and exiting elements, animate only `transform` and `opacity`, originate from the trigger, stay interruptible, and be skipped entirely for high-frequency or keyboard-initiated actions. Respect `prefers-reduced-motion` by swapping movement for an opacity fade.

### Cited Findings

**Durations**
- "Your animations should also usually be shorter than 300ms." A 500 ms enter animation on a frequently opened launcher (Raycast) is cited as frustrating. [Emil Kowalski, Great animations](https://emilkowal.ski/ui/great-animations)
- A 180 ms select animation feels more responsive than a 400 ms one; remove animations for interactions seen many times a day. [Emil Kowalski, 7 practical animation tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- Tooltip example: `transition: transform 0.125s ease-out, opacity 0.125s ease-out;` from `opacity: 0; transform: scale(0.97)`. [Emil Kowalski, 7 tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- Larger, gesture-driven surfaces run longer: Vaul's drawer uses 500 ms with `cubic-bezier(0.32, 0.72, 0, 1)` (borrowed from Ionic to match the iOS sheet). [Emil Kowalski, Building a drawer component](https://emilkowal.ski/ui/building-a-drawer-component)
- Sticky header slide-in: roughly 300 to 400 ms. [NN/g](https://www.nngroup.com/articles/sticky-headers/)
- Material 3 duration tokens (secondary sources, official page did not render): short1 to short4 = 50 to 200 ms, medium1 to medium4 = 250 to 400 ms, long1 to long4 = 450 to 600 ms, extra-long1 to extra-long4 = 700 to 1000 ms, in 50 ms steps. [hydrolysis-m3 tokens](https://docs.rs/crate/hydrolysis-m3/latest/source/src/theme/motion/tokens.rs); [bevy_material_ui tokens](https://docs.rs/crate/bevy_material_ui/latest/source/src/tokens.rs)

**Easing**
- Use `ease-out` for entering and exiting elements; it starts fast and so feels more responsive. At the same 300 ms, an `ease-in` dropdown feels slower than an `ease-out` one. Built-in CSS easings are often too weak; use custom stronger ease-out curves. [Emil Kowalski, 7 tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- Sonner deliberately uses `ease` and a slightly slower toast for an elegant feel. [Emil Kowalski, Great animations](https://emilkowal.ski/ui/great-animations)
- Material 3 easing (secondary sources): emphasized `cubic-bezier(0.2, 0, 0, 1)`; emphasized-decelerate `(0.05, 0.7, 0.1, 1)` for entering; emphasized-accelerate `(0.3, 0, 0.8, 0.15)` for exiting. Newer M3 Expressive material lists `(0.05, 0.7, 0.1, 1)` as "expressive", so naming has shifted. [hydrolysis-m3](https://docs.rs/crate/hydrolysis-m3/latest/source/src/theme/motion/tokens.rs); conflicting naming in [Material 3 motion skill doc](https://www.skills.lc/shelbeely/Shelbeely-Agent-skills/shelbeely-shelbeely-agent-skills-skills-material-design-3-motion-skill-md)
- Match easing to what changes (size, distance, trigger). [Vercel](https://vercel.com/design/guidelines)

**Specific techniques**
- Press feedback: scale buttons to `0.97` on `:active`. [Emil Kowalski, 7 tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- Never animate from `scale(0)`; start at 0.9 or above (example 0.93). [Emil Kowalski, 7 tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- Popovers scale from their trigger, not from centre: use `var(--radix-dropdown-menu-content-transform-origin)` (Radix) or `var(--transform-origin)` (Base UI). [Emil Kowalski, 7 tips](https://emilkowal.ski/ui/7-practical-animation-tips) Vercel: anchor transform origin to where motion physically starts. [Vercel](https://vercel.com/design/guidelines)
- Use `filter: blur(2px)` during a crossfade to mask imperfect transitions. [Emil Kowalski, 7 tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- Drawer items: combine opacity with a height animation. [Emil Kowalski, Great animations](https://emilkowal.ski/ui/great-animations)
- Never use `transition: all`; list properties explicitly. For SVG, transform a `<g>` wrapper with `transform-box: fill-box; transform-origin: center`. [Vercel](https://vercel.com/design/guidelines)

**When to animate, and when not**
- Animate only where it adds information (state change, modal enter/exit); "never animate keyboard initiated actions" because they can repeat hundreds of times a day. [Emil Kowalski, Great animations](https://emilkowal.ski/ui/great-animations)
- Animate only to clarify cause and effect or for deliberate delight. [Vercel](https://vercel.com/design/guidelines)
- Frequent, low-novelty actions should skip animation: macOS context menus and the app switcher appear without motion. [Rauno](https://rauno.me/craft/interaction-design)
- Avoid autoplay except muted, non-essential loops; motion lasting over 5 seconds alongside other content needs pause/stop/hide controls. [Vercel](https://vercel.com/design/guidelines)

**Interruptibility, physics, gestures**
- Animations must be cancellable by user input. [Vercel](https://vercel.com/design/guidelines)
- In CSS, prefer transitions over keyframes for interactive UI because transitions retarget smoothly mid-flight; use libraries such as Framer Motion for interruptible JS animation. [Emil Kowalski, Great animations](https://emilkowal.ski/ui/great-animations)
- Motion should inherit momentum and angle from the gesture; a settings screen that ignores a reverse swipe until its animation ends feels unresponsive. [Rauno](https://rauno.me/craft/interaction-design)
- Gestures should apply input directly (scale follows the pinch) rather than play a canned animation after a threshold. Lightweight actions can fire mid-gesture; destructive ones should wait for gesture end. [Rauno](https://rauno.me/craft/interaction-design)
- Spatial consistency: motion should show where content comes from and goes to. [Rauno](https://rauno.me/craft/interaction-design)
- Vaul details: drag is only allowed when content is scrolled to the top; drag is locked for 100 ms after scrolling reaches the top to stop accidental dismissal; only the first touch is honoured; snap points can be viewport fractions or pixels. [Emil Kowalski, drawer](https://emilkowal.ski/ui/building-a-drawer-component)
- Springs: tune stiffness, damping and mass; Emil gives no specific values. [Emil Kowalski, Great animations](https://emilkowal.ski/ui/great-animations)

**Performance of motion**
- Animate `transform` and `opacity` only; they trigger only compositing, while padding/margin/width trigger layout and paint. Target 60 fps. When the main thread is busy, prefer CSS or WAAPI (hardware accelerated) over `requestAnimationFrame`-driven libraries. [Emil Kowalski, Great animations](https://emilkowal.ski/ui/great-animations)
- Preference order: CSS, then Web Animations API, then JS libraries. [Vercel](https://vercel.com/design/guidelines)
- Animating `height`, `width` or position properties causes layout shifts that count towards CLS; use `transform: scale()` / `translate()`. [web.dev, CLS](https://web.dev/articles/cls)

**Reduced motion**
- Under `@media (prefers-reduced-motion: reduce)`, swap movement for a fade (example 0.2 s), or in Framer Motion use `useReducedMotion` and set the x offset to 0; animate only opacity for these users. [Emil Kowalski, Great animations](https://emilkowal.ski/ui/great-animations)
- WCAG 2.3.3 Animation from Interactions (AAA): motion animation triggered by interaction can be disabled unless essential. Colour and opacity changes are not "motion animation"; parallax and scroll-linked decorative motion are typically non-essential. Sufficient techniques C39/SCR40 use `prefers-reduced-motion`. [W3C Understanding 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)

**View Transitions API**
- Same-document transitions via `document.startViewTransition(callback)`; cross-document (MPA) transitions opt in with `@view-transition { navigation: auto; }` on both pages, with `pageswap`/`pagereveal` events as hooks. `view-transition-name` lets an element morph independently; pseudo-elements `::view-transition`, `::view-transition-group()`, `::view-transition-image-pair()`, `::view-transition-old()`, `::view-transition-new()`; also `view-transition-class` and `:active-view-transition-type()`. [MDN, View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)

### Inferences
- A sensible default token set for web UI: 100 to 150 ms for hovers, presses and tooltips; 150 to 250 ms for dropdowns, popovers and small surfaces; 250 to 400 ms for modals, sheets and page transitions; up to 500 ms only for large gesture-driven sheets. This aligns Emil's under-300 ms rule with M3's short/medium bands.
- Enter/exit asymmetry: exits can be shorter than entries because the user has already decided; Emil's ease-out-for-both advice and M3's decelerate-in/accelerate-out tokens both support fast, non-lingering exits.
- With view transitions, wrap `startViewTransition` in a reduced-motion check and feature-detect it.

### Gaps
- Apple HIG Motion page did not render; no direct quotes. General HIG themes (purposeful, brief, cancellable, honour Reduce Motion) are consistent with the sources above but are not cited here.
- Official Material 3 token page did not render; M3 values above come from third-party token implementations and should be treated as secondary. Material 2 "speed and timing" page also failed to render.
- No primary source gave specific spring parameter values or a dismissal velocity threshold.
- Browser support status for cross-document view transitions was not confirmed from MDN's compatibility table.

## 3. Micro-interactions and polish

### Takeaway
Polish comes from a dense set of small rules: visible `:focus-visible` rings, hit areas of at least 24px (44px on mobile), delayed then minimum-duration loading indicators, optimistic updates with rollback or undo, skeletons that match final layout, aria-live toasts, and forms that never block input. The Vercel Web Interface Guidelines are the most complete public checklist.

### Cited Findings
All bullets in this subsection are from [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines) unless otherwise stated.

**States and feedback**
- Loading timing: delay spinners or skeletons by about 150 to 300 ms, and once shown keep them visible for at least about 300 to 500 ms (prevents flashes).
- Loading buttons show an indicator and keep the original label.
- Optimistic updates: update UI immediately, reconcile with server, and on failure show an error and roll back or offer Undo.
- Destructive actions require confirmation or offer Undo within a safe window.
- Use an ellipsis character for menu items that open a follow-up and for in-progress states ("Saving…").
- Hover, active and focus states have more contrast than rest state.
- Every screen offers a next step or recovery path; design empty, sparse, dense and error states; layouts handle short, average and very long content.
- Skeletons match final content exactly.
- Error messages explain how to fix the problem; labels are specific ("Save API Key" not "Continue").

**Skeletons versus spinners versus progress (NN/g)**
- Under 1 second: no skeleton or spinner (a flash is jarring). About 2 to 10 seconds: skeleton for full-page loads, spinner for a single module. Over 10 seconds: progress bar with time estimate. Uploads/downloads/conversions: progress bar, not skeleton. Avoid frame-display skeletons (header/footer only); pulsing or shimmer skeletons can distract and raise accessibility concerns. [NN/g, Skeleton Screens 101](https://www.nngroup.com/articles/skeleton-screens/)

**Tooltips and toasts**
- Delay the first tooltip in a group; peers then open instantly. [Vercel](https://vercel.com/design/guidelines) Emil: once one tooltip is open, neighbours open with no delay and no animation (Base UI `data-instant` with `transition-duration: 0ms`). [Emil Kowalski, 7 tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- Prefer inline help; tooltips are a last resort.
- Toasts and inline validation announce via polite `aria-live`.

**Focus and keyboard**
- Every focusable element has a visible, unobscured ring; use `:focus-visible` rather than `:focus`, `:focus-within` for grouped controls; sticky elements and overlays must not cover focused elements.
- Every flow works by keyboard following WAI-ARIA authoring patterns; trap, move and restore focus per those patterns.
- Shortcuts support non-QWERTY layouts and show platform-specific symbols.
- Autofocus the single primary input on desktop; rarely on mobile.

**Targets and touch**
- Hit target matches the visual; if the visual is under 24px expand the hit area to at least 24px; on mobile at least 44px.
- Checkboxes and radios share one generous hit target with their labels; no dead zones (anything that looks interactive is interactive).
- `touch-action: manipulation` on controls to prevent double-tap zoom; set `-webkit-tap-highlight-color` deliberately.
- Every drag, swipe or pinch has a click/tap and keyboard alternative unless essential; during drag, disable text selection and set `inert` on the dragged element.
- Touch occlusion: a finger hides what it acts on, hence magnifier loupes and enlarged keys; sliders may keep drag active when the thumb wanders. [Rauno](https://rauno.me/craft/interaction-design)

**Scroll behaviour**
- `overscroll-behavior: contain` in modals and drawers; under `@media (pointer: fine)` set `overscroll-behavior: none` on `<html>` to stop desktop rubber-banding.
- Back/Forward restores scroll; show only useful scrollbars and test with macOS scrollbars set to "Always".

**Forms**
- Input font size at least 16px to prevent iOS Safari zoom on focus; never disable browser zoom; never block paste.
- Enter submits when one text input is focused; in textareas Cmd/Ctrl+Enter submits.
- Keep submit enabled until submission starts, then disable it, show a spinner and send an idempotency key; do not pre-disable submit, let users submit to see errors.
- Do not block keystrokes; show validation instead. Errors sit beside fields and the first error receives focus on submit.
- Correct `type`, `inputmode`, `autocomplete` and `name`; disable spellcheck for emails, codes and usernames; trim whitespace; warn before leaving with unsaved changes; inputs keep focus and value after hydration.

**Visual polish details**
- At least two shadow layers (ambient plus direct light); combine borders with shadows, semi-transparent borders sharpen edges; child radii no larger than and concentric with the parent; nudge ±1px for optical alignment; `tabular-nums` for comparable numbers; curly quotes and the single ellipsis character; non-breaking spaces between numbers and units; `theme-color` matches page background; `color-scheme` set on `<html>` in dark themes; respect safe areas with `env()` insets.

### Inferences
- The Vercel delay-then-minimum rule (150 to 300 ms delay, 300 to 500 ms minimum) and the NN/g "nothing under 1 s" rule agree: most fast actions should show no loading indicator at all, only the result.
- Optimistic UI is the practical way to stay under NN/g's 0.1 s "instantaneous" limit for network-bound actions.

### Gaps
- Primary NN/g articles on empty states, error message design and toast timing (auto-dismiss duration) were not fetched; no sourced number for toast display duration was found.
- No research-grade source was found quantifying the effect of press-scale or hover feedback on perceived quality.

## 4. Perceived performance

### Takeaway
Hit Core Web Vitals at the 75th percentile (LCP at most 2.5 s, INP at most 200 ms, CLS at most 0.1), respond to input within 100 ms where possible and 400 ms at most, reserve space for everything that loads late, control font swapping, and prefetch or prerender likely next pages with Speculation Rules.

### Cited Findings

**Response-time limits**
- 0.1 s: feels instantaneous, direct manipulation, no extra feedback needed. 1 s: flow of thought preserved; beyond 1 s show that work is happening. 10 s: attention limit; beyond it show a percent-done indicator and a clear way to interrupt. For 2 to 10 s, subtler feedback (busy cursor, slowly changing counter) beats a full progress bar. When work amount is unknown, show progress in absolute terms (items processed); spinners are the last resort. [NN/g, Response Times: The 3 Important Limits](https://www.nngroup.com/articles/response-times-3-important-limits/)
- Doherty threshold: feedback within 400 ms. [Laws of UX](https://lawsofux.com/doherty-threshold/)
- `POST`, `PATCH` and `DELETE` should complete in under 500 ms. [Vercel](https://vercel.com/design/guidelines)

**Core Web Vitals**
- Good thresholds: LCP at most 2.5 s; INP at most 200 ms; CLS at most 0.1; assessed at the 75th percentile of page loads, segmented by mobile and desktop; a page passes only if all three pass. INP became stable in 2024, replacing FID. Page last updated 31 October 2024. [web.dev, Web Vitals](https://web.dev/articles/vitals)
- INP: good at most 200 ms, needs improvement 200 to 500 ms, poor over 500 ms. Counts clicks, taps and key presses (not scroll, hover or zoom). Three phases: input delay, processing duration, presentation delay. Unlike FID, INP considers all interactions. [web.dev, INP](https://web.dev/articles/inp)
- CLS: good at most 0.1, needs improvement 0.1 to 0.25, poor over 0.25. Shifts within 500 ms of a discrete input (tap, click, keypress) are excluded; scrolls and drags do not count as input. Session windows: shifts less than 1 s apart, window capped at 5 s; CLS is the worst window. [web.dev, CLS](https://web.dev/articles/cls)
- CLS causes and fixes: set image/video dimensions; reserve space for ads and embeds; insert dynamic content below the viewport or into reserved space; match fallback font metrics; animate with transforms; show a loader and reserve space immediately for user-triggered loads. [web.dev, CLS](https://web.dev/articles/cls)

**Fonts**
- `font-display: swap` (0 ms block, infinite swap) for branding text that must show immediately; `optional` (100 ms block, no swap) is the most performant with no swap shift, suited to body text; `fallback` (100 ms block, 3 s swap) is a middle ground; `block` hides text 2 to 3 s; `auto` varies (Chromium/Firefox up to 3 s, Safari indefinitely), so set an explicit value. [web.dev, Font best practices](https://web.dev/articles/font-best-practices)
- Use WOFF2 only (about 30% smaller than WOFF); subset with `unicode-range`; preload only a few critical fonts (preload ignores `unicode-range`); preconnect to the font origin with `crossorigin`; inline `@font-face` in `<head>`; use `size-adjust` on the fallback to reduce shift; replace icon fonts with SVG. [web.dev, Font best practices](https://web.dev/articles/font-best-practices)

**Loading and rendering hygiene** ([Vercel](https://vercel.com/design/guidelines))
- Preload only above-the-fold images, lazy-load the rest; explicit image dimensions; preconnect to asset/CDN origins; virtualise large lists or use `content-visibility: auto`; move long tasks to Web Workers; batch DOM reads and writes; prefer uncontrolled inputs; prefer looping `<video>` over GIFs; profile with CPU and network throttling and test on iOS Low Power Mode and macOS Safari.

**Prefetching and prerendering (Speculation Rules API)**
- Chrome's blog described `moderate` eagerness as triggering after a 200 ms hover or on pointerdown; Chromium allows up to 50 prefetches and 10 prerenders for immediate/eager, and 2 each (FIFO) for moderate/conservative. [Chrome for Developers, Speculation rules improvements](https://developer.chrome.com/blog/speculation-rules-improvements?authuser=00)
- A December 2025 article by Barry Pollard (Chrome DevRel) states desktop `moderate` now fires after a 10 ms hover; mobile `eager` considers all viewport links 100 ms after scrolling stops; mobile `moderate` uses heuristics (500 ms after scroll stops, links within 30% vertical distance of the last pointerdown, links at least 0.5 times the size of the largest viewport anchor). Recommended pattern: prefetch with `eager`, prerender with `moderate`. `prerender_until_script` is behind a flag. [HTMHell Advent 2025, Barry Pollard](https://htmhell.dev/adventcalendar/2025/3/) This contradicts the earlier 200 ms figure; the newer source is likely current.

**View Transitions** for perceived continuity between states and pages: see section 2. [MDN](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)

### Inferences
- INP's 200 ms "good" bound is looser than NN/g's 100 ms "instantaneous" bound; aim for the visual response (pressed state, optimistic change) within 100 ms and use INP as the floor, not the goal.
- Combining speculation-rules prerender with cross-document view transitions gives MPAs near-instant, animated navigations without an SPA.

### Gaps
- LCP "needs improvement" and "poor" thresholds were not in the fetched text (widely known as 2.5 to 4 s and over 4 s, but not verified in this session).
- The exact date INP replaced FID (web.dev says 2024; commonly reported as March 2024) was not confirmed in fetched text.
- Current browser support for Speculation Rules beyond Chromium was not confirmed.

## 5. Accessibility as part of quality

### Takeaway
WCAG 2.2 AA adds three requirements that directly shape "feel": focus must not be fully hidden (2.4.11), dragging needs a single-pointer alternative (2.5.7) and pointer targets must be at least 24 by 24 CSS px (2.5.8). Contrast stays at 4.5:1 for body text and 3:1 for large text and UI components. Spectacle stays accessible by honouring reduced motion, keeping motion off colour/opacity-only paths, and using semantic HTML before ARIA.

### Cited Findings
- WCAG 2.2 adds 9 success criteria: 2.4.11 Focus Not Obscured (Minimum, AA): focused component not entirely hidden by author content; 2.4.12 Focus Not Obscured (Enhanced, AAA): no part hidden; 2.4.13 Focus Appearance (AAA): indicator at least a 2 CSS px thick perimeter with at least 3:1 contrast between focused and unfocused states; 2.5.7 Dragging Movements (AA): single-pointer alternative unless essential; 2.5.8 Target Size Minimum (AA): at least 24 by 24 CSS px, with spacing, equivalent, inline, user-agent and essential exceptions; 3.2.6 Consistent Help (A); 3.3.7 Redundant Entry (A); 3.3.8 Accessible Authentication Minimum (AA): no cognitive function test without alternative or assistance (so allow paste and password managers); 3.3.9 Enhanced (AAA). 4.1.1 Parsing is removed as obsolete. [W3C, What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- 1.4.3 Contrast Minimum (AA): 4.5:1 for normal text, 3:1 for large text (18pt or 14pt bold, about 24px or 18.5px bold). 1.4.6 Enhanced (AAA): 7:1. Non-text UI and icons fall under 1.4.11 Non-text Contrast at 3:1. [W3C Understanding 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- 2.3.3 Animation from Interactions (AAA): interaction-triggered motion can be disabled; honour `prefers-reduced-motion`; colour/opacity changes are not motion animation; parallax is non-essential. [W3C Understanding 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
- Vercel's checklist puts accessibility into everyday polish: semantic HTML before ARIA; hierarchical headings and a skip link; accessible names for icon-only buttons; `aria-hidden` on decoration and verify in the accessibility tree; never rely on colour alone; captions and transcripts; keyboard-operable media controls; never disable zoom; recommends APCA over WCAG 2 contrast for design decisions. [Vercel](https://vercel.com/design/guidelines)
- Sticky headers must not cover focused elements (aligns with 2.4.11); use `scroll-margin-top`/`scroll-padding-top`. [Vercel](https://vercel.com/design/guidelines)
- Shimmering/pulsing skeletons can distract and create accessibility problems; prefer static or subtle. [NN/g, Skeleton Screens](https://www.nngroup.com/articles/skeleton-screens/)
- Reduced-motion implementations: replace movement with opacity fades. [Emil Kowalski](https://emilkowal.ski/ui/great-animations) For view transitions, disable `::view-transition-*` animations under reduced motion or skip `startViewTransition()` (MDN page did not itself cover this; pattern noted by the fetch summary as common practice). [MDN, View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API)

### Inferences
- Target-size layering: 24px is the WCAG AA legal floor, 44px is the practical mobile target (Vercel), and NN/g's 1 cm by 1 cm is roughly 38px on typical displays; designing to 44px on touch satisfies all three.
- "Accessible spectacle" pattern: use opacity, colour and blur for flourish (not counted as motion animation under 2.3.3), gate translate/scale/parallax behind `prefers-reduced-motion: no-preference`, and never trap focus or block input during an animation.
- Vercel's APCA recommendation conflicts with WCAG 2.2's normative ratio method; APCA is not part of WCAG 2.2, so legal conformance still requires the 4.5:1 / 3:1 checks.

### Gaps
- WCAG 2.5.5 Target Size (Enhanced, AAA, 44 by 44 CSS px) and 2.2.2 Pause, Stop, Hide were not fetched in this session.
- No primary source examined how specific award-winning, motion-heavy sites implement reduced-motion fallbacks in practice.
- WCAG 3.0 status in late 2026 was not researched.
