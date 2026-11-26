# PW-01 — offline mehanizam u test1 0.8.92: šta je provereno, šta nije

> **Stanje identiteta (25.11.2026):** ovaj dokument navodi p1 (`2d66e55`, `index.html` SHA-256 `c19cc1ac…`). Istorijski snapshot izvršnog koda bio je **p3** (`5b4b030`, SHA `594026b9…`, `VERSION = '0.8.92-css-unified-p3'`). Tvrdnje o proverama u ovom dokumentu važe za p1 i **nisu ponovo proverene na p3 niti P10**. Merodavan izvor je [docs/README.md](https://github.com/tihidon/test1/blob/main/docs/README.md).

**Datum:** 25.11.2026. **Build:** `tihidon/test1` `main` `2d66e55`, `index.html` SHA-256 `c19cc1ac…`, `sw.js` `CACHE_NAME = 'snail-city-shell-0.8.92-css-unified-p1-r2'`.
**Vrsta:** statička provera koda prema migraciji PW-01 iz 0.8.90. **Nije** offline test na uređaju. Pregled dokumenata: [docs/README.md](../../README.md).

**Aktuelni dodatak:** pogledati odeljak PW-01 — Cloudflare P11-r2 na kraju dokumenta. Odeljci 1–3 ispod su istorijski P1 pregled; ne predstavljaju sadašnje stanje oba hostinga.

## 1. Poreklo

PW-01 rešenje uvedeno je u 0.8.90 (projektni dokument `PW-01-MIGRATION-AND-QA.md`, 23.11.2026). Tamo utvrđen uzrok: u 0.8.89 SW se registrovao samo ako postoji `link[rel="manifest"]`, a HTML ga nije imao, i to tek posle uspešnog `boot()`. Rešenje: pravi manifest link, rana nezavisna registracija jednog SW-a, dijagnostika `SC_PWA_STATUS`, atomaran precache 7 resursa, `_headers`. Stvarni Android offline relaunch potvrđen je za **0.8.90** ([stabilna referenca](https://github.com/tihidon/snail-city-test/blob/1e3258f/docs/tehnika/pwa-offline/SC-v0.8.90-STABLE-PW01-ANDROID.md)); taj PASS ne važi automatski za 0.8.92.

## 2. Da li 0.8.92 i dalje ima isti mehanizam

| Element PW-01 iz 0.8.90 | test1 0.8.92 | Dokaz (sidro) |
|---|---|---|
| `<link rel="manifest">` u `<head>` | ✓ | `index.html` L7: `href="./manifest.webmanifest"` |
| Jedna rana registracija, pre ugrađenih slika i nezavisno od `boot()` | ✓ | `#sc-pwa-bootstrap` (L66): `nav.register('./sw.js',{scope:'./',updateViaCache:'none'})`; to je jedini poziv `register` u `index.html` |
| Samo HTTPS ili localhost, ne u nativnom omotaču | ✓ | uslov `location.protocol==='https:'…` i `Capacitor?.isNativePlatform?.()` |
| Dijagnostika `SC_PWA_STATUS` (`state`, `ready`, `controlled`, `error`, `scope`) | ✓ | isti blok; `state` prolazi `registering` → `registered` → `offline-ready` ili `failed`, `version:'0.8.92'` |
| Sedam `CORE_PATHS`, bez API/Supabase keširanja | ✓ | `sw.js`: index, manifest, tri ikonice iz `img/`, privacy, delete-account; `fetch` vraća samo `isCore` URL-ove |
| Budžet 16 MiB ukupno, 12 MiB po resursu | ✓ | `CORE_SIZE_LIMIT`, `PER_RESOURCE_LIMIT` |
| Odbijanje `!ok`, `opaque`, `redirected` i pogrešnog MIME pri instalaciji | ✓ | `install` rukovalac, provera `content-type` |
| `skipWaiting` tek posle potpune instalacije; neuspeh briše samo novi keš | ✓ | `install`: `self.skipWaiting()` posle petlje; u `catch` `caches.delete(CACHE_NAME)` |
| Aktivacija briše samo sopstvene stare keševe, ne IndexedDB | ✓ | `activate`: filter `OWNED_PREFIXES` (`snail-city-08`, `snail-city-shell-`), zatim `clients.claim()` |
| Navigacija: mreža prvo, keš kao rezerva | ✓ | grana `isEntryNavigation`; rizik K04 ([SC-FUNC-01 §3](../standardi/SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md#3-kontradikcije-i-rizici-ponovo-provereni-za-test1)) |
| `_headers` za `sw.js`, `index.html`, `/`, manifest MIME | ✓ | `_headers` (PR #2) |
| Ikonice na putanjama koje traže SW i manifest | ✓ | `img/icon-192.png`, `img/icon-512.png`, `img/icon-maskable.png` |

**Razlika od 0.8.90:** novi `CACHE_NAME` (`…0.8.92-css-unified-p1-r2`). Prelazak sa 0.8.90 keša na ovaj ide kroz `activate` filter iznad; na uređaju **nije testiran**.

## 3. Šta nije provereno (NIJE TESTIRANO)

1. Instalacija SW-a i `SC_PWA_STATUS.state === 'offline-ready'` na stvarnom HTTPS deploy-u ovog builda.
2. Offline relaunch i Force Stop na Androidu, isti `saveId`/`revision`/`level`.
3. Prelazak sa 0.8.90 (`snail-city-shell-0.8.90-r2`) na ovaj keš bez gubitka sejva.
4. Stvarni HTTP status i `Content-Type` svih sedam fajlova sa Netlify-ja (zavisi i od publish direktorijuma, vidi [SC-ARCH-01 §2](../standardi/SC-ARCH-01-STRUKTURA-I-ARHITEKTURA.md#2-fizička-struktura-distribucije)).

Postupak testa ostaje isti kao u 0.8.90: izvoz rezervne kopije pre deploy-a, isti origin, nikad „Clear site data“ na stvarnom sejvu, provera `caches.keys()` i sedam fajlova, offline osvežavanje, pa zatvaranje i ponovno otvaranje instalirane PWA ([SC-AGENT-01 §8](../standardi/SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md#8-sc-a08--pw-01-offline-i-release-integritet)).


## PW-01 — Cloudflare P11-r2, 26.11.2026

- Origin: https://test-cl1.bojan-tihojevic.workers.dev/ ; reference `tihidon/test-cl1` main `8d9fec8405674cbfcc97dd97224bb3a8de596c15` (HTML blob `f730698c8251c30c91d798ea816986a91e189a01`, expected SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a`; SW blob `2f57bfd2fd38f8d220af090caa5c55c7580007f3`, cache `snail-city-shell-0.8.92-css-unified-p11-r2`).
- Cloudflare API confirmed build `2a7682f6-dee9-4ce2-8b9b-227e3ff58dfd` success, deployment `f6ca2f98-9969-41aa-b45e-63771d596006`, version `420b108e-3fcf-4fed-9c62-77f123e4f8c9` at 100%. Original build log: 7606179 B generated, build command success, Wrangler 4.168.0 deploy success. GitHub post-merge [engineering](https://github.com/tihidon/test-cl1/actions/runs/45836823254) and [MCP](https://github.com/tihidon/test-cl1/actions/runs/45836823391) completed success.
- Physical phone smoke, owner-reported (conversation 26.11.2026): “Cloudflare PW-01: svih sedam koraka uspešno izvršeno, offline radi i napredak je sačuvan.” Owner confirmed install, progress change, close, disable Wi-Fi and mobile data, reopen, graphics/level/progress. PASS for this reported basic scenario only. No raw screenshots, device/browser details, timings, exact saveId/revision, force-stop evidence or captured SC_PWA_STATUS/cache inventory supplied; no claim of automated physical test, cross-origin migration or full device matrix.
- Public response byte/MIME identity remains BLOCKED in current environment (curl to /index.html: DNS resolution failure). D7 independent review and full PMV/release closure remain unverified. Do not clear user data or assume Netlify storage migrated. No runtime, cache or deploy change in this evidence-only candidate.
