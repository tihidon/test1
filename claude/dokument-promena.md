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

## Odluke
- 0.8.90 PW-01 ostaje zvanična stabilna referenca (`docs/SC-PL-01`). p3 je kandidat do završenog QA na fizičkom HONOR uređaju.
- Netlify publish ide samo iz bele liste (PR #12).

## Otvoreno
- QA na HONOR telefonu, koraci 3–8: prodavnica (ponovljena merenja vs v0.8.90), jaja/inkubator, kartice i modali, portret/landscape, trka i povratak, sejv posle reload-a.
- Merenje `firstIslandFrameMs`: prijavljeno 2788,9 ms ranije, trace sa telefona 940 ms. Nisu sigurno isti uslovi; treba ponovljeno merenje.
- Vizuelno na deploy-u: ostrvo odsečeno sa leve i desne strane na 360 px; natpisi zgrada (`Razbijač vremena`, `Inkubator`) ispod desnih dugmadi; verzija prekrivena pilulom `Local`.
- Supabase CDN nije keširan (sync radi samo online, po dizajnu); blok `SC_LEGACY_CLOUD` i dalje postoji sa drugim project ref-om.
- Bot za 90 dana (`tools/bot-p3.js`): čeka odgovor o grani i definiciji „max“ valuta. Trenutni `tools/bot.js` ne radi na p3.
