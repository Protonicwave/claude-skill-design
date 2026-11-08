# Hero artefacts

Every acclaimed site in the benchmark carries one piece made to a very high standard, and the rest of the page stays quiet around it: Linear's product screen, Stripe's checkout and terminal, Teenage Engineering's studio-lit product, Family's illustrated cast, PostHog's whole desktop. Most of those sites use several generated-UI tells and still look expensive, because the eye lands on the piece first. A page without one looks basic however correct its type and spacing are.

This file is how to make that piece when the work happens in code, usually with no photographs, renders or illustrations supplied.

## Choose the piece

Pick by what the subject's world looks like, then name the piece in the brief's Signature line.

| Subject | Piece | Benchmark |
|---|---|---|
| Software, developer tools, dashboards | The product's interface at true fidelity, caught mid-task | Linear, Stripe, Raycast |
| Physical product | The object, lit, drawn in SVG and CSS or rendered; or an exploded or annotated diagram | Teenage Engineering, Apple |
| Finance, data, infrastructure | One live or precise figure, or a chart drawn from real-shaped data | Stripe's share of global GDP |
| Consumer, playful, education | An illustrated cast or set of objects drawn for this subject | Family |
| Culture, editorial, place | Photography with one treatment, or type set as the image | Mercury, editorial sites |
| A brand whose site is the experience | One real-time or scroll-driven scene | Lando Norris, Igloo Inc |

Where real assets exist (product screenshots, photographs, renders, a brand illustration library), use them and give them one treatment. Where the session has an image-generation tool, it can supply photography or texture, art-directed in one sentence (light, lens, palette, mood) taken from the brief; check each image for broken hands, text and geometry, and never use one for product UI, real people or anything presented as evidence. Where neither exists, build the piece in code. Never ship an empty frame, a grey placeholder rectangle or a stock-looking stand-in.

## Product interfaces

A product mock-up is the strongest proof a software page can show, and generated pages usually reduce it to a rounded box with three grey bars. Build it as a real interface.

- **Real markup at real size.** Text is text, not an image. Interface type is 11 to 14 px, with the product's own density: tighter spacing than the marketing page around it, tabular numbers, a mono face only where the product would use one.
- **Enough structure to read as a product.** Navigation or a sidebar, the main view, and one detail (a panel, a row expanded, a popover). One view alone reads as a wireframe.
- **Believable data in the domain's own vocabulary.** Identifiers with the product's own prefixes, people's first names, relative times, statuses, units and uneven figures: a freight tool shows `SHP-20931`, `Rotterdam`, `ETA 14:40`, `18.6 t`; a clinic rota shows `Dr Okafor`, `Ward 7B`, `3 of 11 shifts open`. Round numbers and "Lorem" read as fake at once. These examples show the form only: take every value from the subject, never from this page, or every mock-up made with this skill shares the same identifiers. Invented names and figures are fine in a mock-up; invented customer quotes, logos and metrics presented as real are not.
- **Caught mid-task.** Show the moment the product exists for: a job part-way through, a review waiting, a check turning green. A static, empty dashboard says nothing.
- **Its own theme if the product has one.** A dark product screen on a light page is normal; it still draws from the page's tokens for hue and neutral tint, so the two read as one brand.
- **A frame only as heavy as the real product's.** A thin border and one lit edge usually suffice. Window controls only when the product really is a desktop app.
- **A deliberate crop.** Let the screen bleed off the edge of the page or under the next section rather than shrinking it to fit. On a phone, show a cropped region at readable size, not the whole screen at 30%.
- **Out of the way of assistive technology.** Give the outer element `role="img"` and an `aria-label` that says what the screen shows, and put `inert` on an inner wrapper so nothing inside is focusable. `inert` also hides its subtree from screen readers, so it must not sit on the labelled element itself. A piece the visitor can operate (keys that play, a slider that changes the demo) is a working control, not a picture: leave its controls in the tab order, label the group once, and skip `role="img"` and `inert`.

```html
<figure class="product-shot" role="img" aria-label="A dispatch board with shipment SHP-20931 en route, ETA 14:40">
  <div inert>
    <!-- sidebar, main view and one detail panel, built from the product's own density tokens -->
  </div>
</figure>
```

## Pieces that play themselves

The most premium motion on these sites is the hero piece demonstrating itself: Stripe's figure ticking, PostHog's demo panel running, an interface moving from one state to the next. It is cheap to build with CSS keyframes and a short script, and it proves the claim better than any copy.

- Loop one short story (6 to 12 s) that shows the primary job happening: a request arriving, the product handling it, the result landing.
- Start only when the piece is on screen (IntersectionObserver) and pause when it leaves or the tab is hidden (`visibilitychange`).
- Anything that moves for more than five seconds gets a visible pause control (WCAG 2.2.2).
- Under `prefers-reduced-motion: reduce`, show one good finished frame. Never show the first, empty frame.
- Each step of the loop is choreographed as "The signature moment" in `interaction.md` describes: one lead element, followers overlapping 40 to 80 ms behind it, and a settling spring for anything that changes place.
- If the piece answers the pointer, follow "Pointer response" in `interaction.md`.

## Illustration in one hand

Illustration reads as owned only when one hand drew all of it. In SVG:

- One stroke width, one cap and join style, one corner treatment, one perspective.
- Colours from the page tokens (`currentColor` or CSS variables), so a theme change recolours the drawing.
- Built from the subject's own shapes: the product's materials, tools, places and characters. Blobs, sparkles and abstract waves belong to no subject.
- At real scale. An illustration the size of an icon is decoration; one that holds a third of the first screen is a signature.

## Light as a material

Every dark premium site in the benchmark lights its hero: Teenage Engineering's spotlight and cast shadow, the pool of light under Linear's product screen, Raycast's light streaks. Light is allowed when it behaves like light:

- **One source** for the whole page, with its direction named in the brief's Depth line. Highlights face it; shadows fall away from it.
- **It reveals something.** Light falls on the product, the object or the type. Light behind nothing is a glow, and a glow is a tell.
- **Low chroma, from the subject.** A warm studio light, a cold daylight, the product's own colour. Not the purple-to-blue aurora.
- **Once.** One lit moment, usually the hero. Repeating it behind every section turns it back into decoration.

Starting points, all static gradients that cost almost nothing to render:

```css
/* Spotlight from above onto a dark field, as in a product photograph. */
.spotlight {
  background:
    radial-gradient(ellipse 60% 50% at 50% 0%, oklch(0.92 0.01 h / 0.22), transparent 70%),
    var(--n-1);
}

/* Pool of light spilling from under a product frame. */
.light-pool { position: relative; isolation: isolate; }
.light-pool::before {
  content: ""; position: absolute; inset: auto -10% -18% -10%; height: 50%; z-index: -1;
  background: radial-gradient(ellipse 50% 60% at 50% 0%, oklch(0.80 0.03 h / 0.35), transparent 70%);
  filter: blur(24px);
  pointer-events: none;
}

/* Contact shadow under an object, cast away from a light above and to the left. */
.contact-shadow {
  background: radial-gradient(ellipse 50% 50% at 50% 50%, oklch(0.15 0.01 h / 0.5), transparent 70%);
  transform: translateX(6%) scaleY(0.18);
  filter: blur(8px);
}
```

A spotlight or pool reads only against a dark field. On a light page the same source shows on the object instead: highlights on the edges that face it, a gradient across its top face, and a shadow cast away from it onto the page.

Animating a blurred layer is expensive; move lit layers with `transform` and `opacity` only, or keep them still.

## Fidelity checklist

Run this on the rendered piece, at desktop and phone widths.

- [ ] A person who uses this kind of product would believe it: vocabulary, numbers, states and density are right.
- [ ] Three levels of detail are visible at once: the headline, the piece, and small detail that rewards a closer look.
- [ ] Every word inside the piece is real, crisp text or a clearly drawn shape, never a grey bar standing in for text.
- [ ] Light, if any, comes from one direction across the piece and the page.
- [ ] The phone layout shows a deliberate crop at readable size.
- [ ] The static frame looks finished without motion.
- [ ] A picture-like piece is out of the tab order with one accessible description; an operable piece has reachable, labelled controls.
- [ ] Swap test: with the wordmark replaced, the piece still says which product this is.
