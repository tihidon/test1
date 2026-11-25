# Snail City — source (build 0.8.92-css-unified-p3)

Source izvučen iz `index.html` sa grane `main` (commit `f52f0f0`).
SHA-256 izvornog `index.html`: `594026b9ffab62ceb8dbbfa181c887edea3f903ff84a27151a2330fb978dc58a`.

## Kako se koristi
- `python3 tools/split.py` razbija `reference/index-p3-main.html` u `src/` (menjati samo kad se referenca svesno menja).
- `python3 tools/build.py` spaja `src/` u `dist/index.html`.
- `python3 tools/test_roundtrip.py` je gate: build mora biti bajt-identičan referenci, a svi izvršni blokovi moraju proći `node --check`.

## Deploy
- Netlify objavljuje samo beli spisak fajlova (`netlify.toml`). `index.html` u korenu ostaje izvor deploy-a, a `dist/` je lokalni izlaz i nije u repou (`.gitignore`).
- Ovaj PR ne menja deploy ni keš (`CACHE_NAME` ostaje `snail-city-shell-0.8.92-css-unified-p3-r2`).

## Struktura
- `src/html/index.template.html` — HTML sa oznakama `<!--SC-INLINE NN-->`.
- `src/html/blocks.json` — redosled, otvoreni/zatvoreni tag i SHA-256 svakog bloka. Redosled je bitan (skripte se izvršavaju redom).
- `src/js/`, `src/css/`, `src/data/` — tela blokova, bajt-za-bajt.
- `tools/` — `split.py`, `build.py`, `test_roundtrip.py`.

## Mapa blokova
| ID | Element | Fajl | Bajtova | id atribut | Napomena |
|---|---|---|---:|---|---|
| 00 | `script` | `src/js/block-00.js` | 2913 | sc-startup-trace | (function(){ |
| 01 | `script` | `src/js/block-01.js` | 1369 | sc-pwa-bootstrap | // PW-01: register the ONE existing scoped Service Worker independentl |
| 02 | `style` | `src/css/block-02.css` | 602653 | sc-main-css | Jedinstveni CSS (sc-main-css), redosled pravila nepromenjen |
| 03 | `script` | `src/data/block-03.b64` | 67272 | sc-sky-day | Base64 WebP (sprite / ilustracija) |
| 04 | `script` | `src/data/block-04.b64` | 92324 | sc-sky-night | Base64 WebP (sprite / ilustracija) |
| 05 | `script` | `src/data/block-05.b64` | 411008 | illustrated-map-webp | Base64 WebP (sprite / ilustracija) |
| 06 | `script` | `src/js/block-06.js` | 125 | — | window.SC_LEGACY_CLOUD={url:'https://ezuuiurkelbeillfdxra.supabase.co' |
| 07 | `script` | `src/data/block-07.b64` | 646656 | detached-map-sprites | Base64 WebP (sprite / ilustracija) |
| 08 | `script` | `src/js/block-08.js` | 36374 | — | /* Snail City catalog data (izdvojeno iz app.js u 0.8.18-beta). |
| 09 | `script` | `src/data/block-09.json` | 519564 | asset-secondary | JSON podaci |
| 10 | `script` | `src/data/block-10.json` | 189876 | asset-race-extra | JSON podaci |
| 11 | `script` | `src/data/block-11.json` | 359519 | asset-race | JSON podaci |
| 12 | `script` | `src/data/block-12.json` | 321061 | asset-audio | JSON podaci |
| 13 | `script` | `src/data/block-13.json` | 282497 | asset-snails-1 | JSON podaci |
| 14 | `script` | `src/data/block-14.json` | 356513 | asset-snails-6 | JSON podaci |
| 15 | `script` | `src/data/block-15.json` | 337117 | asset-snails-5 | JSON podaci |
| 16 | `script` | `src/data/block-16.json` | 336269 | asset-snails-4 | JSON podaci |
| 17 | `script` | `src/data/block-17.json` | 331705 | asset-snails-3 | JSON podaci |
| 18 | `script` | `src/data/block-18.json` | 290689 | asset-snails-2 | JSON podaci |
| 19 | `script` | `src/data/block-19.json` | 319669 | asset-snails-0 | JSON podaci |
| 20 | `script` | `src/data/block-20.json` | 116729 | asset-snails-7 | JSON podaci |
| 21 | `script` | `src/js/block-21.js` | 1691395 | — | globalThis.SC_STARTUP_TRACE?.mark('mainScript.start'); |

## Namerno nije urađeno
- **Prodavnica (CSS):** sporo prvo otvaranje nije potvrđeno na telefonu; izolovana promena nije dovoljna za izdanje (`docs/SC-v0.8.92-P1-CSS-SINGLE-SOURCE-AUDIT.md`).
- **Podela CSS-a na module:** odložena do vizuelne regresije.
- **Učitavanje posle trke (v174):** nije deo ovog repoa.
