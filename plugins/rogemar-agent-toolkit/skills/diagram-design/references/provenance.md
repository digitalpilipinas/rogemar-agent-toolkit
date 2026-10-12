# Provenance and adaptations

Source: https://github.com/cathrynlavery/diagram-design
Revision: `7a2e22170ee838e859d8142ba825d83f8b6375e6`, plugin 2.6.74, MIT.
The upstream file hashes are recorded in `catalog/imported-sources.json` in the
toolkit repository; installed copies retain the notices in `upstream-notices/`.

Local adaptations: focused entry and conditional routing; project-only branding
with read-only resolution; no routine approval pauses; system-font generation and
SVG export defaults; one selected variant; destination-driven exports. Upstream
extractors, self-check and SVG transformation remain unchanged. Original example
HTML retains upstream styling and may reference web fonts; treat it as source
material, strip external font references for offline output, and do not mistake
examples for regenerated output. Maintainer-only geometry and chart verifiers
are not packaged. Packaged self-checks do not prove rendering or source fidelity.

The SVG exporter rejects some upstream examples (nested SVG or invalid XML
comments). Report the failure and repair only the requested artifact or use a
verified browser PNG route; never claim universal conversion or bypass the gate.
The icon set has separate notices and trademarks. Use only marks needed for the
artifact; omit an icon when its redistribution rights cannot be established.
Toolkit integration is an independent adaptation, not an upstream endorsement.

Vendored text is normalized to LF with trailing whitespace removed for the
toolkit repository. Original upstream byte hashes remain in the import record.
