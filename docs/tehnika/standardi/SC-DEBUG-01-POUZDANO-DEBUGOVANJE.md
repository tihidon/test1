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
Remaining functional depth (race completion/reward, natural progression, direct reducer and concurrent command rejection, save recovery/cache upgrade); actual RAF/timer/listener teardown, async interleaving, GPU/heap/texture identity, layout trace, phase-separated CPU, generated-to-src offset map, flake harness, near clones, lockfile and separately verified Node24 actions, agent behavioral eval. Physical HONOR proof remains separate.

## Sources checked 2026-11-26
ESLint https://eslint.org/blog/2026/11/eslint-v10.15.0-released/ ; https://eslint.org/docs/latest/integrate/nodejs-api ; https://eslint.org/docs/latest/rules/
CDP https://chromedevtools.github.io/devtools-protocol/tot/Profiler/ ; https://chromedevtools.github.io/devtools-protocol/tot/CSS/
DevTools https://developer.chrome.com/docs/devtools/javascript/breakpoints/ ; https://developer.chrome.com/docs/devtools/coverage/
Git https://git-scm.com/docs/git-bisect . Installed browser/rules and actual fixtures determine compatibility.


## Phase B — functional contract and scope (candidate)
Reviewed against fcce2f365b64230b1ac4e554265d50329d8b559d, src/js/block-21.js Git blob 893ac8998acabcd0dde557f71de9cc90cba303c2 and current block-08.js/catalog. No production file changes. B uses the same local publish whitelist/origin and external watchdog as shell QA; separate persistent Chromium profiles, no diagnostic coverage or CPU profiling. Traces are evidence, not timing. Run `python tools/qa/runtime_watchdog.py --functional --timeout 300 --out /tmp/sc-functional-new`. Existing --scenario and --diagnostic modes retain their scope; cannot combine with --functional.

| ID | Independent expected behavior |
|---|---|
| B01 | Collection, progress, settings, incubator, shop and race gate through real UI. Level 1 race construction disabled. No durable inventory changes. |
| B02 | 20 shop open/close cycles from places; exact cycle count, same inventory; DOM snapshots first/last. No leak or FPS inference. |
| B03 | Profile name change via real settings UI; same saveId, higher committed revision, visible name. Not a level change. |
| B05 | Fresh level-1 profile has one egg and capacity two; one standard egg costs 100 sliz (block-08.js L12, block-21.js L384/L835–842). Exact debit, one new unique egg of kind 0, no other currency/level/snail changes. Disabled second purchase clicked natively, 300ms bounded negative observation; not direct reducer/concurrency proof. UI incubator count matches IDB. |
| B04 | Close persistent Chromium, reopen same profile/origin in new process/context with network offline; SW response matches HTML SHA and uncached fetch rejects; same save identity, revision nondecreasing, same wallet, level, eggs/snails and visible name/count. Not Android Force Stop or physical network test. |
| B06 | Separate fresh profile; actual UI import synthetic level 3 and built races fixture, then boot normalization. No natural level-up/construction claim. Start training, observe race progress >0, pause, abandon, same canvas, real first shop action after return. No finish/reward/latency claim. |

Source anchors: block-21.js L486–494 newGame; L835–842 buy-egg; L929–931 player-name; L1236 revision; L3310–3388 IndexedDB current/atomic commit; L3548–3554 locked building; L3765–3798 incubator; L3846–3903 shop; L3962–3984 race; L4300–4347 places/settings; L4459–4495 screen; L5096–5159 show/dismiss/open; L5246–5280 commit/replace; L5333–5410 start/return/pause; L5959–5987 controls; L6294–6299 file import; L6351–6437 boot. Actual template navigation controls confirmed. Historical docs are not current execution evidence.

Readonly IDB oracle opens existing database `snail-city-rebuild` version 1, store `snapshots`, key `current`; no fallback, abort unexpected upgrade. Wait for read transaction completion; only test synthetic data, hash save/egg/snail identifiers in summary. Compare stable inventory fields rather than requiring identical revision or timestamps because ordinary settlement can advance them. No runtime state injection. Fixture bytes SHA-256 retained; imported state is explicit setup, not test result. Failure/timeout stops run; unfinished cases NOT RUN/RUNNING (not PASS). Watchdog rejects missing case or zero assertions and missing trace/screenshot. CI requires all B01–B06 (execution order B01 B02 B03 B05 B04 B06) and existing gates. Contract tests exercise double debit, duplicate egg, wrong kind, lost commit, reset, wrong identity, inventory mutation and missing coverage. Real CI evidence pending; no behavioral evaluation claim.

### B04 QA infrastructure correction (26.11.2026)
Run 45725385724: B01/B02/B03/B05 passed (9/22/3/4 recorded checks); B04 failed at uncached network probe, B06 NOT RUN. The failure does not establish a production SW or storage defect. The old probe used a nonexistent URL and checked rejection under browser offline emulation; an HTTP response (including 404) resolves fetch. Actual response status and reason for emulation behavior were not retained, so no causal claim about Playwright routing. The revised test checks a known reachable non-core query variant of index.html (no-store) for HTTP 200 online, closes the real localhost listener before reopening the same persistent profile, verifies TCP connection refusal before and after navigation, requires the same probe to reject, then checks unchanged original save/identity/UI assertions and restarts the same origin for B06. Browser offline emulation remains enabled. This is a stronger independent transport cut, not a weakened oracle or a physical Android/network test. Single server owner shared with existing smoke; two stdlib regression tests verify real cut, restoration and rejection of an active server. No game/SW change. Prior failures retained. CI pending.

### Potvrda u desktop Chromium CI (26.11.2026)

[Izvršavanje 45738292152](https://github.com/tihidon/test1/actions/runs/45738292152) za [PR #39](https://github.com/tihidon/test1/pull/39) beleži PASS za B01–B06. B04 je prošao sa korigovanom proverom prekida transporta do lokalnog origina. Raniji neuspešan run ostaje zabeležen iznad. B06 koristi uvezen testni sejv. Nalaz važi za desktop CI i obuhvaćene scenarije. Fizički Android, produkcioni Netlify i sveža sesija evaluacije agenta imaju zasebne provere.

## Infrastructure strategy pivot — SC-TEAM-004 (26.11.2026)
The overnight task reported repeated DNS failure (`Could not resolve host: github.com`), zero fixes and no runtime evidence. Repeating unchanged attempts did not improve the result. At `8ed4417a6d2e423800a88436b4465a7a28f1dcab` the authenticated GitHub API returned an untruncated tree of 186 blobs (25,352,452 bytes) and pull/push permissions. This proves tree access, not a complete local snapshot or execution.

Mandatory: after an infrastructure failure, record command, exact error, environment, affected gate and available alternative. Do not repeat an identical failed action unless a relevant condition changed or a bounded transient retry is justified and recorded. Architecture owns the pivot: direct checkout → authorized connector/API branch and blob operations → verified owner-provided archive or byte-exact snapshot → existing private GitHub Actions runner. Select the shortest viable alternative rather than blindly executing every step. Verify pinned commit/tree, file bytes and modes against Git objects, completeness and build/publish hashes before claiming equivalent checkout; an archive lacks Git history and cannot satisfy history-based gates by itself. Use CI with full history for those gates. Never expose private source, bypass authentication, lower gates, fabricate D7 or change production to pass a test. If no viable path remains, report BLOCKED per affected gate, preserve original errors and continue only unblocked tasks. A CI run is not independent review.

First follow-up NS01: freeze a real UI quick-race result-close scenario; observe whether the already scheduled quick-bar callback writes to the closed panel after close. Positive control: visible quick-bar animation advances; negative control: ordinary panel without quick bars. Use actual Chromium, synthetic imported training fixture and existing QA infrastructure. NS02/NS03 remain separate cases, no double counting of a shared fix. No runtime claim until raw evidence is captured.


## QA-002 — committed save oracle hardening (26.11.2026)

Baseline 6dbfcb6a824e7d987554df68921bb7622151d967, functional_contract.py blob fc322ff34fc4ca91357c4ded1a3862873632546c. Scope: test tooling only. Eight synthetic controls reproduced four false accepts: same egg ID but changed kind in unchanged_inventory, purchase and durable, and unintended profile name change during purchase. These are oracle defects, not observed production data corruption. Candidate preserves existing checks, adds sorted hashed-ID/kind pairs, strict integer kind and duplicate-ID rejection, and checks existing egg kinds, profile and built list on purchase. Reordering and normal revision/time changes remain allowed. No whole-save equality or unverified snail attribute assumptions. Original 10 fixtures plus 10 new repository regressions and 8 reproduction tests: 28 local unittest methods PASS; repository CI and actual B01–B06 candidate execution pending. Source catalog block-08.js names kind 0 Siromašno and costs 100; earlier test prose labels it standard. Keep numeric kind 0 and cost 100; this is a naming contradiction, not authorization to change balance. Next: prove actual runtime case outcomes, broaden stable snail attributes/migration/quota/concurrency in separate evidence-based tasks. D7 independent review pending; SC-PMV-01 applies after merge.


## QA-003 — PW-DEF-01 reproduction candidate (26.11.2026)

Baseline 57389ec7d4cd195ac0d26d30b240d075bd599279, SW blob 446a11bc377c036f2dcc5b74217a7b4a4abcab5b. Node VM executed exact worker with simulated CacheStorage/fetch: distinct-name success, HTTP 503 and injected quota controls PASS; same-name HTTP and injected quota FAIL (active cache deleted and offline Response.error). No real quota or production failure claim. Local Chromium blocked at navigation ERR_BLOCKED_BY_ADMINISTRATOR; pivot to existing Chromium CI. New diagnostic uses actual pinned SW, synthetic HTTP resources, separate temporary profiles, single OriginTransport, actual 503, full cache key/hash comparison, real transport cut, sentinel IDB, two tabs and synthetic rollback. Cases: distinct success, distinct 503, same-name 503, rollback. The known failure is explicitly DEFECT_REPRODUCED, not product PASS; exit 0 only for exact expected diagnostic outcomes, all other outcomes fail. Freeze baseline SW hash; replace diagnostic expectation with mandatory preservation regression in correction PR, not permanent waiver. No production SW/runtime change. Actual browser results pending; D7 blocked. QA-002 PR #46 merged at baseline SHA, post-merge run 45792800049 tooling and Chromium success, B01–B06 51 assertions PASS; D7 remains unverified.


## QA-003 — isolated PW-DEF-01 correction candidate (26.11.2026)

PR #47 merge 2df44932708462a191cc0d0d6303b9250e515782, post-merge run 45794135342: actual Chromium same-name 503 defect reproduced, distinct success/failure and rollback PASS; synthetic IDB preserved. Guard proposal: caches.has(CACHE_NAME) before any open/write/delete; reject reused cache names, preserve current shell. Deliberate conservative behavior: orphan namespace after interrupted process may require new cache identity; no automatic destructive cleanup. One SW, no storage schema/economy changes. API transfer of 7.6MB publish HTML failed with HTTP/2 on create_blob and create_tree; source block-21 version-only blob upload succeeded. Pivot: draft PR runs isolated git worktree, exact baseline SW hash, p10->p11 full build labels and cache, existing family 0.8.92 fields retained per AGENTS snapshot distinction, deterministic build and equality to exactly two version substitutions, private candidate artifact and browser preservation regression. No production runtime files modified in draft. Baseline diagnostic retained only until real correction is integrated; candidate regression requires all four scenarios PASS. New cache gate compares current SW and union of previous/current core files against actual PR/push baseline; manual uses first parent. Immediate-baseline protection, not historical namespace uniqueness proof. D7 and actual CI pending; do not merge this draft as fix. Candidate artifact must be integrated with source/publish identity and actual CI, then PMV-01.
