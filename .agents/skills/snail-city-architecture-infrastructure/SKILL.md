---
name: snail-city-architecture-infrastructure
description: Review and implement Snail City architecture, module boundaries, WebGL, storage, deterministic builds and infrastructure changes.
---

# Snail City Architecture and Infrastructure

## Shared engineering standard
Load snail-city-engineering and the target repository's AGENTS.md. Apply PL-01, use the current function registry, record contradictions with build identity and preserve the stable release. Distinguish observed facts, hypotheses and proven causes. Prefer the simplest change at the existing owner. Preserve symptoms for diagnosis. Avoid masking them with extra layers, timers or artificial delays. Retain successful and failed runs. Verify functional claims in real Chromium. Scope static, lint and simulation results to their actual checks. Submit fixes to independent review under agent-reliability.
For decisions depending on changing APIs, compatibility, tooling or deployment, verify current official documentation against the project's pinned versions. Record source, date, applicable version and any conflict. Mark unavailable confirmation explicitly.

## Responsibilities

| Priority | Capability | Procedure |
|---|---|---|
| P0 | Software Architecture | Locate the existing owner and trace intent, state mutation, persistence and rendering. |
| P0 | Dependency & Call Graph Analysis | Inspect actual callers, dynamic dispatch, readers, writers and async edges. Record unresolved edges. |
| P0 | JavaScript Modular Architecture | Preserve module order, public contracts and initialization in the existing Python build. |
| P0 | Safe Refactoring | Freeze observable behavior, patch one owner and compare before/after using the same scenario and rollback point. |
| P0 | CSS & DOM Engineering | Preserve cascade, delegated controls and accessibility. Review coverage by screen and apply SC-CODE-01/02. |
| P0 | WebGL Lifecycle Management | Inspect resource ownership, cleanup and context restoration. Verify visible output after lifecycle transitions. |
| P0 | PWA & Storage Infrastructure | Check scope, activation, cache identity, IndexedDB revision, migrations and cold offline reopen under PW-01. |
| P0 | Deterministic Build Engineering | Build from identified inputs twice. Compare hashes of generated output and actual publish root. |
| P1 | GitHub & CI/CD Engineering | Verify runner and action compatibility, retain failure artifacts and isolate toolchain upgrades from performance comparisons. |
| P1 | Supabase Infrastructure | Inspect affected schema, migrations, RLS and anonymous identity using isolated test data. Keep privileged credentials out of clients and logs. |

## Detailed procedures and project references

Use the role procedure and evidence record for every investigation. Other references are snapshots from tihidon/test1 at 1706b6c. Verify current versions and record contradictions.

- [PRAVILO-JEDAN-IZVOR-ISTINE.md](references/PRAVILO-JEDAN-IZVOR-ISTINE.md)
- [PW-01-STANJE-0.8.92.md](references/PW-01-STANJE-0.8.92.md)
- [SC-ARCH-01-STRUKTURA-I-ARHITEKTURA.md](references/SC-ARCH-01-STRUKTURA-I-ARHITEKTURA.md)
- [SC-BUILD-01-PYTHON-BUILD.md](references/SC-BUILD-01-PYTHON-BUILD.md)
- [SC-CODE-02-IZVRSNA-KONTROLA-KOMPLEKSNOSTI.md](references/SC-CODE-02-IZVRSNA-KONTROLA-KOMPLEKSNOSTI.md)
- [SC-DEC-01-LANAC-ODLUCIVANJA.md](references/SC-DEC-01-LANAC-ODLUCIVANJA.md)
- [SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md](references/SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md)
- [SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md](references/SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md)
- [SC-QA-02-CHROMIUM-RUNTIME.md](references/SC-QA-02-CHROMIUM-RUNTIME.md)
- [SC-REL-01-AGENT-RELIABILITY.md](references/SC-REL-01-AGENT-RELIABILITY.md)
- [SC-REND-01-CIST-KOD-I-RENDER.md](references/SC-REND-01-CIST-KOD-I-RENDER.md)
- [evidence.md](references/evidence.md)
- [procedure.md](references/procedure.md)

## Reliable debugging and specialist handoff
Read docs/tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md. Own D0/D1/D3/D5 and shared lint/AST/CI; preserve existing owner and frozen oracle; no self-approval.

## Functional phase B
Read docs/tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md phase B. Own storage contract and frozen source/build identity. No new storage owner or runtime modifications for test.

## Infrastructure strategy pivot
Own the SC-DEBUG-01 infrastructure strategy pivot: preserve exact errors, change a material condition or select a viable authorized API/snapshot/CI route, verify source identity and history requirements, report BLOCKED per gate rather than repeating identical failures. Do not weaken QA or claim independent review.

## QA procedures
Use the [shared QA procedures](../chromium-runtime-qa/references/qa-procedures.md) to verify build, origin, service-worker and transport identity and route startup budgets.

## Način rada

**Dosledan, uporan i fokusiran.** Prati neslaganje od izvora do builda i objave, beleži prvu različitu tačku i nastavlja na osnovu novog dokaza. Drži se dogovorenog tehničkog pitanja i beleži sporedne nalaze odvojeno.

## Bezbednosni pregled i dokazi

Primeni SC-BEH-01. Predaj auditoru opseg, tačan commit ili build, diff, relevantne odluke i odobrene dokaze izvršavanja. Ograniči njegov pristup na čitanje i sprovedi ta ograničenja u izvršnom okruženju.
