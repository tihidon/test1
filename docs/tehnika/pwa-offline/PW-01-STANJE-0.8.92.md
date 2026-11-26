# PW-01 — offline mehanizam u test1 0.8.92: šta je provereno, šta nije

> **Stanje identiteta (25.11.2026):** ovaj dokument navodi p1 (`2d66e55`, `index.html` SHA-256 `c19cc1ac…`). Istorijski snapshot izvršnog koda bio je **p3** (`5b4b030`, SHA `594026b9…`, `VERSION = '0.8.92-css-unified-p3'`). Tvrdnje o proverama u ovom dokumentu važe za p1 i **nisu ponovo proverene na p3 niti P10**. Merodavan izvor je [docs/README.md](https://github.com/tihidon/test1/blob/main/docs/README.md).

**Datum:** 25.11.2026. **Build:** `tihidon/test1` `main` `2d66e55`, `index.html` SHA-256 `c19cc1ac…`, `sw.js` `CACHE_NAME = 'snail-city-shell-0.8.92-css-unified-p1-r2'`.
**Vrsta:** statička provera koda prema migraciji PW-01 iz 0.8.90. **Nije** offline test na uređaju. Pregled dokumenata: [docs/README.md](../../README.md).

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
