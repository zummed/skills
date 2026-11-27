---
name: animated-deck
description: Plan and build an animated presentation as one offline HTML file (SVG stage, keyed slides, autoplay animations, speaker notes). Use when the user asks for an animated, single-file, offline or HTML slide deck, or wants to plan, reorder or rework slides of such a deck. Not for Google Slides or PowerPoint files (use pptx).
---

# Animated single-file deck

A deck is one HTML file. A 1920x1080 SVG stage holds every slide. Each slide is a pure function of time. One key press moves to the next slide. The animation of each slide plays by itself.

Bundled in `assets/` (copy it to `<project>/deck/`):

* `src/deck.html`: engine, shared helpers, four sample slides (Welcome, two content slides, Thank you).
* `src/inter.woff2`: Inter, Latin subset, inlined at build.
* `build.py`: inlines the font and `icons/*.svg` into one offline file; fails on any unfilled `%%NAME%%` placeholder.
* `deckshot.sh`: headless screenshots of frozen frames.
* `icons/`: brand logos as raw SVG files.

## Process

1. Find the audience, the goal, and the one message the audience must keep. Ask if not clear.
2. Write the plan file (`docs/slides.md`) before any code. Get the user's agreement on it.
3. Copy `assets/` into the project. Build once to prove the template works.
4. Build two or three slides per round, in plan order.
5. After each round, take screenshots of the final frame and one mid-animation frame of each new slide. Look at them before you report.
6. Show the user. Write each piece of feedback into the plan as a rule or a slide change, with "(user, YYYY-MM-DD)".
7. After the first full build, review the length of each section and trim.
8. Keep a short log of each round in the project notes file (`AGENT.md` or equal): what changed, and why.

Delegate code edits to a cheaper model only if the user agrees. Visual design work often needs the stronger model. Ask once per deck.

## Plan file

Keep the plan as the single source of truth. Update it before you change the deck, not after.

```markdown
# Slide plan: <topic> for <audience>

## Deck rules

* Light theme; line icons in one consistent drawing style.
* One offline HTML file.
* One key press per slide; each slide's animation plays automatically.
* A key press during an animation moves to the next slide.
* `N` toggles speaker notes; the notes panel can open in its own window.
* Plain wording; no slogans.
* The final state of each slide shows everything needed to understand it.
* <project-specific rules from the user, each dated>

## Slides

1. Welcome: <what appears, in order, and the final frame>.
2. <Title> (section <NAME>): <elements; what animates; final frame; why this slide is here>.

## Open points

* <questions to the user, trims to consider>
```

* Write each slide entry as a told sequence: what appears first, what follows, what stays at the end.
* Record the user's words when they reject a design ("user: not 'Stuck', which read as broken").
* Record decisions on what is left out ("no footnote", "no cost figures", "in the notes only").
* Keep rejected choices as a short note in the entry, so they do not come back.

## Ordering

* Open with a short welcome, then the problem and the context in the audience's terms.
* Show the demo or the result early. Follow it with one hard comparison (for example real timeline against demo timeline).
* Explain a concept before its detail. Say what a thing is before you show its parts, code or syntax.
* Do not open with code or config. Move code later than you first think.
* Keep slides that build on each other next to each other. Do not put an unrelated slide between two halves of one idea.
* Group a long middle part into sections. Show a small section label beside the title rule (for example MACHINES, AGENTS, SAFETY, RUNNING IT).
* Reintroduce a second subject with its own title slide (mark and name only) before its section starts.
* Put the closing thought (the "why this approach" or the answer to the expected hard question) just before Thank you. It must read without a speaker.
* If a question comes up on an earlier slide, let its notes defer the question to the closing slide.
* Put costs, scale and operations near the end, after the audience knows what the thing does.
* End with Thank you.

## Content and wording

* One message per slide. The title states it as a plain sentence ("A machine is a file that runs jobs").
* Plain words. No slogans, no marketing taglines, no phrases that sound AI-written.
* Use the product's own terms. Do not invent a term the product does not use.
* Keep diagrams sparse. No filler detail, no decoration that carries no meaning.
* Not too minimal: a slide with only a few nodes and no story fails. Tell a short sequence with one changing caption if needed.
* Use real examples from the project (real file names, real syntax, simplified) over abstract boxes.
* Mark measured values and estimates differently. Draw only measured values to scale; show placeholders as dashed and say "not to scale" in the notes.
* Give exact figures where you have them ("147,822 tokens, £0.131 estimate"); state the source of each figure in the notes.
* Show a safe or expected alternative path in amber, not red. Red means a fault.
* Speaker notes: short bullet fragments the speaker can say aloud. Put detail and expected-question answers in the notes, not on the slide.
* State what is real and what is simulated, if the deck shows recorded or reconstructed demos.

## Visual style

Default palette (confirm the accent with the user for each deck):

```js
const STYLE = {
  ink: "#1D2331", ink2: "#5A6272", muted: "#A3ABB9", hair: "#E2E4E9",
  accent: "#4C56D8", accentSoft: "#DADDFB", paper: "#FFFFFF",
  icon: { stroke: 3, radius: 8 },
  card: { radius: 24, border: "#E3E5EA" },
};
```

* Background: warm off-white `#F6F5F1`, a faint dot grid, a soft central white glow.
* Text: navy ink, Inter (embedded). Titles 62px, weight 700, left at x=140 under a short accent rule.
* Cards: white, radius 24, 1.5px light border, soft stacked shadow.
* Icons: one line style only (3px round strokes, round joins). Do not mix icon sets.
* Brand logos: official current marks from the owner or Wikimedia Commons, as raw SVG in `icons/`. Note the source and licence in an HTML comment.

```html
<symbol id="logo-slack" viewBox="%%VB_slack%%">%%SVG_slack%%</symbol>  <!-- in <defs>, one per icons/slack.svg -->
```

```js
logo(s.world, "slack", 330, 400, 96, "#4A154B");  // centred at x, y
```
* No node or vertex decorations on letters or logos. A letter is a clean letter.
* Welcome: one plain box per letter, joined by simple lines; each box folds away and its letter grows in its place. No letter stays framed.
* Thank you: letters rise into place, with a short accent rule under them. No boxes.
* Code: monospace through the inline `MONO_CSS` style; light highlight on the line that is active.

## Animation rules

* The final frame holds the whole message. Nothing that matters appears and then vanishes.
* Results, ticks and crosses stay on screen at the end.
* One key press per slide. No click-to-reveal steps.
* A key press during an animation skips to the next slide.
* Keep total animation per slide short (about 3 to 8 s). Stagger items by 0.05 to 0.4 s.
* Use transitions with meaning: `push` for the next step, `zoomIn` to go into a part of the previous slide (`zoomFrom` set to that part), `zoomOut` to step back to the wider view.
* Before a `zoomIn`, use `lead` and `leave(u)` on the previous slide to dim everything but the target, so the audience sees where the zoom goes.
* The old title fades before the zoom moves; the new title arrives after the zoom.

## Engine contract

```js
defineSlide({
  title: "A machine is a file that runs jobs", // notes header and slide list
  section: "Machines",       // optional label beside the title rule
  duration: 6.5,             // seconds until the final frame
  enter: "push",             // or "zoomIn" | "zoomOut"; omit for a cut
  zoomFrom: { x: 1420, y: 760 }, // zoomIn target, in previous slide's world coordinates
  zoomTime: 1.4,             // optional zoom length
  lead: 0.7,                 // optional time before this slide's timeline, for the previous slide's leave()
  notes: ["Short spoken line.", "Second line."],
  build(s) { buildTitle(s, this.title); /* create all nodes once in s.world / s.hud */ },
  render(t) {                // pure: same t gives the same frame
    renderTitle(this, t, 0);
    return { cx: 960, cy: 540, s: 1 }; // camera
  },
  leave(u) {},               // optional: runs when the next slide zooms (not on push); u goes 0..1 over its lead
});
```

* `build` creates every node once. `render(t)` only sets attributes. It must not create nodes or keep state between calls.
* Use `seg(t, start, dur, ease)` for each motion and `rise(node, p)` for fade-and-rise.
* Never refer to another slide by index (`slides[3]`). Slides get reordered often. Use `this` or the `s` given to `build`. Share drawing through helper functions (for example `buildMark` / `renderMark`).
* Slides are built after `document.fonts.ready`, so text metrics come from the embedded font.
* URL `?slide=N&t=S` freezes slide N at S seconds. `&notes` opens the notes panel. Use these for screenshots and review.
* Keys: Right, Space, Enter, PageDown, click go forward; Left, Backspace, PageUp go back (to the final frame); Home restarts; `N` toggles notes.
* The notes panel has "Open in new window": the deck writes the window itself (works from `file://`), updates it on each slide, and takes its keys.

## Gotchas

* No SVG blur filters. Every camera move repaints them and the deck stutters at 4K. Use stacked faint rects (`buildShadow` / `setShadow`) and canvas bitmaps for text shadows (`buildWordShadow`).
* The frame loop skips the redraw when the slide time has not changed. Keep it: a slide at rest otherwise uses most of a CPU core.
* The stage stylesheet sets the font of every `text`. Code text needs the inline `MONO_CSS` style.
* `build.py` stops on any `%%NAME%%` left in the file. Each `icons/NAME.svg` fills `%%VB_NAME%%` and `%%SVG_NAME%%`.
* Check long words and titles at the final frame for overflow past 1920 px.
* Check the first frame of each slide during its transition for leftover tiles or flashes from the previous slide.
* The notes panel covers the bottom of the slide. Present with the notes in their own window.
* Snap Chromium cannot read `/data` or write `/tmp`. Serve the deck over HTTP and write screenshots under `~/snapshots/`.

## Verify

```bash
python3 deck/build.py                                   # prints size; fails on leftover placeholders
python3 -m http.server 8777 -d deck &                   # snap chromium needs http
deck/deckshot.sh http://127.0.0.1:8777/deck.html ~/snapshots deck 1:6 2:1.5 2:9 3:9notes
```

* Look at every screenshot before you report.
* Check the final frame against the plan entry: every listed element present, nothing overlaps, nothing cut off.
* Report the deck size and the slides changed.
