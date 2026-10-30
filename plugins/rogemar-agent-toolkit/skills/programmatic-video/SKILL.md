---
name: programmatic-video
description: Use when making a short video from code (HTML, Canvas, SVG, three.js, p5 or Remotion) rendered frame by frame, such as a product animation, explainer, launch clip or data story. Covers the brief, storyboard, a deterministic timeline, frame rendering, encoding and frame-level QA. Not for AI text-to-video models.
---

# Programmatic Video

A code-rendered video is software: one timeline drives every frame, so the same
input always renders the same film. Work in this order and keep each artifact.

1. **Brief.** Duration, aspect ratio, frame rate, audience, and whether there is
   audio. No paid API or model calls by default. Name every asset and its license
   before using it: fonts, music, voices, logos and footage need verified rights.
2. **Storyboard first.** List shots with start time, length, what moves and the
   transition into the next shot. Agree it before writing scene code.
3. **One deterministic timeline.** Build a page or composition with a pure
   `render(t)` (or the framework's equivalent): every visual is a function of time,
   with seeded randomness and no wall-clock reads, so any frame can be rendered
   alone. Choose the stack the project already uses; when a Remotion or other video
   plugin is installed and fits, use it rather than rebuilding its pipeline.
4. **Build shot by shot.** Render a still at each shot's key moments before moving
   on. Fix layout, type and contrast on stills; they are cheap.
5. **Render and encode.** Capture frames with a headless browser at the target
   size and frame rate, then encode with ffmpeg. Check that the browser and ffmpeg
   exist first; never install system software without authorization. Mix audio
   onto the same timeline and normalize loudness when there is sound.
6. **Frame-level QA.** Make a contact sheet (a grid of frames across the whole
   film) and a strip per transition. Check each shot against the storyboard, text
   on screen long enough to read, safe margins, reduced flicker, and audio sync and
   duration. A separate review pass against a written rubric catches what the
   author no longer sees.
7. **Deliver** the video with the storyboard, the timeline source, the render
   command and the asset license list, so anyone can re-render it.

Report what was rendered and inspected, and what was not, such as audio heard
only in a waveform or a frame range never viewed.

Method informed by the storyboard-first, contact-sheet workflow in
[JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase)
and the single-timeline render and mux technique in
[lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) (both MIT).
No code or prompts are copied from either.
