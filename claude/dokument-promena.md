# Dokument promena — Snail City test1

Last updated: 2026-11-25 04:00 PM CET

Svaka promena u igri ili u build/deploy pipeline-u upisuje se ovde u istom PR-u.
Format unosa: verzija · oblast · fajl · mesto · stara vrednost · nova vrednost · razlog.

## Unosi

### PR #2 — `fix/netlify-webmanifest-content-type` (commit `b0aa3b4`, merge `2d66e55`)
- **Verzija:** 0.8.92-css-unified-p1-r2
- **Oblast:** PWA / offline keš / Netlify headers
- **Fajl:** `sw.js`, `_headers` (novi)
- **Mesto:** `CACHE_NAME` (sw.js, konstanta na vrhu); ceo fajl `_headers`
- **Stara vrednost:** `snail-city-shell-0.8.92-css-unified-p1-r1`; `_headers` nije postojao, manifest je išao bez JSON MIME-a
- **Nova vrednost:** `snail-city-shell-0.8.92-css-unified-p1-r2`; `_headers` šalje `Content-Type: application/manifest+json` za `/manifest.webmanifest` i `no-cache` za `sw.js`, `index.html`, `/`
- **Razlog:** SW install je padao na `sw.js:40` zbog MIME provere manifesta; keš r2 forsira ponovnu instalaciju.

### PR #6 — `fix/rk1-reduce-motion` (commit `c7feb6c`)
- **Verzija:** 0.8.92-css-unified-p2
- **Oblast:** render / pristupačnost (reduced motion)
- **Fajl:** izvorni kod igre (render sloj)
- **Mesto:** provera `prefers-reduced-motion`
- **Stara vrednost:** dva `MediaQueryList` objekta
- **Nova vrednost:** jedan `MediaQueryList` objekat
- **Razlog:** N02 iz revizije; smanjuje broj listenera.
- **SW keš:** `…p1-r2` → `…p2-r2`

### PR #8 — `fix/rk2-na-main` (commit `01265f9`)
- **Oblast:** render (commit)
- **Mesto:** `commit()` funkcija
- **Stara vrednost:** direktan poziv vremena
- **Nova vrednost:** `commit()` koristi `nowBound()`
- **Razlog:** N01 iz revizije (ograničavanje vremena u renderu).

### PR #12 — `chore/netlify-whitelist-build` (commit `1ec97af`)
- **Oblast:** deploy (Netlify)
- **Fajl:** `netlify.toml`
- **Mesto:** `[build] command`
- **Nova vrednost:** `cp` lista samo za javne fajlove: `index.html sw.js manifest.webmanifest _headers privacy.html delete-account.html` + `cp -r img`
- **Razlog:** `docs/`, `tools/`, `test/`, `.git` ne smeju da se objave.

### PR #13 — `source/0.8.92-extract-from-stable` (commit `80cafac`, merge `5b4b030`)
- **Verzija:** 0.8.92-css-unified-p3
- **Oblast:** build / izvorni kod
- **Fajl:** `index.html` (build), `src/**`, `tools/split.py`, `tools/build.py`, `tools/test_roundtrip.py`, `reference/index-p3-main.html`, `README.md`, `.gitignore`
- **Mesto:** ceo build; `sw.js` `CACHE_NAME`
- **Stara vrednost:** `…p2-r2` (sw.js)
- **Nova vrednost:** `…p3-r2` (sw.js); `index.html` sha256 `594026b9ffab62ceb8dbbfa181c887edea3f903ff84a27151a2330fb978dc58a`
- **Razlog:** izvorni kod je izdvojen iz single-file builda; round-trip (split → build) daje bajt-identičan `index.html` (test PASS).
- **Napomena:** `index.html` je isti kao p3 build na deploy-u. Bez promene logike igre.

### Refaktor `drawIllustratedMap` — build p4 (ovaj PR)
- **Verzija:** 0.8.92-css-unified-p3 → 0.8.92-css-unified-p4
- **Oblast:** render (ilustrovana mapa, vodeni shader)
- **Fajl i mesto:** `src/js/block-21.js` — `drawIllustratedMap` (potpis) i poziv u `paintMap`; `src/js/block-00.js` — build tag u `#sc-startup-trace`; `src/js/block-21.js` — `VERSION`; `sw.js` — `CACHE_NAME`
- **Stara vrednost:** `drawIllustratedMap(x,y,w,h,animateWater=true)` (5 parametara); `build:'…-p3'`; `VERSION='…-p3'`; `CACHE_NAME '…-p3-r2'`
- **Nova vrednost:** `drawIllustratedMap({x,y,w,h},animateWater=true)` (2 parametra), telo nepromenjeno; poziv u `paintMap`: `drawIllustratedMap({x:view.x,y:view.y,w:view.sizeX,h:view.sizeY},animateWater)`; build/VERSION `…-p4`; `CACHE_NAME '…-p4-r2'`
- **Razlog:** `sc_code_metrics.py` ratchet vs baseline p1 davao FAIL (`functionsOver4Params` 25 → 26). Jedini poziv je u `paintMap`, pa je promena lokalna.
- **Provera:** `tools/build.py` + `tools/test_roundtrip.py` PASS; ratchet PASS (25 = baseline). Nije testirano na uređaju: **NIJE TESTIRANO** u igri i na telefonu.
- **Napomena:** `SC_PWA_STATUS.version` (`0.8.92`) i `<title>` (`Snail City 0.8.92`) nisu menjani, jer nose baznu verziju bez p-sufiksa, kao i pre.

### Uklanjanje neiskorišćene slike `island-map.webp` — build p5 (ovaj PR)
- **Verzija:** 0.8.92-css-unified-p4 → 0.8.92-css-unified-p5
- **Oblast:** assets (paket slika, `asset-secondary`)
- **Fajl i mesto:** `src/data/block-09.json` — ključ `island-map.webp` (poslednji u objektu); `index.html` — `asset-secondary` (rezultat builda); `src/js/block-00.js` — `build` tag u `#sc-startup-trace`; `src/js/block-21.js` — `VERSION`; `sw.js` — `CACHE_NAME`
- **Stara vrednost:** `island-map.webp` (480×482, RGBA, 97 KB base64) u `asset-secondary`; `…-p4` u build tagu, VERSION i CACHE
- **Nova vrednost:** ključ uklonjen; `…-p5` u build tagu, VERSION i CACHE (`snail-city-shell-0.8.92-css-unified-p5-r2`)
- **Razlog:** provereno pretragom repoa: `island-map` se ne čita ni iz jednog JS fajla (`assetGroup`/`imagePath` ga nikad ne traže). Ostrvo na ekranu dolazi iz `src/data/block-05.b64` (1448×1086, RGB), ne iz ovog fajla.
- **Provera:** `tools/build.py` izlaz u korenu razlikuje se od `HEAD` tačno za uklonjeni ključ i p4→p5; `node --check` glavnog inline skripta PASS.
- **Napomena:** ovo ne menja izgled ostrva. Nebo unutar kutije ostrva potiče iz `block-05.b64` i ostaje otvoreno (vidi „Otvoreno“).

### Providno ostrvo + animirana fontana — build p6 (PR #18, spojen)
- **Verzija:** 0.8.92-css-unified-p5 → 0.8.92-css-unified-p6
- **Oblast:** render (WebGL ostrvo, fontana, shader), assets
- **Fajl i mesto:**
  - `src/data/block-05.b64` — ostrvo: RGBA webp 1448×1086, alfa normalizovana (253→255), bez fontane i bez neba (ceo blok zamenjen)
  - `src/data/block-22.b64` (NOVO) — fontana: RGBA webp 512×512 (izvor 1254×1254, bez pozadine), blok `<script type="text/plain" id="illustrated-fountain-webp">`
  - `src/html/index.template.html` — marker `<!--SC-INLINE 22-->` odmah posle `05`
  - `src/html/blocks.json` — novi unos `22`, sha256 za `05` i `22`
  - `src/js/block-21.js` — `shader main()` (`fountain`/`falling` uv konstante uklonjene, voda se bira bojom); `preloadIllustratedMap` (učitava fontanu); `uploadIllustratedMap` + novi `uploadMapTexture` (jedan helper za ostrvo i fontanu); `drawIllustratedMap` (ostrvo bez vode, pa fontana kao zaseban animirani sprite; 2D fallback crta i fontanu); `webglcontextlost`/restore (`fountainTexture=null`); `getStats` (`illustratedMapBytes` uključuje fontanu)
  - `src/js/block-00.js`, `src/js/block-21.js` (VERSION), `sw.js` (CACHE_NAME), `index.html` (regenerisan iz `dist`)
- **Stara vrednost:** ostrvo sa ugrađenom fontanom i nebom (RGB, 1448×1086, 411 KB base64); animacija vode preko fiksnih uv regiona `pool`(0.708,0.639) i `fall` (vodopadi) u shader-u; `…-p5`
- **Nova vrednost:** ostrvo providno (~386 KB webp, 514 KB base64); fontana sprite 240×240 u koordinatama ostrva, centar x=0.6975..0.8630, y=0.5820..0.8029 (normalizovano 1448×1086); animacija bojom (turkiz voda: ripple + sjaj); ostali delovi fontane (lotos, listovi, kamen) se blago ljuljaju; `…-p6`
- **Razlog:** odluka korisnika: providno ostrvo bez dvostrukog neba (opcija 1) i animacija cele fontane sa zamenom stare (1 sve, 2 ok). Fiksne uv konstante vezivale su animaciju za jedan raspored ostrva; boja to čini nezavisnim od pozicije.
- **Provera:**
  - `tools/build.py` → `dist/index.html`; root `index.html` = kopija; blokovi `05` i `22` u build-u identični fajlovima (base64 poređenje).
  - `node --check` za `block-21.js` i `block-00.js`: PASS.
  - Headless Chrome (Playwright, SwiftShader WebGL): stranica se učitava, canvas sa WebGL-om, nema JS grešaka; jedina 404 je `favicon.ico` (postojala i ranije).
  - Dva snimka u razmaku 700 ms: razlika samo u kvadratu 171×171 px na mestu fontane; ostrvo i ostale zgrade nepromenjeni.
  - Vizuelno: ostrvo bez kutije neba, fontana bez ostataka stare fontane.
  - `tools/test_roundtrip.py` NIJE pokrenut (poznata opasnost: prepisuje `src/` iz reference).
- **Napomena:** `funkcije-i-animacije.md` ne postoji u repou; animacija je opisana u ovom unosu. Ratchet (`sc_code_metrics`) nije pronađen u repou, pa nije pokrenut.

### Vidljivost animacije fontane — build p7 (PR #19, spojen)
- **Verzija:** 0.8.92-css-unified-p6 → 0.8.92-css-unified-p7
- **Oblast:** render (shader fontane)
- **Fajl i mesto:** `src/js/block-21.js` — `shader main()`: amplitude pomeraja (`poolWave`, vertikalni talas, ljuljanje listova) i `highlight`; `src/js/block-00.js`, `sw.js`, `index.html`
- **Stara vrednost:** pomeraj 0.00088 / 0.00078 / 0.00090 / 0.00070 uv, sjaj 0.045+0.055·farView
- **Nova vrednost:** pomeraj 0.0060 / 0.0050 / 0.0060 / 0.0040 uv, sjaj 0.10+0.08·farView (oko 1–1,5 px na ekranu)
- **Razlog:** posle merge-a p6 animacija nije bila vidljiva. Pomeraji su bili podešeni za ostrvo od 1448 px, a fontana se na ekranu crta na oko 240 px, pa je pomeraj bio oko 0,2 px.
- **Provera:** headless Chrome, 4 kadra u razmacima od 400 ms. Srednja razlika u kvadratu fontane 11–16 od 255 (pre ~1–2). Ostrvo van kvadrata ~2,9.

### Samo voda se pomera, zidovi fiksni — build p8 (PR #20, spojen `2e5081f`)
- **Verzija:** 0.8.92-css-unified-p7 → 0.8.92-css-unified-p8
- **Oblast:** render (shader fontane)
- **Fajl i mesto:** `src/js/block-21.js` — `shader main()`: uklonjeno ljuljanje ne-vodenih piksela (zidovi, kamen, listovi, lotos); pomeraj i sjaj samo na `blue` maski; `src/js/block-00.js`, `sw.js`, `index.html`
- **Stara vrednost:** ceo sprite se pomerao (zidovi su "plivali" sa vodom), p7
- **Nova vrednost:** pomera se samo voda (`blue`), p8
- **Razlog:** korisnik: zidovi fontane moraju biti fiksni, a voda treba da osciluje.
- **Provera:** headless Chrome, 3 kadra po 400 ms: 90% piksela fontane se ne menja između kadrova (p90 = 0), voda oscilira.
- **Napomena:** lotos i listovi sada stoje (ranije "sve"). Ako ih želimo da ljuljaju, dodaje se zelena maska sa malim pomerajem.

### Osvežavanje vode 8 → 4 fps — build p9 (PR #21, spojen `4fd3976`)
- **Verzija:** 0.8.92-css-unified-p8 → 0.8.92-css-unified-p9
- **Oblast:** render (petlja vode)
- **Fajl i mesto:** `src/js/block-21.js` — `loop()`, uslov `waterActive` (interval osvežavanja)
- **Stara vrednost:** 125 ms (8 fps); svaki tik postavlja `dirty=true` i ceo grad se ponovo iscrtava
- **Nova vrednost:** 250 ms (4 fps)
- **Razlog:** procena troška: animacija fontane je jeftina, ali ceo grad se iscrtava svakih 125 ms dok je otvoren grad. Na slabijem telefonu to je najveći trošak baterije i zagrevanja. Odluka korisnika: 4 fps.
- **Provera:** `node --check` PASS. Vizuelni efekat na telefonu: NIJE TESTIRANO.

### Kontrast vrednosti u dijagnostici, obe teme — build p10 (PR #22, na čekanju)
- **Verzija:** 0.8.92-css-unified-p9 → 0.8.92-css-unified-p10
- **Oblast:** UI (CSS, ekran Analitika / Dijagnostika)
- **Fajl i mesto:** `src/css/block-02.css` — pravilo `.summary-grid strong` (pločice sa vrednostima)
- **Stara vrednost:** vrednosti nasleđuju boju panela; u toploj temi `#573a22` (tamnosmeđa) na pločici `#34287b`, kontrast oko 1.4:1
- **Nova vrednost:** `color: var(--fg)` (`#f1ecff`) za obe teme, eksplicitno
- **Razlog:** vrednosti u pločicama nisu čitljive; zahtev korisnika: promena za obe teme. Naslovi, opisi i tekst izvan pločica ostaju isti.
- **Provera:** build prolazi; u `dist/index.html` jedno pravilo `.summary-grid strong`. Kontrast izračunat (WCAG): toplo staro 1.17:1 → novo 10.48:1 na `#34287b`, 8.54:1 na `#4d308e`. Vizuelno u pregledaču i na telefonu: NIJE TESTIRANO.

## Odluke
- Ratchet baseline se ne podiže; refaktor je izabran umesto ažuriranja baseline-a (SC-CODE-01: baseline se ne podiže da bi prošla nova funkcionalnost).
- 0.8.90 PW-01 ostaje zvanična stabilna referenca (`docs/SC-PL-01`). p3 je kandidat do završenog QA na fizičkom HONOR uređaju.
- Netlify publish ide samo iz bele liste (PR #12).
- Ostrvo: providna verzija (izrez korisnika) umesto kutije neba; fontana je zaseban sprite, a animacija cele fontane (voda, lotos, listovi) se radi bojom i blagim ljuljanjem (p6).
- Fontana (p8): zidovi fontane su fiksni; pomera se samo voda. Korisnik je odbacio varijantu u kojoj se cela okrugla forma talasa.
- Osvežavanje vode u gradu: 4 fps (250 ms), odobrio korisnik (p9). Tačan trošak baterije se meri na telefonu.
- Dijagnostika (p10): vrednosti u pločicama su bele (`var(--fg)`) u obe teme; naslovi i opisi ostaju kakvi jesu.

## Otvoreno
- Dijagnostika (p10): vizuelna provera vrednosti u tamnoj i toploj temi na telefonu.
- QA na HONOR telefonu, koraci 3–8: prodavnica (ponovljena merenja vs v0.8.90), jaja/inkubator, kartice i modali, portret/landscape, trka i povratak, sejv posle reload-a.
- Merenje `firstIslandFrameMs`: prijavljeno 2788,9 ms ranije, trace sa telefona 940 ms. Nisu sigurno isti uslovi; treba ponovljeno merenje.
- Vizuelno na deploy-u: ostrvo odsečeno sa leve i desne strane na 360 px; natpisi zgrada (`Razbijač vremena`, `Inkubator`) ispod desnih dugmadi; verzija prekrivena pilulom `Local`.
- Supabase CDN nije keširan (sync radi samo online, po dizajnu); blok `SC_LEGACY_CLOUD` i dalje postoji sa drugim project ref-om.
- Bot za 90 dana (`tools/bot-p3.js`): čeka odgovor o grani i definiciji „max“ valuta. Trenutni `tools/bot.js` ne radi na p3.
- p6 nije testiran na telefonu (HONOR): vizuelno ostrvo i fontana, animacija u trci/povratku, memorija posle više otvaranja ekrana.
- Ljuljanje lotosa i listova je estetska odluka: proveriti na telefonu da nije previše.
- Baterija i zagrevanje na 4 fps (p9): nije izmereno na telefonu.
- Memorija teksture: fontana 512² (~1 MB) i ostrvo 1448×1086 RGBA (~6 MB) na GPU; nije proverena na HONOR-u.

### SC-TEAM-004 — infrastructure strategy pivot (26.11.2026)
- Oblast: agent procedure / QA; no game version or runtime/deploy change.
- Fajlovi: SC-DEBUG-01, AGENTS.md, Engineering/Architecture SKILL.md, docs/README.md.
- Razlog: repeated unchanged DNS failures during overnight work; API tree access confirmed separately at `8ed4417a6d2e423800a88436b4465a7a28f1dcab`.
- Nova vrednost: canonical alternate-path procedure, evidence limits and NS01 initial oracle. CI and independent D7 pending; no gameplay fix counted.


### QA-001 — SC-PMV-01 (kandidat, 26.11.2026)
- **Verzija:** igra/SW nepromenjeni; ChatGPT Coordinator 0.5.1 (zasebno izdanje).
- **Oblast:** CI / QA / dokumentacija.
- **Fajl:** .github/workflows/engineering-gates.yml i povezani kanonski standardi.
- **Stara vrednost:** pull_request i workflow_dispatch; nema automatskog main push; bez eksplicitne checkout provere.
- **Nova vrednost:** push main uz postojeće jobove, HEAD == GITHUB_SHA, push baseline event.before i ancestry validacija; PR i manualni/frozen baseline očuvani.
- **Razlog:** QA-001, PR #41 merged bez potvrđenog post-merge CI. QA-DEF-01–04 popravljeni u zasebnom pluginu, 28 lokalnih fixture testova PASS. CI kandidata i D7 čekaju stvarne dokaze. Bez runtime, SW ili Netlify izmena.


### QA-002 — save oracle (kandidat, 26.11.2026)
- **Verzija:** igra/SW nepromenjeni.
- **Oblast:** QA test tooling, IndexedDB.
- **Fajl/funkcije:** tools/qa/functional_contract.py (egg_kinds, snapshot, unchanged_inventory, purchase; durable inherits), test_functional_contract.py.
- **Staro:** ID-only egg comparison; purchase omitted profile and built invariants.
- **Novo:** ID/kind pairs, strict integer kind, duplicate rejection, unchanged existing egg kind/profile/building. Preserved time/revision flexibility.
- **Dokaz:** baseline four false accepts of eight synthetic controls; candidate 28 local fixture methods PASS. Real Chromium CI and independent review pending. No game/SW/balance or production save changes.


### QA-003 — PW-DEF-01 reproduction candidate (26.11.2026)
- **Version:** game/SW unchanged.
- **Scope:** diagnostic QA and CI only; tools/qa/pwa_migration_diagnostic.py, engineering-gates.yml, SC-DEBUG-01.
- **Old:** no real Chromium cache migration diagnostic; Node VM reproduced conditional same-name cache loss.
- **New:** exact-SW synthetic origin test, real transport cut, cache bytes/IDB controls, explicit DEFECT_REPRODUCED status, artifacts. No product acceptance claim; real CI pending.

### Chrome DevTools MCP — P0 candidate (26.11.2026)
- Oblast: agent tooling, no game version/runtime/deploy change.
- Nova vrednost: pinned 1.14.0 isolated localhost config, synthetic MCP+Chrome smoke and separate private evidence workflow; SC-CLI-01, SC-QA-02 and AGENTS linked.
- Razlog: function-level and memory diagnostics; existing gameplay QA unchanged.
- CI, actual host activation and D7 pending; no game fix counted.

### Chrome DevTools MCP — memory capability correction (26.11.2026)
- Prior run 45796898865: FAIL, missing compare_heapsnapshots after MCP initialization. PR #48 was merged despite failed dedicated test; PMV not established.
- Candidate: enable documented --memory-debugging; preserve same smoke assertions. No game/runtime/build/deploy change. CI and D7 pending.

### MCP page identity correction (26.11.2026)
- Run 45798347841 FAIL after successful tool discovery, exact page ID oracle not satisfied. Tagged source shows title (url) format. Candidate parser accepts exact titled/bare URLs, rejects duplicates and wrong URL; four fixture tests; unchanged DOM marker. No game changes. CI/D7/PMV pending.
