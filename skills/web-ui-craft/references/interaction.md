# Interaction, motion and quality

What makes an interface feel good is mostly a dense set of small, checkable rules. This file holds them, ending with the critique checklist.

## Navigation

- **Keep it visible.** In Nielsen Norman Group's study of 179 people, hidden (hamburger) navigation on desktop was used in 27% of cases against 48% for visible links, cut content discoverability by more than 20%, and made tasks at least 39% slower. Show top-level links on desktop. On mobile, show up to four links visibly and put only the overflow in a menu.
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
  --dur-4: 500ms;  /* drawer or sheet only */
}
```

### Rules

- Keep UI animation under 300 ms. A 180 ms select feels more responsive than a 400 ms one.
- Use ease-out for things entering and leaving. Built-in `ease-out` is weak; use a stronger curve. Avoid `ease-in` for UI: it starts slowly and feels laggy. Avoid bounce and elastic easing in product UI.
- Animate only `transform` and `opacity`. Width, height, top, left, margin and padding trigger layout and paint and cause jank and layout shift.
- Never `transition: all`. List the properties.
- Never animate from `scale(0)`. Start from 0.9 to 0.97 with opacity 0.
- Popovers, menus and tooltips grow from their trigger: use the component library's transform-origin variable (`var(--radix-dropdown-menu-content-transform-origin)`, `var(--transform-origin)`) or set the origin yourself.
- Press feedback: `transform: scale(0.97)` on `:active`.
- In a group of tooltips, delay the first; once one is open, neighbours open instantly with no animation.
- Animations must be interruptible. Prefer CSS transitions (which retarget mid-flight) over keyframes for interactive state.
- Spatial consistency: things should come from where they were summoned and return there. Family's "we fly instead of teleport".
- Gestures apply their movement directly (the sheet follows the finger) rather than playing a canned animation after a threshold. Destructive gesture actions commit on release, not mid-gesture.
- One orchestrated page-load sequence (staggered by 40 to 80 ms) beats scattered effects on every element.
- Scroll-triggered reveals on every section are a template habit. Use them only where they pace a story.
- Content is visible before any script runs. A section hidden until an observer reveals it stays blank on slow devices, in print, to crawlers and in full-page screenshots. Reveal by enhancing visible content (add the hidden starting state from script, then animate), never by hiding it in the stylesheet.
- View Transitions (`document.startViewTransition`, or `@view-transition { navigation: auto; }` for multi-page sites) give shared-element continuity without a single-page framework. Feature-detect and respect reduced motion.

### Reduced motion

Colour and opacity changes do not count as motion under WCAG 2.3.3; translation, scaling and parallax do. Keep the flourish and remove the movement:

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
- **Errors** say what happened and how to fix it, next to the cause.
- **Copy** is specific: "Save API key", not "Continue". Sentence case, active voice, from the user's side. An ellipsis character for in-progress states ("Saving…") and for menu items that open a follow-up.
- **Endings matter** (Peak-End Rule): completion, confirmation and success states deserve as much care as the hero.

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
- Every drag, swipe or pinch has a click and keyboard alternative (WCAG 2.5.7).
- `overscroll-behavior: contain` on modals and drawers.

## Performance

Speed is an aesthetic property.

- **Response limits**: 0.1 s feels instant; 1 s keeps the flow of thought; 10 s is the limit of attention. Productivity drops past about 400 ms (the Doherty threshold).
- **Core Web Vitals** at the 75th percentile: LCP at most 2.5 s, INP at most 200 ms, CLS at most 0.1. A page passes only if all three pass. Aim for a visible response within 100 ms and treat 200 ms as the floor.
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
- [ ] Every section is visible in a full-page screenshot taken without scrolling.
- [ ] Every colour, font, radius, shadow and spacing value comes from a token.
- [ ] Headings balanced, paragraphs at a readable measure, numbers tabular where compared.
- [ ] The tell check in `slop-tells.md` passes, or each remaining tell has a stated reason.

**Use**
- [ ] Top-level navigation visible on desktop; real links; state in the URL where relevant.
- [ ] Hover, active, focus-visible, disabled, loading, empty and error states exist and look designed.
- [ ] Forms: labels, types, autocomplete, 16 px inputs, errors beside fields, paste allowed.
- [ ] Targets at least 24 px, 44 px on touch.

**Motion**
- [ ] No `transition: all`, no `scale(0)`, no layout-property animation.
- [ ] Frequent and keyboard actions are instant.
- [ ] `prefers-reduced-motion` handled; flourishes fall back to opacity.

**Performance and access**
- [ ] Media has dimensions; fonts are WOFF2 with explicit `font-display`; heavy effects lazy and optional.
- [ ] Keyboard-only walk-through completes every flow; focus is always visible.
- [ ] Contrast passes WCAG AA; body text comfortably, not barely.
