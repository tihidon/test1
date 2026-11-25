# SC-DEBUG-01 — pouzdano debugovanje, faza A

Kandidat; baseline cd79662b45b2477d2d53aba000e60f90fefc8662. Dodatak SC-DEC-01, SC-REL-01, SC-CODE-01/02, SC-QA-02, SC-LOOP-01, PL-01 i PW-01. Bez promene igre/builda/deploya. Jedan decision record i isti alati za oba specijalista. Paketi iz PR #35 ostaju istorijski snapshot; merodavne su žive instrukcije i kanonska dokumentacija.

1. Freeze identity, scope, independent oracle, minimal real UI reproducer, expected failure before edits. Record actual/expected state separately.
2. Form falsifiable hypotheses and alternatives. Seek last matching state and first divergent operation. Inspect full function, actual callers, async order, inputs/outputs and resource owner.
3. Prefer targeted conditional breakpoints, logpoints, pause on exception, async stacks in DevTools over production logging. Record source anchor/commit. Paused execution is not timing evidence.
4. Delta debugging reduces test input/events, not arbitrary code. Git bisect only with reproducible oracle and disposable checkout; untestable commits skipped, not good. Control clock/seed only in isolated relevant tests.
5. Minimal owner-level patch, same oracle FAIL-before/PASS-after, intended negative control, repetitions without retry masking. Stop after three failed hypotheses without new evidence/owner authorization.
6. Independent reviewer verifies originals; no self-approval or claims of actual agent evaluation from fixture PASS.

## Phase A tools
- ESLint 10.15.0: 13 selected bug rules, no inline suppression/autofix. Manifest executable blocks + SW. Git baseline and current source; compare multiset fingerprint of file/rule/message/trimmed line, even if total unchanged. Parser/config failures fail. Changed legacy lines require review. No no-undef/global resolution; not full recommended config. Fixed starting baseline and actual PR base. Direct dependency versions pinned in isolated npm; transitive lock pending.
- AST exact duplicate body/params/type, preserve identifier/literal/async semantics; excludes tiny and >100k-char functions, lists largest 30. No near-clone or semantic proof; no deletion.
- Separate watchdog --diagnostic run: CDP JS precise coverage counts and CSS rule usage deltas, page target only, startup, online remainder, optional assertion boundaries and offline reload; retains script/style locations and session-local IDs. No simultaneous CPU profile/trace; no comparison with performance timings. CSS non-observation not dead code; deltas are newly observed rules, not complete per-phase coverage. Offsets require source identity.
- Existing shell smoke retains original CPU/trace; not performance benchmark. New real browser fixture tests exact counts (3 then 2) and late CSS; negative control rejects empty/wrong origin observation. All five skills included in validation/to-prompt. No claim of gameplay or agent behavioral proof.

## Handoff
Stress specialist owns D2/D4/D6 and gives frozen scenario, first divergence, raw phase logs and negative controls. Architecture specialist owns D0/D1/D3/D5 and minimal owner-level fix/build/CI. Reliability D7/D8 independent review, owner if both participated. Same tools, no competing probes.

## Commands
From repository root with isolated CI dependencies installed:
- node --test tools/agent/test_debug_tools.cjs
- node tools/agent/eslint_ratchet.cjs FULL_BASE_SHA /tmp/sc-eslint.json
- node tools/agent/audit_duplicates.cjs /tmp/sc-duplicates.json
- python -m unittest discover -s tools/qa -p 'test_cdp_diagnostic.py' -v
- python tools/qa/runtime_watchdog.py --diagnostic --out /tmp/sc-diagnostic-new
- Use --scenario REVIEWED_JSON for real actions; empty scenario proves shell only.
- Preserve original artifacts in private CI; do not expose source/data from real accounts.

## Next phase (NOT RUN)
Real gameplay/save/cold reopen scenarios; actual RAF/timer/listener teardown, async interleaving, GPU/heap/texture identity, layout trace, phase-separated CPU, generated-to-src offset map, flake harness, near clones, lockfile and separately verified Node24 actions, agent behavioral eval. Physical HONOR proof remains separate.

## Sources checked 2026-11-26
ESLint https://eslint.org/blog/2026/11/eslint-v10.15.0-released/ ; https://eslint.org/docs/latest/integrate/nodejs-api ; https://eslint.org/docs/latest/rules/
CDP https://chromedevtools.github.io/devtools-protocol/tot/Profiler/ ; https://chromedevtools.github.io/devtools-protocol/tot/CSS/
DevTools https://developer.chrome.com/docs/devtools/javascript/breakpoints/ ; https://developer.chrome.com/docs/devtools/coverage/
Git https://git-scm.com/docs/git-bisect . Installed browser/rules and actual fixtures determine compatibility.
