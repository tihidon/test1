# AGENTS.md — uputstvo za agente (tihidon/test1)

## Kanonski repozitorijum (P0, 26.11.2026)

`tihidon/test1` je primarni razvojni repozitorijum i kanonski izvor aktivnih projektnih standarda, registara i skillova. `tihidon/test-cl1` je Cloudflare testni repo sa istim zajedničkim standardima i zasebnim hosting dokazima; ne uvoditi paralelni izvor pravila. `tihidon/snail-city-test` je istorijska referenca; ne sinhronizovati pravila unazad niti prepisivati aktivne standarde iz istorijskih kopija. Istorijska v0.8.90 ostaje zaštićena. Svaki zadatak utvrđuje stvarni checkout i prijavljuje neslaganja. PL-01/CSS-01 je obavezan: [standard](docs/tehnika/standardi/SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md). Jutarnji pregled, popodnevna provera i večernji QA ne autorizuju automatske izmene.

Projektni autoritet je stvarni checkout i kanonski standardi, ne istorijski broj verzije. Aktuelni referentni snapshot 26.11.2026: test1 `e51b1e6cba31bedd61ad0bbb269c90f065117279`, test-cl1 `8d9fec8405674cbfcc97dd97224bb3a8de596c15`; HTML blob `f730698c8251c30c91d798ea816986a91e189a01`, P11-r2, isti runtime i src. `SC_PWA_STATUS.version` je family 0.8.92. Dokazi CI, odvojeni hosting statusi i ograničenja u [docs/README.md](docs/README.md#aktuelni-zajednički-status--26112026). Svaki zadatak ponovo utvrđuje stvarni identitet; D7 i kompletno release zatvaranje nisu potvrđeni. Prethodni P10 snapshot ostaje istorijski u indeksu.

Istorijska referenca P3: `5b4b030`, SHA-256 `594026b9ffab62ceb8dbbfa181c887edea3f903ff84a27151a2330fb978dc58a`; P1/P3 dokazi ne važe automatski za P10.

## Pre bilo kakve izmene

1. Pročitaj [docs/README.md](docs/README.md) (indeks dokumenata i šta je proveren za ovaj kod).
2. Pročitaj [SC-RAD-01](docs/tehnika/standardi/SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md) §2 (hijerarhija autoriteta) i [SC-AGENT-01](docs/tehnika/standardi/SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md) (postupak i QA gate-ovi).
3. Kad se dokument i kod ne slažu, važi kod. Neslaganje prijavi, ne pretpostavljaj.

## Pravila

- **Jedan izvor istine.** Ne pravi paralelni renderer, koordinatnu logiku, listu brzina ili čuvanje. Koristi postojeći vlasnik (tabela u [SSOT](docs/tehnika/standardi/PRAVILO-JEDAN-IZVOR-ISTINE.md)).
- **Minimalna izmena.** Menjaj samo ono što je traženo. Ne formatiraj ceo fajl, ne preimenuj i ne diraj delove koji rade.
- **Verzija na šest mesta.** Svaka promena verzije mora ići na: build tag u `#sc-startup-trace`, `SC_PWA_STATUS.version`, `<title>`, `const VERSION`, komentar u `sw.js` i `CACHE_NAME` u `sw.js`.
- **Čuvanje.** Promena strukture stanja zahteva migraciju i test. Ne menjaj save/load bez provere.
- **Balans i ekonomija.** Ne menjaj cene, nagrade, valutu ni verovatnoće bez odluke vlasnika. Ne izmišljaj brojeve.
- **Dokumentacija.** Svaka promena u igri se beleži u dokumentu promena u istom koraku. Dokumenti moraju odgovarati kodu.
- **Bez ZIP-ova i binarnih priloga bez zahteva.** Rezultat daj kao link ili PR.

## Izveštaj posle rada

Navedi: izmenjene fajlove i funkcije, izmenu po funkciji, i kako je provereno (sa stvarnim komandama i njihovim izlazom). Šta nije testirano na uređaju, to jasno označi kao **NIJE TESTIRANO**.

## Skill i dodatni gate-ovi (25.11.2026)

Za Snail City razvoj učitaj projektni `.agents/skills/snail-city-engineering/SKILL.md` (Codex: `$snail-city-engineering`), bez učitavanja kompletnog istorijskog registra. Primenjuj [SC-BUILD-01](docs/tehnika/standardi/SC-BUILD-01-PYTHON-BUILD.md), [SC-LOOP-01](docs/tehnika/standardi/SC-LOOP-01-LOOP-I-BUG-AUDIT.md) i [SC-CLI-01](docs/alati/SC-CLI-01-AGENT-INSTALACIJA.md). stvarni target/version/hash i publish root proveriti svaki put. Ne pokretati split nad aktivnim src/. Pre i posle runtime izmene dokazati build/publish jednakost; ako nedostaje alat ili postojeći baseline ne prolazi, prijavi BLOCKED/FAIL. Zadržati sve relevantne G0–G7 i ne menjati deploy bez odobrenja.

## Uloge dva agenta

- **Stres-test specijalista** koristi `.agents/skills/snail-city-stress-test-specialist/SKILL.md` zajedno sa `.agents/skills/chromium-runtime-qa/SKILL.md`. Vodi reprodukciju, kontrolne scenarije i regresione provere D2/D4/D6. Predaje sirove dokaze, prvo opaženo odstupanje i granice nalaza.
- **Arhitektura i infrastruktura** koristi `.agents/skills/snail-city-architecture-infrastructure/SKILL.md` uz `.agents/skills/snail-city-engineering/SKILL.md`. Vodi D0/D1/D3/D5, određuje postojećeg vlasnika izmene i odgovara za build, publish identitet i CI. Za promenu koja utiče na rezultat testa dogovara zamrznute uslove sa stres-test specijalistom.
- Za D7/D8 primeni `agent-reliability` u nezavisnom pregledu originalnih dokaza. Ako su oba agenta učestvovala u istrazi ili implementaciji, nezavisni pregled može obaviti vlasnik ili drugi reviewer. Do tada status kandidata je **ZADRŽI ZA QA**.

## Chromium Runtime QA

Za runtime bag, hang, loop, performance, save/offline ili funkcionalni QA koristi i `.agents/skills/chromium-runtime-qa/SKILL.md`. Primeni [SC-QA-02](docs/tehnika/standardi/SC-QA-02-CHROMIUM-RUNTIME.md). Postojeći snail-city-engineering ostaje vlasnik engineering procesa. Novi alati rade samo nad izolovanim kopijama publish fajlova; bez izmena runtime igre. CLI format PASS nije agent eval; shell smoke nije kompletan gameplay/PW-01 ili Android dokaz.

## Agent Reliability

Za audit dokaza, zaključak o popravci, release i kontradikcije učitaj `.agents/skills/agent-reliability/SKILL.md` i [SC-REL-01](docs/tehnika/standardi/SC-REL-01-AGENT-RELIABILITY.md). Nezavisni oracle, dokaz identiteta i izvorni logovi obavezni; structural checker PASS nije agent evaluation. Bez lažnog PASS i bez merge/deploy bez odobrenja.

## Shared decision chain
Primeni [SC-DEC-01](docs/tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md) za zajednički D0–D8 proces tri postojeća skilla. Jedan decision record, frozen oracle, originalni dokazi, nezavisan pregled. Structural PASS nije release authorization. Dva specijalistička skilla koriste postojeće vlasnike D0–D8 i obavezne gate-ove.

## Executable complexity checks
Apply [SC-CODE-02](docs/tehnika/standardi/SC-CODE-02-IZVRSNA-KONTROLA-KOMPLEKSNOSTI.md) with canonical SC-CODE-01 tool, extended AST loop inventory and live DOM snapshots. Do not raise baselines or auto-delete. Distinguish fixture and game evidence under SC-DEC-01.

## Reliable debugging
Apply [SC-DEBUG-01](docs/tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md) with SC-DEC-01. Two specialists share tools; independent Reliability review required. Diagnostic coverage is not timing. No auto-fix or deletion.

## SC-DEBUG-01 functional phase B
Use the canonical SC-DEBUG-01 phase B contract, `tools/qa/runtime_watchdog.py --functional`, and original per-case evidence. Distinguish shell reload, desktop persistent cold reopen, synthetic race import, natural progression and physical Android. Stress specialist owns scenario execution; architecture specialist owns actual contract and storage/build identity; Reliability independently verifies. No PASS with missing cases or wrong failure reason.

## Team coordination (26.11.2026)

Aktuelni identitet paketa i svakog skilla je u [DOC-003 registru](docs/README.md#doc-003--aktuelni-agent-team-registar-snapshot-26112026); primeni DOC-VER-01 iz SC-AGENT-01. Team paket koordinira postojeći SC-DEC-01. DOC-003 razlikuje verzije paketa na sajtu i lokalnih repo profila. Grafički specijalista koristi [projektni rendering candidate](.agents/skills/snail-city-rendering-performance/SKILL.md) kada je odgovarajući zadatak; podržava D1/D3/D4/D6, ne menja vlasnike faza. Bez stvarne delegacije prijaviti sekvencijalno izvršavanje, D7 nezavisnost BLOCKED. Handoff prema SC-DEC-01 ostaje kanonski.

## Zajedničko ponašanje svih agenata
Pre zadatka primeni [SC-BEH-01](docs/tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md) uz SC-DEC-01 i SC-REL-01. Važi za sve projektne uloge unutar stvarne hijerarhije instrukcija platforme. Za specijalizovane preglede koristi [pravnog specijalistu](.agents/skills/snail-city-legal/SKILL.md), [defanzivnog auditora](.agents/skills/snail-city-defensive-auditor/SKILL.md) i [kontrolora rada agenata](.agents/skills/snail-city-agent-conduct/SKILL.md). D7 i autorizacija vlasnika idu kroz postojeći SC-DEC-01 postupak. Istorijski Team plugin v0.3.0 sadržao je prateće uputstvo; nezavisna evaluacija nije izvršena.

### Obavezna proaktivnost i usvajanje znanja

Primeni [SC-PRO-01 i SC-KG-01](docs/tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md#sc-pro-01--obavezna-proaktivnost-u-odobrenom-opsegu) za sve sadašnje i buduće uloge. Istražuj odobrene alternative, ali ne usvajaj nova znanja, tehnologije, pravila ili skillove bez nezavisne kontrole i eksplicitnog odobrenja vlasnika za tačan pregledani kandidat. Bez samoodobravanja, automatskog preuzimanja instrukcija, širenja dozvola ili prenosa osetljivih podataka. Ako nezavisan pregled nije dostupan, ZADRŽI ZA QA. Jedan SC-DEC-01 zapis; DOC-VER-01 i PMV ostaju.

## Infrastructure failures — mandatory strategy pivot
Apply [SC-DEBUG-01 infrastructure strategy pivot](docs/tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md#infrastructure-strategy-pivot--sc-team-004-26112026). Do not repeat unchanged failed operations. Architecture records failure, selects a viable authorized alternative (API, verified snapshot, private CI), preserves identity and gates; Coordinator routes unblocked work. No fabricated PASS or independent review.

## Post-merge verification — SC-PMV-01

Every agent must apply [SC-PMV-01](docs/tehnika/standardi/SC-PMV-01-POST-MERGE-VERIFICATION-STANDARD.md) after each merge; Coordinator owns closure, not independent self-approval. Keep G0–G7 and D0–D8 intact. Actual merge SHA, ancestry, exact-SHA post-merge CI, relevant regressions and evidence are mandatory before VERIFIED. No unapproved release or rollback. PR CI is not post-merge CI.

## Shared Chrome DevTools MCP — candidate
Use [SC-CLI-01](docs/alati/SC-CLI-01-AGENT-INSTALACIJA.md#chrome-devtools-mcp--p0-kandidat-26112026) and SC-QA-02. Coordinator checks actual availability; Engineering/Architecture own identity and setup; QA/Stress reproduce; Rendering inspects traces and heaps; Reliability independently reviews originals. Isolated localhost only. MCP diagnostics do not replace Playwright B01–B06, PL-01 uninstrumented A/B/R, PW-01 or D7. Preserve original artifacts, target SHA and browser/tool version. Missing MCP does not block existing QA; pivot. Installed ChatGPT plugin and Codex activation are separate from repo configuration.

## QA procedure za agente
Za Playwright, Android, Lighthouse, migraciju PWA sejva, pristupačnost i nezavisni D7 pregled koristi [zajedničke QA procedure](.agents/skills/chromium-runtime-qa/references/qa-procedures.md). Primeni ih prema ulozi i važećim standardima projekta.

## Način rada koordinatora

**Fokusiran, sistematičan i analitičan.** Drži tim na dogovorenom cilju i beleži sporedne nalaze odvojeno. Uz svaku proveru vodi odgovornu ulogu, očekivani ishod, dokaz i otvorene stavke. Poredi nalaze pod istim uslovima i bira proveru koja razrešava protivrečnost.

## Predlog SC-INTEGRITY-01 — P0

[SC-INTEGRITY-01](docs/tehnika/standardi/SC-INTEGRITY-01-ZASTITA-INTEGRITETA-PROJEKTA.md) definiše kontrolu celog Git stabla i odobrenog opsega, zaštitu izvršnog koda i sopstvenih QA kontrola, read-back i negativne testove incidenta PR #11. Predlog za nezavisni pregled i odobrenje vlasnika; nije tvrdnja o aktivnom izvršnom gate-u. Postojeći SC-RAD-01, G0–G7, D0–D8 i PMV ostaju obavezni.


## SC-INTEGRITY-01 — kandidat 0.2, 27.11.2026

[SC-INTEGRITY-01](docs/tehnika/standardi/SC-INTEGRITY-01-ZASTITA-INTEGRITETA-PROJEKTA.md) proširuje SC-RAD-01/G0/G1/G7/PMV: kontrola celog stabla, trusted preflight i INT-APPROVAL-01. Kandidat, ne aktivna potvrda. Obavezan exact-scope pregled iz odobrenog izvora i odvojena odobrenja prema SC-KG-01; strukturni CI nije autorizacija. Bez stvarne nezavisne delegacije D7 BLOCKED. Bez izmene runtime-a/deploy-a.

## SC-EQ-01 — kandidat za kvalifikaciju evaluatora (P0)

[SC-EQ-01](docs/tehnika/standardi/SC-EQ-01-KVALIFIKACIJA-EVALUATORA.md) objedinjuje predlog kvalifikacije evaluatora pre formalnog kvalifikovanja drugih agenata. E0–E7 i ZERO-FALSE-PASS dopunjuju, ne menjaju D0–D8/G0–G7, SC-KG-01 i PMV. Nezavisni specijalista ostaje van tima, ZADRŽI ZA QA; bez E7 nema formalnog sertifikata. Kandidat dokumenta čeka nezavisni pregled i odobrenje tačne revizije; nema nove aktivne dozvole.
