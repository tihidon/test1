---
name: agent-reliability
description: >-
  Audit Snail City agent conclusions, QA evidence, tool execution, release readiness and contradictory documents. Use for reliability reviews, bug-fix acceptance, failed or skipped checks, source identity, independent regression oracles, agent evaluations and claims that work is complete.
metadata:
  version: "1.3.1"
  project: "Snail City"
  status: "candidate"
compatibility: "Agent Skills host with repository access; Python 3.11+ standard library for evidence checker. No game dependencies."
---

# Agent Reliability

Read AGENTS.md and docs/tehnika/standardi/SC-REL-01-AGENT-RELIABILITY.md. This is a cross-check, not a second implementation owner. Use snail-city-engineering for changes and chromium-runtime-qa for runtime reproduction. Do not equate skill presence, CLI validation, tool fixtures or a green aggregate CI with actual agent adherence.

## Independence in the two-agent workflow

Use this skill for D7/D8. A reviewer who took part in the investigation, implementation or production of the evidence cannot independently approve that work. If both agents participated, hand review to the owner or another independent reviewer. Without that review record, keep the candidate at ZADRŽI ZA QA. Verify contract coverage by named assertions and completed steps, including failed runs. Shell, fixture, gameplay, save durability and physical-device claims each require their corresponding evidence.

## Review workflow
1. Freeze scope, target commit, source/publish identity, requirements, independent expected results and required gates before edits. Read canonical sources; log contradictions and distinguish current from historical evidence.
2. Require tool transcript/exit code and artifact provenance for each claimed executed check. A static candidate is not a confirmed bug. Missing tools => BLOCKED; skipped => NOT RUN; negative controls must fail for intended reason.
3. Require per-function evidence for root-cause claims: full affected body, actual callers, source SHA/anchor, pre/post state, async order, first divergence. Runtime sampling alone does not establish exact call counts. No unsupported device claims.
4. Review baseline and candidate with unchanged oracle, relevant coverage and failure reason. Record regression and rollback. Never waive required evidence after a failure. Do not retry to hide flaky results.
5. Check changed file scope, preservation of user changes, save/SSOT, no parallel implementation; do not modify production or merge on your own.
6. Use tools/reliability/check_evidence.py with a reviewer-defined contract and evidence JSON in a private location. It checks structural completeness and file hashes, not the truth of assertions. Independently review original logs, scenario, signatures and tool results; self-reported evidence can be fabricated. No behavioral PASS until independent reviewer verifies actual agent execution.

## Agent evaluation
Use docs/tehnika/standardi/SC-REL-01-AGENT-RELIABILITY.md and tools/reliability/cases.json. Run same tasks with and without skill in disposable independent sessions, record model/version/tools, exact prompt, target, transcript and outputs. Blind independent human/reviewer checks each case against criteria; never let evaluated agent grade itself. Fixtures test checker, not agent. Missing harness or actual transcript = NOT RUN. No release on required FAIL/BLOCKED/NOT RUN. Report findings, limitations, residual risk and decision.

## Shared decision chain (SC-DEC-01)
Read docs/tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md. Own D7/D8 review, not implementation. Check original evidence against frozen contract, challenge alternative explanations, require same oracle and intended failure reason, reject unresolved contradictions. Use tools/reliability/check_decision.py for bug-fix structural gate; never treat its PASS as independent review or release permission. A role in the same agent is not an independent reviewer. Keep missing evidence BLOCKED/NOT RUN.

## Executable complexity checks
Read docs/tehnika/standardi/SC-CODE-02-IZVRSNA-KONTROLA-KOMPLEKSNOSTI.md. Verify actual parser coverage, historical and current ratchet separately, intentional negative browser fixture reason and live DOM evidence. No-growth PASS cannot erase old debt or prove game performance. Distinguish fixture from game, and source bytes from runtime structure.

## Reliable debugging and specialist handoff
Read docs/tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md. Review original logs and oracle, not counts alone. Reject retry masking, self-review, CSS dead-code claims from coverage.
