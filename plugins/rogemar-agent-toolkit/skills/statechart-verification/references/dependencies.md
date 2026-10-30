# Statechart dependencies

Run the bundled CLI's help before selecting a command. Node runs parsing,
comparison and chart-to-TLA conversion without a model checker. These outputs
are not verification. Checking needs Java 11 or newer and TLC; rendering needs
Pele 1.8.0 and resvg-js 2.6.2. These are external dependencies, not bundled runtimes.

Prefer an existing trusted toolchain. Set `TLA2TOOLS` to the installed jar and,
when needed, `JAVA` to the executable. The mise fallback looks for the upstream
checksum-pinned TLC 1.7.4 and Temurin 25. A different explicitly supplied tool
version needs its own compatibility/result evidence. Inspect executable mapping
files before running them. A model or mapping from an external report is code.

An optional engine, [tla-ts](https://github.com/aidenybai/tla-ts) (MIT, pinned
`tla-ts@0.0.3`), checks models without Java. Select it with `STATECHART_ENGINE=tla-ts`
and set `TLA_TS` to a reviewed local executable; with installation authorized, the
same opt-in below lets `npx` fetch the pinned package. TLC remains the default:
tla-ts does not take TLC's `-continue` flag, so a run may stop at the first
violation, and its results are labelled unverified until a trial on this skill's
test corpus matches TLC's.

Automatic installation is disabled. Only after installation is already authorized,
the preparation owner may set `TOOLKIT_STATECHART_ALLOW_INSTALL=1` for the specific
preparation command. That permits upstream mise/npm preparation and network use;
the environment variable itself does not confer authority. Do not persist it in
user/global configuration. Run subsequent verification without that opt-in so
missing dependencies remain visible. No tool is installed merely by selecting a
skill or asking for a diagram.

Renderer packages use a versioned cache under `XDG_CACHE_HOME/statechart`, falling
back to the platform home cache. Cache location does not establish trust. Inspect
and preserve existing data before repairing a cache; do not blindly delete it.
Node scripts and the compiler use caller-selected scratch inputs and write beside
them. Copy accepted artifacts into the authorized project verification location.

Record dependency versions, command, candidate, result, output paths and missing
steps separately. An unrendered Mermaid file can still be delivered as partial
visual evidence. Missing TLC cannot be replaced by saying the chart looks correct.
