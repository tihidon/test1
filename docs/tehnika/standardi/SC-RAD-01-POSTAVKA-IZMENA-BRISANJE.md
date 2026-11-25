# SC-RAD-01 — Postavka, izmena i brisanje koda (radni postupak za agente)

> **Stanje identiteta (25.11.2026):** ovaj dokument navodi p1 (`2d66e55`, `index.html` SHA-256 `c19cc1ac…`). Izvršni kod na `main` je **p3** (`5b4b030`, SHA `594026b9…`, `VERSION = '0.8.92-css-unified-p3'`). Tvrdnje o proverama u ovom dokumentu važe za p1 i **nisu ponovo proverene na p3**. Merodavan izvor je [docs/README.md](https://github.com/tihidon/test1/blob/main/docs/README.md).

> **Kopija za `tihidon/test1` (0.8.92-css-unified-p1).** Izvor: [snail-city-test@12f986c](https://github.com/tihidon/snail-city-test/blob/12f986c/docs/tehnika/standardi/SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md) (grana otvorenog PR #12). Provereno prema test1 `main` `2d66e55` (`index.html` SHA-256 `c19cc1ac…`) 25.11.2026: §3 je **prepisan za test1** (izvorni §3 opisuje `snail-city-test` 0.8.90). Postupak (§4–§7) ne zavisi od builda. Izmene u odnosu na izvor: §3 tabela (uključujući ispravku broja verzijskih tačaka), R04 komande, R05. Pregled svih kopija: [docs/README.md](../../README.md).

**Oznaka:** SC-RAD-01 · **Revizija:** 1.0 · **Datum:** 25.11.2026.
**Status:** PREDLOG STANDARDA ZA USVAJANJE (PR). Dokumentacija i alat za proveru; **runtime igre nije menjan**.
**Opseg:** tri radnje koje agenti najčešće rade u Snail City HTML/CSS/JS PWA: **gde se upisuje nov kod**, **kako se menja postojeći** i **kako se briše**. Važi za AI agente, developere i reviewere.
**Modalitet:** **MORA** = uslov prihvatanja · **ZABRANJENO** = blokira merge · **PREPORUČENO** = primeniti kada se uklapa.

## Sadržaj

1. [Zašto ovaj dokument postoji](#1-zašto-ovaj-dokument-postoji)
2. [Hijerarhija autoriteta](#2-hijerarhija-autoriteta)
3. [Činjenice o kodu koje agent mora znati](#3-činjenice-o-kodu-koje-agent-mora-znati)
4. [Postavka: gde ide nov kod](#4-postavka-gde-ide-nov-kod)
5. [Izmena: kako se menja bez kvara](#5-izmena-kako-se-menja-bez-kvara)
6. [Brisanje: dokaz po vrsti](#6-brisanje-dokaz-po-vrsti)
7. [Kontrolna lista za PR](#7-kontrolna-lista-za-pr)
8. [Otvorena pitanja za odluku vlasnika](#8-otvorena-pitanja-za-odluku-vlasnika)
9. [Izvori](#9-izvori)

## 1. Zašto ovaj dokument postoji

Pregled `docs/tehnika` (25.11.2026, `main` `08402be`) pokazao je:

- **Pravila su rasuta u devet izvora** (AGENTS.md, SSOT, PL-01/CSS-01, SC-CODE-01, SC-BRISANJE-3-PROVERE, uputstva projekta i tri dokumenta koja postoje samo u claude.ai projektu: SC-AGENT-01, SC-ARCH-01, SC-FUNC-01). Pravila se preklapaju, a redosled važenja nije jasan. To je isti problem koji SSOT zabranjuje u kodu.
- **Agent koji radi samo iz repoa ne vidi** SC-AGENT-01, SC-ARCH-01 i SC-FUNC-01, a SC-CODE-01 i C11 se na njih pozivaju za brisanje i QA.
- **Nema pravila za bezbedno uređivanje** `index.html`: 7 MB, od toga 91% u 20 linija ugrađenih resursa. Najčešći kvar agenta (skraćen ili prepisan fajl) nije bio pokriven.
- **Brisanje nema opšti postupak.** `SC-BRISANJE-3-PROVERE.md` je zapis jednog čišćenja CSS-a, ne standard. Brisanje funkcije, polja sejva, keša ili asseta nije bilo opisano.
- **Zastarele činjenice stoje kao važeće:** `app.js` (ne postoji), `main` = 0.8.21 (sada 0.8.90), kontrolni test `qa/race-v075-smoke.cjs` (ne postoji), `.github/scripts/sync_zip.py` (uklonjen), `APP_VER` i `tt()` (ne postoje u kodu; „build tag“ postoji kao `build:` u `#sc-startup-trace`).

Ovaj dokument ne ponavlja SC-CODE-01 (oblik CSS/DOM/funkcija) ni PL-01 (merenje). Propisuje **postupak**, a na njih se poziva po oznaci.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 2. Hijerarhija autoriteta

Kad se dva izvora ne slažu, važi viši red. Konflikt se upisuje u PR; ne rešava se pretpostavkom.

| Red | Izvor | Uloga |
|---:|---|---|
| 1 | Izvršni kod na `main` (`index.html`, `sw.js`, `version.json`, `manifest.webmanifest`) | **Činjenica.** Dokument koji mu protivreči je zastareo. |
| 2 | Odluke vlasnika (odeljak „Odluke“ u dokumentu promena) | Šta se sme menjati i šta ostaje kako jeste. |
| 3 | [AGENTS.md](https://github.com/tihidon/snail-city-test/blob/1e3258f/AGENTS.md) | Kratak indeks obaveznih pravila; ne nosi detalje. |
| 4 | Specijalizovani standardi, svaki za svoju oblast | [SSOT](./PRAVILO-JEDAN-IZVOR-ISTINE.md) — vlasnici podataka · [PL-01/CSS-01](./SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md) — layout i merenje · [PW-01](https://github.com/tihidon/snail-city-test/blob/1e3258f/docs/tehnika/pwa-offline/SC-v0.8.90-STABLE-PW01-ANDROID.md) — offline i sejv · [SC-CODE-01](./SC-CODE-01-CSS-DOM-FUNKCIJE.md) — oblik koda · **SC-RAD-01** — postavka, izmena, brisanje |
| 5 | Istorijski izveštaji i auditi (`docs/analize`, `docs/istorija`, verzionisani izveštaji) | **Nikad autoritet.** Dokaz o prošlom stanju. |

- U okviru reda 4 za svoju oblast važi specijalizovani standard (npr. za sejv PW-01 ima prednost nad SC-RAD-01 §5).
- Dokumenti koji postoje **samo** u claude.ai projektu nisu dostupni agentu iz repoa. Dok se ne prenesu (§8), pravila potrebna za tri radnje iz ovog dokumenta navedena su ovde.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 3. Činjenice o kodu koje agent mora znati

**Za test1** (provereno 25.11.2026 na `main` `2d66e55`, `index.html` SHA-256 `c19cc1ac67a2ccc1…`). Komande za ponovnu proveru su u zagradama. Vrednosti za `snail-city-test` 0.8.90 su u [izvornom dokumentu](https://github.com/tihidon/snail-city-test/blob/12f986c/docs/tehnika/standardi/SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md#3-činjenice-o-kodu-koje-agent-mora-znati).

| Činjenica | Vrednost u test1 |
|---|---|
| Raspored repoa | `index.html`, `sw.js`, `manifest.webmanifest`, `_headers`, `img/` (3 ikonice), `privacy.html`, `delete-account.html`, `docs/`. **Nema** `version.json`, `test/`, `tools/`, `AGENTS.md`, `.github/` |
| Izvršni HTML | jedan `index.html`, 7.404.866 B, 8.355 linija, UTF-8 bez BOM, LF (`wc -c`, `wc -l`, `file`) |
| Ugrađeni resursi | **23 linije duže od 20.000 znakova nose ~6,77 MB (91% fajla)**: data-URI slike i JSON asseti |
| `<script>` tagovi | 21, od toga **5 izvršnih** (`sc-startup-trace`, `sc-pwa-bootstrap` i tri bloka bez `type`, od kojih jedan postavlja `SC_LEGACY_CLOUD` sa javnim `sb_publishable` ključem); ostali su `application/json` / `text/plain` asseti |
| `<style>` blokovi | **1** (`sc-main-css`; C01 ispunjen) |
| Moduli glavnog bloka, redom | `catalog`, `progression`, `islandEvents`, `playerProgress`, `domain`, `frames`, `physics`, `race`, `renderer`, `sceneManager`, `scenes`, `storage`, `ui`, `metrics`, `cloud`, `i18n`, `app` (`grep -noE 'modules\.[A-Za-z0-9]+ *='`); registar funkcija: [SC-FUNC-01](./SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md) |
| Verzijske tačke | **šest** (`python3 -c` pretraga literala `0.8.9…`, 25.11.2026): u `index.html` `build:'0.8.92-css-unified-p1'` u `#sc-startup-trace` (to je „build tag“), `version:'0.8.92'` u `SC_PWA_STATUS` (`#sc-pwa-bootstrap`), `<title>Snail City 0.8.92</title>`, `const VERSION = '0.8.92-css-unified-p1'`; u `sw.js` komentar u prvoj liniji (`v0.8.92`) i `CACHE_NAME = 'snail-city-shell-0.8.92-css-unified-p1-r2'`. `version.json` i `APP_VER` ne postoje. **Ispravka:** izvorni SC-RAD-01 je izostavio `SC_PWA_STATUS.version` (postoji i u 0.8.90), a `verify_edit.py` K2 ne proverava ni nju ni build tag |
| Prevod | `modules.i18n` + `EN_DICTIONARY`. **`tt()` ne postoji** |
| Escape | `const escapeHtml=v=>…` (jedan; 82 poziva) |
| Listeneri | 22 `addEventListener`, 0 `removeEventListener`, 0 `AbortController` |
| Prazni `catch {}` | 4: `oldLocalSave` (namerno, čuva stari ključ), podešavanja i analitika u `localStorage` |
| Sat | `setInterval(settleClock,1000)` osvežava prikaz; vreme igre daje `nowBound()`, tajmeri se računaju iz sačuvanih rokova |
| Testovi i alati | u repou nema testova ni alata; provere se pokreću iz klona `snail-city-test` (R04). PW-01 test `pw01-stable.test.cjs` pisan je za 0.8.90 i **nije** pokretan nad test1 |

**MORA:** mesto u kodu se navodi **sidrom koje se može pretražiti** (ime funkcije, `id` bloka, jedinstven niz), ne brojem linije. Brojevi linija se pomeraju sa svakom izmenom; dokumenti koji citiraju `L759` ili `index.html:3901` važe samo za svoju verziju.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 4. Postavka: gde ide nov kod

### P01 — Prvo pretraga (MORA)
Pre nove funkcije, polja, liste, stila ili asseta: `git grep -n` za ime **i** za ponašanje (sinonim, srpski i engleski naziv, deo imena). Ako postoji vlasnik, proširuje se on (SSOT, SC-CODE-01 J10). U PR se upisuje komanda pretrage i rezultat.

### P02 — Mapa vlasnika (MORA)

| Šta se dodaje | Gde ide | Ne sme |
|---|---|---|
| Polje stanja igrača | model u `modules.domain` + `validateSave` + `migrateLegacy` u `modules.storage` + test sa starim snimkom (§5 R07) | zaseban `localStorage` ključ, podatak samo u DOM-u ili lokalnoj promenljivoj ekrana |
| Cena, nagrada, XP, resurs | komanda u `applyCommand` | računanje u handleru ili prikazu (SC-CODE-01 D04) |
| Tajmer (leženje, uzgoj, žetva) | apsolutni rok u stanju (`…Ts` / `…untilTs`) i obračun u `settleClock` | `setTimeout`/`setInterval` kao izvor istine |
| Konstanta ili lista | jedan `Object.freeze` u modulu vlasnika (primer `modules.race.RACE_SPEED_OPTIONS`) | kopija u UI-ju ili handleru |
| Crtanje | `modules.scenes` (`paintMap`, `paintRace`) kroz postojeću petlju (`schedule`/`loop`, jedan rAF) | logika stanja u crtanju, druga rAF petlja |
| Ekran ili panel | `modules.ui`, otvaranje kroz `openScreen()`, akcije preko `data-action` | nov listener po elementu, ekran koji živi skriven |
| Tekst | srpski u markupu + engleski u `EN_DICTIONARY` | drugi rečnik, ručno prevođenje u kodu |
| CSS | postojeći blok, uz pravila iste komponente (SC-CODE-01 C01–C02) | nov `<style>` blok |
| Slika ili zvuk | postojeći `asset-*` JSON blok ili atlas; velika slika nikad u CSS custom property (CSS-01) | nov `<script>` blok samo za jedan resurs bez odluke |
| Offline resurs | `CORE_PATHS` u `sw.js` + test `test/pw01-stable.test.cjs` | drugi Service Worker, keširanje API-ja |
| Test | `test/*.cjs` (Node test runner) | test koji drži drugi runtime autoritet (SSOT) |
| Alat za proveru | `tools/<oznaka>/` sa README | instalacija zavisnosti u repo |
| Standard / izveštaj | `docs/tehnika/standardi/` / `docs/analize/` ili `docs/istorija/` | izveštaj sa naslovom „standard“ |

### P03 — Zabranjena mesta (ZABRANJENO)
Nova globalna promenljiva na `window`/`globalThis` (osim postojećih bootstrap tačaka), nov izvršni `<script>` blok, nov `<style>` blok, nov modul koji duplira postojeći, kod u `sw.js` koji dira IndexedDB ili `localStorage`.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 5. Izmena: kako se menja bez kvara

### R01 — Identitet pre rada (MORA)
Zapisati `git rev-parse HEAD`, `sha256sum index.html` i verziju iz `version.json`. Bez toga nema poređenja pre/posle ni rollback-a.

### R02 — Čitanje monolita (MORA)
- ZABRANJENO: učitavanje celog `index.html` u kontekst ili ispis dugih linija. 91% fajla su resursi; čitanje ih troši, a ništa ne objašnjava.
- Čitati po opsegu linija ili pretragom sa skraćenim izlazom: `grep -n 'settleClock' index.html | cut -c1-200`.

### R03 — Upis izmene (MORA)
- Izmena je **ciljana zamena jedinstvenog sidra**: alat za izmenu koji odbija nejedinstven pogodak, ili skripta koja pre zamene proverava da sidro postoji **tačno jednom**.
- ZABRANJENO: prepisivanje celog fajla iz memorije ili generisanjem; regex zamena preko celog fajla bez brojanja pogodaka; formatiranje celog fajla (Prettier i slično); promena kodiranja (UTF-8 bez BOM) ili kraja linije (LF).
- Jedna tema po izmeni. Raščišćavanje je zaseban kandidat (SC-CODE-01 §2).

### R04 — Provera posle izmene (MORA)

Za test1: komande iz [SC-CODE-01 §8](./SC-CODE-01-CSS-DOM-FUNKCIJE.md#8-alat-i-ratchet-provera) (blok „Za test1“), zatim:

```bash
node --check sw.js      # SW nema automatski test u ovom repou
git diff --stat         # samo očekivani fajlovi
```

**K2 u test1:** alat `verify_edit.py` živi u `snail-city-test` (`tools/sc-rad-01/`), ne u test1. Ispravka K2 (šest tačaka, `version.json` opcion) je spojena u `snail-city-test` (PR #13, commit `26722c4`). U test1 K2 se proverava ručno: iste verzije na svih šest mesta iz §3 (`grep -n '0\.8\.9' index.html sw.js`, pa pregled pogodaka).

`verify_edit.py` proverava: **K1** sintaksu svih izvršnih blokova (`node --check`), **K2** usklađenost šest verzijskih tačaka iz §3, **K3** da je svaka linija ugrađenog resursa bajt-identična osnovi, i izveštava **K4** broj blokova i **K5** obim izmene. Izmena resursa koja je deo zadatka prolazi samo uz `--allow-asset-change`, navedeno u PR-u.

### R05 — Verzija (MORA)
- Izmena izvršnog koda: podići **sve verzijske tačke** iz §3 u istom commitu (u test1 šest mesta); K2 mora proći (u test1 ručno, vidi R04).
- Izmena samo dokumentacije ili alata: **verzija igre se ne podiže**. Nov `CACHE_NAME` bez promene izvršnog koda forsira novu instalaciju Service Workera kod igrača bez razloga (PW-01).

### R06 — Životni ciklus resursa (MORA za nov kod)
- Listener van delegacije dobija `{ signal }` od `AbortController`-a vlasnika ekrana; `abort()` pri zatvaranju uklanja sve njegove listenere odjednom (MDN). Postojeći globalni listeneri žive koliko i aplikacija i ne diraju se bez kandidata.
- Svaki `requestAnimationFrame` van postojeće petlje, `createObjectURL` i WebGL resurs ima mesto oslobađanja u istom PR-u (`cancelAnimationFrame`, `revokeObjectURL`, `delete*`). Obrada `webglcontextlost` već postoji u `modules.renderer`; nov GPU resurs se uključuje u nju.

### R07 — Promena oblika sejva: proširi → prebaci → suzi (MORA)
Postupak „parallel change“: novo se dodaje pored starog, korisnici se prebacuju, staro se uklanja tek kada ga niko ne koristi.
1. **Proširi:** novo polje je opciono, sa podrazumevanom vrednošću; `validateSave` prihvata stari i novi oblik.
2. **Prebaci:** `migrateLegacy` prevodi stari oblik u novi, idempotentno (dvostruko pokretanje daje isti rezultat); test sa stvarnim starim snimkom; backup/checkpoint ostaje.
3. **Suzi:** uklanjanje starog polja je **zasebno, kasnije izdanje**, posle odluke vlasnika (§6, vrsta S).
- ZABRANJENO: promena imena IndexedDB baze, `schemaVersion` ili `localStorage` ključa bez posebne odluke; automatska popravka geometrije ili podataka pri učitavanju (presedan v0.8.55).

### R08 — Greške (MORA)
Postojeći prazni `catch` (§3) su namerni za podešavanja, analitiku i stari ključ. ZABRANJENO je prenositi taj obrazac na sejv, cloud ili ekonomiju: tamo neuspeh mora biti vidljiv i ne sme izgledati kao uspeh (SC-CODE-01 J08).

### R09 — Izveštaj (MORA)
Format odgovora projekta: 1) fajlovi i funkcije koji se menjaju, 2) izmena po funkciji, 3) kako je provereno (komande i izlaz). Neprovereno se piše kao NIJE TESTIRANO, ne kao PASS. Unos u dokument promena u istom odgovoru.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 6. Brisanje: dokaz po vrsti

### Opšta pravila (MORA)
1. Brisanje je **zasebna izmena** sa jednim ciljem; nikad usput uz funkcionalnost.
2. **Git je arhiva.** ZABRANJENO: zakomentarisan kod, kopije `_old`/`-backup` u repou, „privremeno isključeno“ bez roka.
3. Jedno brisanje = jedan commit koji se može vratiti (`git revert`).
4. Dokaz pre brisanja, u PR-u: komande, izlaz i zaključak. **Nula pogodaka je dokaz samo ako je pretraga dokazano radila**: ista komanda mora naći bar jedan poznat, postojeći simbol (kontrolni pogodak).
5. Ime nije dokaz. „v147“, „old“, „legacy“, oznaka u profileru ili izgled „mrtvog“ koda ne opravdavaju brisanje (PL-01).

### Vrste i potreban dokaz

| Vrsta | Potreban dokaz pre brisanja | Posle brisanja |
|---|---|---|
| **C** CSS pravilo ili selektor | tri provere: statička (uključujući klase koje JS sklapa iz delova i u šablonima), runtime (svi relevantni ekrani × 360×780, 390×780, 840×700), vizuelna (pixel-diff 0). Presedan: [SC-BRISANJE-3-PROVERE](./SC-BRISANJE-3-PROVERE.md) | ratchet SC-CODE-01 + `verify_edit.py` |
| **F** JS funkcija ili član modula | 0 poziva: `git grep` za ime, `data-action` vrednosti, string ključeve (`modules.x[name]`, mape komandi), JSON assete. Ako se ime može sklopiti dinamički, smatra se korišćenim. | `verify_edit.py` K1, svi testovi |
| **S** Polje sejva, `localStorage` ključ, IndexedDB struktura | **Direktno brisanje je ZABRANJENO.** Samo „suzi“ korak iz R07, u izdanju posle prebacivanja, uz odluku vlasnika. `migrateLegacy` i dalje čita stari oblik. Korisnički podaci, backup i checkpoint se nikad ne brišu. | test sa starim i novim snimkom, PW-01 regresija |
| **K** CacheStorage | samo keševi sa sopstvenim prefiksom (`OWNED_PREFIXES` u `sw.js`). Service Worker ne dira IndexedDB ni `localStorage`. „Clear site data“, `unregister` ili reset profila nisu popravka. | `test/pw01-stable.test.cjs` |
| **A** Ugrađeni ili spoljni resurs | 0 referenci u HTML, JS, CSS i `CORE_PATHS` (po `id`-u bloka, putanji i delu imena) + screenshot svih ekrana koji ga mogu prikazati | `verify_edit.py --allow-asset-change`, offline test |
| **R** Fajl u repou (duplikat, stari alat) | byte-identičan kanonski fajl (isti Git blob SHA) **ili** 0 referenci u kodu, workflow-ima i deploy inventaru | `git grep` imena fajla = 0 |
| **W** Workflow ili CI skripta | nijedan workflow, skripta ni dokument ga ne poziva kao aktivan postupak | uspešan sledeći CI run |
| **D** Dokument | **ne briše se.** Zastareo se označava na vrhu („ZASTARELO — važi …“ sa vezom), istorijski se premešta u `docs/istorija/` uz pokazivač na starom mestu | provera relativnih veza |
| **G** Funkcija igre (feature, ekran, mehanika) | **samo odluka vlasnika.** Agent predlaže, ne briše. | puna regresija pogođenih tokova |

### Primer kontrolnog pogotka

```bash
git grep -c 'settleClock' -- index.html     # poznat simbol: mora biti > 0
git grep -c 'kandidatZaBrisanje' -- index.html  # tek tada 0 znači 0
```

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 7. Kontrolna lista za PR

- [ ] R01: identitet pre rada (commit, SHA-256, verzija).
- [ ] P01: komanda pretrage postojećih vlasnika i rezultat.
- [ ] P02/P03: kod je kod vlasnika; nema nove globalne, novog bloka ni duplikata.
- [ ] R03: ciljane zamene; fajl nije prepisan ni formatiran.
- [ ] R04: `verify_edit.py` PASS, ratchet PASS, testovi PASS, `git diff --stat` samo očekivani fajlovi (izlazi u PR-u).
- [ ] R05: verzija podignuta na svih šest mesta iz §3 **samo** ako je menjan izvršni kod.
- [ ] R06/R07: oslobađanje resursa; promena sejva po koracima proširi → prebaci → suzi.
- [ ] §6: za svako brisanje vrsta, dokaz i kontrolni pogodak.
- [ ] R09: izveštaj u formatu projekta; neprovereno označeno; unos u dokument promena.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 8. Otvorena pitanja za odluku vlasnika

Ovo dokument ne menja sam, jer se tiče odluka ili fajlova van ovog PR-a.

1. **Preneti SC-AGENT-01, SC-ARCH-01 i SC-FUNC-01 u repo** (ili ih zameniti). Sada ih agent iz repoa ne vidi, a SC-CODE-01 i ovaj dokument se na njih pozivaju. SC-AGENT-01 §13 još sadrži GameMaker pravila (`instance_exists`, Clean Up), iako projekat nema GML.
2. **Uputstva projekta** pominju `APP_VER`, `tt()` i GML pravila (`global.game_data`, `alarm[]`, `buffer_save`), koji u kodu ne postoje; „build tag“ u test1 postoji (`build:` u `#sc-startup-trace`, ispravka 25.11.2026). Predlog: zameniti stvarnim tačkama iz §3 i izbaciti GML deo.
3. **„Tri dnevna prolaza“ u PL-01** nije proverljiv korak i agent ga ne može izvršiti. Predlog: zameniti kontrolnom listom iz §7. Nije menjano bez pitanja.
4. **CI:** `verify_edit.py`, ratchet i `node --test` kao obavezne provere na PR. Zahteva izmenu workflow-a, pa ide u zaseban PR.
5. **SC-CODE-01 ima status „PREDLOG“, a spojen je u `main` (PR #10).** Potvrditi da li je usvojen.
6. **`test/sw-offline.test.cjs` je zastareo** (0.8.89, 18 WebP) i pada na `main`. Predlog: ukloniti ga kao vrstu **R** iz §6 ili prepisati na 0.8.90 inventar. Ne dira se bez odluke, jer je test.
7. ~~**`legacy-scan` iz GoogleChrome/modern-web-guidance** pokrenuti nad `index.html`.~~ **Rešeno 25.11.2026** (odluka vlasnika): pokrenut nad test1 0.8.92, 6 nalaza `js/copying-array-methods` (P3). Alat preskače fajlove veće od 1 MB, pa se pokreće nad izdvojenim skriptama i CSS-om; detalji u [SC-REND-01 §6](./SC-REND-01-CIST-KOD-I-RENDER.md#6-registar-nalaza-n01n12).

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 9. Izvori

Provereno 25.11.2026.

- Martin Fowler — [Parallel Change (expand / migrate / contract)](https://martinfowler.com/bliki/ParallelChange.html)
- MDN — [EventTarget.addEventListener(): opcija `signal`](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)
- GoogleChrome — [modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) (vodiči i `legacy-scan`)
- Projektni standardi: [SSOT](./PRAVILO-JEDAN-IZVOR-ISTINE.md), [PL-01/CSS-01](./SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md), [SC-CODE-01](./SC-CODE-01-CSS-DOM-FUNKCIJE.md), [PW-01](https://github.com/tihidon/snail-city-test/blob/1e3258f/docs/tehnika/pwa-offline/SC-v0.8.90-STABLE-PW01-ANDROID.md), [v0.8.55 sejv presedan](https://github.com/tihidon/snail-city-test/blob/1e3258f/docs/tehnika/podaci-i-cloud/SC-0.8.55-Integracija-i-Save.md)
- Alat: [`tools/sc-rad-01/`](https://github.com/tihidon/snail-city-test/blob/1e3258f/tools/sc-rad-01/README.md)

<sub>[↑ Sadržaj](#sadržaj)</sub>
