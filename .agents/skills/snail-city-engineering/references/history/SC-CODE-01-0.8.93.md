# SC-CODE-01 — Pravila pisanja: CSS, DOM i funkcije

**Oznaka:** SC-CODE-01 · **Revizija:** 1.0 · **Datum:** 25.11.2026.
**Status:** PREDLOG STANDARDA ZA USVAJANJE (PR). Dokumentacija i alat za merenje; **runtime igre nije menjan**.
**Opseg:** Snail City HTML/CSS/JavaScript PWA (Canvas 2D/WebGL, IndexedDB). Važi za AI agente, developere i reviewere, za svaki nov i menjan kod. GameMaker/GML nije deo ovog standarda (projekat nema `.gml`/`.yy`/`.yyp` fajlova; provereno 25.11.2026).
**Modalitet:** **MORA** = uslov prihvatanja · **ZABRANJENO** = blokira merge · **PREPORUČENO** = primeniti kada se uklapa u postojeću arhitekturu.

## Sadržaj

1. [Odnos prema postojećim standardima](#1-odnos-prema-postojećim-standardima)
2. [Osnovni princip: ratchet, ne masovno prepisivanje](#2-osnovni-princip-ratchet-ne-masovno-prepisivanje)
3. [Izmereno polazno stanje](#3-izmereno-polazno-stanje)
4. [CSS pravila (C01–C12)](#4-css-pravila-c01c12)
5. [DOM pravila (D01–D10)](#5-dom-pravila-d01d10)
6. [Pravila za funkcije (J01–J10)](#6-pravila-za-funkcije-j01j10)
7. [Kandidati za raščišćavanje](#7-kandidati-za-raščišćavanje)
8. [Alat i ratchet provera](#8-alat-i-ratchet-provera)
9. [Kontrolna lista za PR](#9-kontrolna-lista-za-pr)
10. [Šta ovaj standard ne radi](#10-šta-ovaj-standard-ne-radi)
11. [Dodatak A: dokazna osnova iz v0.8.92 CSS P1 audita](#11-dodatak-a-dokazna-osnova-iz-v0892-css-p1-audita)
12. [Izvori](#12-izvori)

## 1. Odnos prema postojećim standardima

Ovaj dokument **dopunjuje** postojeća pravila na nivou pisanja koda. Ne ponavlja njihov sadržaj; poziva se na njih po oznaci.

| Postojeći standard | Šta već pokriva | Šta SC-CODE-01 dodaje |
|---|---|---|
| [PRAVILO-JEDAN-IZVOR-ISTINE](./PRAVILO-JEDAN-IZVOR-ISTINE.md) | vlasnici podataka, zabrana paralelnih autoriteta | primena SSOT na CSS selektore, tokene, escape i prevod |
| [SC-PL-01 + CSS-01](./SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md) | layout, canvas resize, A/B/R merenje, Base64 u `var()` | pravila pisanja selektora, kaskade i animacija |
| [SC-BRISANJE-3-PROVERE](./SC-BRISANJE-3-PROVERE.md) | tri provere pre brisanja | primena na CSS čišćenje (C11) |
| SC-AGENT-01 (projektni dokument, A01–A15) | proces, QA gate G0–G7, pristupačnost (A10), performanse (A11) | merljive granice za CSS/DOM/funkcije |
| SC-ARCH-01 (projektni dokument) | struktura modula, kartica funkcije | pravila oblika i veličine funkcije |
| SC-FUNC-01 §4 (projektni dokument, SC-F01–F08) | vlasnik, pozivaoci, lifecycle, brisanje funkcije | dubina, dužina, parametri, ternari |

**Zamenjuje:** `SC-v0.8.92-P1-CSS-SINGLE-SOURCE-AUDIT.md` (repo `tihidon/test-2`) **kao izvor pravila za CSS**. Taj audit ostaje istorijski zapis kandidata; sve njegove činjenice prenete su u [Dodatak A](#11-dodatak-a-dokazna-osnova-iz-v0892-css-p1-audita).

**Konflikt:** ako ovo pravilo protivreči PL-01, CSS-01, SSOT ili PW-01, važi stariji specijalizovani standard, a konflikt se upisuje u PR. Ovaj dokument ne odobrava runtime izmenu.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 2. Osnovni princip: ratchet, ne masovno prepisivanje

1. **MORA:** nov kod poštuje sva pravila iz §4–§6.
2. **MORA:** menjan kod ne sme pogoršati nijednu praćenu metriku iz §8 (ratchet: brojevi smeju samo da padaju ili ostanu isti).
3. **ZABRANJENO:** raščišćavanje postojećeg koda „usput“ u PR-u za novu funkcionalnost, popravku ili balans. Pravilo projekta „menjaj samo ono što je traženo“ ostaje na snazi.
4. **MORA:** raščišćavanje je **zaseban kandidat** sa jednim ciljem (§7), merenjem pre/posle (§8), Chromium screenshot-diff-om i relevantnim QA gate-ovima iz SC-AGENT-01. Ponašanje i izgled moraju ostati identični.
5. **Razlika koju treba znati:** dubina i dužina JS funkcija utiču na **čitljivost i rizik grešaka**, ne na brzinu izvršavanja. Složenost CSS selektora, broj pogođenih elemenata i veličina DOM-a utiču na **računanje stilova i layout** (web.dev, Chrome Lighthouse). Zato se ubrzanje prikaza nikad ne obećava na osnovu JS refaktora.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 3. Izmereno polazno stanje

Izmereno alatom iz §8 (`tinycss2` 1.5.1, `acorn` 8.19.0), bez pokretanja igre. Brojevi su statički: ne govore koliko se pravila primenjuje u runtime-u.

| Metrika | v0.8.90 (`snail-city-test/main`) | v0.8.92-css-unified-p1 (`test-2/dist`) |
|---|---:|---:|
| `index.html` SHA-256 | `a4d53277…a3bd7` | `c19cc1ac…b7c5d` |
| `<style>` blokova / `link rel=stylesheet` | 9 / 0 | **1** / 0 |
| CSS bajtova | 222.077 | 602.653 |
| Selektora (posle razdvajanja zarezom) | 1.583 | 1.568 |
| Selektora sa više od 3 dela | 348 | 341 |
| Najveća dubina selektora | 6 | 6 |
| Isti selektor definisan više puta u istom kontekstu | 156 | 154 |
| Pregažene deklaracije (isti kontekst + selektor + svojstvo) | 470 | 461 |
| `!important` | 76 | 76 |
| Selektora sa `#id` | 597 | 590 |
| Hex boja u CSS tekstu (van stringova i `url()`) | 1.053 | 1.032 |
| Custom property vrednosti > 4.096 znakova (CSS-01) | 5 | 5 |
| Različitih `@media` uslova | 18 | 18 |
| JS funkcija (bez modulskih IIFE omotača) | 943 | 960 |
| Funkcija dužih od 60 / 150 linija | 17 / 3 | 17 / 3 |
| Funkcija sa kontrolnom dubinom > 3 | 11 | 11 |
| Najveća kontrolna dubina | 5 | 5 |
| Funkcija sa više od 4 parametra | 24 | 25 |
| Lančanih ternara (`a?b:c?d:e`) | 71 | 71 |
| `innerHTML =` / `innerHTML +=` | 4 / 0 | 4 / 0 |
| Pisanja `el.style.x =` | 10 | 10 |
| Čitanja geometrije (`getBoundingClientRect`, `offset*`, `client*`, …) | 8 | 8 |
| `addEventListener` / `removeEventListener` | 20 / 0 | 22 / 0 |

**Ispravka ranije procene (25.11.2026):** gruba regex procena istog dana navela je „JS dubinu 10“, „172 bloka dubine ≥ 6“ i „~143 lančana ternara“. AST merenje pokazuje da je to bilo pogrešno: vitičaste zagrade objekata i modulskih omotača nisu kontrolna dubina. Stvarno stanje: **najveća dubina 5, 11 funkcija preko 3, 71 lančani ternar**. JS gnežđenje je umereno; glavni teret su **CSS kaskada i nekoliko predugih funkcija**.

**Najduže funkcije (v0.8.92, glavni skript #5):** `applyCommand` L759 (481 linija), `controls` L5949 (285), `paintRace` L2804 (164), `validateSave` L3027 (114), `migrateLegacy` L3159 (101), `cloudAction` L5620 (96), `attachUI` L6234 (90), `boot` L6341 (89).
**Najdublje (dubina 5):** `paintRace` L2804, `scPaintMapSigns` L2619.
**Postojeći `@media` uslovi:** `prefers-reduced-motion:reduce` (12×), `max-width:620px` (7×), `(orientation:landscape) and (max-height:540px)` (5×), `max-width:540px`, `max-width:380px`, `min-width:700px`, `max-width:350px` (po 3×) i još 11 pojedinačnih širina (365, 360, 420, 440, 480, 500, 600 max; 600 min; 699 max) plus `forced-colors:active` i `prefers-reduced-motion:no-preference`.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 4. CSS pravila (C01–C12)

### C01 — Jedan stilski blok (MORA)
Izvršni HTML ima tačno **jedan** `<style id="sc-main-css">` i **nula** `link rel="stylesheet"`. Nov CSS ide u taj blok. ZABRANJENO: novi `<style>` blok, CSS u JS stringu koji se ubacuje kao `<style>`, ili verzijski „bridge“ blok (`v174 visual bridge`, `polished cards` i slično su uzrok današnjih 10 → 1 blokova).

### C02 — Gde se upisuje novo pravilo (MORA)
- Pravilo za postojeću komponentu upisuje se **neposredno posle poslednjeg postojećeg pravila iste komponente**, ne na kraj fajla.
- Ciljni redosled sekcija (primenjuje se tek kroz poseban kandidat §7-K4, jer premeštanje menja kaskadu): **tokeni (`:root`) → osnova (element selektori) → komponente → ekrani → responsive (`@media`) → pristupačnost (`prefers-reduced-motion`, `forced-colors`) → `@keyframes`**.
- Svaka sekcija počinje komentarom `/* == SC: <naziv sekcije> == */`. Komentari ne nose istoriju verzija; istorija je u Git-u i dokumentu promena.

### C03 — Jedan selektor, jedno pravilo (MORA)
Isti selektor u istom kontekstu (`@media`, `@supports`) postoji **jednom**. Za promenu izgleda menja se postojeće pravilo. ZABRANJENO: novo pravilo kasnije u fajlu koje pregazi staro (današnje stanje: 154 dupla selektora, 461 pregažena deklaracija).

### C04 — Dubina selektora najviše 3 dela (MORA za nov kod)
- Najviše 3 dela odvojena kombinatorima: `.shop-card .price` (2), `.shop .card > .price` (3). Za dublje ciljanje element dobija **sopstvenu klasu**.
- Sadržaj `:is()`, `:where()`, `:not()` se ne broji kao novi deo, ali ZABRANJENO je skrivati dubinu u njima.
- PREPORUČENO: jedna klasa umesto složenog selektora, posebno umesto `:nth-*` lanaca (web.dev: jednostavniji selektor ubrzava računanje stilova).

### C05 — Specifičnost (MORA)
- ZABRANJENO u novom kodu: stilizovanje preko `#id` (danas 590 selektora). `id` služi za ARIA veze, `label for` i JS hook jedinstvenih elemenata, ne za izgled. Po MDN-u svaki ID dodaje `1-0-0` specifičnosti i pobeđuje bilo koji broj klasa.
- ZABRANJENO: nov `!important`. Izuzeci, uz komentar razloga (MDN preporuka): `prefers-reduced-motion` i `forced-colors` blokovi i pomoćna klasa koja mora da sakrije element (`[hidden]`).
- PREPORUČENO: kada treba nadjačati postojeće pravilo, prvo izmeni to pravilo (C03). `:where()` (specifičnost 0) koristiti za osnovna pravila koja komponente treba lako da nadjačaju.
- Cascade layers (`@layer`) se **ne uvode** u ovaj build bez posebnog kandidata: menjaju poredak cele kaskade.

### C06 — Boje i tokeni (MORA za nov kod)
- Nova boja ide kroz postojeći token u `:root` (danas 25 različitih custom properties) ili kroz nov token u sekciji tokena. ZABRANJENO: nova sirova hex/rgb vrednost u pravilu komponente (danas 1.032 hex vrednosti).
- Token se imenuje po ulozi, ne po izgledu: `--sc-text-muted`, ne `--sc-gray-2`.
- Velike slike u custom property: važi **CSS-01** (prag 4.096 znakova). Danas postoji 5 takvih vrednosti; broj sme samo da pada.

### C07 — Raspored i jedinice (MORA)
- CSS Grid i Flex su legitimni rasporedi i **ne brišu se** radi benchmarka (PL-01, CSS-01).
- Bez fiksnih širina kontejnera u `px` gde sadržaj treba da se prilagodi; koristiti `%`, `fr`, `minmax()`, `clamp()` ili postojeće vrednosti.
- Touch ciljevi, kontrast i fokus: važi SC-AGENT-01 A10 (minimum 24×24 CSS px, za touch preferirano 44×44).

### C08 — Animacije (MORA za nov kod)
- Nova animacija menja **samo `transform` i `opacity`**. Po web.dev, to su jedina svojstva koja pregledač animira samo u compositoru; ostala traže više rada i mogu da seku na slabijim telefonima.
- ZABRANJENO u novim animacijama ponovljenih elemenata (kartice, liste): animiranje `width`, `height`, `top`, `left`, `margin`, `box-shadow`, `filter`. Postojeći efekti se ne uklanjaju bez posebnog kandidata i merenja (PL-01).
- `will-change` samo na elementu koji se zaista animira i samo tokom animacije; ZABRANJENO na grupama ili `*` (web.dev: svaki sloj troši memoriju).
- Svaki nov `@keyframes` ima jedinstveno ime sa prefiksom `sc-`. Svaka nova animacija dobija pravilo u `prefers-reduced-motion:reduce` bloku koje uklanja neobavezno kretanje, ali ne i povratnu informaciju (SC-AGENT-01 A10).

### C09 — Selektori koje ne pisati (ZABRANJENO u novom kodu)
- Univerzalni selektor kao poslednji deo (`.panel *`).
- Selektori po delu atributa (`[class*="card"]`, `[style*=...]`).
- Selektor po stanju koje JS ne postavlja eksplicitno: stanje se postavlja klasom ili `data-state` atributom koji postavlja vlasnik komponente.

### C10 — Media upiti (MORA)
- Nov `@media` koristi **postojeću** vrednost (§3). Prednost imaju najkorišćenije: `max-width:380px`, `max-width:540px`, `max-width:620px`, `min-width:700px` i `(orientation:landscape) and (max-height:540px)`.
- Nova širina dozvoljena je samo uz obrazloženje u PR-u (koji uređaj/viewport je razlog). Broj različitih uslova (danas 18) sme samo da pada.
- Pravilo za isti selektor u istom `@media` uslovu upisuje se u postojeći blok tog uslova kada on postoji u istoj sekciji.

### C11 — Brisanje CSS-a (MORA)
Brisanje pravila samo posle **tri nezavisne provere** iz SC-BRISANJE-3-PROVERE i SC-AGENT-01 A12: statičke (uključujući klase koje JS generiše), runtime (svi relevantni ekrani i viewport-i) i vizuelne (pixel-diff). Nula pogodaka u HTML-u nije dokaz: klase se generišu u JavaScript-u.

### C12 — SVG (prenešeno iz SC-CSS-01, v0.8.92 audit)
Trenutni build ne koristi SVG resurse. Nov SVG se uvodi samo uz konkretan funkcionalni razlog, izmerenu korist i Chromium/Android dokaz. Stari SVG ukrasi se ne vraćaju samo radi izgleda. SVG nije univerzalno loš format.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 5. DOM pravila (D01–D10)

Postojeći obrazac (v0.8.92, glavni skript #5): UI gradi HTML string, upisuje ga **jednom** u kontejner (`sheet.innerHTML = html`), a zatim poziva `modules.i18n.apply(sheet)`. Akcije idu preko `data-action` atributa (20 mesta) i jednog delegiranog rukovaoca (`closest('button[data-action]')`). Ova pravila čuvaju taj obrazac i ne uvode drugi.

### D01 — Jedan upis po prikazu (MORA)
Panel ili ekran se gradi kao jedan string i upisuje **jednom** po prikazu. ZABRANJENO: `innerHTML +=` (danas 0), upis u petlji i delimično dopisivanje istog kontejnera u više koraka istog prikaza.

### D02 — Escape je obavezan (MORA, bezbednost)
- Svaka dinamička vrednost u HTML stringu (ime puža, naziv, broj iz sejva, tekst iz clouda) prolazi kroz **postojeći `escapeHtml`** (skript #5, L3487; danas 82 upotrebe). ZABRANJENO: drugi escaper, ručni `.replace('<', …)` ili sklapanje HTML-a od neproverenog teksta. MDN navodi `innerHTML` kao najčešći put za XSS.
- Za promenu samo teksta postojećeg elementa koristi se `textContent`, ne `innerHTML` (MDN preporuka za čist tekst).
- Tekst koji unosi igrač dobija i klasu `player-typed`, da ga `modules.i18n` ne prevodi. **Nalaz 25.11.2026:** `modules.i18n` preskače `.player-typed`, ali u v0.8.92 klasa se **nigde ne dodeljuje** (1 pogodak, samo u selektoru preskakanja). Ime puža koje se poklopi sa ključem rečnika može biti prevedeno. Nije potvrđeno u igri; upisano u „Otvoreno“.
- Atributi sa dinamičkom vrednošću moraju biti pod navodnicima i escape-ovani: `data-id="${escapeHtml(id)}"`.
- ZABRANJENO: inline handleri (`onclick="…"`) u HTML stringu.

### D03 — Prevod (MORA)
Tekst u markupu piše se na **srpskom** i to je ključ. Engleski prevod ide u **postojeći `EN_DICTIONARY`** u `modules.i18n` (jedan rečnik; šabloni sa `{0}` se izvode iz istog rečnika). Posle upisa poziva se `modules.i18n.apply(root)`, a za tekst van DOM-a `modules.i18n.translate()`.
**Konflikt sa uputstvom projekta:** uputstvo kaže „svaki tekst ide kroz `tt()`“, ali funkcija `tt()` **ne postoji** u kodu (0 pogodaka u v0.8.90 i v0.8.92). Važi stvarni mehanizam iznad; uputstvo treba ispraviti.

### D04 — Događaji (MORA)
- Nova akcija = native `<button>` sa `data-action="ime"`, obrađena u **postojećem delegiranom rukovaocu**. ZABRANJENO: nov `addEventListener` po elementu pri svakom prikazu. Pravi drugi put obrade pored delegacije, a ponovno vezivanje na element koji preživi prikaz duplira obradu klika.
- Listener van delegacije (window, document, canvas) ima vlasnika i mesto uklanjanja (SC-F05). Danas: 22 `addEventListener`, 0 `removeEventListener`. To nije automatski greška (globalni listeneri žive koliko i aplikacija), ali **svaki nov** listener koji ne živi do kraja aplikacije MORA imati `removeEventListener` ili `AbortController` signal u istom PR-u.
- Akcija koja menja stanje ide kroz reducer (`applyCommand`); handler ne računa novac, XP ni nagrade (SC-F03).

### D05 — Struktura i veličina DOM-a (MORA za nov kod, merenje u Chromiumu)
- ZABRANJENO: omotač `<div>` koji postoji samo radi stila; raspored ide na postojećeg roditelja.
- Projektni pragovi po otvorenom ekranu, izvedeni iz Lighthouse revizije: **upozorenje iznad ~800 elemenata, greška iznad ~1.400; dubina do 32; do 60 dece jednog roditelja**. Nova lista koja može da pređe 60 stavki (zbirka puževa, istorija trka) dobija stranice ili ograničen prikaz.
- Merenje se radi u stvarnom Chromiumu po ekranu (DOM je dinamičan, statički se ne može izmeriti). Komanda za konzolu je u §8.

### D06 — Ekrani se grade kad zatrebaju (PREPORUČENO, MORA za nove ekrane)
Nov ekran se gradi pri otvaranju kroz `openScreen()` i uklanja ili prazni pri zatvaranju. Ne drže se skriveni gotovi ekrani u DOM-u „za svaki slučaj“ (Lighthouse: praviti čvorove kad su potrebni, uklanjati kad nisu). Postojeće ekrane ne menjati bez posebnog kandidata.

### D07 — Geometrija (MORA)
Čitanja geometrije grupisati **pre** pisanja stilova; bez ciklusa čitanje → pisanje → čitanje u istom frejmu. Detalji i dokazi: PL-01. Danas 8 čitanja; nova čitanja u rAF petlji ZABRANJENA bez merenja.

### D08 — Stilovi iz JS-a (MORA)
Stanje se menja **klasom** ili `data-state` atributom. Dinamička vrednost (procenat, pozicija) ide kroz custom property: `el.style.setProperty('--sc-progress', value)`, a CSS je čita. ZABRANJENO: niz pojedinačnih `el.style.width/height/...` pisanja u novom kodu (danas 10 mesta). Za kretanje DOM elementa u rAF petlji dozvoljen je samo `transform`.

### D09 — `id` atributi (MORA)
`id` samo za jedinstvene elemente: ARIA (`aria-labelledby`), `label for`, JS hook singleton elementa, sidro. Isti `id` nikad dva puta u DOM-u (ponovljene kartice koriste klasu i `data-*`). Ne stilizovati preko `id` (C05).

### D10 — Pristupačnost (MORA)
Važi SC-AGENT-01 A10 (WCAG 2.2 AA cilj, native kontrole, fokus, kontrast, `prefers-reduced-motion`). Ovaj standard je ne ponavlja.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 6. Pravila za funkcije (J01–J10)

Oznake J01–J10 su namerno različite od SC-F01–F08 (SC-FUNC-01), koje pokrivaju vlasništvo, pozivaoce i lifecycle. Ovde se propisuje **oblik** funkcije.

### J01 — Kontrolna dubina najviše 3 (MORA za nov kod)
Najviše 3 ugnježdena nivoa `if`/petlja/`switch`/`try` u jednoj funkciji. `else if` lanac se broji kao jedan nivo. Za dublje: rani `return` (guard clause) ili izdvojena imenovana funkcija u istom modulu.

```js
// ZABRANJENO (dubina 4)
function feed(snail){
  if(snail){
    if(snail.habitatId){
      for(const item of items){
        if(item.type==='food'){ /* ... */ }
      }
    }
  }
}

// ISPRAVNO (dubina 2)
function feed(snail){
  if(!snail?.habitatId) return;
  for(const item of items){
    if(item.type!=='food') continue;
    /* ... */
  }
}
```

### J02 — Bez lančanih ternara (MORA za nov kod)
Jedan ternar je dozvoljen. Lanac `a ? b : c ? d : e` (danas 71) zamenjuje se `if`/`else` ili zamrznutom mapom:

```js
// ZABRANJENO
const label = pct>=1 ? 'full' : pct>=.85 ? 'almost' : pct>=.5 ? 'filling' : 'idle';

// ISPRAVNO
const FILL_STATES = Object.freeze([[1,'full'],[.85,'almost'],[.5,'filling']]);
const label = FILL_STATES.find(([min]) => pct >= min)?.[1] ?? 'idle';
```

### J03 — Dužina (MORA za nov kod)
- Nova funkcija: najviše **60 linija** (prag alata iz §8).
- Menjana funkcija kraća od 60 linija ne sme preći 60 u istom PR-u; ako mora, izdvaja se pomoćna funkcija.
- Postojeće duge funkcije (`applyCommand`, `controls`, `paintRace`) se **ne dele usput**. Podela je zaseban kandidat sa testovima koji pre podele pokazuju isto ponašanje (§7-K5).

### J04 — Parametri (MORA za nov kod)
Najviše 4 pozicione vrednosti. Za više koristi se jedan objekat sa imenovanim poljima i podrazumevanim vrednostima: `createRace({ track, snails, speed, seed, practice })`.

### J05 — Jedna odgovornost (MORA)
Funkcija ili računa, ili crta, ili menja DOM, ili čuva. ZABRANJENO u istoj funkciji: promena stanja + crtanje, ili promena stanja + upis u DOM. Važi SC-F03 i SC-AGENT-01 A06: `paintMap`/`paintRace` samo crtaju.

### J06 — Imena (MORA za nov kod)
- Akcija: glagol (`openScreen`, `settleArenaResult`). Logička vrednost: `is/has/can` (`canPlace`, `isReady`).
- Jedinica u imenu kada vrednost nije bezdimenzionalna: `durationMs`, `widthPx`, `sizeCells`, `untilTs`.
- Isto ime ne znači istu funkciju u drugom modulu (`app.commit` ≠ `storage commit`); pre nove funkcije proveriti registar SC-FUNC-01.

### J07 — Mesto i doseg (MORA)
Nova funkcija živi u postojećem modulu vlasnika (`modules.domain`, `modules.ui`, …). ZABRANJENO: nova globalna funkcija ili promenljiva na `window`/`globalThis` (osim postojećih bootstrap tačaka), novi modul koji duplira postojeći (SSOT).

### J08 — Greške (MORA)
- ZABRANJENO: prazan `catch {}` i `catch` koji vraća podrazumevanu vrednost kao da je uspeh. Greška se ne guta: funkcija vraća jasan neuspeh, a modul je beleži ili prikazuje na svoj postojeći način (SC-F04: bez delimične transakcije).
- Svaki `Promise` ima obradu odbijanja; `await` u petlji samo kada je redosled potreban.

### J09 — Komentari (MORA)
Komentar objašnjava **zašto**, ne šta. ZABRANJENO: zakomentarisan stari kod (istorija je u Git-u), komentar koji samo ponavlja ime funkcije, oznake verzija kao jedina informacija.

### J10 — Pre nove funkcije (MORA)
Pretražiti postojeće funkcije i registar (SC-FUNC-01, SSOT tabela vlasnika). Gotova funkcija sa sličnim ponašanjem se proširuje; novi „skoro isti“ duplikat je ZABRANJEN. Apstrakcija tek na drugom ili trećem stvarnom korisniku, ne unapred.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 7. Kandidati za raščišćavanje

Redosled je po odnosu koristi i rizika. Svaki kandidat je **poseban PR**, sa A/R merenjem, screenshot-diff-om (PL-01, SC-AGENT-01 G3) i PW-01 regresijom kada se dira izvršni build. Nijedan nije odobren ovim dokumentom.

| ID | Kandidat | Koristi | Rizik | Dokaz za prihvatanje |
|---|---|---|---|---|
| K1 | Spajanje 154 dupla selektora / 461 pregažene deklaracije u jedno pravilo po selektoru | čitljivost + manje pravila za kaskadu | srednji: redosled kaskade | identičan computed style i pixel-diff na svim ekranima iz Dodatka A §A.4 |
| K2 | Velike custom property slike (5) po CSS-01 | prikaz prodavnice | srednji | A/B/R po CSS-01 protokolu |
| K3 | `#id` selektori → klase (590), u grupama po komponenti | specifičnost, manje `!important` | visok: specifičnost | pixel-diff + fokus/hover/aktivna stanja |
| K4 | Uvođenje redosleda sekcija iz C02 | snalaženje | visok: premeštanje menja kaskadu | posle K1 i K3; identičan computed style |
| K5 | Podela `applyCommand` (481), `controls` (285), `paintRace` (164) | čitljivost, testabilnost | visok: ekonomija/trka | testovi postojećeg ponašanja pre podele; null test trke (25%) za `paintRace`/fiziku |
| K6 | 71 lančani ternar → mape/if | čitljivost | nizak | jedinični test za svaku zamenjenu granu |

Brojevi u tabeli su statički (§3). Zaključak o brzini sme da se izvede samo iz izmerenog A/B/R rezultata.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 8. Alat i ratchet provera

Alat: [`tools/sc-code-01/`](../../../tools/sc-code-01/) — samo čita HTML, ne menja kod i ne izvršava igru.

```bash
# jednom, u privremenom folderu van repoa
mkdir -p /tmp/sc-tools && cd /tmp/sc-tools
npm install acorn@8.19.0 acorn-walk@8.3.5
pip install tinycss2==1.5.1

# merenje i ratchet poređenje sa polaznim stanjem
export NODE_PATH=/tmp/sc-tools/node_modules
python3 -I tools/sc-code-01/sc_code_metrics.py index.html \
  --baseline tools/sc-code-01/baseline-0.8.90.json
```

- Izlaz `0` + `RATCHET PASS`: nijedna praćena metrika nije porasla. Izlaz `1` + `RATCHET FAIL`: ispisuje koje su porasle.
- Polazna stanja: `baseline-0.8.90.json` (`snail-city-test/main`) i `baseline-0.8.92-css-unified-p1.json` (`test-2/dist`, SHA-256 `c19cc1ac…`). Kandidat se meri prema baseline-u **svoje** polazne verzije.
- Posle prihvaćenog kandidata za raščišćavanje baseline se ažurira u **istom** PR-u, sa obrazloženjem. ZABRANJENO: podizanje baseline-a da bi prošla nova funkcionalnost.
- Provereno 25.11.2026: na neizmenjenom v0.8.92 HTML-u → PASS; posle ubacivanja jednog selektora sa 4 dela, `!important`, hex boje i lančanog ternara → FAIL sa tačno te 4 metrike.

**Praćene metrike (smeju samo da padaju):** `styleBlocks`, `stylesheetLinks`, `selectorsOver3Parts`, `duplicateSelectors`, `overriddenDeclarations`, `important`, `idSelectors`, `rawHexColors`, `bigCustomProperties`, `distinctMediaQueries`, `functionsOver60Lines`, `functionsOver150Lines`, `functionsDepthOver3`, `functionsOver4Params`, `chainedTernary`, `innerHTMLAppend`, `styleWrites`, `geometryReads`.

**Ograničenja alata:** statička analiza; ne vidi klase koje JS sklapa iz delova, ne zna koliko se pravila zaista primenjuje, ne meri DOM. Kontrolna dubina ne broji ternare i logičke izraze. Rezultat nije dokaz performansi.

**DOM merenje po ekranu (Chromium konzola, otvoren ekran):**

```js
(() => {
  const all = [...document.body.querySelectorAll('*')];
  const depth = (el) => { let d = 0; for (let p = el; p.parentElement; p = p.parentElement) d++; return d; };
  const maxChildren = Math.max(...all.map((el) => el.childElementCount));
  return { elements: all.length, maxDepth: Math.max(...all.map(depth)), maxChildren };
})();
```

Zapisati po ekranu: naziv ekrana, verzija, viewport/DPR i tri broja. Pragovi: D05.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 9. Kontrolna lista za PR

- [ ] Opseg: samo traženo; raščišćavanje nije pomešano sa funkcionalnom izmenom (§2).
- [ ] `sc_code_metrics.py --baseline …` → RATCHET PASS (izlaz komande u PR-u).
- [ ] CSS: jedan blok (C01), pravilo uz svoju komponentu (C02), bez duplog selektora (C03), dubina ≤ 3 (C04), bez novog `#id` i `!important` (C05), boja kroz token (C06), animacija samo `transform`/`opacity` + reduced-motion (C08), postojeći `@media` (C10).
- [ ] DOM: jedan upis po prikazu (D01), `escapeHtml` za svaku dinamičku vrednost (D02), srpski ključ + `EN_DICTIONARY` (D03), `data-action` + delegacija (D04), merenje ekrana ako je dodat ekran ili lista (D05).
- [ ] Funkcije: dubina ≤ 3 (J01), bez lančanih ternara (J02), ≤ 60 linija (J03), ≤ 4 parametra (J04), jedna odgovornost (J05), bez praznog `catch` (J08).
- [ ] Za izmenu izgleda: Chromium screenshot pre/posle istog kadra (SC-AGENT-01 G3).
- [ ] Za izvršni build: verzija podignuta svuda (naslov, `APP_VER`, build tag, `CACHE` u `sw.js`) i PW-01 regresija po pravilima projekta.
- [ ] Odstupanje od pravila: navedena oznaka pravila (npr. „C05“), razlog i plan uklanjanja.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 10. Šta ovaj standard ne radi

- Ne menja `index.html`, `sw.js`, sejv, ekonomiju, fiziku ni izgled.
- Ne odobrava nijedan kandidat iz §7.
- Ne tvrdi ubrzanje: nijedan broj u §3 nije merenje performansi.
- Ne zamenjuje PL-01, CSS-01, SSOT, SC-AGENT-01, SC-ARCH-01 ni SC-FUNC-01.
- Ne propisuje framework, bundler, cascade layers ni novi build sistem.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 11. Dodatak A: dokazna osnova iz v0.8.92 CSS P1 audita

Prenos činjenica iz `SC-v0.8.92-P1-CSS-SINGLE-SOURCE-AUDIT.md` (23.11.2026, `tihidon/test-2`), da zamena tog dokumenta ne izgubi dokaze.

### A.1 Identitet kandidata
- Polaz: `Snail-City-v0.8.91-raster.zip`, `index.html` SHA-256 `c92ac29fb2d4f5915e4336c974a496435aeed5ce57b0516f78a79d8168db5d77`, 7.405.157 B.
- Kandidat: `v0.8.92-css-unified-p1`, `index.html` SHA-256 `c19cc1ac67a2ccc184d2938f0252700205f689d4124bcdf56b672d573c6b7c5d`, 7.404.866 B (−291 B). Isti SHA ima `test-2/dist/index.html` (provereno 25.11.2026).
- SW `CACHE_NAME`: `snail-city-shell-0.8.92-css-unified-p1-r1`; `CORE_PATHS` nepromenjeni (7 putanja).
- **Status: izolovani kandidat, nije odobren za produkciju.**

### A.2 Izmena
- 10 `<style>` blokova spojeno u jedan `<style id="sc-main-css">`, sadržaj **redom, bajt za bajt** po bloku, razdvojen jednim `\n`.
- CSS AST čvorova najvišeg nivoa: 1.096 pre i posle (isti serijalizovani sadržaj); CSS 602.644 → 602.653 B (+9 B separatora).
- Izvršni JS (5 skriptova) isti osim verzijskih literala; `node --check` 5/5 PASS. HTML `<table>` 0, SVG elementi/URL-ovi 0, dodatni mrežni zahtevi 0.
- Nisu dodati framework, `content-visibility`, layout guard, JS handler ni resize heuristika. Nije obrisan CSS, nisu uklonjeni efekti.

### A.3 Ograničenja i kontradikcije (ostaju važeća)
1. Nema HTML tabela; postoje Grid/Flex rasporedi. Broj ugnježdenih Grid elemenata sam po sebi ne dokazuje 400 ms.
2. Spajanje 10 blokova u 1 je organizacija, **nije dokaz ubrzanja**: kaskada sa istim sadržajem može biti jednako skupa.
3. Uklanjanje SVG-a nije dokaz da raster zastoja nema; raster postoji i za PNG/WebP, senke i WebGL.
4. `InvalidateLayout` je interni Chrome događaj; `canvas.width/height` se ne briše.
5. Canvas 2D nije automatsko rešenje (u P1 probi dug compositor period).
6. Promena SW verzije zahteva precache test pre objave.
7. Chromium u kontejneru audita vraćao je `ERR_BLOCKED_BY_ADMINISTRATOR`; nema screenshot-a ni INP/FPS za v0.8.92.

### A.4 Otvoreni QA (nije urađeno)
Chromium screenshot v0.8.92 · Android/Adreno INP/FPS A/B · offline hladno otvaranje sa istim IndexedDB `saveId/revision/level` · dokaz smanjenja P1 zastoja · spajanje na produkciju. Ekrani za vizuelnu proveru: ostrvo, prodavnica sa 8 kartica, inkubator, stanište, zbirka, podešavanja, prvi ekran trke; desktop 772×731 i Android 360×697 DPR 3; `prefers-reduced-motion`.

### A.5 Istorijska merenja (ne mešati verzije)
| Izvor | Rezultat | Ograničenje |
|---|---:|---|
| v0.8.90 trace | Layout 400,896 ms wall / 70,061 ms CPU | nije v0.8.92 |
| v0.8.90 trace | logo 1.488,460 ms; prvo ostrvo 1.802,708 ms od navigacije | screenshot trace-a |
| v0.8.90 prodavnica | ~880–960 ms medijana | SwiftShader, 360×697 DPR 3 |
| P1 eksperiment, 4 SVG → PNG | 416–480 ms medijana | testna varijanta |
| RendererRasterWorker | 377–523 ms → 129–131 ms | lokalni Chromium, ne Adreno |
| v0.8.91, v0.8.92 | **nije izmereno** | ne pripisivati rezultate |

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 12. Izvori

Provereno 25.11.2026.

- web.dev — [Reduce the scope and complexity of style calculations](https://web.dev/articles/reduce-the-scope-and-complexity-of-style-calculations): jednostavniji selektori i manje pogođenih elemenata smanjuju računanje stilova; meriti „Recalculate Style“ i Selector Stats u DevTools (C04, C09).
- web.dev — [Stick to compositor-only properties and manage layer count](https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count): samo `transform` i `opacity`; ne promovisati elemente bez potrebe (C08).
- MDN — [Specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity): ID `1-0-0`, `!important` kao loša praksa uz obavezan komentar, `:where()` nulte specifičnosti (C05).
- MDN — [Element.innerHTML, Security considerations](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML#security_considerations): XSS rizik, `textContent` za čist tekst (D02).
- Chrome — [Avoid an excessive DOM size](https://developer.chrome.com/docs/lighthouse/performance/dom-size): ~800 upozorenje, ~1.400 greška, praviti čvorove kad su potrebni (D05, D06).
- Projektni: [PRAVILO-JEDAN-IZVOR-ISTINE](./PRAVILO-JEDAN-IZVOR-ISTINE.md), [SC-PL-01 + CSS-01](./SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md), [SC-BRISANJE-3-PROVERE](./SC-BRISANJE-3-PROVERE.md); projektni dokumenti SC-AGENT-01, SC-ARCH-01, SC-FUNC-01 (Claude projekat „APP SC 0.8.92-css-unified“).
- Projektni pragovi (3 dela selektora, 60 linija, 4 parametra, dubina 3) su **odluka ovog standarda**, ne univerzalni web standard.

<sub>[↑ Sadržaj](#sadržaj)</sub>
