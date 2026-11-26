# Snail City — obavezno pravilo: JEDAN IZVOR ISTINE

> **Stanje identiteta (25.11.2026):** ovaj dokument navodi p1 (`2d66e55`, `index.html` SHA-256 `c19cc1ac…`). Istorijski snapshot izvršnog koda bio je **p3** (`5b4b030`, SHA `594026b9…`, `VERSION = '0.8.92-css-unified-p3'`). Tvrdnje o proverama u ovom dokumentu važe za p1 i **nisu ponovo proverene na p3 niti P10**. Merodavan izvor je [docs/README.md](https://github.com/tihidon/test1/blob/main/docs/README.md).

> **Kopija za `tihidon/test1` (0.8.92-css-unified-p1).** Izvor: [snail-city-test@1e3258f](https://github.com/tihidon/snail-city-test/blob/1e3258f/docs/tehnika/standardi/PRAVILO-JEDAN-IZVOR-ISTINE.md). Provereno prema test1 `main` `2d66e55` (`index.html` SHA-256 `c19cc1ac…`) 25.11.2026: svih 19 vlasnika iz tabele postoji u test1 (`git grep`); `RACE_SPEED_OPTIONS` je i ovde `[10,20,30,40,50,55]`, jedna deklaracija; kontrolne komande daju isti rezultat. Izmene u odnosu na izvor: red „Oznaka verzije“ dopunjen za test1 (šest mesta, bez `version.json`). Pregled svih kopija: [docs/README.md](../../README.md).

Datum: 2026-11-22 · Primena: od v0.8.75 · Opseg: svaki budući agent, modul i izmena (HTML/JS PWA).
**Revizija 25.11.2026:** činjenice usklađene sa `main` 0.8.90; tabela vlasnika proširena; GML deo uklonjen (projekat nema GameMaker koda). Postupak postavke, izmene i brisanja: [SC-RAD-01](./SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md).

## Nepregovarljivo pravilo

**Ne praviti novu autorsku listu, konfiguraciju, kolizionu masku, proračun, renderer, sistem tajmera, game-loop ili save-polje ako odgovarajući izvor ili funkcija već postoji.** Prvo pretraži aktivni izvršni kod (deklaracije i sve upotrebe). Proširi postojeći izvor, a sve korisnike usmeri da ga čitaju. Ako postoji stvarni razlog za novu strukturu, dokumentuj zašto se postojeća ne može koristiti, vlasništvo, životni ciklus i dokaz da nema kontradikcije.

Primena za listu brzina trke: `modules.race.RACE_SPEED_OPTIONS` — **jedina vrednosna lista u aktivnoj igri**. Na `main` 0.8.90 i u test1 0.8.92 (provereno 25.11.2026) vrednost je `Object.freeze([10,20,30,40,50,55])`; raniji tekst ovog pravila navodio je `…,60]` iz v0.8.75. Važi kod (SC-RAD-01 §2); poreklo promene 60 → 55 nije upisano u dokumentaciju. `RACE_NORMAL_SPEED` se izvodi iz te liste; panel pauze i toolbar čitaju ovaj isti niz. Ne kopirati taj niz u UI ili handler. Testovi mogu sadržati **očekivanu vrednost** radi nezavisne verifikacije, ali ne i drugi runtime autoritet.

## Redosled pre početka izmene

1. Potvrdi tačan commit, SHA-256 `index.html` i verziju iz `version.json`/`sw.js` (SC-RAD-01 R01). Ne mešaj `main` sa ZIP-om ili testnim kandidatom.
2. Pronađi postojeće funkcije/strukture i sve čitaoce/pisce (`git grep`, pretraga simbola, `data-action`, string ključevi). Nula pogodaka važi samo uz kontrolni pogodak poznatog simbola (SC-RAD-01 §6).
3. Nacrtaj tok: vlasnik podataka → korisnici → proračun → crtanje → UI → potvrda → save.
4. Uvedi najmanji patch **u vlasnika podataka**; ukloni duplikate, ali ne briši stare podatke igrača.
5. Izvedeni keš je dozvoljen **samo** ako ima jasno označenog vlasnika, važi za jednu sesiju/raspored i nema poslovna pravila. Ne sme se čuvati u sejv kao novi izvor istine.
6. Testiraj negativne i pozitivne slučajeve, JS sintaksu, realni Chromium render i staro stanje; Android FPS i produkciju označi kao neproverene ako nisu zaista mereni.
7. Završni izveštaj: urađeno / delimično / nije urađeno, sa tačnim dokazima i otvorenim rizicima.

## Autorski autoriteti koje ne duplirati

| Oblast | Postojeći vlasnik |
|---|---|
| Teren i trajne prepreke grada | `FIELD.rows` → `forbiddenCell()` |
| Osnova objekata / sidrište | `SC_STRUCTURE` → `supportFootprint()` |
| Gradnja | `placementRules()` → `fitsTerrain()` / `canPlace()` |
| Položaji objekata | `s.islandPositions` |
| Vizuelna projekcija grada | `mapRect()` → `scBuildVisualInstances()` |
| Brzine trke | `modules.race.RACE_SPEED_OPTIONS` |
| Fizika i kolizije trke | `modules.physics.integrate()` / `step()` |
| Perspektiva i orijentacija trke | `modules.race.createProjection()` |
| Crtanje staze | `modules.scenes.paintRace()` u postojećem rendereru |
| Nagrade i promena profila | postojeći reducer / `applyCommand()` |
| Render petlja | postojeći `schedule()` / `loop()` (jedan rAF) |
| Lokalni i cloud sejv | postojeće `modules.storage` (`repository()`) i `modules.cloud` |
| Validacija i migracija sejva | `validateSave()` / `migrateLegacy()` |
| Tajmeri u realnom vremenu | sačuvani apsolutni rokovi u stanju → `settleClock()` |
| Prelaz ekrana | `openScreen()` |
| Prevod | `modules.i18n` + `EN_DICTIONARY` (`tt()` ne postoji) |
| Escape dinamičkog HTML-a | `escapeHtml` |
| Offline keš | `sw.js`: `CORE_PATHS`, `OWNED_PREFIXES`, `CACHE_NAME` |
| Oznaka verzije | `<title>`, `const VERSION`, `CACHE_NAME`, `version.json` (`APP_VER` ne postoji). **U test1 nema `version.json`;** verzija je na šest mesta: build tag u `#sc-startup-trace`, `SC_PWA_STATUS.version`, `<title>`, `const VERSION`, komentar i `CACHE_NAME` u `sw.js` ([SC-RAD-01 §3](./SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md#3-činjenice-o-kodu-koje-agent-mora-znati)). |

### Obavezni kontra-primer

**ZABRANJENO:** `[10,20,30,40,50]` u UI funkciji, pa `const speeds=[10,20,30,40,50]` u handleru. To su dva autoriteta koja se mogu razići.

**ISPRAVNO:** jedna zamrznuta lista u domenskom `modules.race`, oba prikaza je uvoze/čitaju. Pri promeni najveće brzine menja se **samo jedna deklaracija**.

### Granica pravila

Pomoćni render-keš (`roadRows`) ili izvedeni parovi za fizičke sudare (`race.collisionPairs`) **nisu nova poslovna lista**: vrednosti se računaju iz postojećeg autoriteta, nisu editable, ne ulaze u save i brišu se zajedno sa privremenom scenom.

## Kontrolni test

**Ispravka 25.11.2026:** ranije navedeni `node qa/race-v075-smoke.cjs` bio je deo ZIP-a v0.8.75 i **ne postoji u repou** (`qa/` sadrži samo `boot-measure.js`). Dok se test ne vrati, provera iz korena repoa:

```bash
git grep -c 'RACE_SPEED_OPTIONS *=' -- index.html          # očekivano 1 (jedna deklaracija)
git grep -c '\[10,20,30,40,50\]' -- index.html             # očekivano: bez izlaza, kod 1 (nema stare petočlane kopije)
git grep -c 'RACE_SPEED_OPTIONS' -- index.html             # kontrolni pogodak: > 1 (čitaoci postoje)
```

Ovo potvrđuje jedan autoritet, ne ponašanje trke. Fizika i balans trke se proveravaju null testom (identičan tim, očekivano 25%).
