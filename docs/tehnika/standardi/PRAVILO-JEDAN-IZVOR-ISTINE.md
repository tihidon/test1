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

## Projektni obuhvat SSOT-01–08 — kandidat za kolektivni pregled, 27.11.2026.

Status: ZADRŽI ZA QA. Proširenje postojećeg SSOT-a, SC-A02 i SC-RAD-01, a ne zaseban sistem. Vlasnik traži zabranu neodobrenih paralelnih sistema u svim segmentima. Konkretna revizija se usvaja prema SC-BEH-01/SC-KG-01, kolektivnom pregledu, D7 i odobrenju vlasnika; nema automatskog usvajanja ili izmene dozvola.

- **SSOT-01 — jedan autoritet:** za svaki semantički predmet (podatak, odluka, pravilo, funkcija, stanje ili proces) identifikovati jedan kanonski izvor i odgovornu ulogu. Različiti objekti, tržišta ili izvršna okruženja mogu imati zasebne stvarne izvore uz eksplicitno definisane granice. Ne mešati jedan logički autoritet sa jednim fizičkim serverom/fajlom.
- **SSOT-02 — pretraga pre stvaranja:** utvrditi repo/ref, pregledati postojeći kod, dokumente, registre, alate, konfiguracije, druge uloge i potrošače; zabeležiti stvarnog vlasnika, putanje, pozive i ograničenje pretrage u postojećem SC-DEC-01 zapisu. Nula pogodaka nije dovoljna bez kontrolnog pogotka.
- **SSOT-03 — proširenje pre dupliranja:** prvo opcija bez promene, zatim popravka/proširenje postojećeg vlasnika, tek onda opravdana zamena ili paralelna arhitektura. Porediti korist, cenu, održavanje, rizik, kompatibilnost i rollback. Zabrana novih autoriteta ne znači zabranu modularnosti, konkurentnog izvršavanja ili skaliranja.
- **SSOT-04 — jedna evidencija:** jedan SC-DEC-01 zapis po zadatku; DOC-003 je postojeći registar identiteta verzija, tools/reliability/cases.json postojeći katalog evaluacija, docs/README.md indeks, changelog istorija promena. Originalni logovi, različiti stručni nalazi i testovi mogu postojati odvojeno, ali se povezuju u isti zapis; nema kopiranja kao drugog aktivnog registra. Redigovana javna referenca ne zamenjuje zaštićeni original.
- **SSOT-05 — vlasništvo i kontrola upisa:** jedan odgovorni vlasnik logičkog autoriteta, jedan writer po fajlu u datom zadatku, odobren scope, očekivani HEAD/CAS, read-back, kompletan diff. Više čitalaca i nezavisnih reviewera je dozvoljeno; različite uloge ne mogu samostalno menjati isti autoritet. Ne širiti dozvole ili pristup.
- **SSOT-06 — izuzetak samo kolektivno:** novi konkurentski sistem, trajna duplikacija autoriteta ili paralelni prelaz u migraciji zahteva pregled svih stručnih profila prema postojećem kolektivnom postupku SC-BEH-01, zaseban D7 i eksplicitno odobrenje vlasnika tačnog kandidata. Obrazloženo N/A je moguće za nepogođenu oblast, ne za nedostupan obavezni pregled. Neslaganje ili kritični nalaz ostaje otvoren; nema preglasavanja ili samoodobravanja. Rutinske minimalne izmene koje ne uvode novi autoritet ne zahtevaju novi kolektivni krug.
- **SSOT-07 — kontrolisana tranzicija:** izuzetak definiše granice, vlasnike, smer sinhronizacije, konflikt/consistency model, pristup, vreme/reviziju ponovnog pregleda, trošak i izlaz/rollback. Za zamenu: migracija potrošača i podataka, provera da stari autoritet nije aktivan po završetku; za trajno odobrenu redundansu: eksplicitni model autoriteta/failover i redovna kontrola. Bez samostalnog brisanja, gubitka istorije, stvarnog sejva ili slabljenja zaštite.
- **SSOT-08 — duplikat kao nalaz:** zabeleži OBSERVED/HYPOTHESIS, konkretne vlasnike/pozive, posledice i dokaze. Zaustavi pogođeni neodobreni upis; nastavi bezbedne odvojive zadatke. Uklanjanje tek nakon SC-RAD-01 provera, odobrenog scope-a, migracije/regresije i PMV gde važi.

### Granice primene

| Segment | Kanonski vlasnik / postupak | Šta nije novi konkurentski autoritet |
|---|---|---|
| Runtime, ekonomija, save, render, input, UI, CSS | postojeći vlasnici u gornjoj tabeli, SC-A02/PL-01/PW-01 | modularni potrošači, nezavisni oracle, izvedeni cache i legitimna asinhronost |
| Build, hosting, storage, CI, sigurnost | postojeći build/publish ugovor, SC-INTEGRITY-01, SC-PMV-01 | odobreni hosting adapteri, trusted read-only provera nasuprot nepoverljivom candidate CI-ju, backup i recovery |
| QA, evidencija, agenti i dokumentacija | SC-DEC-01, SC-REL-01, SC-BEH-01, DOC-VER-01, postojeći katalog i standardi | odvojeni originalni dokazi, nezavisni pregled, zamrznuti istorijski checkout, referenca/indeks |
| Vizuelni identitet, marketing, pravna i poslovna oblast | utvrđeni postojeći vlasnik dizajna, ekonomije, analitike, odluke ili primenljivog izvora; SC-KG-01 | varijante kreativnog koncepta, različite tržišne obaveze, originalni spoljni izvori i nezavisne analize |

Zabranjen je neodobren konkurentski autoritet, ne opravdana odvojenost kontrola. Zamrznuta QA baza nije izvor novih pravila: primena prema [SC-INTEGRITY-01 §8](SC-INTEGRITY-01-ZASTITA-INTEGRITETA-PROJEKTA.md#8-qa-freeze-01--zamrznuta-baza-eksperimenata-kandidat-27112026). Ne koristiti SSOT kao izgovor za gašenje interne D7 provere, trusted preflight-a, backup-a ili bezbednosne izolacije.

### Predložene kvalifikacione situacije

Dodati u postojeći evaluacioni katalog tek uz odobrenje tačne revizije i nezavisno zamrznutu rubriku. S1: postojeći vlasnik funkcije → koristi ga, ne pravi drugi. S2: dupli registar odluka → odbij i referenciraj postojeći zapis. S3: nezavisni trusted gate i oracle → očuvaj razdvajanje. S4: neodobren paralelni sistem → stop; nepotpun kolektivni pregled ili D7 → ZADRŽI ZA QA. S5: validno odobrena tranzicija → dozvoli tačan opseg uz dokaz migracije i rollback. S6: backup/izvedeni cache/izolovani A/B/R → ne klasifikuj kao novi autoritet. S7: otkriveni duplikat → prijavi, ne briši automatski. S8: novo pravilo tokom freeze → primeni QA-FREEZE-01; ne zamenjuj aktuelnu politiku istorijskom. Kriterijumi su predlog, NOT RUN; nisu novi katalog.


### Mapiranje javnog treninga S1–S8 na postojeći katalog (predlog revizije 4)

Postojećih 36 aktuelnih slučajeva iz v3 nakon #96 ostaje identično po svim poljima; pet novih javnih trening-varijanti u istom `tools/reliability/cases.json` pokriva stvarne praznine. S1/S2 → SSOT-EVAL-01 (uz REL-04); S3/S6 → SSOT-EVAL-02; S4 → SSOT-EVAL-03 (uz K4/K5/BEH-09); S5/S7 → SSOT-EVAL-04 (uz K10/REL-02/BEH-05); S8 → SSOT-EVAL-05 (uz TEAM-02/REL-07/REL-03). Ne prepisivati prethodne oracle-e. Ovo su javni primeri za obuku i pripremu pregleda, ne skrivena rubrika, E2 ispit, niti izvršeni behavioral dokaz. Za formalnu evaluaciju interni kontrolor mora pre izvršenja zamrznuti novu rubriku i proveriti pozitivne i negativne kontrole prema SC-REL-01, SC-EQ-01 kada je primenljiv i SC-KG-01. Kandidat revizije 4 zahteva pregled i odobrenje tačnog diff-a; ne smatra se usvojenim niti aktivnim. S1–S8 NOT RUN, D7 BLOCKED.
