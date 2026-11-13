# App screens

A dashboard, console, queue or admin screen is the product at work, not a page about it. People keep it open for hours and return to it for one reason: to find what needs doing and do it. Generated screens of this kind fail in four ways that a marketing page never shows: the things people came to watch appear only as counts, a column of identical buttons names nothing, labels print over the marks they name, and the screen sits still although the operation behind it never does.

## What the brief lines mean here

The brief in SKILL.md still applies, read as follows.

- **Primary job**: the working loop. See what needs attention, act on it, see that it is done. List every thing the request says people need to watch (stock below its reorder point, tickets past their deadline, beds free on each ward): that list is the screen's content, and each entry gets its own panel or tab.
- **Signature**: the working view the operation runs on (the floor plan, the route map, the board), drawn from the subject's own geography or layout and made to the standard `artefacts.md` sets for a hero piece. It is not a picture placed above the work, and the screen has no marketing headline.
- **Claim, proof, action** becomes **attention, item, action**: what needs doing now, the specific items, and the action beside each.
- **Copy**: the action names its object (below), and status words come from the trade, not from the template ("Breached SLA", "Awaiting pharmacy", not "Warning", "Pending").
- **Motion**: the operation changing state (below). A page-load entrance adds nothing to a screen opened once a shift.

## List what was asked for

Everything people are asked to watch is shown as the items themselves: which ones, where, since when, and the action beside each. A count heads the list; it never replaces it. "6 tickets past deadline" says there is a problem; "#4471, Harlow branch, 3 h over, Assign to Priya" lets someone fix it.

- When space is short, show the worst few, say how many there are in all ("3 of 11, longest waiting first"), and link to the rest.
- Each list has one job. Two panels that list the same items (a jobs queue and a table of the places those jobs serve) are one list; merge them and spend the space on something the request asked for.
- Order by what needs acting on first, not by identifier or name.

Check: write down every noun in the request that people need to see, then find each one on the first or second screen as named items. A noun found only as a number is missing.

## The action names its object

When an action repeats down a list, each button says what it acts on or with: "Assign to Priya", "Move to Ward 7B", "Refund £48.20". A column of identical "Assign" buttons makes the reader parse each row to learn what its button does, and offers nothing to choose between.

- Pre-select the best choice (the nearest free crew, the agent with the shortest queue) and put a control to change it beside the button, so the default is visible and one click confirms it.
- The confirmation repeats the object: "Ticket #4471 assigned to Priya", in the same words as the button, as SKILL.md's one-name rule requires.
- The primary action keeps the strongest weight on the screen, but only the first item's button is filled; the rest are outlined or quieter, so the eye lands on the next thing to do.

These values show the form only: take every name, identifier and figure from the subject.

## Labels never sit on marks

A label printed over a dot or a line reads as broken ("Harl●w") in every screenshot and at every size. On maps and charts with many marks:

- Label only what people need to find: the selected item, the exceptions and a few landmarks for orientation. The list carries every name; hovering or focusing a mark shows its own.
- Place each label beside its mark, clear of it by the mark's radius plus 4 px, on the side with room. Draw a short leader line when it has to move further.
- Area names (districts, zones, aisles) sit in empty space, in a quieter style than mark labels, and give way to them.
- Give text a halo in the background colour so a line passing behind it does not cut it: `paint-order: stroke; stroke: var(--surface); stroke-width: 3px;` on SVG text.
- Check collisions in code, not by eye, and look at the result at both widths. A map that is redrawn for a phone gets fewer labels, not smaller ones.

```js
// Marks and labels share the SVG's viewBox coordinates. `labels` holds { text, x, y, r } for each
// labelled mark, highest priority first; each label tries four sides and is hidden if no side is
// clear of other marks and labels and inside the map.
const GAP = 4;
const SIDES = [
  { dx: 1, dy: 0, anchor: "start", baseline: "middle" },
  { dx: -1, dy: 0, anchor: "end", baseline: "middle" },
  { dx: 0, dy: -1, anchor: "middle", baseline: "auto" },
  { dx: 0, dy: 1, anchor: "middle", baseline: "hanging" },
];
const overlaps = (a, b) =>
  a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + b.height && b.y < a.y + a.height;
const view = svg.viewBox.baseVal;
const inside = (box) =>
  box.x >= view.x && box.y >= view.y &&
  box.x + box.width <= view.x + view.width && box.y + box.height <= view.y + view.height;

function place(text, x, y, r, side) {
  text.setAttribute("x", x + side.dx * (r + GAP));
  text.setAttribute("y", y + side.dy * (r + GAP));
  text.setAttribute("text-anchor", side.anchor);
  text.setAttribute("dominant-baseline", side.baseline);
  return text.getBBox();
}

const taken = [...svg.querySelectorAll(".mark")].map((mark) => mark.getBBox());
for (const { text, x, y, r } of labels) {
  text.style.display = "";
  const side = SIDES.find((s) => {
    const box = place(text, x, y, r, s);
    return inside(box) && !taken.some((other) => overlaps(box, other));
  });
  if (side === undefined) text.style.display = "none";
  else taken.push(text.getBBox());
}
```

## Show the state changing

An operations screen is live, and its motion is the operation: a vehicle moves along its route, a new report joins the queue, a job travels from the queue to whoever took it, a count ticks down. With no backend, play the sample data on a timer so the screen shows its first change within a second of loading and proves the loop.

- One change every few seconds, never several at once, so each can be followed.
- Each change follows the product tier in `interaction.md`: an item that changes place travels there (Shared-element motion), a new row enters where it belongs, a figure updates in place with tabular numbers, and a tint layer marks what changed and fades out over 1 to 2 s by opacity.
- Nothing moves under the pointer or the focus. New rows enter below the one being read, and a list holds still while it is hovered or focused, applying the changes when attention leaves.
- A visible "Pause live updates" control (WCAG 2.2.2). Under reduced motion the changes still apply, without the travel.
- Acting on an item is the screen's signature moment: the confirmed job leaves the queue for its new owner, and the place it served changes state.

## Check before calling it done

- [ ] Every thing the request asks people to watch appears as named items, not only a count.
- [ ] No two panels list the same items.
- [ ] Every repeated action names its object, and its confirmation uses the same words.
- [ ] No label overlaps a mark or another label at 1440 px or 375 px.
- [ ] The screen changes on its own within its first second, one change at a time, with a pause control.
