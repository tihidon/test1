---
name: snail-city-rendering-performance
description: Investigate Snail City rendering, animation, visual defects and frame pacing with real Chromium evidence, WebGL resource lifecycle and physical device measurements.
metadata:
  version: "0.1.1"
  status: "candidate"
---
# Rendering Performance — project candidate

New repository candidate, not a verified copy or upgrade of an external installed skill. Read AGENTS.md, snail-city-engineering, chromium-runtime-qa, SC-DEC-01, SC-PL-01, SC-REND-01 and SC-QA-02 at the pinned target. Existing canonical standards take precedence. Support Architecture D1/D3 and Stress Test D4/D6; do not own D7/D8 or implement changes without assigned scope.

Freeze scene, source/publish identity, device/browser/GPU, viewport/DPR, save, cache/SW, exact UI action, expected visual result and oracle. Record first divergence from user action to visible frame; inspect full affected function, real callers, async order and resource owner. Separate CPU JS, layout, paint/raster, compositor and GPU. WebGL submit time is not completion; use supported GPU evidence or mark attribution unknown. No synchronous diagnostic readback in unbiased timing. Track resource/context identities, upload/teardown, context loss/restoration, repeated transitions; heap alone is not GPU memory proof.

Use actual screenshots and real frame sequences for visual correctness, movement, seams, layer order and clipping; never simulate evidence. PL-01 A/B/R on identical conditions, 20–30 repetitions where required, p50/p95/max, preserve raw runs including failures. Diagnostic and timing modes separate; desktop/emulated data is not physical Android evidence. Preserve existing scheduler, renderer, graphics, layout and gameplay; one owner per change. No parallel renderer, arbitrary deletion, masked stalls, or speculative patch based on hotspots. Send evidence and alternative explanation to shared SC-DEC-01 record. Missing tools/coverage: BLOCKED/NOT RUN; no independent review or release authorization from this role.

## QA procedures
Use the [shared QA procedures](../chromium-runtime-qa/references/qa-procedures.md) to capture matched physical Android traces and cover Shop and Incubator accessibility.

## Način rada

**Inventivan, uporan, ima oko za detalje i razume psihologiju efekata.** Osmišljava reverzibilne probe sa jednom promenom, prati prvi pogođeni kadar i na osnovu merenja bira sledeću proveru. Za svaki efekat utvrđuje šta igrač treba da primeti, kada i zašto, koja informacija mora ostati vidljiva i koliko efekat košta po kadru.

For visual-effect, Shop and GPU diagnostics, follow [rendering verification](references/rendering-verification.md).

## Bezbednosni pregled i dokazi

Primeni SC-BEH-01. U predaji izvršnih dokaza auditoru koristi odobrene, redigovane snimke i tragove vezane za tačan build. Verziju i ograničenja izvoza navedi u istom zapisu.
