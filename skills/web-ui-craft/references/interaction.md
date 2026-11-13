# Interaction, motion and quality

What makes an interface feel good is mostly a dense set of small, checkable rules. This file holds them, ending with the critique checklist.

## Navigation

- **Keep it visible.** In Nielsen Norman Group's study of 179 people, hidden (hamburger) navigation on desktop was used in 27% of cases against 48% for visible links, cut content discoverability by more than 20%, and made tasks at least 39% slower. Show top-level links on desktop. On mobile, show up to four links visibly and put only the overflow in a menu. The phone header, links and action together, fits one row at 375 px: shorten labels, show fewer links or move the rest into the menu rather than let it wrap or push past the edge.
- **Sticky headers**: small, opaque, high-contrast, barely animated. Best compromise: hide on scroll down, slide back in over 300 to 400 ms on scroll up. Aim for a content-to-chrome ratio near 13:1, not 2:1.
- **Command palette** (Cmd/Ctrl+K) for apps with many actions: the one place every command can be found, fuzzy matching with synonyms, each result showing its shortcut, opening instantly with no animation. It sits on top of visible navigation, never instead of it.
- **Mechanics people notice when broken:**
  - Navigation uses real `<a>` elements so Cmd-click, middle-click and "open in new tab" work.
  - Filters, tabs, pagination and open panels live in the URL so refresh, share and Back work.
  - Back restores scroll position.
  - `<title>` reflects the current view.
  - Anchored headings have `scroll-margin-top` so sticky headers do not cover them.
- **Jakob's Law**: people expect a site to behave like the sites they already know. Invent visuals, not conventions. A beautiful page that breaks the Back button reads as broken.
- **Hick's Law**: each extra choice slows the decision. One primary action per view; secondary actions visibly secondary.

## Motion

Acclaimed sites move in one of two ways. Product sites (Linear, Raycast, Stripe) are fast and quiet: routine motion takes 120 to 300 ms, and the effort goes into the hero piece demonstrating itself and into elements travelling between states. Brand sites, where the site is the experience (Lando Norris, the Awwwards winners), choreograph the scroll itself with scrubbed scenes, smooth scrolling and real-time 3D. Pick the tier from the subject, name it in the brief's Motion line, and spend the motion where that tier spends it.

Every page gets one signature movement, a quiet page included, and it is a movement the subject makes in its own world: a parcel travelling its route, a print head laying down a line, the needle of a scale settling, a departure board flipping to the next train. On a restrained page it can be small, a figure ticking once or a mark drawing itself, but it still comes from the subject. A fade or slide applied to every block belongs to no subject: put the Motion line through the swap test, and if a neighbouring product could keep it unchanged, the movement has not been chosen yet.

### Choose the tier

| | Product tier | Brand tier |
|---|---|---|
| Subjects | Software, tools, finance, documentation, most businesses | A launch, a person, a studio, a physical product sold as an object of desire |
| Where motion goes | The hero piece playing itself, and elements moving between states | One scroll-driven scene, plus everything the product tier does elsewhere on the page |
| Timing | 120 to 300 ms for interface motion; 6 to 12 s loops for the hero piece | Scrubbed to the scroll, so the reader sets the pace; entrances up to about 1 s |
| Curves | Strong ease-out, and a settling spring with no visible overshoot | Expo ease-outs, and springs with visible overshoot |
| Tools | CSS transitions and keyframes, View Transitions, a few lines of script | CSS scroll-driven animations; GSAP ScrollTrigger when a scene pins through several steps; WebGL in one isolated layer |
| Benchmark | Linear, Raycast, Stripe | Lando Norris |

A Motion line that someone else could build from:

```
Motion: product tier. Signature moment: the dispatch board opens complete, every load
        placed, then plays a 9 s loop (a load is assigned, its lorry crosses the route map,
        the delivery slot turns green), lead element the lorry marker. Menus 150 ms ease-out;
        tabs and the command menu instant; nothing moves on scroll.
```

### Budget by frequency

Motion is earned by how rarely something happens and how much the change needs explaining.

| Frequency | Treatment |
|---|---|
| Many times a day, or keyboard-initiated (command menu, shortcuts, tab switching, typing) | No animation |
| Routine (hover, press, tooltip, dropdown) | 100 to 200 ms, or none |
| Occasional (modal, sheet, page transition, toast) | 200 to 400 ms |
| Rare and meaningful (onboarding, completion, the signature moment) | Longer and richer is fine |

Family's rule, "mastering delight is mastering selective emphasis": confetti only after a wallet backup, sound only on the trash action.

### Tokens

```css
:root {
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);   /* strong ease-out: fast start feels responsive */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1); /* elements moving between two on-screen positions */
  --ease-sheet: cubic-bezier(0.32, 0.72, 0, 1);  /* large gesture-driven sheets, as in Vaul */
  --dur-1: 120ms;  /* hover, press, tooltip */
  --dur-2: 200ms;  /* dropdown, popover */
  --dur-3: 300ms;  /* modal, page transition */
  --dur-4: 500ms;  /* drawer or sheet only, on a curve */

  /* Damped springs sampled into linear(); each shape belongs to its own duration. */
  /* Damping ratio 0.9: 95% of the way by 240 ms, overshoot 0.15%. Both tiers. */
  --spring-settle: linear(0, 0.005 1.2%, 0.023 2.8%, 0.094 6%, 0.494 18.8%, 0.591 22.2%,
    0.67 25.5%, 0.738 28.7%, 0.795 32%, 0.845 35.5%, 0.884 39%, 0.921 43.2%, 0.95 48%,
    0.972 53.2%, 0.986 59%, 0.995 65.5%, 1 73.5%, 1);
  --dur-settle: 500ms;
  /* Damping ratio 0.6: overshoots by 9% and settles back. Brand tier and playful subjects only. */
  --spring-bounce: linear(0, 0.008 1.2%, 0.029 2.5%, 0.123 5.5%, 0.244 8.2%, 0.65 16.5%,
    0.848 21.5%, 0.918 23.8%, 0.98 26.2%, 1.026 28.7%, 1.062 31.5%, 1.077 33.2%, 1.088 35.2%,
    1.094 37.5%, 1.094 39.8%, 1.081 44.8%, 1.019 58.8%, 0.998 67%, 0.993 72%, 0.991 78%, 1);
  --dur-bounce: 800ms;
}
```

### Rules

- Keep routine UI animation under 300 ms; a 180 ms select feels more responsive than a 400 ms one. Modals, sheets and page transitions take 200 to 400 ms, and only large gesture-driven sheets go up to 500 ms. These limits are for curves. A spring's duration is the time it takes to come to rest, not to arrive: `--spring-settle` covers 95% of its distance by 240 ms, so at `--dur-settle` it reads as routine motion.
- Use ease-out for things entering and leaving. Built-in `ease-out` is weak; use a stronger curve. Avoid `ease-in` for UI: it starts slowly and feels laggy. No visible overshoot in product UI: use `--spring-settle`, never `--spring-bounce`.
- Animate only `transform` and `opacity`. Width, height, top, left, margin and padding trigger layout and paint and cause jank and layout shift.
- Never `transition: all`. List the properties.
- Never animate from `scale(0)`. Start from 0.9 to 0.97 with opacity 0.
- Popovers, menus and tooltips grow from their trigger: use the component library's transform-origin variable (`var(--radix-dropdown-menu-content-transform-origin)`, `var(--transform-origin)`) or set the origin yourself.
- Press feedback: `transform: scale(0.97)` on `:active`.
- In a group of tooltips, delay the first; once one is open, neighbours open instantly with no animation.
- Animations must be interruptible. Prefer CSS transitions (which retarget mid-flight) over keyframes for interactive state.
- Spatial consistency: things should come from where they were summoned and return there. Family's "we fly instead of teleport".
- Gestures apply their movement directly (the sheet follows the finger) rather than playing a canned animation after a threshold, and the motion after release carries the gesture's velocity, which needs a JavaScript spring (Motion's `type: "spring"`), not a CSS curve. Destructive gesture actions commit on release, not mid-gesture.
- Content is visible before any script runs. A section hidden until an observer reveals it stays blank on slow devices, in print, to crawlers and in full-page screenshots. Reveal by enhancing visible content (add the hidden starting state from script, then animate), never by hiding it in the stylesheet.

### The signature moment

The one rare moment that gets rich motion, usually the hero on first view, is choreographed like a short film rather than switched on.

- **One lead.** One element moves first and furthest and carries the eye to where it should land. Everything else follows it and moves less.
- **Overlap, do not queue.** Followers start 40 to 80 ms apart, each before the previous one has finished. Steps that wait for each other read as slow.
- **One curve, durations by distance.** Elements that travel further take longer; small ones are quicker. Mixing curve families looks accidental.
- **Readable fast.** A page-load sequence is over in about 1 s and at rest by 1.5 s at the latest, and the headline is legible within the first 300 ms. Every piece of the first screen is present and readable in the first frame; the entrance moves things into place, it does not build them up. A chart still drawing its axes or a table still filling its rows after 1.5 s reads as loading, not as design. The LCP element never waits at opacity 0: Chrome does not count an element at opacity 0 as painted, so a delayed fade on the headline delays LCP. Move it without fading it.
- **The last frame is the design.** Compose the final frame first, then the route to it. Award jurors judge whether static frames look intentional without motion, and reduced-motion users see only that frame.
- **Once.** An entrance does not replay when the reader scrolls back or follows an anchor.
- **The hero piece can carry it.** On the product tier the signature moment is usually the piece playing itself, built as `artefacts.md` describes; the choreography rules above apply to each step of its loop.

```css
@media (prefers-reduced-motion: no-preference) {
  .hero > * {
    animation: arrive var(--dur-settle) var(--spring-settle) both;
    animation-delay: calc(var(--step, 0) * 60ms);
  }
  .hero > .lead { --rise: 32px; }
  @keyframes arrive { from { transform: translateY(var(--rise, 16px)); } }
}
```

Set `--step` on each child in order, with the lead at 0. Nothing fades: every child is painted at full opacity in the first frame and only moves into place, the lead furthest, so the first screen reads at once and the headline counts for LCP. A follower faded in from opacity 0 is still faint at a quarter of a second, and if it is the primary action, the reader's first look misses it.

### Shared-element motion

When something on screen changes place or state (a card opening into its detail, a thumbnail becoming the hero), move it there rather than cutting. Linear and Raycast both ship this. Two recipes:

**View Transitions**, for changes the browser can snapshot, including navigation between pages:

```js
function transition(applyChange) {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!document.startViewTransition || reduce) {
    applyChange();
    return;
  }
  document.startViewTransition(applyChange);
}
```

```js
// The clicked card carries the name in the old snapshot, the open detail in the new one.
card.style.viewTransitionName = "active-card";
transition(() => {
  card.style.viewTransitionName = "";
  openDetail(card);
});
```

```css
.detail { view-transition-name: active-card; }  /* display: none until opened */
::view-transition-group(active-card) {
  animation-duration: var(--dur-settle);
  animation-timing-function: var(--spring-settle);
}
```

- A `view-transition-name` must be unique among rendered elements when each snapshot is taken, or the transition is skipped. Give it to the one element involved, not to every card.
- For multi-page sites, `@view-transition { navigation: auto; }` in both pages' CSS gives the same continuity on ordinary links. Wrap it in `@media (prefers-reduced-motion: no-preference)`. Chromium and Safari support it; other browsers navigate normally, which is the right fallback.
- A view transition cannot be reversed halfway: starting another one skips the first to its end. For motion the user can reverse mid-flight, use FLIP.

**FLIP** (First, Last, Invert, Play), for changes inside a component or anything that must stay interruptible: measure the element, apply the change, then animate from the old position to the new one with a transform.

```js
function flip(element, applyChange) {
  const first = element.getBoundingClientRect();
  applyChange();
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const last = element.getBoundingClientRect();
  const dx = first.left - last.left;
  const dy = first.top - last.top;
  const style = getComputedStyle(element);
  element.animate(
    [{ transform: `translate(${dx}px, ${dy}px)` }, { transform: "none" }],
    {
      duration: parseFloat(style.getPropertyValue("--dur-settle")) || 500,
      easing: style.getPropertyValue("--spring-settle").trim() || "ease-out",
    },
  );
}
```

Translating is exact. Scaling to cover a size change also stretches text and corner radii, so when the size changes, keep the text in a child that fades in after the box has landed.

### Scroll-linked motion

On the product tier, nothing moves with the scroll unless it explains something, such as a reading-progress bar. Scroll-triggered reveals on every section are a template habit. On the brand tier, one scene can follow the scroll, and it should be scrubbed (its progress tied to scroll position, so the reader can stop it and run it backwards) rather than triggered.

CSS scroll-driven animations drive a keyframe animation from scroll position instead of time, with no script. A reveal tied to the element's own passage through the viewport:

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .scene-step {
      animation: rise linear both;
      animation-timeline: view();         /* after the shorthand, which resets it */
      animation-range: entry 0% cover 30%;
    }
  }
}
```

A pinned, scrubbed scene: a tall section with a sticky stage, the stage's animation driven by the section's passage through the viewport.

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .scene { height: 300vh; view-timeline-name: --scene; }
    .scene-stage { position: sticky; top: 0; height: 100vh; }
    .scene-object {
      animation: turn linear both;
      animation-timeline: --scene;
      animation-range: contain 0% contain 100%;
    }
  }
}
```

- The height and the pinning sit inside the same `@supports` block, so a browser without support shows the scene at its rest frame at normal height rather than 300vh of empty scroll.
- Each frame of the scene, including the first and the last, reads correctly on its own, because the reader can stop anywhere.
- Animate `transform` and `opacity` only, so the compositor can run the animation off the main thread.
- When a scene needs several pinned steps with labels, snapping, or more control than CSS gives, use GSAP's ScrollTrigger (`pin: true`, `scrub: true`). It ships as JavaScript and counts against the spectacle budget.
- Smooth-scroll libraries (Lenis on Lando Norris) belong to the brand tier only. They replace the browser's own scrolling, so test keyboard scrolling, find in page and anchor links after adding one.

### Pointer response

The hero piece can answer the pointer: a lit object turning a few degrees toward it, light moving across a surface. This is the object responding, not the page: a glow that trails the cursor across every card is decoration.

- Fine pointers only, behind `(hover: hover) and (pointer: fine)`. Touch shows the static frame.
- Small and damped: a few degrees of rotation or a few pixels of movement, easing toward the pointer rather than snapping to it, and back to rest when the pointer leaves.
- Read the pointer in `pointermove` and write at most once per frame. Measure the piece only when it may have moved (on the first move, and after a scroll or resize), never on every move.

```js
const piece = document.querySelector(".hero-piece");
const query = "(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)";
if (piece && matchMedia(query).matches) {
  let box = null;
  let pointer = null;
  let frame = 0;
  const forget = () => { box = null; };
  addEventListener("scroll", forget, { passive: true });
  addEventListener("resize", forget);
  piece.addEventListener("pointermove", (event) => {
    pointer = event;
    if (frame) return;
    frame = requestAnimationFrame(() => {
      frame = 0;
      box ??= piece.getBoundingClientRect();
      piece.style.setProperty("--px", ((pointer.clientX - box.left) / box.width - 0.5).toFixed(3));
      piece.style.setProperty("--py", ((pointer.clientY - box.top) / box.height - 0.5).toFixed(3));
    });
  });
  piece.addEventListener("pointerleave", () => {
    piece.style.setProperty("--px", "0");
    piece.style.setProperty("--py", "0");
  });
}
```

```css
.hero-piece {
  transform: perspective(1200px) rotateY(calc(var(--px, 0) * 6deg)) rotateX(calc(var(--py, 0) * -6deg));
  transition: transform var(--dur-settle) var(--spring-settle);
}
```

The transition retargets on every update, which is what makes the piece ease toward the pointer.

### Reduced motion

Colour and opacity changes do not count as motion under WCAG 2.3.3; translation, scaling, parallax and scroll-scrubbed movement do. Keep the flourish and remove the movement:

```css
.panel {
  opacity: 0;
  transition: opacity var(--dur-2) var(--ease-out);
}
.panel[data-open] { opacity: 1; }

@media (prefers-reduced-motion: no-preference) {
  .panel {
    transform: translateY(8px) scale(0.98);
    transition: opacity var(--dur-2) var(--ease-out), transform var(--dur-2) var(--ease-out);
  }
  .panel[data-open] { transform: none; }
}
```

Anything that moves for more than five seconds alongside other content needs a pause control. Autoplay video is muted and non-essential.

## States and feedback

- **Every state designed**: rest, hover, active, focus-visible, disabled, loading, empty, error, success, and content that is very short or very long.
- **Interactive states have more contrast than rest.** Hover and focus are visible changes, not a two-percent tint.
- **Loading indicators**: nothing for actions under about 1 s. Otherwise delay the indicator by 150 to 300 ms and, once shown, keep it for at least 300 to 500 ms so it never flashes. Skeletons for full-page loads of 2 to 10 s, matching the final layout exactly, static or subtly pulsing rather than shimmering. Progress bars with an estimate beyond 10 s.
- **Loading buttons** keep their label and add an indicator.
- **Optimistic updates**: change the interface immediately, reconcile with the server, and on failure roll back with an explanation or offer Undo.
- **Destructive actions** ask for confirmation or offer Undo within a safe window.
- **Empty states** explain what will appear and offer the action that fills them.
- **Errors** say what happened and how to fix it, next to the cause, in the interface's voice. They do not apologise.
- **Copy** is specific: "Save API key", not "Continue". Sentence case, active voice, from the user's side. An action keeps one name through the whole flow: "Publish" on the button, "Publishing…" while it runs, "Published" in the confirmation. An ellipsis character for in-progress states ("Saving…") and for menu items that open a follow-up.
- **Endings matter** (Peak-End Rule): completion, confirmation and success states deserve as much care as the hero.
- **A confirmation appears only after its action.** Success and error messages start `hidden` (or outside the DOM) and are shown by the event that produces them. "Order placed" under an empty form tells the visitor something false. The polite `aria-live` region that will announce the message is present and empty from load, since a region added at the moment of the change is not announced.

## Forms

- Inputs at least 16 px font size, or iOS Safari zooms on focus.
- Never disable browser zoom, never block paste.
- Correct `type`, `inputmode`, `autocomplete` and `name` on every field; `spellcheck="false"` on emails, codes and usernames.
- Enter submits a single-field form; Cmd/Ctrl+Enter submits from a textarea.
- Keep submit enabled until submission starts, then disable it and show progress. Let people submit to see what is missing.
- Validate on blur or submit, not on every keystroke. Errors sit beside their field; focus moves to the first error on submit.
- Required fields are marked; labels are visible, not placeholder-only.
- Warn before leaving with unsaved changes.

## Targets and touch

- Pointer targets at least 24 by 24 CSS px (WCAG 2.5.8); 44 px on touch. If the visual is smaller, extend the hit area with padding or a pseudo-element.
- Checkboxes and radios share a hit area with their labels. Nothing that looks interactive is inert.
- `touch-action: manipulation` on controls to remove double-tap delay.
- Every drag has a single-pointer alternative (WCAG 2.5.7), as does every swipe, pinch or other path or multipoint gesture (2.5.1). Each action also works from the keyboard (2.1.1).
- `overscroll-behavior: contain` on modals and drawers.

## Performance

Speed is an aesthetic property.

- **Response limits**: 0.1 s feels instant; 1 s keeps the flow of thought; 10 s is the limit of attention. Productivity drops past about 400 ms (the Doherty threshold).
- **Core Web Vitals** at the 75th percentile: LCP at most 2.5 s, INP at most 200 ms, CLS at most 0.1. A page passes only if all three pass. Aim for a visible response within 100 ms and treat 200 ms as the ceiling.
- **Measure in the lab** with Lighthouse's mobile profile and `scripts/check_budgets.py` (SKILL.md, step 5). A page-load report has no INP because nothing is clicked; total blocking time at most 200 ms stands in for it.
- **Script weight**: about 365 KiB of compressed JavaScript keeps a script-heavy page interactive within 3 s on a 75th-percentile phone and network; a page built from markup should stay near 75 KiB. The brief sets the page's figure and the spectacle layer's share of it.
- **Keep the LCP element visible.** Chromium does not count an element at opacity 0 as a contentful paint, so a headline held invisible by an entrance animation delays LCP until it appears. Animate the headline from a visible state, or let a different element be the largest.
- **Layout shift**: set dimensions or `aspect-ratio` on all media, reserve space for anything that loads late, match fallback font metrics, animate with transforms.
- **Spectacle budget**: one Spline or WebGL hero can add 0.8 to 2 MB of JavaScript and heavy `backdrop-filter` can cost 15 to 30% of frame rate on mid-range Android (agency-reported figures). Lazy-initialise heavy layers after first paint, pause them off-screen, and serve a static image to constrained devices and reduced-motion users.
- Preload only above-the-fold images and critical fonts; lazy-load the rest; prefer looping `<video>` to GIFs; use `content-visibility: auto` for long pages.
- **Speculation Rules** can prefetch likely next pages and prerender on hover; combined with cross-document View Transitions, multi-page sites feel instant.

## Accessibility

Part of quality, not a separate pass.

- Semantic HTML before ARIA: `<button>` for actions, `<a>` for navigation, landmarks, headings in order, a skip link.
- Every focusable element shows a visible `:focus-visible` ring (2 px or more, 3:1 contrast against its surroundings). Never remove outlines without a replacement. Sticky headers and overlays must not hide the focused element (WCAG 2.4.11).

  ```css
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  ```

- Every flow works with the keyboard alone; dialogs trap and restore focus.
- Icon-only buttons have accessible names; decorative images have empty `alt`; meaningful ones have real `alt`.
- Colour never carries meaning alone.
- Toasts and inline validation announce through a polite `aria-live` region.
- Contrast as in `visual-system.md`.

## Critique checklist

Run this on the built page, not on the plan.

**Look**
- [ ] Viewed at 375 px and 1440 px (and in dark mode if it exists); nothing overflows horizontally.
- [ ] One signature moment, rich enough to reward a long look; everything else quieter than the content.
- [ ] No content needs a script to become visible: hidden starting states for reveals are applied by script, not by the stylesheet.
- [ ] Every colour, font, radius, shadow and spacing value comes from a token.
- [ ] Headings balanced, paragraphs at a readable measure, numbers tabular where compared; no figure, date or duration split across lines; condensed display type with clear word spaces.
- [ ] The tell check in `slop-tells.md` passes, or each remaining tell has a stated reason.
- [ ] Beside a screenshot of the reference site, the largest gap in craft is named and closed or explained.

**Use**
- [ ] Top-level navigation visible on desktop and on one row at 375 px; real links; state in the URL where relevant.
- [ ] Hover, active, focus-visible, disabled, loading, empty and error states exist and look designed.
- [ ] Each action keeps one name from its button to its confirmation.
- [ ] No success, confirmation or error message is visible before the action that produces it.
- [ ] Every date, place, price, count, version, command and rule on the page was supplied; the rest are written around, or shown as placeholders that stay off the first screen, the primary action and the closing section, and listed in the report.
- [ ] Forms: labels, types, autocomplete, 16 px inputs, errors beside fields, paste allowed.
- [ ] Targets at least 24 px, 44 px on touch.

**Motion**
- [ ] The page moves like its tier: no scroll choreography on the product tier; product-tier rules everywhere outside the brand tier's scene.
- [ ] The signature movement is one the subject makes, not a fade applied to every block.
- [ ] The first screen is complete and readable in its first frame and at rest by 1.5 s, with nothing faded in from opacity 0; a looping piece opens on a finished frame and makes its first change within about 1 s.
- [ ] The signature moment has one lead, overlapping followers and a last frame that looks finished on its own.
- [ ] Elements that change place between states travel there instead of cutting.
- [ ] Scroll-linked and pointer motion sit behind `@supports` and `prefers-reduced-motion: no-preference`, and the page reads correctly without them.
- [ ] No `transition: all`, no `scale(0)`, no layout-property animation.
- [ ] Frequent and keyboard actions are instant.
- [ ] `prefers-reduced-motion` handled; flourishes fall back to opacity.

**Performance and access**
- [ ] `scripts/check_budgets.py` passes on a Lighthouse mobile report, or every unmeasured figure is named in the report.
- [ ] The spectacle layer starts after first paint, pauses off-screen, has a static fallback and fits its share of the script budget.
- [ ] The LCP element is visible from first paint, not held at opacity 0 by an entrance animation.
- [ ] Every control shows a pressed state on `:active`, so input gets a visible response within 100 ms even when the work behind it takes longer.
- [ ] Loading indicators wait 150 to 300 ms before appearing and stay at least 300 to 500 ms once shown.
- [ ] Media has dimensions; fonts are WOFF2 with explicit `font-display`; heavy effects lazy and optional.
- [ ] Keyboard-only walk-through completes every flow; focus is always visible.
- [ ] Contrast passes WCAG AA; body text comfortably, not barely.
