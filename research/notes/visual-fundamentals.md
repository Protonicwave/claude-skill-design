# Visual design fundamentals for web UI: implementable rules

Scope: typography, colour, layout and spacing, depth and detail, imagery and iconography, and what the authoritative sources recommend. Every cited line names its source. Lines marked "derived" are my own arithmetic applied to a cited formula. Research date: November 2026.

Source quality note: Butterick, Evil Martians, Josh W. Comeau, Radix, Utopia, MDN, Chrome for Developers, Tailwind, Lucide and the APCA documentation were fetched directly and are primary. Refactoring UI could not be fetched (Medium returned 403, the book is paid), so Refactoring UI points come from third-party summaries and are flagged as secondary. Apple HIG and Material 3 pages render client-side and returned no body text, so their specific numbers are listed under Gaps rather than asserted.

## Typography: choosing and pairing typefaces, scale, measure, leading, tracking, weights, wrapping

### Takeaway
Body text 16 to 20px, line-height roughly 1.4 to 1.5 for body falling towards 1.0 to 1.2 for display, measure 45 to 90 characters (aim for about 65), tracking tightened as size grows (about -0.02em at display sizes for Inter-style grotesques) and loosened 5 to 12% for all caps. Use a constrained modular scale (ratio around 1.2 on mobile rising to 1.25 to 1.333 on desktop, interpolated with clamp()), `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs. The default neo-grotesque (Inter, Roboto, SF, Helvetica) is now widely regarded as a fatigue signal rather than a mistake.

### Cited Findings

Core body text rules (Butterick)
- The four most important considerations for body text are point size, line spacing, line length and font. [Butterick, Practical Typography: summary of key rules](https://practicaltypography.com/summary-of-key-rules.html)
- Body point size: 15 to 25 pixels on the web (10 to 12pt in print). [Butterick](https://practicaltypography.com/summary-of-key-rules.html)
- Line spacing: 120 to 145% of the point size. [Butterick](https://practicaltypography.com/summary-of-key-rules.html)
- Line length: an average of 45 to 90 characters per line, including spaces. [Butterick](https://practicaltypography.com/summary-of-key-rules.html)
- Font choice is "the easiest and most visible improvement"; avoid goofy fonts, monospaced fonts for body, most free fonts, and system fonts, especially Times New Roman and Arial. [Butterick](https://practicaltypography.com/summary-of-key-rules.html)
- Use bold or italic as little as possible, and never together. Never underline except possibly for links. All caps are fine for less than one line. Use centred text sparingly. [Butterick](https://practicaltypography.com/summary-of-key-rules.html)
- Add 5 to 12% extra letterspacing to all caps and small caps; if you lack real small caps do not fake them; kerning should always be on. [Butterick](https://practicaltypography.com/summary-of-key-rules.html)
- Paragraph separation: either a first-line indent of 1 to 4 times the point size, or 4 to 10pt of space between paragraphs. Never both. Always hyphenate justified text. [Butterick](https://practicaltypography.com/summary-of-key-rules.html)
- Use curly quotes, real ellipsis, proper dashes, real trademark and copyright symbols; one space between sentences. [Butterick](https://practicaltypography.com/summary-of-key-rules.html)

Type scale and line-height (Tailwind defaults as a de facto industry baseline)
- Tailwind's default scale in rem / px: xs 0.75/12, sm 0.875/14, base 1/16, lg 1.125/18, xl 1.25/20, 2xl 1.5/24, 3xl 1.875/30, 4xl 2.25/36, 5xl 3/48, 6xl 3.75/60, 7xl 4.5/72, 8xl 6/96, 9xl 8/128. [Tailwind CSS: font-size](https://tailwindcss.com/docs/font-size)
- Paired default line-heights fall as size rises: 12px uses 1rem (about 1.33), 16px uses 1.5, 20px uses 1.4, 24px about 1.33, 30px 1.2, 36px about 1.11, and 48px and above use 1. [Tailwind CSS: font-size](https://tailwindcss.com/docs/font-size)

Fluid modular scales (Utopia)
- Utopia's method: define a type scale for a small screen, define one for a large screen, and let the browser interpolate between them based on viewport width. [Utopia: designing with fluid type scales](https://utopia.fyi/blog/designing-with-fluid-type-scales)
- Utopia's own linked configuration uses 18px base at a 1.2 ratio at a 360px viewport, rising to 20px base at a 1.25 ratio at 1240px; the article's example uses 1.2 at 320px and 1.333 at 1500px. The article says the right ratio depends on fonts, visual style, content, layout and audience rather than prescribing one. [Utopia](https://utopia.fyi/blog/designing-with-fluid-type-scales)
- Derived: interpolating 18px at 360px to 20px at 1240px gives `--step-0: clamp(1.125rem, 1.0739rem + 0.2273vw, 1.25rem);` (computed from the Utopia parameters above). [Utopia](https://utopia.fyi/blog/designing-with-fluid-type-scales)

Tracking that tightens with size (Inter dynamic metrics)
- Rasmus Andersson's dynamic metrics formula for Inter: tracking (em) = a + b × e^(c × z), with a = -0.0223, b = 0.185, c = -0.1745, z = font size in px. [Inter dynamic metrics (archived)](https://d.rsms.me/inter-website/v3/dynmetrics/)
- Derived values from that formula: 12px about +0.0005em, 15px about -0.009em, 16px about -0.011em, 24px about -0.020em, 32px about -0.022em, 48px and above converge on about -0.022em. In practice: no tracking at body sizes, about -0.01em at 16px, about -0.02em for headings 24px and up. These numbers are tuned for Inter; other faces need their own values. [Inter dynamic metrics (archived)](https://d.rsms.me/inter-website/v3/dynmetrics/)

Line wrapping (modern CSS)
- `text-wrap: balance` balances the number of characters per line; `text-wrap: pretty` uses a slower algorithm favouring better layout, such as fewer orphans. [MDN: text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap)
- For performance, balance only applies to short blocks: six lines or fewer in Chromium, ten lines or fewer in Firefox. [MDN: text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap)
- `text-wrap` is Baseline "widely available" since March 2024, with varying support for some values. [MDN: text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap)
- Chrome's guidance: use `balance` for headlines and `pretty` for paragraphs. `pretty` focuses on avoiding single-word orphans at paragraph ends and shipped in Chrome 117. [Chrome for Developers: text-wrap pretty](https://developer.chrome.com/blog/css-text-wrap-pretty)

Minimum sizes and weights tied to contrast (APCA)
- APCA ties readable size and weight to contrast. At Lc 75 (minimum for body columns), body text needs 24px/300, 18px/400, 16px/500 or 14px/700. At Lc 90 (preferred for body), 18px/300 or 14px/400 is enough. At Lc 60, 24px/400 or 16px/700 for non-body content text. Thin fonts need far larger sizes (for example 24px/200 at Lc 90). [APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)
- Those sizes assume an x-height ratio of 0.52 (Helvetica/Arial reference); faces with smaller x-heights need larger sizes. [APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)

Typeface choice: favoured and overused (opinion sources, lower authority)
- Inter, Helvetica Neue, SF Pro and Roboto are named as overused: "the same handful of sans-serifs appeared on essentially every digital product". The complaint is homogeneity, not quality. [Font Alternatives: neo-grotesk fatigue 2026](https://fontalternatives.com/blog/neo-grotesk-fatigue-2026/)
- Suggested alternatives from that source: free geometric sans (Space Grotesk, Jost, Plus Jakarta Sans), free text serifs (EB Garamond, Source Serif), free humanist sans (Cabin, Nunito Sans), DIN-adjacent (Barlow, IBM Plex Sans), and DM Sans as the "safest departure from Inter". Premium picks: GT Canon, Edgar, Appeal, WTF Forma, Marblis. No company evidence is given. [Font Alternatives](https://fontalternatives.com/blog/neo-grotesk-fatigue-2026/)
- Other roundups name Söhne as the aspirational upgrade to Inter, Roboto Flex as a variable upgrade to Roboto, neo-humanist sans as a trend, and Atkinson Hyperlegible, Lexend and Inclusive Sans for accessibility-led work; retro serifs (Recoleta, Ivymode) and oversized display type recur in 2025 to 2026 trend pieces. [Creative Bloq: typography trends 2026](https://www.creativebloq.com/design/fonts-typography/breaking-rules-and-bringing-joy-top-typography-trends-for-2026); [Creative Boom: 15 typefaces designers can't stop using in 2026](https://www.creativeboom.com/resources/15-typefaces-designers-cant-stop-using-or-admiring-in-2026/); [Made Good Designs: popular fonts](https://madegooddesigns.com/popular-fonts/)
- Apple's guidance pairs SF Pro Text for small sizes with SF Pro Display for large sizes (optical sizing), and recommends avoiding ultralight, thin and light weights at small sizes. I could not retrieve the live HIG body text, so treat the switch-over point (commonly stated as 20pt) as unverified. [Apple HIG: typography](https://developer.apple.com/design/human-interface-guidelines/typography)

### Inferences
- A defensible default CSS baseline from the above: `body { font-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem); line-height: 1.5; } p { max-width: 65ch; text-wrap: pretty; } h1, h2, h3 { line-height: 1.1; letter-spacing: -0.02em; text-wrap: balance; } .caps { text-transform: uppercase; letter-spacing: 0.08em; }`. Each number sits inside a cited range (Butterick 120 to 145% leading and 45 to 90 characters; Inter tracking curve; Butterick 5 to 12% caps tracking).
- Line-height should be inversely related to size: about 1.5 for 16px body, about 1.2 to 1.3 for 24 to 30px, 1.0 to 1.1 for 48px and up. This is what Tailwind's defaults encode and what Butterick's percentage range implies for body.
- Hierarchy should come from weight and colour as much as size. Using only two or three weights (for example 400, 500 or 600, and 700) with a scale of 5 to 7 sizes reads as refined; many sizes, many weights and fake small caps read as amateur. Butterick's "bold or italic as little as possible" supports the restraint principle.
- Pairing rule of thumb: one family (ideally variable) for UI, optionally a contrasting serif or display face for headings; a monospace only for code and tabular data. Choosing a less ubiquitous grotesque (DM Sans, Geist, Söhne, IBM Plex) or a serif for display is currently the cheapest way to avoid the "default SaaS" look.
- Variable fonts plus `font-optical-sizing: auto` (the CSS default where the font has an `opsz` axis) give Apple-style Text/Display behaviour automatically; Inter 4 and Roboto Flex ship optical size axes. This is from general knowledge, not a fetched source in this session.
- Use `font-variant-numeric: tabular-nums` for tables, prices and timers so digits align. General knowledge, not fetched.

### Gaps
- Refactoring UI's exact typographic advice (for example its hand-picked type scale and its "line-height proportional to line length" point) could not be verified from the primary text.
- Apple HIG and Material 3 type-scale numbers (iOS Body 17pt; M3 Display Large 57/64 etc.) could not be retrieved because the pages render client-side.
- I found no rigorous usage data ranking which typefaces top design studios use; the "favoured versus overused" findings are opinion pieces and listicles.
- Variable font and `font-optical-sizing` support specifics were not fetched.

## Colour: palettes, tinted neutrals, accents, semantics, OKLCH, APCA, dark mode, gradients

### Takeaway
Build every colour as a 10 to 12 step scale in OKLCH, where lightness is perceptually uniform, so hover states, semantic variants and dark mode can be derived by changing L alone. Most of the interface is neutral (tinted grey), with one accent hue and a small set of semantic hues; assign scale steps to jobs (background, component, border, solid, text) as Radix does. Check contrast with APCA (Lc 75 to 90 for body text), make dark mode a dark grey such as #121212 rather than black with desaturated accents, and interpolate gradients `in oklch` to avoid the grey dead zone.

### Cited Findings

OKLCH
- Syntax `oklch(L C H / a)`: L 0 to 1 (perceptual), C from 0 (grey) up to about 0.37 for sRGB and P3, H 0 to 360 (roughly red 20, yellow 90, green 140, blue 220, purple 320). [Evil Martians: OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- HSL lightness varies by hue, so +10% lightness gives different visual results for blue and purple; OKLCH keeps perceived lightness constant across hues, so a red error colour derived from an accent keeps its contrast. [Evil Martians](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- Hover state: `oklch(0.5 0.2 260)` to `oklch(0.6 0.2 260)`. Relative colour: `oklch(from var(--accent) calc(l - 0.1) c h)` for a darker variant (use 0.1, not 10%, inside calc). Hue swap keeping L and C: `oklch(from var(--error) l c 140)`. One `:hover` rule with `calc(l + 0.1)` can serve every button variant. [Evil Martians](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- Example tokens: `--surface-0: oklch(0.96 0.005 300)` (a near-white neutral with a faint purple tint) and `--accent: oklch(0.57 0.18 286)`; switch themes by redefining the custom properties under `prefers-color-scheme: dark`. [Evil Martians](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- Wide gamut: sRGB covers about 35% of visible colours and P3 about 30% more. Write the sRGB value as default and raise chroma inside `@media (color-gamut: p3)`, for example `oklch(0.7 0.2 145)` to `oklch(0.7 0.29 145)`. Browsers clip out-of-gamut colours and the fast clipping in Chrome and Safari can shift hue. [Evil Martians](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- All major browsers support `oklch()` and relative colour syntax. OKLCH alone is not enough to guarantee contrast; the article recommends APCA. [Evil Martians](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)

Scale composition (Radix Colors)
- 12-step functional scale: 1 app background; 2 subtle background; 3 component background; 4 hovered component; 5 active or selected component; 6 subtle borders on non-interactive elements (cards, separators); 7 borders on interactive elements; 8 stronger borders and focus rings; 9 solid backgrounds (highest chroma); 10 hovered solid; 11 low-contrast text; 12 high-contrast text. [Radix Colors: understanding the scale](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)
- Steps 11 and 12 are guaranteed to reach APCA Lc 60 and Lc 90 respectively on step 2 of the same scale. [Radix Colors](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)
- Most step 9 colours are designed for white text; Sky, Mint, Lime, Yellow and Amber are designed for dark text. [Radix Colors](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)
- Light mode may use pure white as the app background with step 1 or 2 used in dark mode, via a mode-dependent alias such as `AppBg`. [Radix Colors](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)

Greys and accents (Refactoring UI, secondary summaries)
- Almost all of a UI is grey (text, backgrounds, panels, borders, form controls), so build a grey palette of about 8 to 10 shades, start from a very dark grey rather than pure black, and tint greys slightly: blue for cool, yellow or orange for warm. [Refactoring UI book summary (sglavoie)](https://sglavoie-github-io.pages.dev/posts/2023/09/09/book-summary-refactoring-ui/); [Refactoring UI notes (mutt0-ds)](https://mutt0-ds.github.io/books/refactoring-ui)

APCA contrast thresholds
- Lc 90 preferred for body text; Lc 75 minimum for body text columns; Lc 60 minimum for other content text; Lc 45 for headlines and large text and fine pictograms; Lc 30 absolute minimum for placeholder, disabled text and large solid icons; Lc 15 minimum for non-text elements such as dividers; anything below Lc 15 should be treated as invisible. [APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)
- Lc 90 is a suggested maximum for very large bold text (over 36px bold) and large colour areas. Add 15 to each level for AAA-equivalent. [APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)
- APCA is perceptually uniform across light and dark, which is why it is positioned for dark mode, where WCAG 2.x ratios can overstate readability. [APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)

Dark mode
- Material (M2) recommends #121212 as the dark surface, a dark grey rather than black, to keep shadows visible and reduce eye strain for light text; elevated surfaces become lighter via a semi-transparent white overlay. [Material Design 2: dark theme](https://m2.material.io/design/color/dark-theme); [Material Android: dark theme](https://material.io/develop/android/theming/dark)
- Material's baseline dark theme uses the 200 tone of the primary colour (desaturated), which passes WCAG AA 4.5:1 for normal text at all elevations. [Material Design 2: dark theme](https://m2.material.io/design/color/dark-theme)
- A secondhand table of the M2 overlay percentages: 1dp 5% (#1e1e1e), 2dp 7% (#222222), 3dp 8% (#242424), 4dp 9% (#272727). Not verified against the official spec. [Stack Overflow mirror](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/36915508/what-are-the-material-design-dark-theme-colors)
- Material 3 replaces overlays with tonal surface roles; third-party summaries describe a primary-tinted surface at low opacity, but I could not verify the official M3 numbers. [Search summary of M3 dark mode, secondary](https://m2.material.io/design/color/dark-theme)

Gradients
- The "grey dead zone" (Erik Kennedy's term): blending two saturated colours such as yellow and blue in RGB averages each channel to about 127, which is grey. [Josh W. Comeau: make beautiful gradients](https://www.joshwcomeau.com/css/make-beautiful-gradients/)
- Fix: `background: linear-gradient(to right, yellow, blue); background: linear-gradient(to right in oklch, yellow, blue);` (fallback first). The OKLCH version passes through green and aqua instead of grey. Alternatives: precompute many intermediate stops in a perceptual space with chroma.js, or add more stops; HSL interpolation avoids grey but can look over-vivid. [Josh W. Comeau](https://www.joshwcomeau.com/css/make-beautiful-gradients/)
- Grain fixes gradient banding: layer an SVG `feTurbulence` noise tile (with `stitchTiles="stitch"` for seamless repeats) over the gradient, often with `mix-blend-mode: overlay`; generators suggest baseFrequency 0.6 to 1.0 at 0.2 to 0.4 opacity, with lower frequencies (0.3 to 0.5) giving coarser grain. Pure CSS cannot produce the grain without an SVG filter. [CSS-Tricks: grainy gradients](https://css-tricks.com/?p=351302); [Instant Gradient: grainy gradients](https://instantgradient.com/blog/grainy-gradients); [Wild and Free Tools: grainy noise generator](https://wildandfreetools.com/blog/grainy-noise-css-gradient-generator)
- Ana Tudor argues lowering noise opacity weakens the banding fix and proposes using noise as a displacement map instead. [Frontend Masters: grainy gradients](https://frontendmasters.com/blog/grainy-gradients/)

### Inferences
- How many colours: one neutral scale (tinted towards the accent hue with chroma around 0.005 to 0.02), one accent scale, and three or four semantic scales (danger red, warning amber, success green, optionally info blue). Each is a 12-step scale used by role, not by eye. This is the Radix model combined with Refactoring UI's "mostly grey" principle.
- Semantic colours should share the accent's L and C and differ only in H (Evil Martians' hue-swap trick), so they look like one family and keep contrast parity.
- Cheap-looking gradients: RGB interpolation between complementary hues, high-chroma rainbow sweeps, and gradients on text body copy. Good gradients: analogous hues (within about 60 degrees of each other), low chroma differences, interpolated `in oklch` or `in oklab`, often with subtle grain.
- Dark mode is a separate palette, not an inversion: lighter surfaces mean higher elevation, accents drop chroma and rise in lightness, shadows matter less and borders or surface steps carry the separation. Pure white text on pure black is avoided; Radix's step 12 on step 1 or 2 gives Lc 90 by construction.
- Use APCA for design checks but still meet WCAG 2.x 4.5:1 for legal compliance, since WCAG 2.2 remains the referenced standard. General knowledge, not fetched this session.

### Gaps
- Official Material 3 tonal palette mapping (for example primary at tone 40 in light and tone 80 in dark) could not be fetched; only M2 dark theme guidance was verified.
- Vercel Geist's colour system (it uses a 10-step scale with Radix-like roles) was not fetched.
- I found no empirical study on "how many colours" a UI should use; the guidance is practitioner consensus.

## Layout and spacing: spacing scales, grids, whitespace, hierarchy, density, bento and editorial layouts

### Takeaway
Use a constrained spacing scale on a 4px base (4, 8, 12, 16, 24, 32, 48, 64 and so on) and let proximity carry grouping: space inside a group is clearly smaller than space between groups. Constrain content width by measure (about 65ch for prose) rather than stretching to the viewport, interpolate spacing fluidly as Utopia does for type, and create hierarchy by de-emphasising secondary content rather than shouting the primary.

### Cited Findings
- Refactoring UI (via summaries): use a constrained spacing scale rather than arbitrary values; a 4px or 8px base with a sequence such as 4, 8, 12, 16, 24, 32, 48; spacing defines relationships, so closer elements read as more related. [Refactoring UI skill summary (skills.sh)](https://skills.sh/muco-rolle/skills/refactoring-ui); [Refactoring UI book summary (sglavoie)](https://sglavoie-github-io.pages.dev/posts/2023/09/09/book-summary-refactoring-ui/)
- Refactoring UI (via summaries): use borders sparingly, separating content with background colour, spacing or shadow instead. [Refactoring UI notes (mutt0-ds)](https://mutt0-ds.github.io/books/refactoring-ui); [Refactoring UI review (DEV)](https://dev.to/updivision/book-review-refactoring-ui-by-adam-wathan-steve-schoger-2f7m)
- Utopia applies the same small-screen and large-screen interpolation to space and grid as to type (its tool links Type, Space and Grid calculators from one configuration). [Utopia](https://utopia.fyi/blog/designing-with-fluid-type-scales)
- Measure of 45 to 90 characters bounds the width of any text column. [Butterick](https://practicaltypography.com/summary-of-key-rules.html)
- Tailwind's sizes are expressed in rem multiples of a base, and its type scale (12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72, 96, 128px) lands on a 2px or 4px grid throughout. [Tailwind CSS: font-size](https://tailwindcss.com/docs/font-size)

### Inferences
- Concrete spacing tokens: `--space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-5: 24px; --space-6: 32px; --space-7: 48px; --space-8: 64px; --space-9: 96px; --space-10: 128px`. Steps grow geometrically past 16px because perceived difference between 40px and 44px is negligible.
- Proximity rule of thumb: the gap between groups should be at least twice the gap within a group (for example label to input 8px, field to field 24px, section to section 64 to 96px).
- Start with too much whitespace and remove it; generous outer margins and section spacing (64px or more on desktop) is the single largest visual difference between amateur and polished marketing pages. This is the Refactoring UI position as widely summarised, not verified against the book text.
- Hierarchy: de-emphasise secondary text with a lighter grey or smaller size rather than bolding everything; hierarchy should not follow the HTML heading level automatically.
- Density: data-heavy product UI (tables, dashboards) can drop to a 4px rhythm with 13 to 14px text; marketing and editorial pages use 16 to 20px text and an 8px rhythm. Pick one per surface and keep it consistent.
- Bento grids: CSS Grid with a 12 or 6 column track, uniform gap (typically 12 to 24px) and a single radius, with tiles spanning 1 to 4 columns; consistency of gap and radius is what makes them read as one system. Editorial layouts: asymmetric columns (for example 5/7 or 4/8 splits), a strong measure-limited text column and large display type. Container queries (`container-type: inline-size; @container (min-width: ...)`) let tiles adapt to their own width rather than the viewport. These are practitioner conventions; I did not fetch a primary source.

### Gaps
- Every Layout, Material 3 layout (4dp baseline, 8dp grid, window size classes) and Atlassian/Primer spacing tokens were not fetched in this session.
- No primary source was retrieved for bento-grid conventions or editorial grid ratios; the inferences above are unsourced practitioner knowledge.

## Depth and detail: shadows, borders, highlights, grain, glass, radii

### Takeaway
Shadows should come from one consistent light source (vertical offset about twice the horizontal or purely vertical), be built from several layered low-opacity shadows that double in offset and blur, and be tinted with the background hue rather than pure black. Use borders sparingly and subtly (Radix step 6 for non-interactive dividers), keep radii from a small set, and apply the concentric rule: inner radius = outer radius minus the gap. Frosted glass needs an extended backdrop and a translucent tint to look real.

### Cited Findings

Shadows
- One global light source: all shadows share an angle and offset ratio (vertical offset twice the horizontal in Comeau's demo). As elevation rises, offset and blur grow and opacity drops. [Josh W. Comeau: designing beautiful shadows](https://www.joshwcomeau.com/css/designing-shadows/)
- Layer shadows to mimic soft real-world light, for example `0 1px 1px`, `0 2px 2px`, `0 4px 4px`, `0 8px 8px`, `0 16px 16px` each at `hsl(0deg 0% 0% / 0.075)`. Animating layered shadows is costly and discouraged. [Josh W. Comeau](https://www.joshwcomeau.com/css/designing-shadows/)
- Tint shadows with the background hue: on `hsl(220deg 100% 80%)`, transparent black looks washed out and grey; `hsl(220deg 60% 50%)` (same hue, lower saturation and lightness) looks right. Store the shadow colour in a CSS variable (`--shadow-color`) so it can change with the surface. [Josh W. Comeau](https://www.joshwcomeau.com/css/designing-shadows/)
- Elevation system: small `0.5px 1px 1px hsl(var(--shadow-color) / 0.7)`; medium three layers (1/2/2, 2/4/4, 3/6/6) at 0.333; large five layers (1/2/2 doubling to 16/32/32) at 0.2. [Josh W. Comeau](https://www.joshwcomeau.com/css/designing-shadows/)
- `filter: drop-shadow()` follows the shape of transparent images and can be GPU-accelerated; Safari can lag with text inputs. [Josh W. Comeau](https://www.joshwcomeau.com/css/designing-shadows/)
- Refactoring UI (via summaries): define a small fixed set of elevation levels, small shadows for slightly raised elements and large for floating ones, and favour vertical offset. [Refactoring UI skill summary](https://skills.sh/muco-rolle/skills/refactoring-ui); [Refactoring UI book summary](https://sglavoie-github-io.pages.dev/posts/2023/09/09/book-summary-refactoring-ui/)

Borders
- Radix assigns step 6 to subtle borders on non-interactive components (cards, sidebars, separators), step 7 to interactive component borders, and step 8 to stronger borders and focus rings. [Radix Colors](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)
- APCA puts the floor for discernible non-text elements such as dividers at Lc 15, with solid elements at least 5px in their smallest dimension at that level. [APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)

Nested radius
- Inner radius = outer radius minus the gap, where gap = padding + border width; for example 24px outer with 8px padding gives 16px inner. CSS: `border-radius: max(0px, calc(var(--radius) - var(--pad)));`. [30 Seconds of Code: nested border radius](https://30secondsofcode.org/css/s/nested-border-radius); [DEV: the concentric border radius rule](https://dev.to/sgbp/the-concentric-border-radius-rule-why-nested-rounded-corners-look-slightly-wrong-3hog); [CSS-Tricks thread](https://css-tricks.com/?p=15151)
- Caveat: when padding exceeds the outer radius the inner radius goes to 0, which some designers find looks wrong; some tune by eye instead. [DEV: nested CSS borders](https://dev.to/teobourloglou/nested-css-borders-a-hidden-puzzle-3i2c); [UX Planet: corner radius of nested elements](https://uxplanet.org/corner-radius-of-nested-elements-in-ui-design-4c27bb24a854)

Glassmorphism
- Naive `backdrop-filter: blur()` only samples pixels directly behind the element, so it looks flat. Fix: put the blur on a child that is 200% of the header's height, clip it with `mask-image: linear-gradient(to bottom, black 50%, transparent 50%)`, add `pointer-events: none`, and give the parent a translucent tint (about 0.5 to 0.6 alpha). Blur around 16px. [Josh W. Comeau: backdrop-filter](https://www.joshwcomeau.com/css/backdrop-filter/)
- A "glassy edge": a 4 to 6px strip at the bottom with about 8px blur, a slight `brightness()` boost and about 10% white background suggests glass thickness. Wrap glass in `@supports` with a more opaque fallback; support is above 97%. [Josh W. Comeau: backdrop-filter](https://www.joshwcomeau.com/css/backdrop-filter/)

Grain
- See the Colour section: SVG `feTurbulence` noise tiles over gradients, concentrated or masked towards edges, at low opacity. [Instant Gradient](https://instantgradient.com/blog/grainy-gradients); [21st.dev: background patterns](https://21st.dev/blog/react-background-pattern-components)

### Inferences
- A polished card recipe: background one step lighter than the page (or white on a step 1 or 2 page), a 1px border at about Radix step 6 or `oklch(0 0 0 / 0.08)`, a two or three layer tinted shadow, and in dark mode an inset top highlight such as `inset 0 1px 0 oklch(1 0 0 / 0.06)` in place of a strong shadow. The inner highlight technique is common practice (Vercel, Linear, Apple) but I did not fetch a primary source for it.
- Hairline borders: `0.5px` borders render as true hairlines on high-DPI screens in modern browsers; a safer cross-browser technique is `box-shadow: 0 0 0 1px <low-alpha colour>` or a 1px border at low alpha. Not verified this session.
- Radii: choose a small set (for example 4, 8, 12, 16px plus full pill) and derive nested radii with the concentric rule. Mixing unrelated radii is one of the clearest amateur tells.
- Borders versus shadows: on light surfaces use either a subtle border or a subtle shadow for resting cards, not both at full strength; reserve heavier shadows for genuinely floating layers (menus, dialogs, toasts). In dark mode, shadows are weak, so separate with surface lightness and borders.

### Gaps
- Vercel Geist's specific shadow and border tokens, and Material 3's elevation levels, were not fetched.
- No primary source was retrieved for inset highlights or sub-pixel hairline borders.

## Imagery and iconography: photography, illustration, 3D, art direction, icon consistency

### Takeaway
Icon consistency is measurable: one grid (24px), one stroke width (2px for Lucide-style outline sets), one join and cap style, and matched optical weight across the set. For imagery, I found no authoritative numeric guidance in this session; the defensible rule is one art direction per product (one medium, one lighting and colour treatment) rather than mixing photos, flat illustration and 3D.

### Cited Findings
- Lucide icon rules: 24 × 24px canvas; at least 1px padding to the edge; at least 2px between distinct elements; 2px stroke throughout, never mixed; strokes centred; round joins and caps; 2px corner radius for shapes 8px or larger, 1px for smaller shapes; match the visual weight of reference `circle` and `square` icons; centre icons visually; keep detail low; align to the pixel grid; reuse base geometry exactly in variants. [Lucide: icon design guide](https://lucide.dev/guide/design/icon-design-guide)
- APCA: fine-detail pictograms and smaller outline icons need Lc 45; large solid icons can go down to Lc 30 (solid icons at least about 5.5px in their smallest dimension). [APCA in a Nutshell](https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html)

### Inferences
- Never mix icon families (for example Lucide with Heroicons or Material Symbols) in one interface, because stroke width, corner radius and optical size differ; if a needed glyph is missing, draw it to the family's grid rules.
- Icon size should track text: 16px icons with 14px text, 20px with 16 to 18px text, and stroke should be visually similar to the text's stem weight. Practitioner convention, not sourced.
- Imagery: choose one medium per product, apply a consistent grade (colour temperature, contrast, crop ratios such as 16:9 or 4:3 everywhere), and prefer real product screenshots or real photography over generic stock. Abstract 3D renders and gradient blobs have become a common, and increasingly generic, SaaS trope.

### Gaps
- I found no primary or authoritative source (Material, Apple HIG, Atlassian illustration guidelines) on photography versus illustration versus 3D in this session; this whole sub-question is weakly sourced and should be treated as practitioner opinion.
- No data on how imagery choices affect perceived quality or conversion.

## What the authoritative sources recommend (cross-source summary)

### Takeaway
The sources converge: constrain every dimension to a small, systematic scale (type, space, colour steps, radii, shadows), assign each value a role, and derive variants mathematically (OKLCH lightness, modular ratios, concentric radii, doubled shadow layers) rather than picking by eye. Restraint (few weights, mostly grey, one accent, sparing borders) is what separates refined from amateur work.

### Cited Findings
- Butterick: body 15 to 25px, leading 120 to 145%, measure 45 to 90 characters, caps tracked 5 to 12%, bold and italic rarely and never together, avoid system fonts like Arial. [Butterick](https://practicaltypography.com/summary-of-key-rules.html)
- Refactoring UI (secondary summaries): constrained spacing and type scales, 8 to 10 tinted greys, no pure black, fewer borders, a small set of elevation shadows. [sglavoie summary](https://sglavoie-github-io.pages.dev/posts/2023/09/09/book-summary-refactoring-ui/); [mutt0-ds notes](https://mutt0-ds.github.io/books/refactoring-ui)
- Radix Colors: 12-step role-based scales with APCA guarantees (step 11 Lc 60, step 12 Lc 90). [Radix Colors](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)
- Evil Martians: OKLCH for predictable lightness, relative colour syntax for states, P3 enhancement behind a media query, APCA for contrast. [Evil Martians](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- Utopia: fluid type and space scales interpolated between a small-screen and a large-screen modular scale. [Utopia](https://utopia.fyi/blog/designing-with-fluid-type-scales)
- Josh W. Comeau: layered, hue-tinted shadows from one light source; `in oklch` gradient interpolation; extended-backdrop glass. [Shadows](https://www.joshwcomeau.com/css/designing-shadows/); [Gradients](https://www.joshwcomeau.com/css/make-beautiful-gradients/); [Backdrop filter](https://www.joshwcomeau.com/css/backdrop-filter/)
- Material: dark grey (#121212) dark theme, lighter surfaces for elevation, desaturated 200-tone accents. [Material Design 2: dark theme](https://m2.material.io/design/color/dark-theme)
- Tailwind: a 13-step type scale from 12 to 128px with line-height falling from 1.5 to 1. [Tailwind](https://tailwindcss.com/docs/font-size)
- Chrome and MDN: `text-wrap: balance` for headings (six lines max in Chromium, ten in Firefox), `pretty` for paragraphs. [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap); [Chrome for Developers](https://developer.chrome.com/blog/css-text-wrap-pretty)

### Inferences
- A short "refined versus amateur" checklist a developer can apply: body at 16px or more with 1.5 leading and a 65ch measure; headings tightly tracked (-0.01 to -0.03em) with 1.0 to 1.2 leading and balanced wrapping; no more than two families and three weights; greys tinted towards the accent; one accent colour used for primary actions only; contrast checked at Lc 75 or more for body; spacing only from the scale; one radius family with concentric nesting; shadows layered and tinted; gradients in OKLCH with optional grain; one icon set at one stroke width.

### Gaps
- Apple HIG, Material 3, Vercel Geist, Atlassian and Primer pages render client-side or were not fetched within the tool budget, so their specific token values are not verified here. A follow-up should fetch Geist's typography and colour pages and M3's type scale and colour role tables if exact numbers are needed.
- Refactoring UI's primary text was unavailable; all of its points above are via secondary summaries.
