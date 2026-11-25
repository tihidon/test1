---
name: snail-city-engineering
description: >-
  Implement, review, debug, profile, refactor and test Snail City HTML/CSS/JavaScript PWA changes. Enforce existing architecture, function registry, CSS/DOM, render lifecycle, save and offline integrity, safe Python builds, loop investigation and evidence-based QA. Activate for game changes, bug investigation, deletion, performance, releases and agent tooling.
metadata:
  version: "1.1.0"
  project: "Snail City"
  status: "owner-approved-candidate"
compatibility: "Project-local Codex skill; Python 3.11+, Node.js and optional isolated CLI/parser/browser tooling. No new game runtime dependencies."
---

# Snail City engineering

Read root AGENTS.md and docs/README.md, then only the relevant canonical standard below. Do not load the full function registry, HTML or asset data into the model. Locate repository root, target branch/commit, actual version, publish root, source/manifest and existing changes. A past PASS is not current proof. Code identifies observed behavior; owner decisions and adopted standards identify intended behavior. Record conflicts; never silently change intended behavior or invent evidence.

## Mandatory invariants

- Find by responsibility, symbol, aliases, callbacks and readers/writers before adding code. Extend existing owner. No parallel renderer, projection, terrain validation, clock, state, economy, storage, CSS or game loop. UI intent → app orchestration → domain validation → storage durability → presentation. Renderer does not mutate game state.
- One projection and support footprint for preview, hit-test, terrain validation, confirm and persistence. DPR once. Revalidate at commit; reject without debit/movement. No unauthorized balance, pricing, reward or snail-stat changes.
- One authoritative persisted game clock and absolute deadlines; bounded simulation steps independent of offline settlement. Test invalid time, duplicates, reentry and resume. Preserve save identity, revisions, backups, migration and recovery. No silent reset or clearing real storage; test isolated origin/profile.
- One existing scheduler; dirty idle map, bounded active simulation, cleanup timers/listeners/observers/textures, restore GPU resources after context loss. Do not remove needed invalidation/resize or artwork to make metrics green. Trace before optimizing.
- Use existing CSS owner/cascade, native controls, delegation, SR/EN localization, accessibility and safe context-specific output encoding. Apply SC-CODE-01 limits and ratchets; no automatic exceptions, extra style blocks or mass formatting. Function registry is an index, not a complete dynamic graph. Do not delete on zero incoming static calls; use all three deletion checks.
- Python standard-library build stays. Do not run split.py on active src; historical roundtrip isolated. Confirm src/template/manifest matches actual published root index.html before release; do not switch Netlify publish logic without approval. Preserve all six actual version points when version changes. Docs-only no runtime bump. No npm/bundler migration or added game dependencies without approval.
- No destructive operations, unrelated cleanup, merge/deploy or production changes without authorization. No fabricated PASS, screenshot, performance number or test coverage. Block release on required G0–G7 failures/missing evidence. Use actual Chromium frames for graphics/motion; device test for Android claim. Actual GML port requires separate approved standard; do not introduce GML into web.
- Detect loops via AST inventory, then actual reproduction and bounded runtime tracing; static warning is not a bug. Never automatically delete a loop or cap a legitimate simulation just to pass. Separate game RAF, timers, promises/microtasks, observers, recursive calls and agent retry loops. No retry without changed hypothesis/evidence; after 3 unsuccessful attempts stop and report unless owner authorizes new experiment.

## Routing (from repository root)

| Task | Canonical source |
|---|---|
| All edits, agent QA | docs/tehnika/standardi/SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md; SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md |
| Ownership, placement, state | docs/tehnika/standardi/SC-ARCH-01-STRUKTURA-I-ARHITEKTURA.md; PRAVILO-JEDAN-IZVOR-ISTINE.md |
| Function changes / deletion | docs/tehnika/standardi/SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md; SC-BRISANJE-3-PROVERE.md |
| CSS/DOM/JS | docs/tehnika/standardi/SC-CODE-01-CSS-DOM-FUNKCIJE.md |
| Rendering/latency | docs/tehnika/standardi/SC-REND-01-CIST-KOD-I-RENDER.md; SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md |
| Save/PWA | docs/tehnika/pwa-offline/PW-01-STANJE-0.8.92.md |
| Build | docs/tehnika/standardi/SC-BUILD-01-PYTHON-BUILD.md |
| Loops and bugs | docs/tehnika/standardi/SC-LOOP-01-LOOP-I-BUG-AUDIT.md |
| CLI setup, verification | docs/alati/SC-CLI-01-AGENT-INSTALACIJA.md |

## Execute

1. Specify acceptance criteria; inspect scope, baseline, rollback, owner/contract, dependency chain, all affected call sites and test coverage. Use current source, not obsolete line numbers. Preserve user changes.
2. For source changes run trusted checker `python tools/agent/check_build.py --require-publish-match` before and after; do not regenerate active source using split. If baseline fails report separately; do not hide it by rewriting root HTML or references. Run `node tools/agent/audit_loops.cjs` with existing isolated Acorn dependencies; record parsed counts and candidates, compare baseline and changed owner, investigate rather than treating counts as bugs. For documentation-only use relevant validation only.
3. Make minimal targeted patch in existing owner. Follow existing SC-F08 registry generator, ratchets and source-specific rules. If tool is unavailable or skips inputs mark BLOCKED. No false zero-file PASS.
4. Apply applicable G0–G7: syntax and determinism are not functional QA. Test positive, negative, repeat, cancellation, reload, lifecycle, offline, relevant visual and physical device cases; PL-01 A/B/R for performance claims. For suspected hang use externally bounded runner and record exact action, stack/trace, owner and progress criterion; compare unaffected features.
5. Record changed files/symbols, untouched systems, baseline/commit, commands/exit/output, artifacts, risks and rollback. Each deliverable URAĐENO / DELIMIČNO / NIJE URAĐENO; tests PASS / FAIL / BLOCKED / NOT RUN / N/A with reason. Decision PRIHVATI KANDIDAT / ZADRŽI ZA QA / ROLLBACK / NO-CHANGE. Do not accept release solely from CLI or fixture checks.
