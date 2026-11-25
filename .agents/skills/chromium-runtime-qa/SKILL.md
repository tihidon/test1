---
name: chromium-runtime-qa
description: >-
  Reproduce Snail City browser bugs, hangs, incorrect state transitions, save/offline failures and performance regressions in isolated Chromium. Trace real user actions to the first divergent function or asynchronous operation, collect reproducible evidence and compare broken and fixed builds. Activate for runtime QA, Playwright, CDP, lifecycle, RAF/timer loops, profiling and regression investigations.
metadata:
  version: "1.0.1"
  project: "Snail City"
  status: "candidate"
compatibility: "Python 3.11+, Playwright Python 1.56.0, matching Chromium, Git, Ubuntu 24.04 for CI and POSIX for automated watchdog; trusted checkout and local isolated origin."
---

# Chromium Runtime QA

Use with snail-city-engineering, not instead of it. Read AGENTS.md, SC-AGENT-01, relevant canonical standards and docs/tehnika/standardi/SC-QA-02-CHROMIUM-RUNTIME.md. No production instrumentation, balance changes, competing schedulers or real player data. Do not alter the game merely to make a test green.

## Four obligations

1. **Identity:** record candidate and baseline commit, dirty state, HTML/SW SHA-256, actual navigation response bytes, actual version/startup trace, worker controller, active cache and environment. Never conflate diagnostic version family, build tag and cache suffix. Fresh isolated browser context and local publish whitelist. Separate desktop/headless/emulated/physical Android evidence.
2. **Reproduce:** define expected state and action before execution; use real UI and existing domain contracts, not invented selectors or injected fake game behavior. Use actual current source and existing function registry. Correlate action, invocation, async ordering, state before/after and next visible frame. Identify first divergence, not merely longest task. Explicitly distinguish observation, hypothesis and proof.
3. **Prove:** same independent assertion fails on broken build for the intended reason and passes fixed build; unaffected regressions pass. Preserve trace, CPU profile where relevant, exact function/source anchor and inputs/outputs, and raw measurements. For PL-01 use A/B/R, matched conditions and required repetitions; profiling runs are diagnostic, not unbiased timing. Timeout, missing coverage, skipped test, changed assertion or failure for wrong reason is not proof.
4. **Limits:** desktop results apply only to the tested scenario. Android/HONOR FPS and latency require physical device measurements. No claim of PW-01 save preservation from shell-only offline test. Record FAIL/BLOCKED/NOT RUN separately. Stop after three failed hypotheses unless new evidence/owner authorization; no retries to hide flakiness.

## Execute

From trusted repository root:
- Run existing build and AST checks first. Install isolated Playwright per SC-QA-02, not into game runtime.
- `python tools/qa/runtime_watchdog.py --out /tmp/sc-qa-run` runs actual Chromium against a copied local publish whitelist; writes report, screenshots, Playwright trace, CDP sampled CPU profile and watchdog status. It checks shell identity and offline navigation, not complete gameplay or persistence.
- For an actual bug, create a versioned test scenario in the existing tools/qa owner. Use --scenario with reviewed JSON steps (selector visible, click, text assertion); add a targeted independent domain/state assertion where UI alone cannot prove correctness. JSON scenario uses exact CSS selectors read from actual code, never guessed. Record expected states and actual failure reason. For save tests use a separate sanitized test fixture with revision/identity and cold relaunch; not implemented by base smoke.
- Use `python -m playwright show-trace <out>/trace.zip` locally. CPU profile is sampled JS stacks, not exact call counts or GPU completion. CDP Performance/Tracing and function-scoped breakpoints are separate diagnostic runs; trace actual code before suggesting change. Do not automatically patch suspect loops.
- If watchdog kills worker, keep partial evidence and classify hang/time budget exceeded; it does not identify a function. No unconditional PASS when worker fails, skips or omits report. Preserve raw private artifacts only on trusted local/private CI.

## Reliability gate

Before accepting any fix: test oracle independent of candidate; negative control demonstrates detector; exact build identity; bounded execution; baseline/candidate matching; coverage record; no swallowed page errors; explicit unsupported paths; evidence of first divergent operation or mark root cause unproven. Return concise evidence table and function card (owner, symbol, SHA/anchor, callers, async dependencies, state, actual/expected, reproduction, regression). Report uncertainty, untouched systems and rollback. No merge/deploy without existing approval gates.
