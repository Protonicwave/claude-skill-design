# Visual system

How to turn the brief into tokens. Every section gives the rule, the reason and CSS to start from. Values marked "starting point" are tuned defaults, not sourced constants: check them in the browser.

## Colour

### Work in OKLCH

OKLCH is perceptually uniform: the same lightness value reads as equally light across hues, so colour arithmetic gives predictable results. Linear relied on the same property, working in the related LCH space, to cut each theme from 98 hand-set variables to three inputs (base, accent, contrast) and generate every surface from them.

```css
:root {
  --accent: oklch(0.62 0.14 85);
  --accent-hover: oklch(from var(--accent) calc(l + 0.06) c h);
  --accent-press: oklch(from var(--accent) calc(l - 0.06) c h);
  /* Same lightness and chroma, different hue: keeps contrast parity with the accent. */
  --danger: oklch(from var(--accent) l c 25);
  --success: oklch(from var(--accent) l c 150);
}

@media (color-gamut: p3) {
  :root { --accent: oklch(0.62 0.17 85); } /* richer on wide-gamut screens */
}
```

### Palette shape

- **Mostly neutral.** Almost all of an interface is grey. Tint the neutrals toward the subject (warm for paper, food, craft; cool for engineering, finance, medical) with chroma around 0.005 to 0.02. Pure `#000` and `#fff` neutrals read as unconsidered, and so do the habitual stand-ins: cream near `#F4F1EA` and near-black `#111` are defaults of their own (see the clusters in `slop-tells.md`). Sample the tint from a real material in the subject's world rather than from "warm" or "dark".
- **One accent** that carries meaning: primary action, selection, focus, the brand moment. If everything is accented, nothing is.
- **Semantic colours** (danger, warning, success, info) derived from the same lightness and chroma, used only for their meaning, always paired with a non-colour cue (icon, text, position).
- **Colour from the subject.** Take the accent and neutral tint from something true: the product's material, its place, its era, its existing brand. Never from "what looks modern".

### Assign colours by role (12-step model)

Radix gives every step a job. Use the same roles for the neutral and each accent scale.

| Step | Role |
|---|---|
| 1 | App background |
| 2 | Subtle background (cards, sidebars, striped rows) |
| 3, 4, 5 | Component background: rest, hover, pressed or selected |
| 6 | Subtle borders and separators on non-interactive elements |
| 7, 8 | Borders of interactive elements, focus rings |
| 9 | Solid fill: the accent itself, primary buttons |
| 10 | Hover on solid fill |
| 11 | Low-contrast text (secondary copy, labels) |
| 12 | High-contrast text (headings, body) |

Starting point for a light neutral ladder (replace hue `h` with the subject's tint, and raise the chroma column for a stronger tint):

```css
:root {
  --n-1:  oklch(0.990 0.004 h);
  --n-2:  oklch(0.975 0.006 h);
  --n-3:  oklch(0.950 0.008 h);
  --n-4:  oklch(0.930 0.009 h);
  --n-5:  oklch(0.905 0.010 h);
  --n-6:  oklch(0.870 0.011 h);
  --n-7:  oklch(0.820 0.012 h);
  --n-8:  oklch(0.740 0.013 h);
  --n-9:  oklch(0.560 0.014 h);
  --n-10: oklch(0.510 0.014 h);
  --n-11: oklch(0.440 0.012 h);
  --n-12: oklch(0.220 0.010 h);
}
```

### Contrast

- WCAG 2.2 AA is the floor and the legal standard: 4.5:1 for body text, 3:1 for large text (about 24 px, or 18.5 px bold) and for UI components and icons.
- APCA is the better design tool, especially on dark themes: Lc 90 preferred for body text, Lc 75 minimum for body columns, Lc 60 for other content text, Lc 45 for headlines and large text, Lc 30 for placeholder and disabled text, Lc 15 the point of invisibility.
- Thin weights cost contrast. At Lc 75, 16 px body needs weight 500 and 14 px needs 700. A light display weight is a contrast decision as well as a style.
- Mid-grey body text on a dark background that "barely passes" is a known generic tell. Pass comfortably.

### Dark mode

A separate palette, not an inversion.

- Base surface dark grey, not black: Material recommends `#121212` (about `oklch(0.18 0 0)`), tinted to match the neutral.
- Elevation is expressed by lighter surfaces, not by shadows (which do not read on dark).
- Desaturate the accent and lift its lightness so it passes contrast at every surface level.
- Set `color-scheme: dark` on `<html>` so form controls and scrollbars match, and set `<meta name="theme-color">` to the page background.

### Gradients and texture

- RGB interpolation between saturated colours passes through a grey "dead zone". Interpolate in OKLCH:

  ```css
  background: linear-gradient(to bottom right in oklch, oklch(0.80 0.11 95), oklch(0.62 0.14 85));
  ```

- Use adjacent hues. Two distant hues (purple to blue, coral to violet to cyan) are the generic look.
- At most one deliberate gradient per page, and only where it models something: light, a material, a horizon, the product's own visual.
- A fine noise layer removes banding and adds tactility far more cheaply than WebGL. Use it where it models a material (paper, print, film, a cast surface); noise or a dot grid laid over a whole dark page is a default.

  ```css
  .grain { position: relative; isolation: isolate; }
  .grain::after {
    content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none; opacity: 0.07;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  }
  ```

## Typography

### Choosing a typeface

Typography is the fastest signal of quality and of genericness. Choose by the subject's voice, not by popularity. This file names no recommended faces on purpose: a named list becomes the default for anything that reads it, and two pages built from an earlier list both took the same grotesk from it.

1. **Name the voice**: editorial, technical, institutional, warm, playful, luxurious, industrial, archival, civic.
2. **Look in the subject's world first.** What are its own artefacts set in: the legends on the hardware, the signage of the place, the manuals, packaging, timetables, labels or periodicals of its trade and era? Name the quality to carry over, such as narrow and engineered, high stroke contrast, rounded terminals or a stencil cut.
3. **Search a catalogue by that quality, not by popularity.** Filter Google Fonts by classification and properties, or browse Fontshare and foundries' free families. Skip the first screen of a popularity sort: popularity is what makes a face a default. Without catalogue access, work from memory but by the named quality, and say so in the report.
4. **Shortlist three and set the real headline and a real paragraph in each.** Choose by looking at them, not by name.
5. **Reject** any face listed in `slop-tells.md` without a stated reason, any face the project's earlier builds used, and any face you would pick for every page in the category. Linear uses Inter inside a fully computed system; that is a decision, not a default.
6. **One family, used decisively.** A second only when it has a distinct job: display against text, or mono for code, identifiers and figures read character by character. Mono for every label and spec is template chrome.
7. **Write the reason in the brief**: what the face shares with the subject.

A variable family with width or optical-size axes can carry both display and text roles, which gives range without a second family.

### Setting text

- Body 16 to 20 px. Line height 1.4 to 1.6 for body (120 to 145% in print terms); headings 1.0 to 1.2. Line height falls as size rises.
- Measure 45 to 90 characters; aim for about 65. Use `max-width: 65ch` on prose.
- Tracking tightens with size. Inter's published curve gives about -0.011em at 16 px and about -0.022em from 32 px up; most grotesks behave similarly. Never add negative tracking to small text.
- All caps only for short labels, with 0.05em to 0.12em letter-spacing. Bold and italic never together.
- `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs. Browsers without support set ordinary wrapping, so both are safe to add.
- `font-variant-numeric: tabular-nums` wherever numbers are compared (tables, prices, counters, timers).
- Curly quotes, a real ellipsis character, and non-breaking spaces between numbers and units.
- Hierarchy from size and weight steps first, colour second. Big jumps read as confident: a hero at 3x the body size or more is normal on marketing pages.

### Fluid type scale

One scale for a 360 px screen (18 px base, ratio 1.2) and one for 1240 px (20 px base, ratio 1.25), interpolated with `clamp()`. These are the Utopia values:

```css
:root {
  --step--2: clamp(0.7813rem, 0.7736rem + 0.0341vw, 0.8rem);
  --step--1: clamp(0.9375rem, 0.9119rem + 0.1136vw, 1rem);
  --step-0:  clamp(1.125rem, 1.074rem + 0.2273vw, 1.25rem);
  --step-1:  clamp(1.35rem, 1.263rem + 0.3864vw, 1.5625rem);
  --step-2:  clamp(1.62rem, 1.484rem + 0.6057vw, 1.9531rem);
  --step-3:  clamp(1.944rem, 1.741rem + 0.9044vw, 2.4414rem);
  --step-4:  clamp(2.3328rem, 2.039rem + 1.307vw, 3.0518rem);
  --step-5:  clamp(2.7994rem, 2.384rem + 1.846vw, 3.8147rem);
  --step-6:  clamp(3.3592rem, 2.783rem + 2.562vw, 4.7684rem);
}
```

For a more dramatic editorial or brand page, raise the large-screen ratio to 1.333 or 1.414. For a dense product UI, use fixed sizes (12, 13, 14, 16, 20, 24) and let density come from spacing.

### Loading fonts

- WOFF2 only, subset to the scripts you need, self-hosted or preconnected with `crossorigin`.
- Preload only the one or two files used above the fold.
- Set `font-display` explicitly: `swap` for brand display text, `optional` or `fallback` for body.
- Add `size-adjust` (and `ascent-override`) to the fallback `@font-face` so the swap does not shift layout.

## Layout and space

- **Spacing scale** on a 4 px base: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128. Use only these.
- **Proximity carries grouping.** The gap between groups is at least double the gap within a group. Vercel's guide uses spacing tokens 2 to 4 within a group, 6 to 8 between groups, 8 to 12 at section turns, and reserves 16 for a true chapter break.
- **Section spacing** on marketing pages: 64 px or more on desktop, often 96 to 160 px. Generous space is the cheapest visible difference between amateur and polished.
- **Grid**: 12 columns on desktop, 6 on tablet, 4 on mobile is a sound default. Editorial pages can use an asymmetric grid (for example a narrow label column and a wide content column) to escape the centred stack.
- **Composition follows content.** If there are two important things, show two; if there are five of unequal weight, give them unequal sizes. Three equal cards is a template, not a layout. Bento grids work when cell sizes reflect importance and each cell shows something real, not an icon and two lines.
- **Alignment**: one strong left edge beats centred everything. Centre only short, symmetrical content (a single statement, a closing call to action).
- **Density** matches the job: generous for persuasion and reading, compact for tools used all day. Linear keeps density by dimming chrome rather than shrinking content.
- **Containers**: prose at about 65ch, page content at 1100 to 1280 px, full-bleed for the signature moment only.
- Use container queries for components that appear in different widths.

## Depth and surface

Order of preference: tone, then hairline, then shadow, then blur.

- **Tone steps.** In dark mode, raise elevation by lightening the surface one step. In light mode, set a step-2 card on the step-1 page and separate them with a step-6 hairline. Linear's whole elevation system is lightness steps from one generator.
- **Hairlines.** A 1 px border at neutral step 6, or a semi-transparent border (`oklch(0 0 0 / 0.08)`) that adapts to any surface. Linear's rule: "structure should be felt, not seen", so soften borders and remove separators that are not needed. A rule between every section is the broadsheet default: space and a change of content already mark a new section.
- **Shadows** follow physics: one light source for the whole page, several layers that double in offset and blur, low opacity, tinted with the background hue rather than black.

  ```css
  :root {
    --shadow-tint: 0.30 0.02 h; /* lightness, chroma, hue of the surface */
    --shadow-md:
      0 1px 1px oklch(var(--shadow-tint) / 0.06),
      0 2px 2px oklch(var(--shadow-tint) / 0.06),
      0 4px 4px oklch(var(--shadow-tint) / 0.06),
      0 8px 8px oklch(var(--shadow-tint) / 0.06),
      0 16px 16px oklch(var(--shadow-tint) / 0.06);
  }
  ```

  Combine a shadow with a hairline border for crisp edges. Coloured glow shadows (`0 0 40px` of the accent) are a tell.
- **Glass** only where content genuinely scrolls beneath (a sticky header over imagery). A plain `backdrop-filter` samples only what is directly behind and looks flat; extend the blurred layer to about twice the element's height and mask it, add a translucent tint, and provide an opaque fallback in `@supports not (backdrop-filter: blur(1px))`. Heavy blur costs frame rate on mid-range phones, so keep it small and few.
- **Skeuomorphic depth** is justified when it models a real object, as Raycast's keycaps model a keyboard. Depth that models nothing is ornament.
- **Light** is a material, separate from the surface order above. The hero of a premium page is usually lit: a spotlight on a product, a pool of light under a product screen. Light from one named source that falls on something real is allowed and often the difference between plain and premium; a coloured glow behind nothing is still a tell. Rules and CSS are in `artefacts.md`.

## Radii

- Choose two or three values (for example 6 px for controls, 12 px for cards, full for pills and avatars) and use only those. Sharper radii read as precise and editorial; larger radii read as soft and friendly. Pick by voice, not habit: `rounded-2xl` on everything is a default.
- Nested corners are concentric: inner radius = outer radius minus padding (`max(0px, calc(var(--r-outer) - var(--pad)))`). A 24 px card with 8 px padding holds a 16 px child.

## Icons

- One family, one grid (24 px), one stroke width (commonly 1.5 or 2 px), round or square caps chosen once. Lucide, Phosphor, Tabler and Heroicons are each consistent within themselves; never mix them.
- Icons add meaning or speed recognition. An icon that repeats its label, or a decorative icon tile on every card, is noise.
- Never use emoji as interface icons.
- Icon-only buttons need an accessible name.

## Imagery and art direction

- Decide the image strategy in the brief: real product UI, photography, illustration, 3D, data, or type alone. Mixing strategies without a rule looks assembled.
- Real beats generic. A real screenshot, a real number or a real customer is proof; a stock photo of people pointing at a laptop is filler. For product sites, the product is usually the best image.
- Give photography one treatment (colour grade, crop ratio, duotone, grain) so a set reads as one voice.
- Illustration needs one hand: consistent line weight, palette and perspective. Notion's doodles and Stripe's illustration are owned, not sourced.
- 3D and WebGL earn their cost only when the brand is the experience (award-style brand sites, product reveals). Otherwise a still render or a short looping video is lighter and as effective.
- Always set width and height (or `aspect-ratio`) on media, lazy-load below the fold, and serve modern formats (AVIF, WebP).
