# SC-PL-01 — Standard za layout, Canvas resize i zabranu neosnovanog brisanja

> **Kopija za `tihidon/test1` (0.8.92-css-unified-p1).** Izvor: [snail-city-test@1e3258f](https://github.com/tihidon/snail-city-test/blob/1e3258f/docs/tehnika/standardi/SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md). Provereno prema test1 `main` `2d66e55` (`index.html` SHA-256 `c19cc1ac…`) 25.11.2026: tabela CSS-01 (§7) potvrđena nad test1: 4 navedene `--sc85-*` vrednosti postoje sa 3/2/1/3 `var()` referenci; postoji i peta vrednost iznad praga, `--sc174-snail-art` (46.682 znaka, 2 reference). Trace podaci iz §1 i §5 pripadaju 0.8.90 i nisu ponovljeni na 0.8.92. Izmene u odnosu na izvor: dodata napomena o petoj vrednosti u §7. Pregled svih kopija: [docs/README.md](../../README.md).

**Status:** OBAVEZNO PROJEKTNO PRAVILO (referenca: root [AGENTS.md](https://github.com/tihidon/snail-city-test/blob/1e3258f/AGENTS.md)).  
**Datum:** 23.11.2026.  
**Opseg:** Snail City, PWA, WebGL rendering, UI, HTML/CSS, IndexedDB, build i QA.  
**Odgovornost:** svaki AI agent pre patch-a, svaki reviewer pre merge-a.  
**Stabilna referenca:** v0.8.90 PW-01; promene prvo idu u izolovani P1 kandidat.

## 1. Važno pojašnjenje

- `InvalidateLayout` nije autorski zlonameran ili sakriven kod. To je **Chromium interna dijagnostička oznaka** koja znači da je posle promene DOM/CSS/canvas atributa potrebno ponovo izračunati raspored.
- Invalidation sama po sebi nije greška; greška ili optimizacioni rizik je **nepotrebno ponavljanje**, izazivanje prisilnih sinhronih proračuna stila ili skupo blokiranje prikaza.
- `canvas.width` i `canvas.height` su potrebni za WebGL drawing buffer. Ne brisati ih: menjanje može resetovati rendering state i promeniti rezoluciju; treba proveravati da li se vrednost **zaista menja**, ali izmene idu tek kroz kontrolisani A/B.
- Chrome trace dokaz: `boot() → resize() → Renderer.resize()` izaziva `InvalidateLayout` na `index.html:3901`, a naknadni `Layout` traje **400,896 ms wall**, **70,061 ms CPU**, unutar `RunTask` od **412,928 ms**. Dugo trajanje nije u celosti dokazani CPU trošak i ne znamo bez dodatnih profila zašto je wall time tako velik.

## 2. Obavezno pravilo PL-01

> **NIKAD ne brisati funkciju, Canvas resize ili inicijalizaciju zato što profiler pokazuje InvalidateLayout.** Pre svake izmene identifikovati okidač, odvojiti browser internu operaciju od korisničkog JavaScript koda, izmeriti pre/posle i dokazati da nema negativne regresije. Bez dokaza: NO-CHANGE.

### Tehnička kontrolna lista

- [ ] Sačuvan originalni trace / commit SHA i tačan line/column; razlikovati `dur` (wall) od `tdur` (CPU).
- [ ] Mapiran lanac poziva i svi zapisivači veličina: `boot()`, `resize()`, `Renderer.resize()`, `applyTheme()`, `ResizeObserver`, `loop()`.
- [ ] Provereno da se pri `canvas.width/height` upisuje samo kad dimenzije zaista treba da se promene; ne uklanjati obaveznu inicijalizaciju.
- [ ] Izbegnute nepotrebne kombinacije *write→read→write* DOM/geometry pristupa tokom istog frame-a; bez novog layout thrashing-a.
- [ ] Testiran viewport, DPR, portret/landscape, početna mapa, sve staze i povratak sa trke, input hitbox, nivo/ekonomija.
- [ ] Netlify/PWA offline: registracija SW, cached shell, ponovno pokretanje, IndexedDB `saveId/revision/level` i migracioni put nepromenjeni.
- [ ] Uspešni Node/Chrome regresioni testovi i Android realni E2E; bez zaglavljivanja, grafikčkih grešaka ili gubitka WebGL konteksta.
- [ ] Jedna izmena po kandidatu, jasni p50/p95/max merenja 20–30 pokretanja na istom uređaju. Ako dobit nije statistički održiva → rollback.
- [ ] Evidence report ima PASS/FAIL/BLOCKED uz obrazloženje i SHA/zapisnik; ne tvrditi da je potvrđeno ono što nije testirano.

## 3. Razlikovanje dve radnje

**Brisanje (DELETE)** je opravdano samo kad audit svih referenci i migracionih puteva dokaže da kod nije korišćen ili je bezbedno potpuno zamenjen, uz očuvane testove.

**Optimizacija (REFACTOR)** je opravdana ako profilisanje potvrdi trošak i postoji kontrolisani kandidat sa istom funkcionalnošću. Nije opravdano izbaciti delove igre ili preimenovati istorijske resurse na osnovu naziva.

## 4. Dnevna tri prolaza

| Prolaz | Fokus | Pitanje |
|---|---|---|
| Jutarnji | PRE RADA | „Da li imam tačan baseline, trace, dokaz o uzroku, rollback i jednu definisanu izmenu?“ |
| Popodnevni | PRE TESTA | „Da li sam proverio sve funkcijske zavisnosti i sprečio nepotrebno preračunavanje?“ |
| Večernji | PRE MERGE/RELEASE | „Da li imam stvarno poboljšanje p50/p95 i kompletan offline/save/graphics QA?“ |

Dnevne provere su **podsetnik na obavezno pravilo**, a ne automatsko izvršavanje ili odobrenje za promene repozitorijuma. Kada nema aktivnog patch-a, podsetnik služi za kratku proveru pravila. Ponoviti tri puta u toku dana, bez dupliranja testova kada nema novog kandidata.

## 5. Konkretna evaluacija sadašnjeg problema

- **POTVRĐENO:** JS stack `boot:8324 → resize:7192 → Renderer.resize:3901` invalidira layout.
- **POTVRĐENO:** glavni Chrome `Layout` od 400,896 ms i `LocalFrameView::performLayout` od 400,813 ms, ali samo oko 70 ms CPU.
- **POTVRĐENO:** first WebGL frame submission nije isto što i prvi vidljivi kadar; prvi sačuvani screenshot sa ostrvom u trace-u je oko 1.803 ms.
- **NEPOTVRĐENO:** da je baš taj Canvas resize jedini uzrok svih 401 ms.
- **NEPOTVRĐENO:** da uklanjanje resize-a ubrzava igru, a da ne kvari grafiku.
- **SLEDEĆI KORAK:** bezbedan A/B eksperiment na posebnoj P1 verziji; prvo baseline bez ekstenzija, kontrolisani viewport, 20–30 startova.

## 6. Izvori standarda

- [SC-v0.8.90 P1 Chrome trace forenzička analiza](https://github.com/tihidon/snail-city-test/blob/1e3258f/docs/analize/dijagnostika/SC-v0.8.90-P1-CHROME-TRACE-FUNCTION-ROOT-CAUSE.md)
- [Stabilna PW-01 referenca](https://github.com/tihidon/snail-city-test/blob/1e3258f/docs/tehnika/pwa-offline/SC-v0.8.90-STABLE-PW01-ANDROID.md)
- [Chrome forced reflow](https://developer.chrome.com/docs/performance/insights/forced-reflow)
- [web.dev — avoid large complex layouts and layout thrashing](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing/)
- [MDN — HTMLCanvasElement.width](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/width)

**Stabilna v0.8.90 ostaje netaknuta; PL-01 pravilo je na snazi za svaki naredni patch.**


## 7. PL-01/CSS-01 — Velike raster slike u CSS promenljivama (23.11.2026)

**Status: OBAVEZNO PROJEKTNO PRAVILO.** Dopuna postojećeg PL-01, ne paralelni standard. Važi za Snail City PWA, naročito prvi prikaz prodavnice i ponovljene kartice. Ovim dokumentom **nije odobrena runtime promena**.

### Pravilo

> **NE ČUVATI VELIKE BASE64 DATA-URI SLIKE U CSS CUSTOM PROPERTIES AKO SE NJIHOVA VREDNOST PREKO var() KORISTI U PONOVLJENIM UI ELEMENTIMA ILI NA KRITIČNOM PUTU INTERAKCIJE.**

- **Projektni prag za obavezni pregled:** Base64 data:image URI preko **4.096 znakova** unutar CSS promenljive koja se koristi u background, background-image, mask ili content. Prag je **projektni lint/review kriterijum**, nije univerzalna granica Chrome-a.
- **Preferiraj** postojeći raster asset sa stabilnim deljenim URL-om pokrivenim Service Worker precache-om; kada arhitektura zahteva jednu izvršnu HTML datoteku, moguće je ciljno koristiti direktan statički CSS url(data:image/...) izraz u zajedničkom pravilu, bez dupliciranja velikog Base64 sadržaja po karticama. Izbor mora proći postojeći offline i vizuelni QA.
- **Dozvoljeno:** CSS promenljive za boje, kratke dimenzije, jednostavne gradijente i tematske tokene. **Ne zabranjuj var() globalno.** Ne brisati CSS Grid/Flex, slike ili broj kartica radi lažnog benchmark poboljšanja.
- **Jedan izvor istine:** pre izmene istraži postojeću CSS kaskadu, deklaracije i sve potrošače, pa menjaj samo usko izmereno usko grlo. Ne uvoditi novi paralelni CSS, renderer, SW ili sistem resursa.

### Statički dokaz iz dostavljenog ZIP-a v0.8.92

Iz raspakovanog izvršnog index.html: CSS custom properties i direktne var() reference:

| Dekoracija | Dužina deklaracione linije u znakovima | Broj statičkih var() referenci |
|---|---:|---:|
| --sc85-botanical-corner | 107.227 | 3 |
| --sc85-wood-banner | 67.630 | 2 |
| --sc85-xp-ribbon | 17.808 | 1 |
| --sc85-portrait-meadow | 223.786 | 3 |

**Napomena za test1 (25.11.2026):** iznad praga je i `--sc174-snail-art` (vrednost 46.682 znaka, 2 `var()` reference), ukupno 5 vrednosti; isto meri SC-CODE-01 §3 (`bigCustomProperties` = 5).

Devet **statičkih** CSS referenci može pokrivati više DOM elemenata, među njima i osam kartica jaja. Ovo nisu VRAM bajtovi i ne znači devet aktivnih potrošača. U v0.8.92 PNG dekoracije su već rasterizovane; problematična hipoteza odnosi se na **način njihove upotrebe kroz velike CSS promenljive**.

### Prijavljena A/B merenja, 23.11.2026.

| Metrika | A/R original | v6 bez var() | Zaključak |
|---|---:|---:|---|
| Obrada interakcije, okvirno | 298 ms | 167 ms | ~44% kraće |
| Raspon ukupne latencije u izdvojenoj seriji | 360–496 ms | 216–296 ms | Rasponi se ne preklapaju |

**Poreklo:** korisnik je prijavio ove rezultate pri poređenju istih ukrasa bez var(). Ovaj dokumentacioni commit **nije nezavisno pokrenuo v6**. Dodatna serija, p50/p95/max, sirovi trace i screenshot/pixel-diff još nisu priloženi u ovom zapisu. Rezultati snažno podržavaju regresiju vezanu za ovaj obrazac, ali ne dokazuju internu tvrdnju da browser svaki PNG ponovo dekodira zasebno za svaki element. Po CSS standardu var() se razrešava pri izračunavanju stilova; precizan trošak i komponente zahtevaju Performance trace.

### Kontradikcije koje moraju ostati zabeležene

1. Jedan CSS blok umesto deset jeste konsolidacija, **ne dokaz ubrzanja**.
2. U prodavnici nema HTML table elemenata. Postoje Grid/Flex; njihovo uklanjanje nije dokazano rešenje.
3. Rasterizovanje SVG ukrasa nije dovoljno ako preostane skup način primene PNG-a.
4. Brži klik nije automatski dokaz boljeg FPS-a, offline otvaranja ili iste grafike.
5. Raniji startup Layout od 400,896 ms je zasebna pojava; ne pripisivati ga ovom nalazu.
6. Ne menjati canvas resize, invalidate/renderer, IndexedDB ili SW zajedno sa ovom izolacijom.

### Obavezni prihvatni protokol

1. **A → v6 → R** sa rotiranim redosledom, istim PNG bajtovima, sadržajem kartica, sejvom, Chrome verzijom, uređajem, DPR/viewport-om, cache/SW uslovima; idealno 20–30 startova.
2. Posebno izmeriti obradu handlera i latenciju do narednog prikaza; prijaviti p50/p95/max, Recalculate Style/Layout/RasterTask/GPUTask (wall i CPU), broj prikazanih jaja i greške.
3. Stvarni Chromium screenshot i pixel-diff original/v6 u istom stanju: 8 jaja, biljni uglovi, drveni natpisi, XP trake, portreti, fontovi, hitbox i accessibility. Isključiti samo nedeterminističko vreme/animacije u testnoj kopiji.
4. PW-01 regresija: online/offline cold reopen, jedan SW scope, isti IndexedDB saveId/revision/level; shop, kupovina/leženje, mapa, sve staze i povratak; portret/landscape, DPR 3, prefers-reduced-motion, WebGL context lost/restore.
5. **PASS / FAIL / BLOCKED** i rollback: produkcioni merge samo uz potvrđen izgled, funkcionalnost i ponovljenu dobit na fizičkom HONOR uređaju.

### Način, alat, princip i izvori

- **Način:** na postojećoj CSS arhitekturi zameniti samo velike image URI var() reference kada usko A/B merenje opravda izmenu.
- **Alat:** audit izvršnog ZIP-a, Chrome DevTools Performance/Event Timing, stvarni screenshot/piksel-diff, Android Chrome, PW-01 offline/IndexedDB test.
- **Princip:** ista funkcionalnost, isti resurs, najmanja promena, stvarni A/B dokaz i rollback; ne koristiti slike kao žrtvu optimizacije.
- MDN var(): https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/var
- CSS Variables Level 1: https://www.w3.org/TR/css-variables/
- Chrome modern-web-guidance: https://github.com/GoogleChrome/modern-web-guidance
- web.dev custom property benchmark: https://web.dev/blog/at-property-performance

**Odluka:** pravilo CSS-01 važi; **runtime v6 nije ugrađen ovim commitom**. Vizuelni i mobilni QA ostaju **OTVORENI**.
