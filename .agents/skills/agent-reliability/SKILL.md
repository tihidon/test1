---
name: agent-reliability
description: >-
  Audit Snail City agent conclusions, QA evidence, tool execution, release readiness and contradictory documents. Use for reliability reviews, bug-fix acceptance, failed or skipped checks, source identity, independent regression oracles, agent evaluations and claims that work is complete.
metadata:
  version: "1.3.3"
  project: "Snail City"
  status: "candidate"
compatibility: "Agent Skills host with repository access; Python 3.11+ standard library for evidence checker. No game dependencies."
---

# Agent Reliability

Read AGENTS.md and docs/tehnika/standardi/SC-REL-01-AGENT-RELIABILITY.md. This is a cross-check, not a second implementation owner. Use snail-city-engineering for changes and chromium-runtime-qa for runtime reproduction. Do not equate skill presence, CLI validation, tool fixtures or a green aggregate CI with actual agent adherence.

## Independence in the two-agent workflow

Use this skill to coordinate internal D7 evidence verification and hand findings to the owner for D8. External trials and independent-agent approval are retired. Record the actual evidence producer and verifier. Keep mandatory evidence gaps and material contradictions open. Verify contract coverage by named assertions, completed steps and original outputs, including failures.

## Review workflow
1. Freeze scope, target commit, source/publish identity, requirements, independent expected results and required gates before edits. Read canonical sources; log contradictions and distinguish current from historical evidence.
2. Require tool transcript/exit code and artifact provenance for each claimed executed check. A static candidate is not a confirmed bug. Missing tools => BLOCKED; skipped => NOT RUN; negative controls must fail for intended reason.
3. Require per-function evidence for root-cause claims: full affected body, actual callers, source SHA/anchor, pre/post state, async order, first divergence. Runtime sampling alone does not establish exact call counts. No unsupported device claims.
4. Review baseline and candidate with unchanged oracle, relevant coverage and failure reason. Record regression and rollback. Never waive required evidence after a failure. Do not retry to hide flaky results.
5. Check changed file scope, preservation of user changes, save/SSOT, no parallel implementation; do not modify production or merge on your own.
6. Use tools/reliability/check_evidence.py with a reviewer-defined contract and evidence JSON in a private location. It checks structural completeness and file hashes, not the truth of assertions. Review original logs, scenario, signatures and tool results; self-reported evidence can be fabricated. Behavioral PASS requires evidence of actual agent execution under the frozen contract.

## Agent evaluation
Use docs/tehnika/standardi/SC-REL-01-AGENT-RELIABILITY.md and tools/reliability/cases.json. Run the same tasks with and without the skill in fresh internal sessions; record model/version/tools, exact prompt, target, transcript and outputs. For formal evaluator qualification, follow SC-DEC-01: an internal controller (team member or owner, not the tested revision's author or evaluated executor) locks the oracle and grades the locked submission. Keep answer keys outside the evaluator's accessible sources as specified there; never let the evaluated agent grade itself. Fixtures test checker, not agent. Missing harness or actual transcript = NOT RUN. No release on required FAIL/BLOCKED/NOT RUN. Report findings, limitations, residual risk and decision.

## Shared decision chain (SC-DEC-01)
Read docs/tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md. Coordinate internal D7 and report to the owner for D8. Check original evidence against frozen contract, challenge alternative explanations, require same oracle and intended failure reason, reject unresolved contradictions. Use tools/reliability/check_decision.py for bug-fix structural gate; Treat structural PASS as a structural result. Report any sequential role analysis by one executor as such. Keep missing evidence BLOCKED/NOT RUN.

## Executable complexity checks
Read docs/tehnika/standardi/SC-CODE-02-IZVRSNA-KONTROLA-KOMPLEKSNOSTI.md. Verify actual parser coverage, historical and current ratchet separately, intentional negative browser fixture reason and live DOM evidence. No-growth PASS cannot erase old debt or prove game performance. Distinguish fixture from game, and source bytes from runtime structure.

## Reliable debugging and specialist handoff
Read docs/tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md. Review original logs and oracle, not counts alone. Reject retry masking, self-review, CSS dead-code claims from coverage.

## Functional phase B
Read docs/tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md phase B. Review functional oracle and raw original artifacts; reject zero assertions, missing cases, substitution of shell for save or synthetic setup for natural progression.

## QA procedures
Use the [shared QA procedures](../chromium-runtime-qa/references/qa-procedures.md) to review original artifacts independently against the exact commit and frozen oracle.

## Bezbednosni pregled i dokazi

Primeni SC-BEH-01. D7 proverava originalne dokaze i opseg izvršenih provera. Kontrolor rada agenata proverava poštovanje opsega, ovlašćenja i tačnost izveštaja. Razlika u nalazima ide u postojeći SC-DEC-01 zapis uz ciljnu proveru.

Za automatsku klasifikaciju izvršnih dokaza i prioritete nalaza koristi [SC-DEC-01](../../../docs/tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md#automatska-provera-izvršnih-dokaza). Pri D7 proveri original, verziju pravila i obim sintetičkih ili stvarnih dokaza.
