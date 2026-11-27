# Rendering: visual intent, measurement and execution

## Before execution
Identify the pinned build and actual renderer (DOM/CSS, Canvas 2D or WebGL). Reuse the existing renderer and scheduler. Agree on the visual oracle with the design owner: player action, state, expected cue, when it appears, and information that must stay readable. Treat claims about attention as hypotheses until checked in scene. Use actual device-scale screenshots and real motion captures. For eggs compare idle, ready and unavailable; check that the ready cue remains legible with reduced motion and without color alone. Apply relevant WCAG 2.2 criteria, particularly 1.4.1, 1.4.3 and 2.3.1 when applicable. 2.3.3 is AAA. Test the resolved reduced-motion behavior for DOM and game-rendered cues.

## Measure and attribute
For the Shop measure input to first visible feedback and input to usable panel separately. Define usability in advance (e.g. rendered price and an operable purchase control for an eligible fixture). Keep first and repeat opens separate. Match physical device, browser, build, save, viewport, DPR, refresh rate, quality settings and cache state appropriate to each cohort. Log sample count, p50, p95, max and late/dropped frames using the available track. Preserve all raw attempts. Keep diagnostics separate from comparison timings; disable screencasting for timing. Treat INP's 200 ms good threshold as field guidance at p75, not a Shop-ready budget.

Link input, function and caller, trace event and first affected frame. Inspect main-thread JS, layout, paint/raster and compositor tracks. Record transfer bytes, decode, upload and texture lifetime separately. Use device-supported GPU evidence or report attribution unknown. For supported WebGL timer queries, poll asynchronously, discard disjoint results and scope measurements to the queried commands. Avoid synchronous readback during comparison. Estimate uncompressed RGBA8 base-level texture bytes as width × height × 4, document mip levels and other allocations separately, and label estimates. Inspect repeated transitions and resource teardown. Validate context-loss recovery only on the isolated test build when applicable. Evaluate atlasing or batching against measured costs and actual device limits; treat GameMaker export rules as port-specific.

## Execute a controlled Shop drill
Use a synthetic save and existing QA entry points. Record the unmodified baseline (A). Temporarily change only one egg-card effect (B), preserving prices, layout, eligibility and the readiness cue. Restore the original (R) and repeat the scenario under matched conditions according to PL-01. Keep diagnostic captures and comparable measurements separate. Record first and repeated opens for A/B/R, then check motion, readiness, visible focus and actual purchase on a disposable fixture after timing. If the expected difference does not reproduce after rollback, keep attribution open and state the next discriminating check. Capture matched frames or clips, exact source symbol and caller, original trace, metric endpoints, sample counts and limitations for internal D7 evidence verification. If Android or GPU evidence is unavailable, mark that check BLOCKED or NOT RUN with the reason.

## References
- https://www.w3.org/TR/WCAG22/
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://developer.chrome.com/docs/devtools/performance/reference
- https://web.dev/articles/inp
- https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices
- https://developer.mozilla.org/en-US/docs/Web/API/EXT_disjoint_timer_query
