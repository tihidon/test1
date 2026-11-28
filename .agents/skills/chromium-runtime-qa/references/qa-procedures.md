# Snail City QA procedures

**Vizuelna konvencija (pilot):** sivi citat sa oznakom ODOBRENO — AKTUELNO označava potvrđen postojeći sadržaj. NOVO — ZA PROVERU ostaje standardnom bojom i ne predstavlja ovlašćenje. Neoznačeni postojeći pasusi zadržavaju prethodni status do pojedinačne provere; boja nije dokaz usvajanja.

## Browser automation and evidence
Start with the existing runtime watchdog and approved functional scenarios in test1. Capture a Playwright trace on failure through the runner's supported API. With Playwright Test use `retain-on-failure`; for direct browser contexts start tracing before navigation and stop in cleanup before closing the context. Preserve the original failed attempt even when a retry passes. Attach the trace, assertions, console and relevant request failures to the existing GitHub job. Record repository, exact commit, origin, build, browser and fixture. Restrict artifact access and use synthetic data because traces can retain DOM and network contents. Open the trace with Trace Viewer to find the first failed assertion. Use Chrome DevTools for CPU, layout and rendering attribution. Use Playwright MCP when interactive DOM snapshots or action history help reproduce a problem. Check host capabilities before relying on MCP. Convert recurring failures to repeatable assertions.

## Same-origin PWA upgrade with an existing save
Engineering freezes the predecessor and candidate identities, supported save/schema versions, fixture and expected values before execution. Use an isolated persistent profile and the same authorized HTTPS test origin for both builds. Create and commit progress through the predecessor UI where practical. Record the baseline values and service-worker controller. Publish the candidate to that test origin and drive the documented update lifecycle. Verify the candidate controls the page and the migrated values match the oracle. Change progress through the UI and wait for the storage transaction to commit. Close the installed app, cut actual network transport, cold-relaunch it and verify the new progress plus actual decoding/rendering of representative map and Shop assets. Capture build/controller/cache identity, UI and IndexedDB assertions, network isolation evidence and device details. Preserve fixture provenance and distinguish automated browser evidence from physical installed-app evidence. Exercise the affected migration and lifecycle checks on the exact merged commit before release closure.

## Android and startup budgets
For mobile jank use Chrome Remote Debugging on physical Android. Match device, browser, build, save and interaction. Capture first and repeat Shop opens. Disable screencasting for timing runs and record diagnostic and comparison runs separately. Escalate to Perfetto only when browser traces leave a scheduling, compositor or GPU question open. Verify the required tracks exist before making a causal claim. Use Lighthouse CI for navigation and resource budgets after establishing a repeatable baseline under a pinned environment. Begin with reported warnings and agree on thresholds before enabling blocking assertions.

## Shop and Incubator accessibility
Exercise keyboard focus order, visible focus and focus return, accessible names and roles, physical touch targets, reduced motion, and access to essential canvas interactions where applicable. Use axe-core as a supplement for DOM checks. Preserve affected control, state, observed result and evidence. Record physical touch and assistive technology coverage separately.

## Internal evidence review
> **ODOBRENO — AKTUELNO** · [SC-DEC-01](../../../../docs/tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md), [SC-REL-01](../../../../docs/tehnika/standardi/SC-REL-01-AGENT-RELIABILITY.md), [SC-PMV-01](../../../../docs/tehnika/standardi/SC-PMV-01-POST-MERGE-VERIFICATION-STANDARD.md)
>
> Engineering owns the oracle. Chromium QA records the actual steps, assertions and original artifacts. Reliability verifies the exact commit, CI attempts, build/origin and raw evidence against the oracle. Coordinator records coverage gaps and applies the existing PMV process. Record the actual executor and evidence coverage. Keep D7 open where required evidence is missing or materially disputed. The owner decides D8. An untested gate stays explicit.

## References

- [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer)
- [Playwright MCP tracing](https://playwright.dev/mcp/tools/tracing)
- [Chrome Remote Debugging](https://developer.chrome.com/docs/devtools/remote-debugging/)
- [Perfetto Chrome tracing](https://perfetto.dev/docs/getting-started/chrome-tracing)
- [Lighthouse CI configuration](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md)
