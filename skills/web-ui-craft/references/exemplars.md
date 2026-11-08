# Exemplars

What to learn from the most admired sites, and the aesthetic directions they represent. Take the reasoning, not the surface. Copying Linear's dark glow without its contrast discipline is how "the Linear effect" became a cliché.

## Directions

A named direction is a bundle of correlated decisions. Choose the one the subject calls for, then make it specific to this subject. These are starting points, not templates. Each direction has a generic version it slides into when the subject stops steering; the last column names it, using the clusters in `slop-tells.md`.

| Direction | Fits | Characteristic decisions | Slides into |
|---|---|---|---|
| Calm product tool | Developer tools, productivity apps, dashboards | Monochrome or near-monochrome, one accent for meaning, one sans, mono only for code and identifiers, tone-step depth, dimmed chrome, almost no motion, dense but quiet | Near-black and acid, or the dark SaaS template |
| Editorial | Publications, research, cultural organisations, personal sites | Serif or characterful grotesk, large type contrast, asymmetric grid, generous measure-led layout, photography or type alone, very little colour | Cream and clay, or broadsheet |
| Swiss and civic | Public services, institutions, transport, documentation | Strict grid, one grotesk, flush-left everything, strong numbers, high contrast, primary colour used as signal | Broadsheet, with caps labels everywhere |
| Tactile and playful | Consumer apps, finance for people, education | Warm palette, soft but consistent radii, spatial motion from the trigger, rare celebratory moments, sound or haptics with restraint | SaaS card kit in pastels |
| Immersive brand | Launches, studios, fashion, automotive, entertainment | One real-time or scroll-driven idea carried through, kinetic type, custom transitions, a static frame that still looks intentional | Cursor spotlights, page-wide kinetic type and a decorative 3D blob with no idea behind them |
| Utilitarian or brutalist | Tools for experts, art and music, counter-positioning | Raw system fonts or mono by choice, visible structure, hard edges, information density as aesthetic | Near-black and acid, mono on every label |
| Retro or material | Products with heritage or a physical counterpart | Palette, type and texture from a specific era or object, grain, skeuomorphic detail only where it models the real thing | Cream and clay with grain over everything |

## Product sites

### Linear

- **Colour by computation.** Themes generated in LCH from three inputs (base, accent, contrast) instead of 98 hand-set values. Elevation is lightness steps from the same generator. Blue in the chrome deliberately capped for a neutral, timeless look.
- **2026 refresh**: cool blue-grey moved to a warmer, less saturated grey; sidebar "a few notches dimmer"; borders softened and separators removed. Principles: "structure should be felt, not seen" and "don't compete for attention you haven't earned".
- **Type**: Inter Display for headings, Inter for everything else.
- **Process**: shipped behind a feature flag with an old-versus-new toggle; colour tokens exported as JSON so design and code match.
- **Lesson**: the look comes from a system and from dimming everything that is not the content.

### Vercel (Geist)

- Monochrome by default; colour only for meaning, always paired with a non-colour cue.
- Geist Sans for prose and controls, Geist Mono for code, paths, timestamps and identifiers. Weights 400 to 600 only.
- 12, 6 and 4 column grid; prose at 60 to 68 characters.
- "Shadows: none. Ornamental shadows and fake depth are rejected." No gradients, glows or glass in its generated-page guide; stillness by default.
- Emphasis is scarce; pills and badges for ordinary metadata, cards in cards and decorative icon tiles are rejected.
- **Lesson**: restraint, enforced by rules, reads as authority.

### Stripe

- A signature gradient wave rendered on a WebGL canvas (originally "minigl", a tiny custom WebGL wrapper), isolated so the rest of the page stays cheap. Refined over years rather than replaced.
- January 2026 homepage began with "what is a website for?" and answered with a bento grid presenting the product as one suite, modals revealing detail progressively, and a live counter of the share of global GDP running on Stripe as proof.
- **Lesson**: one owned visual signature, and proof that is live and specific.

### Family

- "We fly instead of teleport": trays rise from the element that summoned them, tabs slide in the direction of the tapped tab, "Continue" morphs into "Confirm" by reusing shared letters.
- "Mastering delight is mastering selective emphasis": confetti only after backing up a wallet, sound only on the trash action.
- Rejects "everything is right there, all the time"; reveals features as they become relevant.
- **Lesson**: motion as spatial explanation, and delight rationed to moments that matter.

### Apple product pages

- Scroll position mapped to a frame index and drawn to a `<canvas>` (147 frames for the AirPods Pro hero), so the product rotates and assembles as you scroll.
- A single static image on constrained devices.
- **Lesson**: spectacle tied to the product itself, with a fallback.

### Raycast

- 3D keycaps with gradients and inset highlights: depth that models a real object, the keyboard, so it reads as meaning rather than ornament.
- The launcher itself does not animate, because it is opened constantly.
- **Lesson**: skeuomorphism is justified by a referent; frequency decides motion.

### Teenage Engineering

- Monospace across site, products, packaging and social: one typographic decision held everywhere becomes identity.
- **Lesson**: consistency across every touchpoint is a style in itself.

### Rauno Freiberg and Emil Kowalski

- Interaction craft: instant command menus, gestures that apply input directly, interruptible motion, popovers from their trigger, nothing animated from `scale(0)`, nothing animated on keyboard actions.
- **Lesson**: invisible details are where "feel" comes from (see `interaction.md`).

## Award winners

Awwwards weights Design 40%, Usability 30%, Creativity 20% and Content 10%, with at least 18 jurors and outliers dropped, which rewards coherent polish over polarising experiments.

- **Sites of the Year**: Lusion v3 by Lusion (2023), Igloo Inc by abeto (2024), Lando Norris by OFF+BRAND (2025). Recurring studios: Immersive Garden, Resn, Lusion, abeto, The First The Last.
- **Common stack**: GSAP, Lenis smooth scroll, scroll-driven storytelling, Three.js or WebGL, kinetic type, custom cursors, page transitions. WebGPU, native View Transitions, CSS grain and type-led editorial layouts are rising; heavy glassmorphism and decorative 3D heroes on non-brand sites are fading.
- **What jurors reward** (Hon Tran, an Awwwards juror): one strong idea carried through that could not move to another brand; static frames that look intentional without motion; smooth frame rates on mid-range phones; reduced-motion fallbacks. Jank, desktop-only thinking and effects without a concept cap a site in the mid-7s.
- **Igloo Inc** was praised for pairing an immersive 3D world with easy scroll navigation.
- **Dropbox Brand by Daybreak Studio** won CSS Design Awards Website of the Year and Best UX in 2025 with a systematised, type-led brand guidelines site and no reliance on 3D: proof that spectacle is optional.
- **Caution**: award sites are a craft benchmark, not a usability benchmark. Some nominees have scored highly despite many accessibility errors. Take their ideas, not their weight.

## Where the frontier is moving

- The originators are moving toward calm: Linear warmer and dimmer, Vercel still. The dark-glow look now signals imitation.
- Award work is splitting between immersive real-time 3D and quiet, type-led editorial systems.
- Distinctiveness comes from one subject-specific idea executed well, or from disciplined restraint. Rarely from adding effects.
