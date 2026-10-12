# Toolkit showcase

Original, static HTML/CSS/SVG with small progressive-enhancement controls. Open
`index.html` directly or serve this directory with any static HTTP server.
Without JavaScript all three diagrams remain visible. The method illustration
never starts agents, authenticates services or installs anything.

Regenerate the SVG/HTML and inline figure regions:

```sh
python3 scripts/build_showcase.py
```

Run browser acceptance checks with an existing Node Playwright installation and
its Chromium browser. `SHOWCASE_CHROME` may point to an already installed Chrome;
`NODE_PATH` may identify the host's existing Node package directory. No tool is
installed by the check. From the toolkit root:

```sh
node scripts/check_showcase.cjs /path/to/evidence
```

Set `SHOWCASE_URL` to the published gallery for hosted verification. The check
rejects requests to other origins, exercises desktop/mobile themes, keyboard
step controls, pause/reset, reduced motion and no-JavaScript behavior, and captures
PNGs/animation frames. This does not establish a physical screen-reader session.
Pillow is needed only for `scripts/build_showcase_demo.py` when rebuilding the GIF.

`FIDELITY.md` records the installation redraw's source relationships. SVG content
and the surrounding prose explain ownership, conditional delegation and evidence
boundaries. Node layout follows the toolkit's adapted Diagram Design methods;
no diagram represents observed cloud installation or live execution.

GitHub Pages publishes only this directory, not the repository or skill tree.
