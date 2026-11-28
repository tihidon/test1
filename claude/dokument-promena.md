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

### QA-003 — PW-DEF-01 correction (draft, 26.11.2026)
- **Version:** candidate full build 0.8.92-css-unified-p11, cache p11-r1; family 0.8.92 unchanged. Root artifact remains p10 due connector transport failure; do not merge.
- **Scope:** existing SW install handler, two build identity anchors, manifest digests, CI cache revision gate and regression. No game economy/logic/save change.
- **Evidence:** Node VM 5/5 PASS; actual Chromium regression pending. Root build/publish gate remains mandatory, D7 and PMV pending.

- Integration follow-up: preserve latest main MCP changes and P11 candidate. Root HTML remains P10; build and release blocked until generated P11 root is committed and CI passes.


### P0 recovery after PR #49 (26.11.2026)
- Merged commit `9b5658db2bde10b2c1a938212429d4a26eb55f6d`: source P11, root HTML P10; post-merge tooling run [45807116303](https://github.com/tihidon/test1/actions/runs/45807116303) failed build/publish equality. Expected P11 SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a` from independent CI assembly.
- Corrective candidate: regenerate root HTML using existing Python build, verify exact digest and existing build gate. Advance CACHE_NAME to `snail-city-shell-0.8.92-css-unified-p11-r2` because r1 may contain old HTML. Retain existing collision guard, all game sources, family labels (title/status/SW comment 0.8.92), no save/economy changes. No Netlify configuration change. Actual deployed origin/ID unknown; no release claim.
- Candidate PR and CI required; D7 and post-merge PMV pending. Revert candidate only under owner approval; never delete player data or manually clear caches.

Recovery evidence: [run 45808612656](https://github.com/tihidon/test1/actions/runs/45808612656), job 139870295474, generated commit `bcd3c6e658f1684649fb26dabcca7c0fb8a0cdd5`, HTML blob `f730698c8251c30c91d798ea816986a91e189a01`, SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a`, 7606179 bytes, independent assembly/syntax and root equality PASS. Temporary write-enabled recovery workflow removed before PR. Full PR CI, D7 and exact-SHA PMV remain pending. No deploy claim.

## P0 publish identity gate candidate (26.11.2026)

Incident: PR #49 merged source P11 with P10 root; [push CI 45807116303](https://github.com/tihidon/test1/actions/runs/45807116303) failed exact equality. PR #53 repaired the artifact and advanced cache to P11-r2. [Push CI 45811647016](https://github.com/tihidon/test1/actions/runs/45811647016) on `73a58e45a996ca1f3fb48f4af9befa785a8e0be4`: both jobs succeeded, P11 SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a`, B01–B06 51 assertions and QA-003 67 checks across 5 cases. D7 and production deployment identity not verified.

Candidate Netlify command uses existing Python build, then exact byte comparison with committed root before copying the remaining unchanged publish whitelist. Nonzero exit on mismatch; no automatic root overwrite or cache deletion. Two isolated real-command regression tests join existing tools/agent unittest discovery: valid exact whitelist, deliberately stale root rejected for the expected reason. No duplicate job, runtime change, cache bump or new dependency. This mitigates mismatched HTML deployment only, not all unsafe merges or release gates. Actual Netlify preview and owner approval of deployment configuration required; no deployment authorized by this draft. Private repository branch protection API unavailable (403; rulesets plan restriction); do not make repository public to bypass it.


## PW-01 — Cloudflare P11-r2, 26.11.2026

- Origin: https://test-cl1.bojan-tihojevic.workers.dev/ ; reference `tihidon/test-cl1` main `8d9fec8405674cbfcc97dd97224bb3a8de596c15` (HTML blob `f730698c8251c30c91d798ea816986a91e189a01`, expected SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a`; SW blob `2f57bfd2fd38f8d220af090caa5c55c7580007f3`, cache `snail-city-shell-0.8.92-css-unified-p11-r2`).
- Cloudflare API confirmed build `2a7682f6-dee9-4ce2-8b9b-227e3ff58dfd` success, deployment `f6ca2f98-9969-41aa-b45e-63771d596006`, version `420b108e-3fcf-4fed-9c62-77f123e4f8c9` at 100%. Original build log: 7606179 B generated, build command success, Wrangler 4.168.0 deploy success. GitHub post-merge [engineering](https://github.com/tihidon/test-cl1/actions/runs/45836823254) and [MCP](https://github.com/tihidon/test-cl1/actions/runs/45836823391) completed success.
- Physical phone smoke, owner-reported (conversation 26.11.2026): “Cloudflare PW-01: svih sedam koraka uspešno izvršeno, offline radi i napredak je sačuvan.” Owner confirmed install, progress change, close, disable Wi-Fi and mobile data, reopen, graphics/level/progress. PASS for this reported basic scenario only. No raw screenshots, device/browser details, timings, exact saveId/revision, force-stop evidence or captured SC_PWA_STATUS/cache inventory supplied; no claim of automated physical test, cross-origin migration or full device matrix.
- Public response byte/MIME identity remains BLOCKED in current environment (curl to /index.html: DNS resolution failure). D7 independent review and full PMV/release closure remain unverified. Do not clear user data or assume Netlify storage migrated. No runtime, cache or deploy change in this evidence-only candidate.


## Usklađivanje test1 / test-cl1 — 26.11.2026

Zajednički referentni snapshot: test1 `e51b1e6cba31bedd61ad0bbb269c90f065117279`, test-cl1 `8d9fec8405674cbfcc97dd97224bb3a8de596c15`. Oba imaju iste runtime/src/SW i standarde; Cloudflare ima četiri posebna infrastrukturna fajla. Usklađeni AGENTS.md, docs/README.md, kanonski PW-01 i ovaj changelog, sa istim sadržajem u oba kandidata. Zadržana istorija P1/P3/P10, neuspešni CI i razlike između hostinga. Aktuelni status u docs/README.md; fizički test je potvrda vlasnika, ne pun device dokaz. Nezavisni D7, javni HTTP integritet i formalno release zatvaranje ostaju otvoreni. Docs-only: nema izmene runtime-a, SW, hostinga, CI gate-ova ili istorijskih skill kopija; nema odobrenog merge/deploy. Potrebno pregledati oba PR-a i izvršiti PMV posle merge-a.

### DOC-003 — razdvajanje istorije i aktuelnih verzija (26.11.2026)
- Istorijski QA-001 i v0.5.1 ostaju sačuvani. Team 0.5.5 i 11 stvarnih skill metapodataka evidentirani odvojeno u docs/README.md; team-handoff 0.5.4, ostalih 10 0.5.5.
- DOC-VER-01 u SC-AGENT-01; AGENTS i PMV upućuju na isti registar. Bez izmene igre, SW, CI ili deployment konfiguracije; bez ponovne objave plugina. Kandidat za oba aktivna repoa; merge/PMV i nezavisni pregled nisu potvrđeni.


## P1 — SC-DEC-01 dijagnostički zapis, 27.11.2026.

**D0 / identitet:** test1 main `fd1bdbe17bc388941b4517b4846975ea67189244`, tree `03769d5926c821cc855a9596eaf4721f50f8eb28`, HTML blob `f730698c8251c30c91d798ea816986a91e189a01`, SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a`, SW blob `2f57bfd2fd38f8d220af090caa5c55c7580007f3`, P11-r2. Izvršni kod i src identični checkpointu a58441b; 20 promenjenih fajlova su dokumentacija/skillovi. Scope: read-only analiza i izolovana dijagnostika; bez patcha, novog pravila, dependencija, merge/deploy. Jedan izvršilac, sekvencijalne uloge; nezavisni D7 BLOCKED.

**Originalni dokaz:** [engineering push CI 45910626289](https://github.com/tihidon/test1/actions/runs/45910626289), [MCP 45914147521](https://github.com/tihidon/test1/actions/runs/45914147521) success. Preuzet [artifact 15159209425](https://github.com/tihidon/test1/actions/runs/45910626289/artifacts/15159209425), lokalno SHA-256 potvrđen `8de5e7c0c342dbdc0d50a9b4afba7fd7497e629d7c4324b8764625c543886882`. Iz originalnog sc-runtime-evidence/trace.zip izdvojen HTML (7606179 B) sa očekivanim SHA-256. sc-functional-evidence/report.json: 51/51 assertions; B02 20 ciklusa, shop DOM 268 elemenata, dubina 13, bez duplicate IDs; ista veličina u prvom i poslednjem snapshotu. Nema dokaza o heap leak-u ili punom napredovanju. B06 je trening, pauza, napuštanje i prvi shop posle povratka, ne završena trka.

**D1 / statički dokaz:** src/js/block-21.js blob `30181db6f3caee3b80e2e047e0d8169482990f53`: shop 3846–3904 (jaja 3894–3899), renderPanel dispatch 4479, openScreen 5132–5159, showSheet 5096–5121 (innerHTML i i18n), settleClock 6334–6349 (uslovni updatePanel), boot 6351–6432. Renderer.resize 1976–1981 već ima guard iste width/height/dpr; resize wrapper 5287–5297 označava dirty i schedule. Ne brisati resize. Boot ima paralelni save/atlas/map preload, UI hydrate i firstSubmittedFrame; texImage2D mark je CPU submission, ne GPU completion.
CSS src/css/block-02.css: pet data:image custom property vrednosti preko 4096 znakova: snail-art 46681/2 refs, botanical-corner 107200/3, wood-banner 67608/2, xp-ribbon 17788/1, portrait-meadow 223760/3 (dužina pronađenog izraza, statički broj var referenci, ne VRAM). Za shop relevantne tri: botanical (1371,1421), wood (1376,1405), xp (1440). Portrait meadow i snail-art nisu direktni shop selektori. Ukupno 192596 znakova tri shop vrednosti. Jedan CSS blok nije dokaz performansi; prodavnica koristi generisane grid/div kartice, ne predlagati uklanjanje grafike.

**D2 / D3, analiza izvornog trace-a:** headless Chromium 141.0.7390.37, 360x780, DPR1. functional-online-trace.zip/trace.trace: before/after istog callId sa method click i selectorom shop. B01 prvi click 53.655 ms; B02 narednih 20 click API trajanja: p50 27.212, p95 nearest-rank 39.457, max 43.581, min 21.152 ms. B05 dodatni click 39.006 ms. functional-race-trace.zip: jedan post-race click 72.88 ms. To su Playwright click API trajanja uz tracing i čekanja, NE handler, INP, prikaz kadra ili validan PL-01 benchmark. Jedan post-race uzorak nije dokaz regresije. sc-runtime-evidence/cpu-profile.json: 1508 sample/timeDelta parova, 1674854 us zbir; exclusive sampled delta sum upload 199882 us, uploadMapTexture 109372 us, uploadDetachedAtlas 105994 us. Profil obuhvata online i offline shell reload; ne sabirati kao GPU time niti kao pojedinačno hladno pokretanje. CDP diagnostic.json timing_comparable=false; scope glavni page target, ne SW/GPU. Hipoteza H1: veliki raster var() potrošači povećavaju style/raster trošak pri shop otvaranju; alternativa H2: DOM rebuild/i18n ili ponovno renderovanje posle race lifecycle. H3: startup teksture su kandidat za zasebno istraživanje. Nema PROVEN uzroka.

**D4 / D6 ograničenja i sledeća provera:** lokalni pokušaj sa exact HTML, izolovan HTTP localhost, Playwright/system Chromium 144.0.7559.96, bez SW, blokiran eksterni saobraćaj: Page.goto net::ERR_BLOCKED_BY_ADMINISTRATOR. 0 uspešnih lokalnih scenario runova; ne zaobilaziti politiku. Pivot: već odobreni private CI. Predlog izolovanog, neintegrisanog PL-01 A/B/R: isti PNG bytes, sadržaj, viewport/DPR i verzija browsera, rotiran redosled; menjati samo jednu veliku CSS var vrednost (xp-ribbon, jedan potrošač) na statički URL, bez dupliranja. Prvo baseline meriti 20–30 ponavljanja, zasebno handler/next frame i profilisanje, cold/warm/post-race odvojeno; ista vizuelna i funkcionalna provera, p50/p95/max. Ako nema održive razlike, NO-CHANGE. Predlog nije izvršen ni odobren kao trajna izmena. Startup: izvesti postojeći SC_STARTUP_TRACE u originalni artefakt sa fazama i odvojiti GPU submission od presentation. Fizički uređaj, A/B/R, D7 NOT RUN/BLOCKED. D8 ZADRŽI ZA QA. Ne menjati runtime, save, CSS, SW, CI ili produkciju ovim zapisom.


## SC-INTEGRITY-01 0.2 — 27.11.2026

Implementacioni kandidat P0 za oba repoa; incident test-cl1 PR #11 (205 D, 381 A, 1 M; oba CI workflow-a uklonjena). Uveden read-only tree checker, fixtures, postojeći CI korak i zasebni base-controlled trusted workflow (ne izvršava kandidat). Exact-scope dokument obavezan van PR-a; owner/team D7 odobrenje još nije potvrđeno. GitHub protection 403 oba, rulesets test1 prazno, test-cl1 403. Nema izmene igre, hostinga ili deploy-a. CI, read-back i nezavisni pregled potrebni pre usvajanja.


## P1 — zamrznuta QA baza (27.11.2026)

Vlasnik odobrio koncept. Kreiran i read-back potvrđen `qa/base/p1-20261127-r1` na `07b7dcb7e9b6dbe2c42d893af939f43493fffe72`, tree `edd42ebc1fd69b7c01dddbb61a032650b4081785`; main ostaje netaknut. Zapis QA-FREEZE-01 u postojećem SC-INTEGRITY-01 je kandidat za pregled, ne drugi registar. PR #71 ostaje privremena dijagnostika, neuspešni preflight artefakti sačuvani. Nema novog izvršavanja, merge/deploy-a ni promene dozvola/privatnosti; tehnička zaštita ref-a i izvršni postupak nisu kvalifikovani. Repo API prijavio public; prethodna pretpostavka privatnog CI-a nije potvrđena. D7 BLOCKED. D8 ZADRŽI ZA QA.
