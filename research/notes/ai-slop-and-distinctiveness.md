# AI slop and distinctiveness in web UI: tells, causes and remedies (2024 to 2026)

Note on formatting: per the user's writing rules, sources follow each claim after a colon rather than an em dash.

## Q1. What are the recognised tells of AI-generated or "vibe-coded" frontends, and what do designers say?

### Takeaway
The tells are now catalogued in near-identical form by Anthropic, independent designers, agencies and a measured Hacker News study: Inter (or Space Grotesk / Geist / Instrument Serif as the "second wave"), indigo/purple-to-blue gradients including gradient headline text, a centred hero with a badge above the H1, three identical icon-topped feature cards, numbered 1-2-3 steps, stat banner rows, emoji as icons, glows and coloured shadows, glassmorphism, nested cards, coloured side-border tabs, status dots, all-caps micro-labels, permanent dark mode with low-contrast grey text, and weightless copy such as "Build faster. Ship smarter." One measured study found 22% of recent Show HN sites trip four or more of these patterns.

### Cited Findings

Measured study (the strongest evidence found)
- Adrian Krebs (20 April 2026) scored ~1,400 to 1,590 recent Show HN submissions with Playwright plus deterministic DOM and computed-style checks, deliberately avoiding screenshots or LLM judgement; manual QA estimated a 5 to 10% false-positive rate: [Krebs, "Scoring Show HN submissions for AI design patterns"](https://www.adriankrebs.ch/blog/design-slop/)
- Results: 22% (347 sites) triggered 4+ patterns ("high"), 32% (508) triggered 2 to 3, 46% (735) triggered 0 to 1: [Krebs](https://www.adriankrebs.ch/blog/design-slop/)
- Patterns Krebs checked, grouped as he presents them: [Krebs](https://www.adriankrebs.ch/blog/design-slop/)
  - Fonts: Inter everywhere, especially centred hero headlines; "LLM font combos" Space Grotesk, Instrument Serif, Geist; a serif italic accent word inside an otherwise Inter hero.
  - Colour: "VibeCode Purple"; permanent dark mode with medium-grey body text and all-caps section labels; barely-passing body text contrast on dark themes; gradients everywhere; large coloured glows or coloured box-shadows.
  - Layout: centred hero in a generic sans; a badge/pill directly above the hero H1; coloured top or left borders on cards; identical icon-topped feature cards; numbered "1, 2, 3" steps; stat banner rows; emoji icons in sidebars/navs; all-caps headings and labels.
  - CSS: shadcn/ui and glassmorphism.
- Krebs's verdict: the trend is "not really [bad], just uninspired"; the real line is between crafting a design and shipping LLM defaults, a problem that predates LLMs via templates. He links the surge to Claude Code and notes HN moderators restricted Show HN for new accounts: [Krebs](https://www.adriankrebs.ch/blog/design-slop/)

Anthropic's own diagnosis
- Anthropic's Applied AI team (Prithvi Rajasekaran, Justin Wei, Alexander Bricken; 12 November 2025) states that an unguided LLM landing page "almost always" converges on Inter, purple gradients on white backgrounds, and minimal animation, and names the result the "AI slop" aesthetic: [Anthropic, "Improving frontend design through Skills"](https://claude.com/resources/articles/improving-frontend-design-through-skills)
- Anthropic's current frontend-design SKILL.md additionally names as tells: the default hero formula of "a big number, a small label, supporting stats and a gradient accent"; single-word accent styling in headlines; all-caps labels; unnecessary labels above content; numbered markers used for things that are not sequences; decorative borders and dividers that carry no information; scattered motion: [anthropics/skills frontend-design SKILL.md (as fetched Nov 2026, summarised by fetch tool)](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)

Designer and practitioner catalogues
- Jeff Humble (Fountain Institute), "7 tells": (1) neon palettes with 5+ neon colours and no focus; (2) dark-mode "aurora" radial glow behind hero content; (3) emoji as primary icons, background elements and nav items; (4) purple gradients on H1s, buttons and backgrounds; (5) cards inside cards inside cards; (6) multicoloured side tabs on every card, colours cancelling each other out; (7) status dots on every element, detached from any real "live"/"connected" meaning: [Fountain Institute, "7 Tells that a UI is AI-Generated"](https://pages.thefountaininstitute.com/posts/7-tells-that-a-ui-is-ai-generated)
- 925Studios (agency, 2026): Inter in a tight modern weight; blue-to-purple gradient behind the headline and on the "Get Started" CTA; dark hero with gradient; three rounded cards in a row with soft shadows and a thin line icon each; weightless headlines like "Build faster. Ship smarter."; interchangeable thin line icons: [925Studios, "AI Slop Fonts and Gradients"](https://www.925studios.co/blog/ai-slop-design-tells)
- Specific Tailwind class tells named in a DEV write-up: `bg-indigo-500` buttons, `text-indigo-600` headings, `from-indigo-500 to-purple-600` gradients, white or light grey backgrounds, Inter or system-ui, `border-radius: 0.5rem`, low-opacity soft shadows, three-column icon feature grid, gradient hero text, purple CTA: [DEV, "Why every AI-built website looks the same: blame Tailwind's indigo-500"](https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p)
- prg.sh lists the recurring default set as Inter/Roboto, purple/indigo accents, centred hero with CTA, three icon boxes in a grid, white or light grey backgrounds, subtle shadows; it also flags functional slop: forms without validation, error states, required-field indicators or accessibility: [prg.sh, "Why Your AI Keeps Building the Same Purple Gradient Website"](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website)
- Paul Bakaus's open-source "Impeccable" skill lists anti-patterns including Inter/Roboto/Arial, cyan-on-dark and purple-gradient palettes, pure black or pure white neutrals, and nested cards; its `npx impeccable detect` CLI scans code for 24 issues including side-tab borders, purple gradients and bounce easing: [DEV, Impeccable overview](https://dev.to/apilover/impeccable-the-claude-code-skill-for-unique-frontend-ui-4n37); [Impeccable README mirror](https://git.secluded.site/agent-skills/blob/3ddb608fc22d01dfe58d5d51185d5fd3f78765bb/vendor/impeccable/README.md)

The SaaS "template" tells (pre-AI and AI-amplified)
- Brainy Papers (Boone, updated 18 September 2026) names five SaaS tells: (1) dark slate/near-black surface with white type and a faint cyan or violet accent, claimed on "roughly 70%" of new B2B SaaS launches in 18 months; (2) a blurred coral-to-violet-to-cyan radial gradient mesh across the top third of the homepage; (3) a monospace accent word in the H1 (JetBrains Mono, IBM Plex Mono, Berkeley Mono, Geist Mono); (4) a Command-K pill top right; (5) geometric grain: dot pattern, hairline grid or noise on the dark surface. Also the "trusted by" logo row at about 60% opacity: [Brainy Papers, "Why Every SaaS Looks the Same in 2026"](https://brainy.ink/paper/why-every-saas-looks-the-same-2026). The 70% figure has no stated methodology.
- Daryl Ginn coined "the Linear effect" (10 January 2023): dark backgrounds, subtle blurred gradients behind product visuals, animated glowing elements; "Until everyone gets a little too inspired." He notes Stripe (2020) was the "old Linear", spawning diagonal coloured shapes, gradients and duotone icons: [Ginn, "The Linear effect", Rectangle](https://rectangle.substack.com/p/the-linear-effect)
- LogRocket observes "almost every SaaS website looks the same" under the Linear style: [LogRocket, "Linear design"](https://blog.logrocket.com/ux-design/linear-design)

Community sentiment
- A Hacker News commenter on shadcn: "when every LLM defaults to using this UI, it just makes mine look LLM generated" (seen via an HN mirror; verify against the original thread before quoting): [astro-hackernews mirror](https://astro-hackernews.pages.dev/stories/47984512)
- A Design Systems Collective piece: most Tailwind + shadcn apps "look like they were built by the same person or worse, the same AI model": [Design Systems Collective](https://www.designsystemscollective.com/is-anyone-else-tired-of-every-tailwind-shadcn-app-looking-the-same-69c545e73114)
- Vercel's own community team acknowledged the default v0 look "is becoming overused at this point": [Vercel Community, "Theming in v0"](https://community.vercel.com/t/theming-in-v0/17000)

### Inferences
- The tells cluster into four layers: type (Inter and its second-wave substitutes), colour (indigo/violet gradients, glows, neon on dark), structure (centred hero, badge, 3-card grid, 1-2-3 steps, stat row, logo row, nested cards) and micro-ornament (emoji icons, status dots, side tabs, all-caps eyebrow labels, gradient or italic accent words). A useful catalogue for a skill should cover all four, since banning only fonts and colour leaves the structural template intact.
- The "accent word" tell (a single italic serif, monospace or gradient word in an otherwise plain headline) appears independently in Krebs, Brainy Papers and Anthropic's SKILL.md, which suggests it is the newest and fastest-spreading tell, partly a product of models being told to avoid Inter.
- Functional slop (missing error, empty and loading states, no validation, no focus states) is a separate tell family that is under-discussed relative to visual tells.

### Gaps
- No primary source found for exact shadcn/ui default token values (base colour, radius) or for the frequency of Geist in create-next-app scaffolds; not verified in this research.
- Reddit r/web_design and r/UXDesign threads were not fetched directly; sentiment above comes from HN mirrors and articles.
- Krebs's post has an internal inconsistency (16 vs 18 patterns, ~1,400 vs 1,590 sites).

## Q2. Why do LLMs and templates converge on these defaults?

### Takeaway
Two mechanisms dominate: distributional convergence (models sample the high-probability centre of training data, which is dominated by safe, universal choices and Tailwind/template code) and path dependence from a few influential defaults, most famously Tailwind UI's `bg-indigo-500`. A feedback loop then tightens variance as AI-built sites are scraped back into training data.

### Cited Findings
- Anthropic names the mechanism "distributional convergence": "Safe design choices, those that work universally and offend no one, dominate web training data", so without direction the model samples from that centre: [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills)
- Banning defaults displaces rather than removes convergence: Anthropic reports the model still drifts to Space Grotesk even when told to avoid common choices, and Space Grotesk is in its own recommended list: [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills). Krebs independently lists Space Grotesk, Instrument Serif and Geist as "LLM font combos": [Krebs](https://www.adriankrebs.ch/blog/design-slop/)
- Adam Wathan (Tailwind CSS creator) posted on X on 7 August 2025 a joking apology for making every Tailwind UI button `bg-indigo-500` five years earlier; secondary reports put views between 684,000 and over a million. The original tweet was not retrieved, and the training-data causation is commentators' inference, not Wathan's claim: [AIbase news](https://news.aibase.com/news/20365); [925Studios](https://www.925studios.co/blog/ai-slop-design-tells); [DEV](https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p)
- prg.sh: LLMs are "statistical pattern matchers"; ambiguous prompts get filled with the commonest patterns; indigo was chosen in Tailwind UI only because a demo colour was needed, then copied until purple read as "modern web design": [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website)
- Three-column card grids are learned from Tailwind tutorials as "how a feature section looks"; LLMs return the statistical median for any unspecified decision: [925Studios](https://www.925studios.co/blog/ai-slop-design-tells)
- Feedback loop: v0, Lovable, Bolt, Cursor and Figma AI learn from shipped products that already share the template, their output feeds the next crawl, and variance shrinks; founders also pattern-match safe references under uncertainty, and component libraries make the full template achievable in an afternoon: [Brainy Papers](https://brainy.ink/paper/why-every-saas-looks-the-same-2026)
- Functional gaps arise because models train on static code, not on user interaction: [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website)
- Imitators copy the Linear surface without its reasoning; Anthony Hobday argues Linear's dark mode fits its brand where followers' does not: [Hobday, "A critique of the Linear website"](https://anthonyhobday.com/blog/20230119.html); [925Studios, Linear breakdown](https://www.925studios.co/blog/linear-design-breakdown-saas-ui-2026)

### Inferences
- Because convergence is distributional, any fixed ban list creates a new mode one step away (Inter to Space Grotesk to Instrument Serif italic). Guidance therefore works better when it forces a decision derived from the subject (brand, audience, domain vernacular) than when it only lists forbidden values.
- Templates and AI share the same root cause: decisions left unmade default to the most common answer. AI simply makes the unmade-decision path cheaper and faster.

### Gaps
- No peer-reviewed or quantitative study on training-data composition (for instance, share of Tailwind code using indigo) was found; the indigo causation is widely asserted but unproven.

## Q3. What guidance exists for steering AI towards distinctive frontends?

### Takeaway
Anthropic's guidance is the most specific published source: ban generic fonts by name, pick one distinctive font and use it decisively with extreme weight and size contrast, commit to a cohesive aesthetic in CSS variables with a dominant colour and sharp accent, orchestrate one page-load animation rather than scattered micro-interactions, build atmospheric backgrounds, and vary themes between generations. Its newer SKILL.md shifts emphasis from ban lists to grounding in the subject, a written design plan, a self-review against "generic default" and a quality floor. Community skills (Impeccable) and v0's design-system import follow the same direction: supply tokens and decisions so the model is not choosing.

### Cited Findings

Anthropic, "Improving frontend design through Skills" (12 November 2025)
- Guidance must sit at "the right altitude": not hard-coded hex values, not vague advice: [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills)
- Typography block `<use_interesting_fonts>`: "Typography instantly signals quality. Avoid using boring, generic fonts." "Never use: Inter, Roboto, Open Sans, Lato, default system fonts." Suggested by category: code aesthetic (JetBrains Mono, Fira Code, Space Grotesk); editorial (Playfair Display, Crimson Pro); technical (IBM Plex family, Source Sans 3); distinctive (Bricolage Grotesque, Newsreader). Pair for high contrast (display + monospace, serif + geometric sans). "Use extremes: 100/200 weight vs 800/900, not 400 vs 600." Size jumps of 3x or more, not 1.5x. "Pick one distinctive font, use it decisively", loaded from Google Fonts: [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills)
- The typography mandate alone improved other aspects of the design: [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills)
- The ~400-token `<frontend_aesthetics>` prompt: "Commit to a cohesive aesthetic. Use CSS variables for consistency." "Dominant colors with sharp accents outperform timid, evenly-distributed palettes." Motion: CSS-only for HTML, the Motion library for React; prefer "one well-orchestrated page load with staggered reveals (animation-delay)". Backgrounds: "Create atmosphere and depth rather than defaulting to solid colors" (layered gradients, geometric patterns, contextual effects). Avoid overused fonts, clichéd schemes (purple gradients on white), predictable layouts and cookie-cutter components. Vary light/dark and fonts across generations; "it is critical that you think outside the box!": [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills)
- Theme prompting example `<always_use_rpg_theme>`: fantasy palettes, ornate borders, parchment and leather textures, medieval serif headers, showing that naming a concrete theme steers strongly: [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills)
- Evidence is qualitative (before/after screenshots of a SaaS landing page, blog and admin dashboard); no metrics: [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills)

Anthropic frontend-design SKILL.md (current version, summarised)
- Adopt the mindset of a design lead; first identify subject, audience and primary job, and draw visual choices from the subject's industry and vernacular. Open the hero with the most characteristic element of the subject's world rather than the big-number/small-label/stats/gradient formula. One or two clearly distinct typefaces, a clear type scale, headline type treated as an active design element. Lines under 80 characters; slightly more leading for serif body text. Borders, numbering, dividers and labels must carry information; numbered markers only for real sequences. Motion sparingly: one orchestrated moment, responsive to user action. Copy in plain, active, sentence-case language from the user's perspective; specific, actionable errors; empty states that invite action. Process: write a compact design plan (4 to 6 hex colours, type roles, layout concept with ASCII wireframe, alignment, principles), review it against the brief and revise anything that reads as a generic default, then build. Quality floor: responsive, visible focus, reduced-motion support, accessibility. Self-critique with screenshots and remove decoration that does not serve the brief: [anthropics/skills SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)

Other prompting guidance
- prg.sh's nine fixes: assign a role (senior frontend designer); constrain typography, colour, motion and backgrounds separately; reference a specific aesthetic ("a 1970s ski lodge palette") rather than "nice-looking"; list what to avoid; isolate one dimension per iteration; use XML tags such as `<theme>` to hold an aesthetic across generations; ask for multiple directions to escape the first, most probable result; extract references from Dribbble, Mobbin or Awwwards and describe why they work; check validation, error states and accessibility afterwards: [prg.sh](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website)
- Supply design tokens and tell the model to use only those names, rather than letting it invent `bg-indigo-500`: [DEV](https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p)
- 925Studios: give the tool a specific typeface, a brand-derived palette, a layout principle and a tone, and treat output as a draft; brand decisions still need a human because the model cannot hold a brand across prompts: [925Studios](https://www.925studios.co/blog/ai-slop-design-tells)
- Impeccable builds on Anthropic's frontend-design skill and adds reference files for typography, colour, spatial design, motion, interaction, responsive design and UX writing, plus a detector CLI: [Impeccable docs](https://www.mintlify.com/pbakaus/impeccable/introduction)

Vercel v0
- v0 offers a design-system feature, positioned by Vercel staff as the answer to the overused default look; v0 can import a system from GitHub repos, npm packages, Storybook and Figma frames and learn components, props, tokens and themes (company social post, not docs): [Vercel Community](https://community.vercel.com/t/theming-in-v0/17000); [v0 LinkedIn](https://www.linkedin.com/company/v0dev)
- v0 sometimes emits absolute colours like `text-red-600` and must be reminded to use semantic tokens like `text-destructive`: [Vercel Community](https://community.vercel.com/t/theming-in-v0/17000)

### Inferences
- Anthropic's own guidance evolved from a ban-and-recommend list (Nov 2025) to a process (ground, plan, critique, revise), which is consistent with its admission that bans just shift the mode. The process approach is the more durable model for a skill.
- The recommended "distinctive" fonts in Anthropic's 2025 list (Space Grotesk, Playfair Display, JetBrains Mono) have themselves become tells by 2026 per Krebs and Brainy Papers, so any skill should avoid naming a small fixed set of "good" fonts.

### Gaps
- No official Vercel v0 documentation on prompt wording for avoiding the default look was found.
- The cookbook notebook (`prompting_for_frontend_aesthetics.ipynb`) was not fetched directly; its wording was taken from the article.

## Q4. How do skilled designers create distinctive identity?

### Takeaway
Distinctive work derives choices from something true about the product and commits to them: a named aesthetic direction, a typeface with a point of view, a palette with a dominant colour, art direction or illustration owned by the brand, product-specific copy and a layout that breaks the triptych. Practitioners advise picking a fight with one or two tells rather than all of them, and carrying the identity into the product itself.

### Cited Findings
- Build the palette from something true about the product; choose a typeface with a point of view; break the three-card triptych with asymmetry, a different rhythm, or content that does not fit three equal columns; write copy naming the audience and what is specific; use icons tied to the product's own vocabulary: [925Studios](https://www.925studios.co/blog/ai-slop-design-tells)
- "Pick a fight with one or two tells, not all five"; the full inversion of the SaaS template is a high-saturation light surface, a serif or display H1, an illustrative hero, a non-Cmd-K affordance and warm grain. Keep the template's useful parts (clear type, strong hierarchy); name one visual choice you would never copy; carry the brand into dashboard, loading states and onboarding; test whether a stranger could swap your wordmark with a competitor's unnoticed: [Brainy Papers](https://brainy.ink/paper/why-every-saas-looks-the-same-2026)
- Examples cited as breaking the mould: Stripe (illustration, typography, documentation, dashboard taste), Notion (doodled illustrations, cream surface), Figma (playful spectrum, multiplayer cursors), Anthropic (warm, slightly literary brand in a sterile category): [Brainy Papers](https://brainy.ink/paper/why-every-saas-looks-the-same-2026)
- Ground choices in the subject's industry and vernacular, and open with the most characteristic element of the subject's world: [anthropics/skills SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
- Concrete theme direction (the RPG example: parchment, leather, ornate borders, medieval serifs) produces markedly different output than generic instructions: [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills)
- Restraint as distinctiveness: at most one deliberate gradient, one dominant accent, a colour budget so accent carries meaning, dots only for real status: [Fountain Institute](https://pages.thefountaininstitute.com/posts/7-tells-that-a-ui-is-ai-generated)
- Ginn's advice on the Linear effect: following its traits too closely makes a site part of the trend; it "wouldn't hurt to be a little different": [Ginn](https://rectangle.substack.com/p/the-linear-effect)
- Linear's own look works because it understands what a dark-mode site allows; copying aesthetics without the reasoning makes clones hollow: [Hobday](https://anthonyhobday.com/blog/20230119.html); [925Studios, Linear breakdown](https://www.925studios.co/blog/linear-design-breakdown-saas-ui-2026)

### Inferences
- The common thread is provenance: a choice is distinctive when it can be justified by the product's subject or audience, not by what is fashionable. "Could this choice belong to any product?" is a usable test for each decision.
- Named aesthetic directions (brutalist, editorial, Swiss, retro-futurist, maximalist) function as compressed bundles of decisions; they are effective prompts precisely because they force many correlated choices at once.

### Gaps
- No sources were fetched that systematically document brutalist, Swiss or editorial revival case studies in 2024 to 2026; this section relies on SaaS-focused commentary.
- No evidence was found on whether distinctive design measurably improves conversion versus templated design.

## Q5. The broader taste and craft discourse, 2024 to 2026

### Takeaway
"Everything looks the same" predates AI (the Stripe wave around 2020, the Linear effect from 2022/23) but AI tooling has industrialised it, producing a "SaaS monoculture". The 2025/26 discourse frames taste and deliberate decisions as the scarce input, while sceptics note sameness is not new and arguably harmless for validating ideas.

### Cited Findings
- Stripe (2020) and Linear (2022) each spawned waves of imitation: [Ginn](https://rectangle.substack.com/p/the-linear-effect)
- 2026 framing as a "SaaS monoculture" driven by Linear as reference point plus AI tools' feedback loop; visual identity described as a compounding asset worth investing in before the next feature: [Brainy Papers](https://brainy.ink/paper/why-every-saas-looks-the-same-2026)
- Show HN submissions tripled and mostly share the vibe-coded look; Krebs expects people to return to distinctive design to stand out, while questioning how much design matters once AI agents are the main web users: [Krebs](https://www.adriankrebs.ch/blog/design-slop/); [Gigazine coverage](https://www.gigazine.net/gsc_news/en/20260423-design-slop)
- Anthropic frames generic output as undermining brand identity and making AI interfaces "easy to dismiss": [Anthropic](https://claude.com/resources/articles/improving-frontend-design-through-skills)
- Brainy Papers: "the template is free; the brand is not", looking the same carries no visible cost until competitors catch up: [Brainy Papers](https://brainy.ink/paper/why-every-saas-looks-the-same-2026)
- Counterpoints: sameness is "nothing new" (Reddit thread), and Krebs calls it "just uninspired", not bad, since validating a business never depended on fancy design: [Krebs](https://www.adriankrebs.ch/blog/design-slop/); [Reddit snapshot](https://reddit.sentinel-team.org/posts/1torg9k/snapshots/2026-05-28T06%3A43%3A31.622178Z)
- An ecosystem of "de-slop" tooling emerged: Impeccable (reported at 10,000+ GitHub stars by March 2026 and higher later, figures vary), unslop-ui skills, Uiverse "De-slop your AI generated websites", AI design checkers: [mejba.me](https://www.mejba.me/blog/impeccable-claude-code-design-skill); [Product Hunt, Uiverse Design](https://www.producthunt.com/p/uiverse-io/uiverse-design); [ai-design-checker via HN reader](https://hn.jakechampion.name/reader/https://github.com/AdrianKrebs/ai-design-checker)

### Inferences
- The discourse has moved from "AI cannot design" to "AI ships the median unless a human supplies decisions". Taste in this framing is the set of decisions made before generation, which is exactly what a design skill can encode.
- Because the tell set mutates (Inter to Space Grotesk to serif italic accent; light purple to dark aurora), a skill should teach the principle (derive, commit, justify, remove what does not serve) and treat specific ban lists as examples rather than an exhaustive rule set.

### Gaps
- Original X/Twitter threads (Wathan's post, designer reactions) were not retrieved; all X content is via secondary reporting.
- Smashing Magazine and Sidebar.io coverage was not located within the search budget.
