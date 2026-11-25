# Snail City — v0.8.92-css-unified-p1: CSS jedan izvor istine, P1 audit

> **Stanje identiteta (25.11.2026):** ovaj dokument navodi p1 (`2d66e55`, `index.html` SHA-256 `c19cc1ac…`). Izvršni kod na `main` je **p3** (`5b4b030`, SHA `594026b9…`, `VERSION = '0.8.92-css-unified-p3'`). Tvrdnje o proverama u ovom dokumentu važe za p1 i **nisu ponovo proverene na p3**. Merodavan izvor je [docs/README.md](https://github.com/tihidon/test1/blob/main/docs/README.md).

**Datum:** 23. novembar 2026.  
**Status:** **IZOLOVANI KANDIDAT, NIJE ODOBREN ZA PRODUKCIJU**  
**Polazna izvršna aplikacija:** korisnikov `Snail-City-v0.8.91-raster.zip`, lokalno izvučen `index.html` SHA-256 `c92ac29fb2d4f5915e4336c974a496435aeed5ce57b0516f78a79d8168db5d77`.  
**Novi kandidat:** `v0.8.92-css-unified-p1`, `index.html` SHA-256 `c19cc1ac67a2ccc184d2938f0252700205f689d4124bcdf56b672d573c6b7c5d`.  
**Izvor projektnih pravila:** `AGENTS.md` i `docs/SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md`, provereni na GitHub `tihidon/snail-city-test` 23.11.2026.

## 0. Uslovi prihvatanja

1. U izvršnom HTML-u ostaje **jedan CSS `<style>`** i nijedan `link rel=stylesheet`; nema novog mrežnog zahteva.
2. Sva ranija CSS pravila, deklaracije, redosled, `@media`, `@keyframes` i custom properties ostaju semantički identični pre vizuelne regresije.
3. Nema HTML tabela u prodavnici, nema izvršnih SVG elemenata/SVG asset URL-ova; jaja ostaju originalni WebP, a prethodno rasterizovani ukrasi PNG.
4. Ne dirati `Renderer.resize`, `canvas.width/height`, `paintMap`, `openScreen`, `shop`, koordinatni/hit-test lanac, state, ekonomiju i GML.
5. PW-01: isti IndexedDB `saveId/revision/level` nakon online → offline → gašenja → hladnog otvaranja, nov Service Worker potpuno precache-ovan.
6. Dokaz realnog prikaza u Chromiumu i na HONOR telefonu: ostrvo, prodavnica/jaja, inkubator, kartice, modal, portret/landscape, trka/povratak; ne izmišljati screenshot ili FPS.
7. Uporediti **istu verziju, isti sejv i isti uređaj** u ponovljenim A/B/R merenjima (startup first visible, pointerup → next paint, `Layout` wall/CPU, raster, long tasks, p50/p95/max).

## 1. Faktičko stanje ZIP-a pre izmene

| Svojstvo | v0.8.91 raster | Izvor/provera |
|---|---:|---|
| `index.html` | 7.405.157 bajtova | Fajl u ZIP-u |
| `<style>` u HTML-u | **10** | HTML parser |
| CSS tekst svih blokova | **602.644 bajta** | UTF-8 bajtovi |
| CSS AST čvorovi najvišeg nivoa (pravila + direktive) | **1.096** | `tinycss2`, bez whitespace/komentara |
| `<table>` u HTML-u | **0** | HTML parser |
| `<svg>` u HTML-u | **0** | HTML parser |
| `data:image/svg+xml`, `<svg`, `.svg` | **0** | Pregled izvršnog HTML-a |
| Izvršni `<script>` elementi (ostali su i JSON podaci) | **5** | Pregled tipova skriptova |
| `<script>` ukupno | **21** | HTML parser |
| Upotreba `@keyframes` | **26 pojavljivanja** | Tekst CSS-a, ne broj aktivnih animacija |
| Pojavljivanja `filter:` | **15** | Tekst CSS-a, bez merene cene |
| Pojavljivanja `drop-shadow(` | **10** | Tekst CSS-a, bez merene cene |
| Pojavljivanja `animation:` | **37** | Tekst CSS-a, bez merene cene |

Postojeći stilovi su bili dodavani kroz verzijske blokove: osnovni; accessibility; v174 visual bridge; v147 Mesta; desktop; arena; responsive cards; habitat gate; polished cards; ikonice. CSS je složen, ali nisu u pitanju HTML tabele u tabelama. **CSS Grid i Flex su legitimni rasporedi**. Na osnovu HTML-a ne može se tvrditi da je svaki raniji selektor mrtav: prikaz je dinamičan i klase se generišu u JavaScript-u.

## 2. Tačna izmena i princip

- **Način:** uklonjeno je devet dodatnih `<style>` omotača, a sadržaj svih deset zadržan je **redom, bajt za bajt po izvornom bloku**, razdvojen jednim `\n`, unutar jedinog `<style id="sc-main-css">`.
- **Alat:** Python, `bs4`, `tinycss2`; Node `--check` za izvršne skriptove.
- **Princip:** očuvanje cascade source-order i CSS AST-a bez menjanja izgleda, elemenata, efekata, izvornih podataka ili runtime-a. Nije dodavan CSS framework, `content-visibility`, nova tabela, DOM inkapsulacija, layout guard, JS handler ili resize heuristika.
- **Oznake:** samo izvršne verzijske oznake `0.8.91`/`0.8.91-raster` promenjene su u `0.8.92`/`0.8.92-css-unified-p1`; drugi JavaScript netaknut.
- **PWA:** zadržan jedan postojeći `sw.js`, `CORE_PATHS` i storage logika; promenjen samo namespace `CACHE_NAME` u `snail-city-shell-0.8.92-css-unified-p1-r1` i komentar verzije. To izoluje keš kandidata. **Ovo ne dokazuje offline ponovni start.**
- **SVG politika SC-CSS-01:** ne koristiti SVG u ovom trenutnom izvršnom buildu, pošto su svi direktni SVG resursi već uklonjeni i potrebe za SVG-om ovde nisu identifikovane. Ne proglašavati SVG univerzalno lošim: novo uvođenje samo uz konkretan funkcionalni razlog, izmerenu korist i Chromium/Android dokaz. Ne reaktivirati stare SVG ukrase samo radi izgleda.
- **GML:** GameMaker objekti i sobe **nisu izmenjeni**. `Create`, `Step`, `Draw GUI` i `Clean Up` nisu predmet ovog PWA HTML patch-a. Svi podsistemi `global.game_data`, save/load i tajmeri ostaju netaknuti.

### Strukturna kontrola posle izmene

| Provera | Pre | Kandidat | Status |
|---|---:|---:|---|
| CSS `<style>` | 10 | **1** | PASS |
| CSS AST čvorovi | 1.096 | **1.096** | PASS: potpuno isti serijalizovani sadržaj |
| CSS UTF-8 bajtovi | 602.644 | 602.653 | +9 B od separatora |
| `index.html` ukupno | 7.405.157 B | **7.404.866 B** | −291 B, uključuje nove oznake verzije |
| Izvršni JS (osim verzijskih literala) | 5 | 5 | PASS: isti sadržaj |
| `node --check` izvršnih skriptova | nije ovaj test | 5/5 PASS | Sintaksa proverena |
| HTML table | 0 | 0 | PASS |
| SVG asset elementi/referentni URL-ovi | 0 | 0 | PASS |
| CSS/JS dodatni mrežni zahtevi | 0 | 0 | PASS iz strukture, ne HTTP snimka |
| PWA precache putanje | 7 postojećih | 7 postojećih | PASS: fajlovi postoje; HTTP/HTTPS QA čeka |

### Šta **nije** urađeno

- **Nije obrisano** 600 KB CSS-a: to bi bilo slepo brisanje 1.096 pravila/direktiva. Ovde je konsolidovana *organizacija*, ne kompleksnost computed style-a.
- **Nisu uklonjene** animacije, filteri, efekti jaja ili CSS senke: njihovo uklanjanje mora biti **zaseban P1 kandidat** uz sačuvanu geometriju, klik i dokaz stvarnog prikaza, a ne pomiksano sa konsolidacijom.
- **Nije zabranjen** normalan Chrome `InvalidateLayout`: to je interna operacija browsera, ne naš poziv `invalidate()`. Bezbedan cilj je manje nepotrebnih DOM promena/forced sync layout-a, ne nula invalidacija.
- **Nije dokazano** smanjenje `Layout`, INP ili raster wall vremena. Nema legitimnog broja milisekundi „posle“ samo iz analize CSS teksta.

## 3. Prethodna P1 dokazna linija, ne mešati verzije

| Dokaz iz korisnikovih priloga | Rezultat | Obuhvat / ograničenje |
|---|---:|---|
| `Snail-City-P1-izolacija-zastoja.md`, v0.8.90 | `Layout` **400,896 ms wall / 70,061 ms CPU** | Izvorni Chrome trace, ne v0.8.92 |
| Isti trace: logo posle JS submit | **1.488,460 ms** od navigacije | Screenshot trace-a, nije prve prezentacije |
| Isti trace: prvo zabeleženo ostrvo | **1.802,708 ms** od navigacije | Originalni trace screenshot |
| Izolacija prodavnice, izvorna kontrola | **~880–960 ms medijana**, zavisi od serije | WebGL 1 SwiftShader, 360×697 DPR 3, v0.8.90 |
| Četiri SVG ukrasa zamenjena PNG, P1 lokalni eksperiment | **416–480 ms medijana** | Testna varijanta, pre izdanja v0.8.91 |
| RendererRasterWorker / Flush | **original 377–523 ms**, sa PNG **129–131 ms** pojedinačni trag | Lokalni Chromium, ne direktno trošak fizičkog Adreno GPU-a |
| v0.8.91 raster | **Nema u datim izvorima novog A/B merenja** | Nije dozvoljeno imputirati rezultate iz 0.8.90 |
| v0.8.92 CSS | **Nije izmereno** | Nije dozvoljeno pripisati novu brzinu bez Chromiuma |

### Kontradikcije / ono što može da zavede

1. **„Tabele“ nisu HTML tabele**: nula `<table>`; postoje više nivoa CSS Grid/Flex komponenata. Broj ugnježdenih Grid elemenata sam po sebi ne dokazuje 400 ms.
2. **„10 CSS blokova = 10 puta više layout-a“ nije tačno.** Browser pravi finalnu kaskadu na osnovu pravila; spojeni blokovi uz identičan sadržaj mogu biti podjednako skupi. Zato ne tvrdimo ubrzanje.
3. **„Uklonili smo SVG = raster zastoja nema“ nije dokazano.** Raster/paint/kompozicija ostaju i za PNG/WebP, CSS senke i WebGL. P1 prethodni trag sugeriše cenu četiri dekoracije, ali nije potpuna atribucija.
4. **„Ukloni invalidaciju“ nije validna popravka.** `InvalidateLayout` je Chrome događaj; `Renderer.resize` menja potrebnu drawing-buffer rezoluciju. Ne brisati `canvas.width/height`.
5. **A/R razlike su velike.** U lokalnim P1 merenjima identične kontrole imaju znatnu varijaciju; prost zaključak iz jednog testa, ili poređenje SwiftShader sa fizičkim Adreno, nije dokaz uzroka.
6. **Canvas 2D nije automatsko rešenje.** U P1 proba zadržava dugačak compositor period i ponekad sporiji dodir.
7. **PWA offline je nezavisna kritična funkcija.** Promena verzije workera zahteva precache test pre objavljivanja, čak kada `CORE_PATHS` ostaje isti.
8. **Browser provera blokirana:** instalirani Chromium 144 u ovom kontejneru vraća `net::ERR_BLOCKED_BY_ADMINISTRATOR` i za `data:` i za lokalni HTTP/`file:`. Nema stvarnih screenshot-a kandidata niti merljivog browser FPS/INP; rezultat se **ne označava PASS**. Korisnikov prethodni dokazni kadar jeste stvaran, ali pripada starijem trace-u, a ne novoj verziji.

## 4. Plan validacije bez izmišljanja dokaza

1. Postaviti P1 ZIP kao **poseban Netlify Deploy Preview** pod HTTPS originom. Ne zamenjivati stabilnu produkciju; čuvati rollback v0.8.91.
2. U Chrome DevTools (`Performance`) sa istim profilom, save-om, telefonom i viewport-om izmeriti A=v0.8.91, B=v0.8.92, R=v0.8.91; rotirati redosled u **20–30 startova**. Zapisati p50/p95/max, first *presented* island frame, `Layout` wall/CPU, raster, `pointerup` Jaja i long tasks. Dovoljno ako ne pogorša, ali ne reklamirati ubrzanje bez boljih rezultata.
3. Screenshot-diff: ostrvo, shop sa 8 kartica, inkubator, habitat, zbirka, podešavanja, prvi ekran trke; desktop 772×731 i Android 360×697 DPR 3; test `prefers-reduced-motion`; fokus, touch ciljeve, čitljivost.
4. SW update: proveriti jedan worker, `manifest.webmanifest` MIME, svih 7 core putanja, sačuvani IndexedDB `saveId/revision/level`; potpuno ugasiti PWA, isključiti mrežu, opet otvoriti i proveriti grafiku i napredak.
5. Portret/landscape, sve dostupne staze i povratak, zoom/hitbox i `webglcontextlost` oporavak. Bez clean testova: **ne spajati** u production.
6. Po uspešnom A/B izabrati naredni *jedan* kandidat: test gašenja samo skupih filtera/animacija na osam kartica Jaja ili rasterizacija dodatnih dekoracija (ne istovremeno). Posebno meriti prvi dodir i topli dodir.

## 5. Status stavki

| Stavka | Status |
|---|---|
| Proverena dostupnost v0.8.91 ZIP-a | **URAĐENO** |
| Identifikovan tačan broj CSS blokova i HTML tabela | **URAĐENO** |
| Proveren SVG status izvršnog koda | **URAĐENO** |
| Jedan CSS blok, očuvana pravila i cascade | **URAĐENO** |
| Očuvane GameMaker/WebGL/ekonomija funkcije u izvornom kodu | **URAĐENO** (statička provera, ne E2E) |
| Novi P1 ZIP i rollback originala | **URAĐENO** |
| Node sintaksa, CSS AST, SW core putanje | **URAĐENO** |
| Pravi Chromium screenshot v0.8.92 | **NIJE URAĐENO** (blokirano browser policy) |
| Android 15/Adreno INP/FPS A/B | **NIJE URAĐENO** |
| Offline hladno otvaranje i IndexedDB sejv | **NIJE URAĐENO** |
| Uklonjeni efekti sa jaja | **NIJE URAĐENO** (odvojeni kandidat) |
| Dokazano smanjenje P1 zastoja | **NIJE URAĐENO** |
| Spajanje na GitHub main / Netlify produkciju | **NIJE URAĐENO** (PL-01 zabrana bez QA) |

## 6. Standardi

- [PL-01 GitHub AGENTS.md](https://github.com/tihidon/snail-city-test/blob/main/AGENTS.md)
- [PL-01 projekat](https://github.com/tihidon/snail-city-test/blob/main/docs/SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md)
- [GoogleChrome modern-web-guidance, CSS](https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/css/css.md)
- [GoogleChrome modern-web-guidance, performance](https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/performance/performance.md)
- [web.dev INP](https://web.dev/articles/optimize-inp/)
- [MDN CSS performance](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/CSS)
- [MDN CSS containment](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/contain)

**Zaključak za izdanje:** jedan CSS source-of-truth je **statički potvrđen**. Performanse, PWA/IndexedDB i grafička jednakost **nisu potvrđeni**; zato v0.8.92 ostaje P1 probni build.
