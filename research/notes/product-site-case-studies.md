# Product and brand site case studies: why the acclaimed ones look and feel so good

Scope note: nine cases have usable evidence. Linear, Vercel, Family, Rauno Freiberg and Emil Kowalski have strong primary sources (company or author write-ups). Stripe has a reverse-engineered gradient write-up and secondary summaries of a 2026 redesign interview. Apple has community reconstructions of its scroll technique only. Raycast and Teenage Engineering have only third-party reverse-engineered "design system" files, which disagree with each other, so treat their values as approximate. Arc, Framer, Resend, Paco Coursey, Notion and Figma were not researched for lack of budget (see Gaps).

Dating: Linear's two primary write-ups are March 2024 (redesign) and 12 March 2026 (refresh). Stripe's homepage was replaced in January 2026; the minigl gradient write-up dates from 2021 and describes the older (2020-era) site. Family's essay is 8 July 2024. Rauno's essay is July 2023.

## 1. Visual system per site: type, scale, colour, grid, spacing, imagery, depth

### Takeaway
The best-documented sites build colour from a generator or a small token set rather than a hand-picked palette (Linear: three LCH inputs; Vercel: monochrome tokens with colour reserved for meaning), use one neo-grotesque family plus a monospace companion, and take depth from surface tone rather than ornamental shadow. Exact hex and pixel values are rarely published by the companies themselves; most "specs" in circulation are third-party extractions.

### Cited Findings

Linear (product UI, which its marketing site mirrors)
- 2024 redesign moved theme generation from HSL to LCH. Andreas Eldh: LCH is "perceptually uniform", so lightness 50 reads as equally light across hues, and it produces consistently good-looking themes regardless of base colour. [Linear: How we redesigned the Linear UI](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Each theme previously required 98 hand-set variables; the redesign reduced this to three inputs: base colour, accent colour and contrast. A contrast input (compared at values 30 and 100) enables high-contrast accessible themes. [Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)
- The same LCH generator produces elevation surfaces (background, foreground, panels, dialogs, modals), so depth is expressed as lightness steps, not shadows. [Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)
- The team deliberately limited how much blue "chrome colour" fed into calculations, for "a more neutral, timeless look"; text and neutral icons were made darker in light mode and lighter in dark mode to raise content contrast. [Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Typography: Inter Display for headings ("expression while keeping them readable"), regular Inter for everything else. No sizes published. [Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)
- March 2026 refresh: default light and dark palettes moved from cool blue-ish greys to a warmer, less saturated grey; the team warned that going too warm reads as "muddy" and iterated heavily. [Linear: A calmer interface for a product in motion](https://linear.app/blog/behind-the-latest-design-refresh)
- 2026 refresh also rounded edges, softened border contrast and removed separators under the principle "Structure should be felt, not seen". [Linear](https://linear.app/blog/behind-the-latest-design-refresh)

Vercel (Geist)
- Geist is described as the colours, typography, materials, layout and React components behind Vercel's products. Typefaces are Geist Sans and Geist Mono; Geist Pixel (bitmap-style) was added later and Geist Serif is in progress. [Vercel Geist](https://vercel.com/geist); [Geist font](https://vercel.com/geist/font)
- Vercel's machine-readable brand spec assigns Geist Sans to prose, headings, labels, controls, KPIs and figures, and Geist Mono to code, commands, paths, timestamps and short identifiers (region, plan, environment IDs). Weights loaded: 400 to 600 only. [vercel.com/design.md](https://vercel.com/design.md)
- The same spec defines type roles (display for "one page-defining statement", title, heading-24, heading-20, heading-16, lede, body, label, caption, metadata), prose at 60 to 68 characters per line, tabular numerals for comparisons, sentence-case headings, no all-caps eyebrows, and no arbitrary sizes or numeric weights. [vercel.com/design.md](https://vercel.com/design.md)
- Colour: "monochrome by default; colour only for meaning, always paired with a non-colour cue", WCAG AA. A search summary of the spec lists primary #171717, secondary #4d4d4d, tertiary (blue) #006bff, neutral #f2f2f2. [vercel.com/design.md via search summary](https://vercel.com/design.md) (my own fetch of the page returned token names only, so the hex values are from the search snippet)
- Grid: 12 columns desktop, 6 tablet, 4 mobile; prose spans 6 to 7 columns; tables and charts may span 12. Spacing tokens 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, with within-group gaps 2 to 4, between-group 6 to 8, section turns 8 to 12, and 16 reserved for "a true chapter break". [vercel.com/design.md](https://vercel.com/design.md)
- Depth: "Shadows: none. Ornamental shadows and fake depth are rejected." [vercel.com/design.md](https://vercel.com/design.md)
- A third-party style reference describes vercel.com as #fafafa with a faint 1px "engineer grid" (#f2f2f2 or 4% #171717, 40px module); not confirmed against Vercel's own grid page, which only calls the grid "a core part of the Vercel aesthetic". [Refero style extraction](https://styles.refero.design/style/f24daf3a-d43f-4dec-85a9-8ac1d5148a03); [Vercel Geist](https://vercel.com/geist)
- Third-party sources disagree on tracking: one says body about -0.02em and display down to -0.06em; another reports display at -2.4px to -2.88px. Unverified. [getdesign.md analysis](https://getdesign.md/design-md/vercel/preview.html)

Stripe
- The 2020-era homepage gradient was rendered with a custom minimal WebGL wrapper Stripe called "minigl" plus a Gradient class holding animation settings, reverse-engineered by Kevin Hufnagl. [Bram.us, Oct 2021](https://www.bram.us/2021/10/13/how-to-create-the-stripe-website-gradient-effect)
- Community copies set the four gradient colours through CSS custom properties on the canvas, so the palette changes without touching shader code. [Stripe Mesh Gradient gist](https://gist.github.com/kulshekhar/ea59041d9e9ab0a71b6b5edfc99ca49c)
- January 2026 redesign (led by Head of Design Katie Dill) replaced the 2020 site; it uses a bento grid to present many products, keeps a signature gradient wave that went through years of iteration, and adds a live counter of the share of global GDP running on Stripe. [Crypto Briefing summary of YC podcast](https://cryptobriefing.com/katie-dill-stripes-homepage-redesign-reflects-its-growth-78-of-forbes-ai-50-rely-on-its-products-and-the-importance-of-clarity-in-web-design-y-combinator-startup-podcast/); [Summify key moments](https://summify.io/discover/how-stripe-built-their-new-website-ypzNhw/)
- The team used AI image generation and prototyping to speed exploration, framed as complementing craft and taste. [YouTube transcript summary](https://youtube-transcript.ai/docs/how-stripe-built-their-new-website-xjvghrn4pb)

Raycast (third-party extraction only)
- Near-black, blue-tinted background reported as #07080a; keycap gradients #121212 to #0d0d0d to suggest physical key depth; white borders at roughly 6 to 10% opacity; layered shadows plus inset highlights for raised or pressed glass. [open-design.ai Raycast](https://open-design.ai/systems/raycast/); [hagicode Raycast DESIGN.md](https://design.hagicode.com/designs/raycast/DESIGN.md)
- Conflicts: sources disagree on the mono face (JetBrains Mono vs Geist Mono) and on whether cards use shadows or tone-only elevation. [webdesignhot Raycast](https://www.webdesignhot.com/design.md/raycast/); [hagicode](https://design.hagicode.com/designs/raycast/)

Teenage Engineering (third-party extraction only)
- Rigid modular grid on a 980-unit base width, products in square cells separated by 1px hairlines, generous section padding; square corners make the web surface "feel like hardware" even though the products are rounded. [shadcn.io TE design](https://www.shadcn.io/design/teenage-engineering); [Refero TE](https://styles.refero.design/style/aecf9dda-5cba-4dc7-9e73-59b65d895cdf)
- Monospace type used consistently across site, products, packaging and social as a deliberate identity choice. [Blake Crosley: Teenage Engineering, constraints as aesthetic](https://blakecrosley.com/guides/design/teenage-engineering)

### Inferences
- The strongest documented pattern is "systems over swatches": Linear generates every surface from three LCH inputs, Vercel exposes only role tokens. This is why these sites look coherent at every elevation and in both themes; the colour relationships are computed, not eyeballed.
- Depth in this cohort comes from luminance steps and hairline borders. Raycast is the exception that proves the rule: its depth is tied to a literal object (keycaps), not decoration.
- Constrained weight ranges (Vercel loads 400 to 600 only) and a display cut for headings (Inter Display) give hierarchy through size and tracking rather than heavy weights.

### Gaps
- No primary source found for Stripe's typeface or palette on the 2026 site (Söhne by Klim is widely believed but I found no citation in this session), nor for how the 2026 wave is built.
- Apple's type and colour (SF Pro, black/white product sections) were not sourced in this session.
- No first-party pixel values for Linear's marketing site type scale.

## 2. Motion and micro-interactions, and how they are implemented

### Takeaway
The respected practitioners converge on a narrow motion grammar: short (usually under 300ms), ease-out, transform and opacity only, interruptible, spatially consistent with where things came from, and absent from high-frequency or keyboard-driven actions. Showpiece motion (Stripe's gradient, Apple's scroll sequences) is confined to the hero and is implemented with canvas or WebGL rather than DOM animation.

### Cited Findings
- Emil Kowalski: keep UI animations usually under 300ms; a 500ms enter animation on a frequent action is frustrating; use ease-out for snappy feedback ("starts fast and slows down at the end"); Sonner deliberately uses `ease` and a slightly slower timing for a more elegant feel. [Emil Kowalski: Great animations](https://emilkowal.ski/ui/great-animations)
- Kowalski: animate only `transform` and `opacity` (padding and margin trigger layout and paint); prefer CSS or WAAPI when the main thread is busy because Framer Motion's requestAnimationFrame path can drop frames; animations must be interruptible; respect `prefers-reduced-motion` by falling back to a fade; "never animate keyboard-initiated actions", citing Raycast, used many times a day, as having no animations. [Emil Kowalski](https://emilkowal.ski/ui/great-animations)
- Third-party skill packs derived from Kowalski's teaching cite a stronger ease-out `cubic-bezier(0.23, 1, 0.32, 1)`, `scale(0.97)` on `:active`, and never entering from `scale(0)`; I could not confirm these in his own text. [skills.cat emilkowal-animations](https://skills.cat/skills/mrmps/smry/emilkowal-animations)
- Rauno Freiberg (July 2023): "Interaction design is an artform to make experiences that fluidly respond to human intent"; "Great interactions are modeled after properties from the real world, like interruptibility." [Rauno: Invisible details of interaction design](https://rauno.me/craft/interaction-design)
- Rauno on commit timing: lightweight overlays (search) can trigger mid-gesture so users can peek; destructive actions wait for finger lift; pinch-to-scale should apply the delta immediately rather than after a threshold. [Rauno](https://rauno.me/craft/interaction-design)
- Rauno on frequency: command menus, macOS context menus and the app switcher appear instantly; he removed animations from his own bookmarking tool after they felt sluggish over days of use. [Rauno](https://rauno.me/craft/interaction-design)
- Rauno on spatial consistency: elements should launch from their source (an Island app expands from its icon) so the user understands origin. [Rauno](https://rauno.me/craft/interaction-design)
- Family: "We fly instead of teleport." Trays overlay the current screen and emerge from the element that summoned them (the swap approval tray rises from the swap screen); successive trays vary in height so the transition is legible; tab switches move in the direction of the tapped tab. [Family Values, 8 July 2024](https://benji.org/family-values)
- Family shared elements and text morphing: wallet cards move between screens rather than duplicating; "Continue" morphs into "Confirm" using shared letters; in empty states only the changing words update; a pending spinner travels to the Activity tab. [Family Values](https://benji.org/family-values)
- Family delight scaled to frequency: "Mastering delight is mastering selective emphasis." Confetti only after a wallet backup; sound only on the trash action. [Family Values](https://benji.org/family-values)
- Kowalski recreated the Family drawer and notes its easing must work with combined opacity and height changes. [Emil Kowalski](https://emilkowal.ski/ui/great-animations)
- Stripe gradient: a WebGL canvas (minigl) draws triangles with custom shaders, a Gradient class drives animation. A 2020 forum comment called the original battery-hungry (anecdotal). [Bram.us](https://www.bram.us/2021/10/13/how-to-create-the-stripe-website-gradient-effect); [GSAP forum](https://greensock.com/forums/topic/24837-animating-gradients/)
- Stripe 2026: animation and subtle interactive elements used deliberately "to convey the care and precision" behind the products, with interactive modals inside the bento grid revealing detail progressively. [YouTube transcript summary](https://youtube-transcript.ai/docs/how-stripe-built-their-new-website-xjvghrn4pb)
- Apple scroll-driven reveals (community reconstruction): scroll progress maps to a frame index (`Math.floor(scrollFraction * frameCount)`) and one `drawImage` per frame on a `<canvas>`; the AirPods Pro hero is 147 frames at 1158x770 pulled from Apple's CDN; Apple serves a single fallback image on constrained devices. [CSS-Tricks](https://css-tricks.com/?p=308477); [GitHub Apple-Scroll-Animation](https://github.com/Rachit-Pal/Apple-Scroll-Animation/blob/master/app.js)
- Packing the AirPods WebP frames into one sprite sheet reduced total size from 1.7MB to 1.5MB, and pure-CSS scroll-driven animations can now reproduce the effect. [geyer.dev via HN reader](https://hn.jakechampion.name/reader/https://geyer.dev/blog/css-image-sequence-animations)
- Vercel's brand spec takes the opposite pole: "default to stillness"; motion only to explain a state change, preserve continuity or confirm an action; no bounce, parallax, cinematic transitions, scroll-triggered reveals, marquees, typing cursors or pulsing indicators. [vercel.com/design.md](https://vercel.com/design.md)

### Inferences
- Motion is budgeted by frequency: rare, emotional moments (Family backup, Stripe hero, Apple product reveal) get spectacle; repeated actions get none. This single rule explains both Raycast's lack of animation and Family's confetti.
- Spatial continuity (origin-aware entry, shared elements, directional tabs) is the common mechanism behind the "feels native" reputation of Family, Rauno's work and Linear's app.
- Spectacle is isolated to a GPU-rendered layer (canvas or WebGL) so the rest of the DOM stays cheap and the hero can be swapped for a static fallback.

### Gaps
- No first-party documentation of Linear's marketing-site glow and gradient effects, or of Apple's actual implementation.
- No spring constants or timing values published by Rauno or Family.

## 3. Navigation, information hierarchy and calls to action

### Takeaway
The documented approach is to make the content the brightest thing on the page and dim everything else: Linear dims its sidebar and shrinks chrome, Vercel restricts emphasis and pills, Family reveals features only when relevant, and Stripe's 2026 bento grid uses progressive disclosure to show breadth without a feature dump.

### Cited Findings
- Linear 2026 principle "Don't compete for attention you haven't earned": sidebar made "a few notches dimmer" so the main content takes precedence; desktop tab bar made compact, no longer full width, with rounded corners and smaller icons and text; coloured team icon backgrounds removed and icon usage reduced. [Linear](https://linear.app/blog/behind-the-latest-design-refresh)
- Linear 2026 goal: keep information density "without the interface feeling overwhelming"; header actions (share, copy link, open PR) were moved back to predictable places for consistency. [Linear](https://linear.app/blog/behind-the-latest-design-refresh)
- Linear 2024: labels, icons and buttons in sidebar and tabs aligned on both axes; views tested by type (list, board, timeline, split, fullscreen) rather than one by one; navigation chrome designed to be removable so the app works in browser and Electron; Apple platform standards used to approach a native feel. [Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Vercel spec: establish "the reader's question and strongest supported answer before layout"; emphasis is scarce; rejects pills and badges for ordinary metadata, cards nested in cards, decorative icons or icon tiles; one owner per gap; header has wordmark left, footer at most one line. [vercel.com/design.md](https://vercel.com/design.md)
- Family simplicity principle: show fundamentals up front and reveal other features as they become relevant, rejecting "Everything is right there, all the time, whether you need it or not." [Family Values](https://benji.org/family-values)
- Stripe 2026: the redesign was prompted by Patrick Collison asking what a website is for; Dill frames the site as a company manifesto; the bento grid presents the expanded suite (billing, usage-based pricing for AI firms, tax) as an integrated whole rather than a list. [Crypto Briefing](https://cryptobriefing.com/katie-dill-stripes-homepage-redesign-reflects-its-growth-78-of-forbes-ai-50-rely-on-its-products-and-the-importance-of-clarity-in-web-design-y-combinator-startup-podcast/); [YouTube transcript summary](https://youtube-transcript.ai/docs/how-stripe-built-their-new-website-xjvghrn4pb)
- Rauno on Fitts's Law: screen corners are effectively infinite targets; radial menus keep distance and size equal so muscle memory forms. [Rauno](https://rauno.me/craft/interaction-design)
- Raycast product screenshots sit in macOS-style window chrome, and keyboard shortcuts are shown as keycap chips, foregrounding the product's keyboard-first use. [hagicode Raycast DESIGN.md](https://design.hagicode.com/designs/raycast/DESIGN.md)

### Inferences
- A real product screenshot or live data point (Stripe's GDP counter, Raycast's window chrome) acts as the proof element next to the primary CTA; the hierarchy reads claim, proof, action.
- Dimming chrome is cheaper and more effective than enlarging content: Linear achieves hierarchy by subtracting contrast from secondary areas.

### Gaps
- No primary source describing CTA copy, button styling or top-nav structure on linear.app, vercel.com or stripe.com marketing pages.

## 4. What designers, critics and the companies themselves say

### Takeaway
The companies attribute quality to process (feature-flagged rollouts, side-by-side toggles, tools that tie Figma to code) and to restraint. Critics credit Linear with setting a whole SaaS genre and then fault the imitators, who copy the dark-glow surface without the discipline of hierarchy and contrast underneath.

### Cited Findings
- Karri Saarinen: a redesign should be an "exciting evolution", not a teardown; he produced hundreds of exploratory screens from November 2023; the 2024 project took about six weeks in five milestones (stress tests, behaviour definitions, chrome refresh behind a flag, private beta rolled out daily to more workspaces, GA), with an internal toolbar toggle for old and new UI. Yann-Edern Gillet kept asking how "real" the concept car could be. [Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Linear 2026 (Charlie Aufmann and Maxime Heckel): a colour tool built with Claude Code inside the dev toolbar exposed hue, chroma and lightness per token; team members shared "recipes"; final tokens were exported as JSON into Figma via a plugin by Yann-Edern Gillet so design and code stayed in sync. [Linear](https://linear.app/blog/behind-the-latest-design-refresh)
- Linear also published "A design reset" and "A Linear spin on Liquid Glass" (not read in this session). [Linear: A design reset](https://linear.app/now/a-design-reset); [Linear Liquid Glass](https://linear.app/blog/linear-liquid-glass)
- "Linear style" is defined by critics as a dark background with linear gradients, blurs, "dynamic streamers" and micro-motion; LogRocket notes "almost every SaaS website looks the same" and that there is "no real evidence to suggest that it's better". [LogRocket: Linear design](https://blog.logrocket.com/ux-design/linear-design)
- A breakdown argues imitators want both the editorial mood and the feature dump, producing "dark-mode marketing pages that have lost the discipline that made the original work". [webtrends Linear landing page breakdown](https://webtrends.pages.dev/posts/linear-landing-page-breakdown)
- Critics now treat the dark-glow mesh-gradient hero as the default output of AI design tools, reached for "before it has made a single real decision about information hierarchy or brand tone"; dark themes tempt designers to assume contrast passes. [aismells: Gradient fog](https://aismells.pages.dev/gradient-fog.html); [buildmvpfast](https://www.buildmvpfast.com/blog/linear-aesthetic-tokens-density-keyboard-first-ux-2026)
- Anthony Hobday credits Linear with setting the trend and notes dark mode allows lighting-style effects not possible on light pages (cited via search summary; the original page returned 404 on fetch). [Anthony Hobday: A critique of the Linear website](https://anthonyhobday.com/blog/20230119.html)
- Stripe's team describes resisting "good enough" thinking so that every decision is intentional. [YouTube transcript summary](https://youtube-transcript.ai/docs/how-stripe-built-their-new-website-xjvghrn4pb)
- Rauno's essay opens by challenging the notion that design has "no science to it, only feel and intuition". He also built cmdk and Devouring Details. [Rauno](https://rauno.me/craft/interaction-design); [uiuxshowcase](https://uiuxshowcase.com/resources/invisible-details-of-interaction-design-by-rauno-freiberg)
- Family (by Benji Taylor's team) frames delight as showing users their emotional experience matters. Third-party reports say the company was acquired by Aave Labs, the wallet wound down in early 2026, and Taylor now leads design at X (low-reliability source). [lavx news](https://news.lavx.hu/article/redefining-crypto-ux-how-family-wallet-masters-simplicity-fluidity-and-delight); [yespress profile](https://yespress.io/benji-taylor)

### Inferences
- The companies' own write-ups say almost nothing about aesthetics for their own sake; they talk about contrast, consistency, density and tooling. The look is a by-product of a system and a review process.
- A shared toggle between old and new UI (Linear 2024 and 2026) is a recurring quality mechanism: it lets the team judge regressions by direct comparison.

### Gaps
- No primary Linear write-up on the marketing site itself (as opposed to the app).
- Full Katie Dill transcript unavailable; quotes are paraphrased by secondary summaries.

## 5. Common threads and what they deliberately avoid

### Takeaway
Across the cohort: computed colour systems, one sans plus one mono, depth from tone, motion budgeted by frequency and anchored to spatial origin, chrome dimmed so content leads, and process tooling that keeps design and code identical. They avoid ornamental shadows, gratuitous colour, animation on frequent actions, feature dumps, and the generic dark-glow hero that has become the imitator's signature.

### Cited Findings
- Avoid ornament: Vercel rejects gradients, glows, blobs, textures, glass effects, ornamental shadows and fake depth. [vercel.com/design.md](https://vercel.com/design.md)
- Avoid noise: Linear softens borders and removes separators ("structure should be felt, not seen") and removes coloured icon backgrounds. [Linear](https://linear.app/blog/behind-the-latest-design-refresh)
- Avoid saturated chrome: Linear capped blue chrome colour for a "timeless" neutral and in 2026 desaturated further toward warm grey. [Linear 2024](https://linear.app/now/how-we-redesigned-the-linear-ui); [Linear 2026](https://linear.app/blog/behind-the-latest-design-refresh)
- Avoid animating frequent actions: Kowalski and Rauno both cite instant command menus and Raycast's absence of animation. [Emil Kowalski](https://emilkowal.ski/ui/great-animations); [Rauno](https://rauno.me/craft/interaction-design)
- Avoid scroll-jacking effects in documentation contexts: Vercel bans parallax and scroll-triggered reveals. [vercel.com/design.md](https://vercel.com/design.md)
- Avoid showing everything at once: Family's progressive disclosure, Stripe's progressive-disclosure bento modals. [Family Values](https://benji.org/family-values); [YouTube transcript summary](https://youtube-transcript.ai/docs/how-stripe-built-their-new-website-xjvghrn4pb)
- Avoid layout-triggering animation: animate only transform and opacity. [Emil Kowalski](https://emilkowal.ski/ui/great-animations)
- Avoid copying the surface: critics blame the imitators' loss of hierarchy discipline, not the original style. [webtrends](https://webtrends.pages.dev/posts/linear-landing-page-breakdown); [LogRocket](https://blog.logrocket.com/ux-design/linear-design)

### Inferences
- Common threads, ranked by strength of evidence:
  1. Colour is generated from few inputs in a perceptual space (LCH or OKLCH), and colour carries meaning, not decoration.
  2. One neo-grotesque (Inter or Geist) with a display cut or tight tracking for headings, plus a monospace for technical detail; narrow weight range.
  3. Depth from luminance steps and hairline borders; shadows only where they model a real object.
  4. Motion under about 300ms, ease-out, transform and opacity, interruptible, origin-aware; zero motion on keyboard or high-frequency actions; spectacle confined to a GPU-rendered hero with a static fallback.
  5. Secondary chrome dimmed and shrunk so content is the highest-contrast element.
  6. Progressive disclosure instead of feature lists.
  7. Quality enforced through process: feature flags, old-versus-new toggles, token pipelines from code to Figma.
- Vercel's spec and Linear's 2026 refresh show a drift since 2024 from expressive dark-glow aesthetics toward calmer, warmer, lower-contrast chrome, partly as a reaction to the style's commoditisation.
- Note that Vercel's design.md is an agent-facing brand guide for generated pages, so its bans (no gradients, no glass) describe Vercel's documentation and report register more strictly than its own marketing homepage, which has historically used gradients.

### Gaps
- Not researched: Arc / The Browser Company, Framer, Resend, Paco Coursey, Notion, Figma, Emil Kowalski's personal site layout, rauno.me's own visual layout.
- No conversion or performance data linking any of these aesthetics to business outcomes; LogRocket explicitly notes the absence of such evidence.
- Raycast and Teenage Engineering values come from reverse-engineered files that contradict each other; a first-hand inspection of computed styles would be needed to confirm hex values and fonts.
