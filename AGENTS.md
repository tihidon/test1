# AGENTS.md — uputstvo za agente (tihidon/test1)

Ovaj repozitorijum sadrži build Snail City **0.8.92-css-unified-p3** (`index.html` je jedini izvršni fajl igre, plus `sw.js`, `manifest.webmanifest`, `_headers`, `img/`). Izvršni kod na `main` je merodavan: `index.html` SHA-256 `594026b9ffab62ceb8dbbfa181c887edea3f903ff84a27151a2330fb978dc58a`, `VERSION = '0.8.92-css-unified-p3'`, SW `snail-city-shell-0.8.92-css-unified-p3-r2`. Dokumenti koji još pominju p1 (`2d66e55`, SHA `c19cc1ac…`) važe samo za taj commit.

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

Za Snail City razvoj učitaj projektni `.agents/skills/snail-city-engineering/SKILL.md` (Codex: `$snail-city-engineering`), bez učitavanja kompletnog istorijskog registra. Primenjuj [SC-BUILD-01](docs/tehnika/standardi/SC-BUILD-01-PYTHON-BUILD.md), [SC-LOOP-01](docs/tehnika/standardi/SC-LOOP-01-LOOP-I-BUG-AUDIT.md) i [SC-CLI-01](docs/alati/SC-CLI-01-AGENT-INSTALACIJA.md). Stari P3 identitet iz vrha je istorijski; stvarni target/version/hash i publish root proveriti svaki put. Ne pokretati split nad aktivnim src/. Pre i posle runtime izmene dokazati build/publish jednakost; ako nedostaje alat ili postojeći baseline ne prolazi, prijavi BLOCKED/FAIL. Zadržati sve relevantne G0–G7 i ne menjati deploy bez odobrenja.

## Chromium Runtime QA

Za runtime bag, hang, loop, performance, save/offline ili funkcionalni QA koristi i `.agents/skills/chromium-runtime-qa/SKILL.md`. Primeni [SC-QA-02](docs/tehnika/standardi/SC-QA-02-CHROMIUM-RUNTIME.md). Postojeći snail-city-engineering ostaje vlasnik engineering procesa. Novi alati rade samo nad izolovanim kopijama publish fajlova; bez izmena runtime igre. CLI format PASS nije agent eval; shell smoke nije kompletan gameplay/PW-01 ili Android dokaz.

## Agent Reliability

Za audit dokaza, zaključak o popravci, release i kontradikcije učitaj `.agents/skills/agent-reliability/SKILL.md` i [SC-REL-01](docs/tehnika/standardi/SC-REL-01-AGENT-RELIABILITY.md). Nezavisni oracle, dokaz identiteta i izvorni logovi obavezni; structural checker PASS nije agent evaluation. Bez lažnog PASS i bez merge/deploy bez odobrenja.
