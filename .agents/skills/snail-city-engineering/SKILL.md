---
name: snail-city-engineering
description: >-
  Implement, review, debug, profile, refactor and test Snail City HTML/CSS/JavaScript PWA changes. Enforce existing architecture, function registry, CSS/DOM rules, WebGL lifecycle, save integrity, offline behavior, deterministic Python builds, loop investigation and evidence-based QA. Activate for game code, bugs, deletion, optimization, map placement, race/battle, releases and agent tooling.
metadata:
  version: "1.2.0"
  project: "Snail City"
  status: "owner-approved-candidate"
compatibility: "Compatible Agent Skills host with repository access; Python 3.11+, Node.js and isolated developer CLI/parser/browser tools for applicable checks. No additional game runtime dependencies."
---

# Snail City engineering

## Authority
Read target AGENTS.md and docs/README.md, then relevant canonical standards. Confirm target checkout, SHA, version, deployment root, source authority and user changes. Repository-approved standards and owner decisions define intended behavior; actual code defines observed behavior. Bundled copies are dated references, not a competing policy. Report contradictions; preserve protective invariants; do not make unauthorized changes. If target documents or tools are unavailable, use available evidence and mark verification BLOCKED. Never dump entire registry or embedded assets into context.

## Mandatory rules
1. Find existing owner by symbol and responsibility before adding code. Inspect full affected bodies, callers, aliases, dynamic dispatch, reads/writes, dependencies and tests. No duplicate renderer, projection, state, economy, pricing, clock, terrain, save adapter, styles or game loop.
2. UI emits intent; app orchestrates; domain validates/settles; storage confirms durability; renderer paints. No gameplay writes in paint. Preserve public contracts and approved balance. Invalid/duplicate actions cannot debit, reward or move objects. Shared ground footprint, terrain, projection and placement validation for preview/hit-test/confirm/persistence; apply DPR once.
3. Persist canonical effective game clock and absolute deadlines. Separate simulation/frame timing and profiling from offline settlement. Bound catch-up, test clock changes, pause/resume and duplicate events. Preserve save identity, revisions, backup, migration and recovery; never silently reset or clear real storage. Isolated test profiles, no secrets or real player data in logs.
4. Existing scheduler/renderer only. Dirty idle map, bounded active simulation, no unnecessary layout reads, texture upload or cache churn. Clean timers/listeners/observers/RAF/textures and restore GPU resources after context loss. Never remove needed invalidation/resize, graphics or controls for better metrics.
5. Existing CSS owner and cascade, scoped DOM updates, native controls, delegated actions, SR/EN localization, focus and accessibility. Apply approved SC-CODE-01 C/D/J and ratchet constraints; no new duplicate selectors/logic, style system, mass format or patch-on-patch. Validate output by context; generic HTML escaping does not secure URL/JS/CSS.
6. Python standard-library build stays. Once migration verified, src/ is development authority; reference HTML frozen. Never run split.py on active edited src/. In test1 current Netlify layout, prove generated dist/index.html equals published root index.html. Don't silently overwrite mismatch or change deployment. Maintain all six actual version points for runtime changes; docs-only no runtime/SW bump. Never invent version.json.
7. Detect loops with AST and bounded real runtime tracing. Static warnings are candidates, not proven bugs. Review exit/progress, reentry, recursion, RAF/timers, microtask starvation, observers, render/layout cycles, save/retry and cleanup. No deleting valid loops to improve metrics. After three failed attempts at one hypothesis stop or get owner authorization; retry only with new evidence.
8. Preserve user edits. No destructive actions, unapproved feature deletion, balance changes, architecture migration, merge/deploy or production operations. No fabricated PASS, screenshot, simulated motion or current claim from historical evidence. GML only for actual explicitly identified port.

## Load only relevant references
| Task | Read |
|---|---|
| Any runtime edit/deletion | [workflow](references/workflow.md) |
| Ownership, map, state | [architecture](references/architecture.md) |
| CSS, DOM, JS | [coding](references/coding.md) |
| Render/latency/loops | [render-performance](references/render-performance.md), [SC-LOOP-01](references/standards/standardi/SC-LOOP-01-LOOP-I-BUG-AUDIT.md) |
| Save/PWA/release | [qa-release](references/qa-release.md) |
| Build/CLI | [SC-BUILD-01](references/standards/standardi/SC-BUILD-01-PYTHON-BUILD.md), [cli](references/cli.md) |
| Registry | [sources](references/sources.md); search current source first |
| Conflicts | [audit](references/audit.md) |

## Execution
1. Identify deliverables, acceptance, target SHA/hash, current versions/source/publish identity, local changes, risk, rollback, access/tools and scope. Docs-only work does not require fake runtime QA.
2. Search actual owner, contract and call chain including SR/EN, generated DOM/actions and dynamic keys. Record function card: owner/symbol, file+SHA/anchor, contract/units/errors, callers/dependencies, reads/writes, lifecycle and tests. Extract full relevant bodies with local tools; avoid dumping base64 or all HTML.
3. Run applicable G0–G7 and existing static/ratchet tools. For compatible trusted checkout use bundled scripts only as fallback, with explicit target path (see cli.md). Verify parser coverage; missing tools, skips and zero input not PASS. Baseline failures stay separate. Deletion needs all three independent checks; if dynamic use unresolved, NO-CHANGE.
4. Minimal targeted patch, unique anchors, preserve unrelated bytes/assets, encoding, cascade and user edits. Update existing change record and canonical function index via SC-F08.
5. Actual positive/negative/repeated/reload/lifecycle tests; real Chromium before/after screenshots and actual frame GIF/video (Pogledaj kretanje) for graphics/motion. PL-01 A/B/R for performance, 20–30 repeats when required, matched actual target device for Android. For hangs, external watchdog and trace; timeout alone doesn't identify culprit. No runtime watchdog installed by this skill.
6. Report changed files/symbols, unchanged systems, actual commands/exits/coverage, artifacts, risks and rollback. Per deliverable URAĐENO / DELIMIČNO / NIJE URAĐENO; per test PASS / FAIL / BLOCKED / NOT RUN / N/A with reason. Decision PRIHVATI KANDIDAT / ZADRŽI ZA QA / ROLLBACK / NO-CHANGE. No release with required P0/P1 failures or missing evidence.

Scope-aware reading never waives applicable gates. CLI format validation is not agent or runtime proof. See VALIDATION.md.

## Shared decision chain (SC-DEC-01)
Read docs/tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md. Own D0/D1/D3/D5; hand off actual runtime reproduction and regression to Chromium Runtime QA, independent review to Agent Reliability. Freeze oracle and required gates before editing. Do not treat a hypothesis as proof or implement a speculative patch. Scope-specific G0–G7 remain mandatory. Record one shared decision record; no parallel policy.
