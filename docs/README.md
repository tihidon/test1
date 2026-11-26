# Snail City test1 — dokumentacija

Poslednja izmena indeksa: 2026-11-26

**P0 — kanonski autoritet:** `tihidon/test1` je primarni razvojni repo; `snail-city-test` je istorijski izvor. Aktivna pravila se održavaju ovde. P1/P3 podaci ispod su istorijski, ne dokaz za P10. P10 je koordinacioni snapshot iz AGENTS.md, ne novo izvršno merenje.

Istorijski indeks dokumenata za P3 (nije trenutni runtime dokaz): `tihidon/test1` `main` `5b4b030` (PR #13), `index.html` SHA-256 `594026b9ffab62ceb8dbbfa181c887edea3f903ff84a27151a2330fb978dc58a`, `const VERSION = '0.8.92-css-unified-p3'`, SW `snail-city-shell-0.8.92-css-unified-p3-r2`. Kopije označene „`2d66e55` / `c19cc1ac…`“ proverene su samo nad p1 commit-om i nisu ponovo proverene nad p3. Svaki dokument je pre prenosa proveren prema ovom kodu 25.11.2026; netačne tvrdnje su ispravljene ili dokument nije prenet (§3).

## Sadržaj

1. [Odakle početi](#1-odakle-početi)
2. [Dokumenti i status provere](#2-dokumenti-i-status-provere)
3. [Šta nije preneto i zašto](#3-šta-nije-preneto-i-zašto)
4. [Ispravke nađene pri proveri](#4-ispravke-nađene-pri-proveri)
5. [Održavanje kopija](#5-održavanje-kopija)
6. [Otvoreno](#6-otvoreno)

## 1. Odakle početi

1. [SC-RAD-01 §2–§3](./tehnika/standardi/SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md#2-hijerarhija-autoriteta): redosled važenja izvora i činjenice o ovom kodu.
2. [SC-AGENT-01](./tehnika/standardi/SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md): obavezni postupak rada i QA gate-ovi G0–G7.
3. Za konkretnu izmenu: standard njene oblasti iz tabele ispod.

Kad se dokument i kod ne slažu, važi kod; neslaganje se upisuje, ne rešava pretpostavkom.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 2. Dokumenti i status provere

**Kopija** = prenet iz drugog izvora uz proveru i ispravke za test1. **Izdanje za test1** = pravila iz izvora, činjenice ponovo izmerene. **Novo** = napisano nad test1.

### Standardi (`tehnika/standardi/`)

| Dokument | Oblast | Vrsta i izvor | Provera prema test1 |
|---|---|---|---|
| [SC-AGENT-01](./tehnika/standardi/SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md) | postupak rada agenata, QA gate | izdanje za test1; projekat (rev. 1.0, 0.8.93) | identitet buildova, lista brzina, CSS blok, ikonice ispravljeni; GML deo uklonjen |
| [SC-ARCH-01](./tehnika/standardi/SC-ARCH-01-STRUKTURA-I-ARHITEKTURA.md) | struktura fajlova i modula, PWA slojevi | izdanje za test1; projekat (rev. 1.0, 0.8.93) | stablo, `_headers`, linije 17 modula, `sw.js` vrednosti i tabela paketa izmereni nad test1 |
| [SC-FUNC-01](./tehnika/standardi/SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md) | registar funkcija, K01–K08 | izdanje za test1; projekat (rev. 1.0, 0.8.93) | registar regenerisan (983 čvora); K01, K02 ne važe za test1, K03–K08 potvrđeni |
| [SSOT — jedan izvor istine](./tehnika/standardi/PRAVILO-JEDAN-IZVOR-ISTINE.md) | vlasnici podataka | kopija; `snail-city-test@1e3258f` | svih 19 vlasnika postoji; red verzije dopunjen |
| [SC-PL-01 / CSS-01](./tehnika/standardi/SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md) | layout, canvas resize, velike slike u CSS promenljivama | kopija; `snail-city-test@1e3258f` | tabela CSS-01 potvrđena; dodata peta vrednost `--sc174-snail-art`; trace brojevi su iz 0.8.90 |
| [SC-CODE-01](./tehnika/standardi/SC-CODE-01-CSS-DOM-FUNKCIJE.md) | pisanje CSS, DOM, funkcija; ratchet | kopija; `snail-city-test@12f986c` (PR #12, spojen `f32b290`) | ratchet PASS, 0 razlika prema baseline 0.8.92; dodato pokretanje alata |
| [SC-RAD-01](./tehnika/standardi/SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md) | postavka, izmena, brisanje koda | kopija; `snail-city-test@12f986c` (PR #12, spojen `f32b290`) | §3 prepisan za test1; R04, R05 prilagođeni |
| [SC-REND-01](./tehnika/standardi/SC-REND-01-CIST-KOD-I-RENDER.md) | render, vreme, keš, invalidacija | kopija; `snail-city-test@12f986c` (PR #12, spojen `f32b290`; pisan nad test1) | ratchet PASS; N01, N12 potvrđeni; dva podatka ispravljena (§4) |
| [SC-BRISANJE-3-PROVERE](./tehnika/standardi/SC-BRISANJE-3-PROVERE.md) | presedan brisanja CSS-a | kopija; `snail-city-test@1e3258f` | **ne opisuje test1**: `.map-controls` ovde i dalje postoji (označeno) |

### PWA, QA i alati

| Dokument | Vrsta | Provera |
|---|---|---|
| [PW-01 — stanje u 0.8.92](./tehnika/pwa-offline/PW-01-STANJE-0.8.92.md) | novo | 12 elemenata PW-01 mehanizma iz 0.8.90 potvrđeno u kodu; uređaj nije testiran |
| [Animacije — inventar 0.8.92](./qa/SC-ANIMACIJE-0.8.92-INVENTAR.md) | novo | 26 `@keyframes` popisano; veza sa 37 istorijskih imena |
| [docs/alati](./alati/README.md) | novo | generator registra za SC-FUNC-01 |

### Dokumenti koji su već bili u test1 (nisu menjani)

| Dokument | Šta je |
|---|---|
| [SC-v0.8.92-P1-CSS-SINGLE-SOURCE-AUDIT.md](./SC-v0.8.92-P1-CSS-SINGLE-SOURCE-AUDIT.md) i [JSON](./SC-v0.8.92-P1-static-audit.json) | audit kandidata 0.8.92 (23.11.2026); isti `index.html` SHA-256 kao ovaj build; jedina razlika je `CACHE_NAME` `…-r1` u auditu, `…-r2` ovde (PR #2). Kao izvor CSS pravila zamenjen je SC-CODE-01 |

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 3. Šta nije preneto i zašto

| Dokument (izvor) | Razlog |
|---|---|
| `Snail-City-0.8.93-SOURCES.md` (projekat) | opisuje drugi build (0.8.93 u test-2); linije ne važe za test1. Njegova pravila su u SC-AGENT-01 i SSOT, mapa koda u SC-ARCH-01 i SC-FUNC-01 |
| `Snail-City-Faza-4-detaljna-revizija-v2.md` (projekat) | cilj je 0.8.87, a izvršni kod tada nije bio pročitan; matrica 42 animacije koristi imena iz v174 koja u test1 uglavnom ne postoje. Zamenjen [inventarom animacija](./qa/SC-ANIMACIJE-0.8.92-INVENTAR.md); ekonomske stavke EC-01–EC-10 ostaju otvorene u projektu |
| `Snail-City-P1-izolacija-zastoja.md`, `Snail-City-P1-prodavnica.md` (projekat) | merenja na buildu `0.8.90-p1-startup-probe`; ne mogu se ponovo proveriti bez tadašnjih trace-ova i priloga. Zaključci su već u PL-01/CSS-01 |
| `PW-01-MIGRATION-AND-QA.md` (projekat) | istorija 0.8.90; ono što je i dalje tačno za 0.8.92 provereno je u [PW-01 stanje](./tehnika/pwa-offline/PW-01-STANJE-0.8.92.md) |
| `claude/dokument-promena.md` (projekat) | jedan dnevnik promena; dupla kopija bi se razišla |
| Istorijski izveštaji `snail-city-test/docs` (arhitektura 0.8.21–0.8.87, PW-01 0.8.88–0.8.90, cloud v1.0.7, IndexedDB 0.8.87) | opisuju starije buildove; dostupni u [snail-city-test/docs](https://github.com/tihidon/snail-city-test/tree/1e3258f/docs) |
| `AGENTS.md` (`snail-city-test`) | zadatak je bio `docs/`; vidi §6 |

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 4. Ispravke nađene pri proveri

Netačne tvrdnje u izvornim dokumentima, provereno nad kodom 25.11.2026:

| Tvrdnja u izvoru | Stvarno stanje | Gde je ispravljeno |
|---|---|---|
| „verzijske tačke: 4 sa `version.json`“ (SC-RAD-01), „3 tačke“ za test1 (SC-REND-01) | **šest mesta**: build tag u `#sc-startup-trace`, `SC_PWA_STATUS.version`, `<title>`, `const VERSION`, komentar i `CACHE_NAME` u `sw.js`. `SC_PWA_STATUS.version` postoji i u 0.8.90 i alat ga ne proverava | SC-RAD-01 §3, SSOT, SC-REND-01, SC-CODE-01 §9 |
| „build tag ne postoji“ | postoji: `build:'0.8.92-css-unified-p1'` u `#sc-startup-trace` | SC-RAD-01 §1, §8 |
| „samo 2 od 26 `@keyframes` van compositora“ | 3: i `logo-fill` animira `clip-path` | SC-REND-01 §6 |
| lista brzina `[…,60]` (SC-AGENT-01) | `[10,20,30,40,50,55]` | SC-AGENT-01 §2 |
| linije modula i funkcija iz 0.8.93 | u test1 su drugačije (npr. `applyCommand` L2678, ne L2690) | SC-ARCH-01 §4, SC-FUNC-01 §4 |
| K01 ikonice, K02 `_headers` (0.8.93) | u test1 rešeno | SC-FUNC-01 §3 |
| šest `.map-controls` deklaracija obrisano | u test1 selektor i dalje postoji u 2 grupna pravila | SC-BRISANJE-3-PROVERE (napomena) |

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 5. Održavanje kopija

- Opšta pravila (SSOT, PL-01, SC-CODE-01, SC-RAD-01, SC-REND-01) održavaju se kanonski u `tihidon/test1`. Istorijske izvore i commit reference sačuvati; nema obaveznog prenosa iz starog repoa.
- Činjenice o ovom buildu (linije, verzije, putanje) važe za `2d66e55`. Posle izmene `index.html` regenerisati [SC-FUNC-01](./tehnika/standardi/SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md) (SC-F08) i ažurirati SC-RAD-01 §3 i SC-ARCH-01 §4 u istom PR-u.
- Mesto u kodu se navodi imenom funkcije ili sidrom; broj linije samo uz commit.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 6. Otvoreno

1. **Javnost `docs/`:** konfiguracija u repozitorijumu objavljuje whitelist fajlova iz `dist/`. Stvarni Netlify deploy i podešavanja sajta nisu provereni u ovom pregledu.
2. **`AGENTS.md` u korenu test1:** dodat u PR #4 (spojen); sadrži redosled čitanja i ključna pravila sa vezom na ovaj indeks.
3. **`verify_edit.py` K2:** ispravka (šest tačaka, `version.json` opcion) je u PR #13 `snail-city-test`, istorijski status PR-a, nije aktuelna potvrda. Ranije provereno: test1 PASS, build tag 0.8.91 u kopiji FAIL.
4. **`snail-city-test` SC-RAD-01 §3:** broj verzijskih tačaka ispravljen na šest u PR #13 (istorijski status, nije aktuelna potvrda).
5. PW-01 na uređaju, vizuelni QA i animacije za 0.8.92: NIJE TESTIRANO.
6. PR #12 u `snail-city-test` (SC-REND-01, SC-CODE-01, SC-RAD-01) spojen je 25.11.2026 kao `f32b290`. Kopije u ovom repou su rađene sa `12f986c`, koji je sadržan u tom spajanju.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 7. Agent upgrade v1.1.0 (25.11.2026)

- [SC-BUILD-01](tehnika/standardi/SC-BUILD-01-PYTHON-BUILD.md) — izolovani istorijski round-trip, current-source gate, build/publish identitet.
- [SC-LOOP-01](tehnika/standardi/SC-LOOP-01-LOOP-I-BUG-AUDIT.md) — AST kandidati, watchdog, lifecycle, PL-01, agent retry.
- [SC-CLI-01](alati/SC-CLI-01-AGENT-INSTALACIJA.md) — projektna instalacija, zavisnosti, komande, eval.
- [SKILL.md](../.agents/skills/snail-city-engineering/SKILL.md) — operativni ulaz, postojeći standardi ostaju kanonski.

Novi standardi su pripremljeni na osnovu commita 360efc7a88897c50a7d58305e1cbef0794191c53; stariji identiteti u odeljcima 1–6 nisu trenutna verifikacija. Netlify konfiguracija sada postoji i objavljuje whitelist u dist/; ne menja se u ovom upgrade-u. Python/JS i official CLI rezultate vezati za tačan commit i izvršne logove. Originalne projektne priloge i raniji overlay ZIP nije bilo moguće ponovo pročitati u ovom okruženju; postojeća test1 izdanja standarda sačuvana su bez prepisivanja. Ne tvrditi byte-identical prenos kompletnog v1.0.0/v1.1.0 paketa.

## 8. Chromium Runtime QA — kandidat v1.0.0

[SC-QA-02](tehnika/standardi/SC-QA-02-CHROMIUM-RUNTIME.md) i [skill](../.agents/skills/chromium-runtime-qa/SKILL.md). Testni alati tools/qa/; zaseban CI job. Baseline 325ff6a9965a4081bda55f55eb7a35a1881b2e10. Scope: shell identity, worker/cache, offline navigation, external watchdog, trace and CPU sample; gameplay/state/device and actual agent activation remain separate. No game version or publish changes.

## 9. QA v1.0.1 i Agent Reliability v1.0.0

[SC-QA-02](tehnika/standardi/SC-QA-02-CHROMIUM-RUNTIME.md): CI incident Ubuntu 26.04/Playwright 1.56, pin browser runner 24.04 i setup diagnostics. [SC-REL-01](tehnika/standardi/SC-REL-01-AGENT-RELIABILITY.md): nezavisni evidence contract, checker fixtures i behavioral eval katalog. [Agent Reliability skill](../.agents/skills/agent-reliability/SKILL.md). Stvarno ponašanje agenta još NOT RUN. Bez promene igre.

## 10. Shared Decision Chain
[SC-DEC-01](tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md), zajednički D0–D8, tools/reliability/check_decision.py i regression fixtures; postojeći CI discovery pokriva nove testove. Verzije skillova 1.2.0 / 1.1.0 / 1.1.0. Runtime igre nepromenjen. Trace(2).zip analiza BLOCKED, stvarni agent eval NOT RUN.

## 11. Executable complexity controls
[SC-CODE-02](tehnika/standardi/SC-CODE-02-IZVRSNA-KONTROLA-KOMPLEKSNOSTI.md): canonical SC-CODE-01 tools installed, historical baseline preserved, current ratchet and locations, loop inventory and Chromium fixtures/live DOM. CI candidate; no runtime game changes.

## SC-DEBUG-01 phase A
[Pouzdano debugovanje](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md): selected lint ratchet, exact AST duplicates, separate CDP counts/CSS deltas and shared specialist handoff. Candidate; game unchanged.

## SC-DEBUG-01 phase B
Functional contract in [SC-DEBUG-01](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md#phase-b--functional-contract-and-scope-candidate). Six real UI/IDB cases, 10 contract fixtures; desktop CI PASS za B01–B06 (vidi §15). No production change. B06 fixture not natural progression, cold offline desktop not Android.

## 12. Team coordination (26.11.2026)

Snapshot koordinacije 26.11.2026: commit `5d57b32919477b6636c9093b2f81b9f8ae897e16`; root `index.html` Git blob `57ff0991646cff4e63c8c74868168905d1004b62`; `src/js/block-00.js` startup build `0.8.92-css-unified-p10`; `sw.js` cache `snail-city-shell-0.8.92-css-unified-p10-r1`. `SC_PWA_STATUS.version` je family `0.8.92`, ne dokaz punog build identiteta. Netlify kopira whitelist root fajlova u `dist/`. SHA-256 HTML-a, svih šest tačaka verzije, build/publish jednakost i runtime nisu ponovo izvršno provereni u ovom docs-only zadatku; ne proglašavati ih PASS. Svaki budući zadatak ponovo utvrđuje identitet iz checkout-a.

[Rendering Performance kandidat](../.agents/skills/snail-city-rendering-performance/SKILL.md) je novo lokalno uputstvo, ne potvrđena kopija zasebnog instaliranog skilla. Koristi postojeći [SC-DEC-01](tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md). Team plugin v0.2.0 ažuriran i ponovo pročitan; agent behavioral eval i nezavisna delegacija NOT RUN/BLOCKED. Bez runtime/SW/deploy izmene.

## 13. Team CI coverage correction (26.11.2026)

PR #38 merged at `f422312`. Run [45738038440](https://github.com/tihidon/test1/actions/runs/45738038440) tooling job passed but its explicit skill list did not include Rendering Performance. Add the existing rendering candidate to `skills-ref validate` and `to-prompt`; do not weaken any existing gate. Correct historical P3 labels in SC-RAD-01 and SC-AGENT-01 without changing normative rules. CI za PR #39 je prošao (vidi §15); nezavisan pregled ostaje otvoren; no game/SW/deploy configuration changes. Official skill validation is not behavioral agent evaluation.

## 14. Model Spec — SC-BEH-01 (26.11.2026)

[Zajedničko ponašanje agenata](tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md), povezano iz AGENTS.md. Koordinator v0.3.0. Jedini evaluacioni katalog proširen na 26 REL/TEAM/BEH slučajeva; behavioral NOT RUN. Bez runtime/SW/deploy izmene.

## 15. Stanje dokaza tima (26.11.2026)

Dokumentacija pregledana na `test1@d82f17e2149c4c9ec5ed8e950c373eb7487f78de`. Različite verzije repo uputstava i ChatGPT paketa imaju zasebne izvore i cikluse provere.

| Oblast | Potvrda i granica |
|---|---|
| CLI, statička analiza, build/publish | `tooling` PASS u [CI za PR #39](https://github.com/tihidon/test1/actions/runs/45738292152), uključujući proveru build/publish bajtova i validaciju strukture uputstava. Rezultat je vezan za taj run. |
| Funkcionalni desktop Chromium | B01–B06 PASS u istom runu. Obuhvata UI, trajnost sejva i hladno offline pokretanje sa prekidom transporta do lokalnog origina. Detalji i raniji B04 FAIL u [SC-DEBUG-01](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md#b04-qa-infrastructure-correction-26112026). |
| Ponašanje agenata | [SC-BEH-01](tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md) definiše 26 slučajeva. Izvršna evaluacija kataloga NOT RUN. D7 nezavisan pregled nije potvrđen. |
| Android, produkcija i performanse | Sveže izvršavanje za ovaj pregled NOT RUN. Za tvrdnju o uzroku zastoja potrebni su originalni trace, konkretan poziv, prvo odstupanje i uporediv kontrolni scenario. |
| Noćni zadatak | Prijavljeno 0/10 ispravki i 0 commitova iz tog zadatka. Lokalni Git bio je blokiran DNS-om. Raniji CI prolazi pripadaju zasebnim PR-ovima. |

## 16. SC-TEAM-004 — infrastructure lesson (26.11.2026)
See [SC-DEBUG-01 infrastructure strategy pivot](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md#infrastructure-strategy-pivot--sc-team-004-26112026). The authenticated API tree was accessible at `8ed4417a6d2e423800a88436b4465a7a28f1dcab`; full local snapshot and runtime were not verified. Engineering/Architecture and AGENTS entry points refer to the same rule. External Coordinator package update and behavioral evaluation remain separate. NS01 oracle is defined in the canonical standard; no game fix claimed.

## 17. Central QA / PMV-01 (26.11.2026)

[SC-PMV-01](tehnika/standardi/SC-PMV-01-POST-MERGE-VERIFICATION-STANDARD.md) — mandatory closure gate for all agents, extending existing G0–G7 and D0–D8. QA-001 found no automatic main-push workflow; proposed existing workflow extension, preserved ratchets and exact checkout verification. ChatGPT Coordinator v0.5.1 package read back; 28 helper fixture tests PASS, independent agent eval not run. Actual post-merge CI and release remain unverified until original evidence exists. No game/SW/deploy change.

## 18. QA-002 — save oracle

[SC-DEBUG-01 QA-002](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md#qa-002--committed-save-oracle-hardening-26112026) records four reproduced false accepts and candidate oracle corrections. 28 local fixture methods passed; real candidate Chromium and independent review remain pending. No production save or game change.
