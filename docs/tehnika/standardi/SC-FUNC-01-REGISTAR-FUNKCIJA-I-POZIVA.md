# SC-FUNC-01 — Registar funkcija, poziva i kontradikcija (test1 0.8.92)

> **Stanje identiteta (25.11.2026):** ovaj dokument navodi p1 (`2d66e55`, `index.html` SHA-256 `c19cc1ac…`). Istorijski snapshot izvršnog koda bio je **p3** (`5b4b030`, SHA `594026b9…`, `VERSION = '0.8.92-css-unified-p3'`). Tvrdnje o proverama u ovom dokumentu važe za p1 i **nisu ponovo proverene na p3 niti P10**. Merodavan izvor je [docs/README.md](https://github.com/tihidon/test1/blob/main/docs/README.md).

**Oznaka:** SC-FUNC-01 · **Revizija:** 1.1 za test1 · **Datum:** 25.11.2026.
**Build:** `tihidon/test1` `main` `2d66e55`, `index.html` SHA-256 `c19cc1ac67a2ccc184d2938f0252700205f689d4124bcdf56b672d573c6b7c5d`, `const VERSION = '0.8.92-css-unified-p1'`.
**Poreklo:** revizija 1.0 je projektni dokument nad ZIP-om 0.8.93 (`index.html` SHA-256 `74dc364a…`, repo `test-2`). Po pravilu SC-F08 registar je **regenerisan** za ovaj build; brojevi linija iz 0.8.93 ovde ne važe. §4 (standard) je prenet bez izmene, §5 je ponovo proveren nad test1.
**Status:** statički inventar; nije izvršavana igra. Ne menja kod.

## Sadržaj

1. [Metod i značenje rezultata](#1-metod-i-značenje-rezultata)
2. [Obavezni standard funkcija (SC-F01–F08)](#2-obavezni-standard-funkcija-sc-f01f08)
3. [Kontradikcije i rizici, ponovo provereni za test1](#3-kontradikcije-i-rizici-ponovo-provereni-za-test1)
4. [Ključne funkcije](#4-ključne-funkcije)
5. [Potpuni registar imenovanih funkcija (generisan)](#5-potpuni-registar-imenovanih-funkcija-generisan)

## 1. Metod i značenje rezultata

- Generator [`docs/alati/sc-func-01-registar.cjs`](../../alati/README.md) parsira 5 izvršnih `<script>` blokova pomoću `acorn` 8.19.0 (bez izvršavanja, 0 grešaka parsiranja). `sw.js` nije obuhvaćen.
- Funkcijski čvor = deklaracija, izraz, arrow funkcija ili metoda. Ime se uzima iz deklaracije, promenljive, svojstva, metode ili dodele; ostalo je „anonimno“ (callbackovi) i broji se, ali se ne navodi u tabeli.
- Modul je određen linijom dodele `modules.<ime>=`; funkcije pre prvog modula nose `id` bloka (`#sc-startup-trace`, `#sc-pwa-bootstrap`) ili `blok@L<linija>`.
- **„Poziva po imenu“** broji mesta poziva sa istim imenom (`ime(` ili `x.ime(`) u svim izvršnim blokovima. To je **gornja procena**, ne graf poziva: istoimene funkcije (npr. tri `commit`) dele broj, a pozivi kroz `data-action`, mape komandi ili callback ne ulaze. **0 nije dokaz da je funkcija mrtva** (SC-F06).
- Razlika prema reviziji 1.0: tamo je korišćen TypeScript checker sa vezama poziva (5.046 mesta poziva). Ovde te veze nisu ponovo izračunate; za graf poziva pre izmene važi SC-F01 (ručna provera).

Rezultat nad test1: **983 funkcijska čvora** (494 imenovana, 489 anonimnih) u 21 grupi. Raspodela po modulima je gotovo ista kao u 0.8.93 (npr. `domain` 168, `ui` 259, `app` 164, `storage` 113).

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 2. Obavezni standard funkcija (SC-F01–F08)

- SC-F01: identifikuj vlasnika, potpis, pozivaoce, callback registracije, alias/destructuring, string dispatch, ulaz, izlaz, mutacije i greške pre izmene. Funkcija sa istim imenom u različitom scope-u nije sama po sebi duplikat.
- SC-F02: jedan autoritet za teren, oslonac, projekciju, ekonomiju, fiziku, vreme, save i RAF. Izvedeni keš je dozvoljen uz invalidaciju.
- SC-F03: UI šalje nameru; reducer odlučuje; storage potvrđuje trajnost; renderer ne vrši gameplay transakciju. Proveri stvarni redosled, ne kopiraj normativni dijagram u kod.
- SC-F04: ulazi imaju jedinice, preduslove, granice, validaciju; greška ne ostavlja delimičnu transakciju. Kod Promise-a proveri reject, cleanup i paralelne pozive.
- SC-F05: svaki listener, interval, RAF, GPU resurs i observer ima vlasnika i lifecycle; ne uvoditi paralelni manager.
- SC-F06: pre brisanja proveri direktne reference, dinamičke reference i runtime scenarije; 0 statičkih poziva nije dokaz nekorišćenja.
- SC-F07: svi relevantni G0–G7 iz SC-AGENT-01, Chromium screenshot/GIF za grafiku, PW-01 za save/PWA, A/B/R za performanse.
- SC-F08: nakon odobrenog patch-a regeneriši indeks prema novom hash-u; ne ručno menjati izvedene linije i ID.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 3. Kontradikcije i rizici, ponovo provereni za test1

| ID | Nalaz u 0.8.93 | Stanje u test1 0.8.92 (provereno 25.11.2026) | Postupak |
|---|---|---|---|
| K01 | SW i manifest traže `img/`, ikonice u root-u | **ne važi:** ikonice su u `img/`, putanje u `sw.js` `CORE_PATHS` i manifestu se slažu | — |
| K02 | nema `_headers` | **ne važi:** `_headers` postoji (PR #2: manifest `application/manifest+json`, `no-cache` za `sw.js`, `index.html`, `/`) | proveriti stvarne HTTPS odgovore pri deploy-u |
| K03 | `RACE_SPEED_OPTIONS` `[10,20,30,40,50,55]`, stari SSOT navodi 60 | **važi:** ista vrednost (`modules.race`), čitaoci u `ui` (izbor brzine), `app` (destrukturiranje i promena brzine) | ne menjati balans bez vlasnika |
| K04 | SW za navigaciju prihvata `live.ok` bez provere sadržaja | **važi:** `fetch` rukovalac, grana `isEntryNavigation` | ne slabiti install proveru; proveriti decoded SHA-256 i boot |
| K05 | tri `commit` (indexed, local, app) | **važi:** `indexedRepository.commit`, `localRepository.commit` (storage) i `app` `commit(type, fields)`; namerno različiti slojevi | proveriti izbor jednog adaptera i ugovor revizije |
| K06 | `boot` čeka `Promise.all([saved,atlas,mapArt])` | **važi:** isti izraz u `boot` | testirati neuspeh svake grane |
| K07 | `scBuildVisualInstances` keš po identitetu `objects` | **važi:** `scVisualCache.objects===objects` | proveriti sve pisce `objects` (SC-REND-01 §5) |
| K08 | web PWA naspram GML uputstava | **važi kao razlika platformi**, ne kontradikcija koda; GML pravila se ne primenjuju na ovaj build | — |

Nalazi N01–N12 iz [SC-REND-01 §6](./SC-REND-01-CIST-KOD-I-RENDER.md#6-registar-nalaza-n01n12) se ne ponavljaju ovde.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 4. Ključne funkcije

Lokacije su linije u test1 `index.html` (`2d66e55`). Posle bilo koje izmene `index.html` važe tek posle regenerisanja (SC-F08).

| Sistem | Funkcije (linije) | Granica |
|---|---|---|
| Domen | `newGame` L2405, `settle` L2530, `applyCommand` L2678–3158 | validacija, napredak, transakcije; UI ne menja ekonomiju |
| Fizika i trka | `integrate` L3176, `step` L3258, `createRace` L3300, `advanceRace` L3437, `createProjection` L3454 | jedna fizika, stvarne statistike |
| Mapa i gradnja | `supportFootprint` L4280, `forbiddenCell` L4303, `fitsTerrain` L4304, `placementRules` L4461, `canPlace` L4484 | jedna maska i ista validacija za preview i potvrdu |
| Prikaz | `mapRect` L4492, `scBuildVisualInstances` L4514, `paintMap` L4603, `paintRace` L4723 | ista projekcija; crtanje bez logike stanja |
| Save | `validateSave` L4946, `migrateLegacy` L5078, `parseSave` L5179, `openStore` L5223, `indexedRepository` L5233, `localRepository` L5303, `repository` L5336 | validacija, revizija, bez tihog resetovanja |
| UI | `shop` L5759 | prikaz; računanje u domenu |
| App | `openScreen` L7041, `tickClocks` L7082, `commit` L7155, `replaceSave` L7178, `resize` L7196, `returnMap` L7291, `schedule` L7328, `loop` L7329, `mapTap` L7410, `settleClock` L8243, `boot` L8260 | jedna orkestracija i jedan rAF |

**Kartica funkcije** (format za tehničko objašnjenje, iz SC-ARCH-01): simbol · lokacija (fajl + commit + linija) · svrha i preduslovi · ulaz, jedinice, validacija · izlaz i greške · čita / piše / side effects · poziva / pozivaju (proverene reference) · lifecycle i cleanup · pozitivan, negativan i regresioni test · status i dokaz.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 5. Potpuni registar imenovanih funkcija (generisan)

Ponovno generisanje:

```bash
mkdir -p /tmp/sc-tools && (cd /tmp/sc-tools && npm install acorn@8.19.0 acorn-walk@8.3.5)
NODE_PATH=/tmp/sc-tools/node_modules node docs/alati/sc-func-01-registar.cjs index.html > /tmp/registar.md
```

Izlaz zamenjuje sve ispod ove linije.

<!-- generisano: sc-func-01-registar.cjs; ne menjati ručno (SC-F08) -->
Fajl: `index.html` · SHA-256 `c19cc1ac67a2ccc184d2938f0252700205f689d4124bcdf56b672d573c6b7c5d` · izvršnih blokova: 5 · greške parsiranja: 0
Funkcijskih čvorova: 983 (imenovanih 494, anonimnih 489).

| Modul | Funkcija | Imenovanih | Od linije |
|---|---:|---:|---:|
| #sc-startup-trace | 16 | 7 | 9 |
| #sc-pwa-bootstrap | 5 | 0 | 69 |
| blok@L1867 | 1 | 0 | 1873 |
| blok@L1920 | 1 | 0 | 1923 |
| catalog | 1 | 0 | 1924 |
| progression | 16 | 12 | 1930 |
| islandEvents | 16 | 13 | 2056 |
| playerProgress | 5 | 4 | 2146 |
| domain | 168 | 67 | 2204 |
| frames | 1 | 0 | 3164 |
| physics | 6 | 5 | 3169 |
| race | 27 | 16 | 3267 |
| renderer | 54 | 44 | 3488 |
| sceneManager | 13 | 6 | 4068 |
| scenes | 80 | 38 | 4150 |
| storage | 113 | 50 | 4891 |
| ui | 259 | 125 | 5392 |
| metrics | 15 | 12 | 6520 |
| cloud | 11 | 9 | 6599 |
| i18n | 11 | 5 | 6690 |
| app | 164 | 81 | 6759 |

### #sc-startup-trace

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `now` | L13–13 | — | 21 |
| `emit` | L14–26 | `kind, label, start, end, detail` | 4 |
| `begin` | L28–28 | — | 20 |
| `mark` | L29–29 | `label, detail` | 15 |
| `end` | L30–30 | `label, begin, detail` | 26 |
| `probeDecode` | L33–39 | `image, label` | 4 |
| `export` | L40–49 | — | 1 |

### #sc-pwa-bootstrap

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|

### blok@L1867

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|

### blok@L1920

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|

### catalog

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|

### progression

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `divisionOf` | L1936–1936 | `trophies` | 3 |
| `leagueOf` | L1937–1937 | `trophies` | 3 |
| `previousReward` | L1938–1939 | `prev` | 2 |
| `getSeason` | L1940–1948 | `save, now` | 7 |
| `weeklyTasks` | L1949–1949 | `level` | 2 |
| `cosmicTradeCost` | L1950–1950 | `rate` | 2 |
| `creditWeekly` | L1951–1961 | `save, key` | 4 |
| `packAmount` | L1967–1970 | `key, rate` | 2 |
| `inheritedTrait` | L1973–1973 | `prop` | 2 |
| `upgradeInfo` | L1978–2012 | `n, s, key` | 3 |
| `inheritedStat` | L2013–2017 | `snail, key` | 1 |
| `improveSnail` | L2018–2052 | `n, key` | 1 |

### islandEvents

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `timeBreakCost` | L2064–2064 | `production` | 2 |
| `craterPrice` | L2065–2065 | `state` | 2 |
| `nextCraterPrice` | L2066–2066 | `level` | 1 |
| `summonChoices` | L2067–2068 | `phase` | 2 |
| `creditDiamonds` | L2070–2076 | `state, pool, requested` | 7 |
| `canCare` | L2078–2079 | `egg, now` | 7 |
| `releaseExpiredHalf` | L2081–2086 | `state, egg, now` | 2 |
| `accelerateEgg` | L2088–2096 | `state, egg, now, ms` | 3 |
| `tickMeteorRain` | L2098–2108 | `state, now, random` | 1 |
| `nextMeteor` | L2110–2118 | `state, now` | 4 |
| `creditPrestige` | L2120–2135 | `state, snail` | 1 |
| `prestigeBoost` | L2137–2137 | `titles` | 1 |
| `showReference` | L2138–2142 | `level` | 1 |

### playerProgress

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `getLogin` | L2156–2164 | `season, production` | 2 |
| `creditLogin` | L2166–2172 | `save, plan` | 1 |
| `queueReturnGift` | L2174–2186 | `save, elapsed, random` | 1 |
| `creditMuseum` | L2191–2200 | `save, snail, name, at` | 1 |

### domain

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `wheatYield` | L2215–2215 | `s` | 3 |
| `wheatKey` | L2219–2219 | `field` | 3 |
| `wheatBuilt` | L2220–2220 | `s, field` | 4 |
| `wheatDeadline` | L2222–2224 | `s, field=0` | 2 |
| `wheatStage` | L2225–2229 | `s, now, field=0` | 7 |
| `expeditionFactor` | L2250–2250 | `level` | 2 |
| `snailPower` | L2251–2251 | `n` | 4 |
| `expeditionSliz` | L2253–2257 | `hours, power, production, skippedMs, level` | 1 |
| `trackAtlas` | L2265–2265 | `key` | 3 |
| `dimensionOf` | L2274–2274 | `level` | 10 |
| `incubationRate` | L2275–2275 | `level` | 3 |
| `expeditionTeam` | L2276–2276 | `e` | 10 |
| `capacity` | L2284–2284 | `level` | 15 |
| `baseXp` | L2286–2286 | `level` | 6 |
| `xpNeeded` | L2287–2287 | `level` | 5 |
| `reservoirHours` | L2293–2293 | `level` | 2 |
| `reservoirCapacity` | L2294–2295 | `s` | 6 |
| `masteryOpen` | L2298–2298 | `s` | 2 |
| `tourists` | L2299–2302 | `s` | 2 |
| `eggCapacity` | L2303–2303 | `s` | 9 |
| `incubatorUsed` | L2304–2304 | `s` | 9 |
| `craterUsed` | L2305–2305 | `s` | 4 |
| `clip` | L2306–2306 | `value, min, max` | 21 |
| `usable` | L2307–2307 | `snail` | 3 |
| `available` | L2308–2309 | `s, snail` | 18 |
| `assignBestHomes` | L2315–2343 | `s, now, stat=s.autoStat??'prod'` | 3 |
| `primary` | L2328–2329 | `n` | 2 |
| `snailName` | L2344–2344 | `snail, lang='sr'` | 23 |
| `dayKey` | L2345–2345 | `now` | 4 |
| `idOk` | L2348–2348 | `id` | 11 |
| `uuid` | L2349–2351 | — | 6 |
| `rng` | L2352–2355 | `seed` | 3 |
| `seedDay` | L2356–2358 | `day` | 1 |
| `makeDaily` | L2359–2364 | `level, day` | 3 |
| `newSnail` | L2365–2382 | `id, i, random=()=>.5, traits=false` | 3 |
| `vary` | L2367–2367 | — | 6 |
| `newEgg` | L2383–2388 | `id, kind, now, level, random, parents=null, recipe=null` | 5 |
| `hatchExperience` | L2389–2395 | `e, level` | 3 |
| `habitatPrice` | L2397–2397 | `i` | 6 |
| `upgradePrice` | L2398–2404 | `home` | 3 |
| `newGame` | L2405–2413 | `now=Date.now(), id=uuid()` | 6 |
| `requireThat` | L2414–2414 | `ok, message` | 81 |
| `pay` | L2415–2415 | `s, amount, key='sliz'` | 25 |
| `hit` | L2416–2416 | `s, key, n=1` | 10 |
| `addXp` | L2418–2431 | `s, amount` | 9 |
| `trackDay` | L2432–2435 | `now` | 3 |
| `weatherFor` | L2436–2440 | `state, now` | 6 |
| `economyMultiplier` | L2446–2493 | `s, snail, now, applyEvents=true` | 4 |
| `rate` | L2494–2502 | `s, now, applyWeather=true, homeId=null` | 21 |
| `silverDiamondChance` | L2505–2515 | `s, now` | 1 |
| `reserveAt` | L2516–2524 | `s, now` | 4 |
| `startWeather` | L2525–2529 | `s, id, now` | 2 |
| `settle` | L2530–2562 | `s, now, random` | 1 |
| `queueCosmic` | L2563–2568 | `s` | 2 |
| `freeHome` | L2569–2573 | `s` | 1 |
| `findSnail` | L2574–2574 | `s, id` | 10 |
| `countLeague` | L2575–2577 | `s, won` | 2 |
| `findEgg` | L2578–2578 | `s, id` | 4 |
| `checkBuilding` | L2579–2579 | `s, id` | 7 |
| `pickSpecies` | L2580–2589 | `s, kind, random` | 1 |
| `breedPlan` | L2590–2599 | `s, a, b` | 2 |
| `battleTurn` | L2603–2647 | `duel, action, target` | 2 |
| `share` | L2641–2642 | `team` | 3 |
| `settleArenaResult` | L2649–2668 | `s` | 2 |
| `playAutomaticTurns` | L2669–2677 | `s` | 2 |
| `applyCommand` | L2678–3158 | `current, cmd, now=Date.now(), random=Math.random` | 1 |
| `power` | L3093–3093 | `n` | 19 |

### frames

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|

### physics

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `clamp` | L3173–3173 | `v, a, b` | 16 |
| `mass` | L3174–3174 | `p` | 5 |
| `pairs` | L3175–3175 | `ps` | 1 |
| `integrate` | L3176–3257 | `rs, dt, onImpact` | 1 |
| `step` | L3258–3262 | `rs, dt, onImpact` | 1 |

### race

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `cycleCamera` | L3291–3293 | `mode` | 2 |
| `participant` | L3295–3299 | `data, lane, isMe, speed` | 2 |
| `createRace` | L3300–3322 | `snail, key, seed, id=uuid(), mode='league', trophies=0, keeperLevel=1` | 2 |
| `laneCommand` | L3323–3326 | `race, delta` | 4 |
| `boostCommand` | L3327–3330 | `race` | 3 |
| `activateTrail` | L3331–3353 | `race, me` | 1 |
| `slow` | L3341–3341 | `racer, seconds` | 3 |
| `recordWake` | L3354–3363 | `race, me` | 1 |
| `recordRivalWake` | L3365–3375 | `race, p` | 1 |
| `tickRace` | L3376–3436 | `race` | 1 |
| `advanceRace` | L3437–3450 | `race, seconds` | 2 |
| `rankOf` | L3451–3453 | `race` | 1 |
| `createProjection` | L3454–3484 | `width, height, race` | 1 |
| `row` | L3466–3472 | `y, out=null` | 5 |
| `at` | L3473–3481 | `distance, lane` | 22 |
| `distanceAt` | L3482–3482 | `y` | 0 |

### renderer

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `colorOf` | L3547–3555 | `hex` | 7 |
| `shaderProgram` | L3556–3568 | `gl` | 1 |
| `compile` | L3557–3563 | `type, source` | 2 |
| `imageHealth` | L3573–3573 | — | 1 |
| `scImageName` | L3574–3578 | `url` | 1 |
| `loadImage` | L3579–3603 | `url` | 4 |
| `attempt` | L3583–3600 | — | 1 |
| `onload` | L3585–3585 | — | 0 |
| `onerror` | L3586–3598 | — | 0 |
| `assetGroup` | L3604–3611 | `path` | 1 |
| `imagePath` | L3612–3623 | `path` | 8 |
| `constructor` | L3627–3678 | `canvas` | 0 |
| `useCanvasFallback` | L3679–3697 | — | 3 |
| `initGL` | L3698–3717 | — | 2 |
| `preload` | L3718–3734 | `key` | 2 |
| `preloadIllustratedMap` | L3735–3767 | — | 1 |
| `uploadIllustratedMap` | L3768–3783 | — | 2 |
| `uploadDetachedAtlas` | L3784–3799 | — | 2 |
| `drawDetachedObjects` | L3800–3816 | `draws` | 3 |
| `uploadSky` | L3819–3823 | `key, image` | 2 |
| `drawSky` | L3824–3841 | `key` | 1 |
| `drawIllustratedMap` | L3842–3864 | `x, y, w, h` | 1 |
| `upload` | L3865–3879 | `key, image` | 5 |
| `releaseTexture` | L3880–3888 | `key` | 1 |
| `resize` | L3889–3894 | `width, height, ratio` | 3 |
| `begin` | L3895–3916 | `key, bg` | 20 |
| `flush` | L3917–3924 | — | 10 |
| `vertex` | L3925–3931 | `x, y, u, v, r, g, b, a` | 6 |
| `quad` | L3932–3965 | `x1, y1, x2, y2, x3, y3, x4, y4, asset, hex, alpha=1, flip=false, bottom=hex, bot` | 12 |
| `rgba` | L3946–3949 | `key, opacity` | 2 |
| `roadStrip` | L3966–4003 | `rows, colors, shoulder=false` | 2 |
| `edge` | L3967–3967 | `half, index` | 4 |
| `tint` | L3968–3968 | `index` | 4 |
| `opacity` | L3969–3969 | `index` | 3 |
| `shadow` | L4004–4006 | `x, y, rx, ry, opacity` | 1 |
| `fill` | L4007–4009 | `x, y, w, h, hex, alpha=1` | 7 |
| `gradient` | L4010–4026 | `x, y, w, h, top, bottom` | 1 |
| `sprite` | L4027–4029 | `name, x, y, w, h, alpha=1, flip=false` | 15 |
| `spriteTurned` | L4031–4040 | `name, px, py, left, top, w, h, angle, alpha=1, flip=false` | 1 |
| `at` | L4037–4037 | `x, y` | 22 |
| `line` | L4042–4045 | `x1, y1, x2, y2, width, hex, alpha=1` | 2 |
| `tint` | L4046–4049 | `l, r, t` | 4 |
| `estimate` | L4050–4063 | — | 1 |
| `sizeOf` | L4051–4051 | `image` | 6 |

### sceneManager

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `constructor` | L4075–4090 | `renderer, {setTimer=(callback,delay)=>globalThis.setTimeout(callback,delay),clea` | 0 |
| `cancelCleanup` | L4091–4095 | — | 1 |
| `activate` | L4096–4115 | `kind, atlas` | 3 |
| `paintedMap` | L4116–4126 | — | 1 |
| `cleanupOne` | L4127–4141 | — | 4 |
| `stats` | L4142–4145 | — | 1 |

### scenes

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `world` | L4154–4154 | `x, y, w` | 1 |
| `mapView` | L4183–4190 | `width, height, camera` | 5 |
| `baseIslandObjects` | L4192–4209 | `s, now` | 6 |
| `mapObjects` | L4210–4217 | `s, now` | 2 |
| `atPosition` | L4218–4222 | `o, pos` | 6 |
| `structureType` | L4267–4272 | `key` | 6 |
| `groundProfile` | L4275–4275 | `key` | 4 |
| `footprint` | L4276–4279 | `key` | 8 |
| `supportFootprint` | L4280–4284 | `key, gx, gy` | 7 |
| `movable` | L4288–4293 | `o, s` | 3 |
| `clearance` | L4297–4297 | `key` | 2 |
| `overlapBox` | L4298–4301 | `a, b, margin` | 1 |
| `reserve` | L4302–4302 | `taken, key, [gx,gy]` | 4 |
| `forbiddenCell` | L4303–4303 | `x, y` | 1 |
| `fitsTerrain` | L4304–4320 | `taken, key, gx, gy, s=null` | 4 |
| `nearestFree` | L4323–4346 | `taken, key, preferred, s` | 2 |
| `artAt` | L4328–4331 | `id, gx, gy` | 2 |
| `buildLayout` | L4347–4388 | `s` | 1 |
| `ensureWheatBuilt` | L4390–4398 | `s` | 1 |
| `stripUnbuiltWheat` | L4399–4403 | `s` | 1 |
| `stripUnbuiltFacilities` | L4404–4409 | `s` | 1 |
| `prepareIsland` | L4410–4459 | `s` | 7 |
| `trySite` | L4448–4452 | `x, y` | 2 |
| `placementRules` | L4461–4482 | `s, now, key` | 2 |
| `canPlace` | L4484–4487 | `s, now, key, gx, gy` | 4 |
| `mapRect` | L4492–4509 | `obj, view, frames` | 7 |
| `scBuildVisualInstances` | L4514–4520 | `objects, renderer` | 2 |
| `scMapArtRect` | L4521–4528 | `o, view, renderer, artRects` | 3 |
| `scRectOverlap` | L4529–4533 | `a, b` | 4 |
| `scPaintMapSigns` | L4538–4577 | `renderer, labels, artRects, view` | 1 |
| `scUpdateReservoirFx` | L4588–4602 | `s, now, rect=null` | 3 |
| `paintMap` | L4603–4681 | `renderer, s, camera, objects, now, editor` | 1 |
| `roadPalette` | L4686–4692 | `renderer, course, key` | 1 |
| `laneSelect` | L4693–4696 | `project, y, lane` | 2 |
| `segment` | L4697–4699 | `r, a, b, x1, x2, w1, w2, ink, alpha=1, bottom=ink, bottomAlpha=alpha` | 3 |
| `paintLine` | L4700–4714 | `renderer, projection, distance, height` | 2 |
| `paintRace` | L4723–4886 | `renderer, race, motion=true` | 2 |
| `at` | L4865–4865 | `x, y` | 22 |

### storage

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `int` | L4898–4898 | `value, fallback, min=0, max=1e12` | 45 |
| `number` | L4899–4899 | `value, fallback, min=0, max=1e12` | 8 |
| `idOk` | L4900–4900 | `v` | 11 |
| `epoch` | L4901–4901 | `v` | 18 |
| `arrayOk` | L4902–4902 | `a, max` | 19 |
| `assert` | L4903–4903 | `ok, m='Sejv je oštećen ili koristi nepodržan format.'` | 98 |
| `checkSnail` | L4906–4921 | `n` | 1 |
| `checkRecords` | L4922–4925 | `records` | 2 |
| `checkSeason` | L4926–4945 | `season` | 1 |
| `integer` | L4927–4927 | `value, max` | 15 |
| `validateSave` | L4946–5059 | `s` | 9 |
| `unique` | L5032–5032 | `arr` | 3 |
| `legacyTrait` | L5061–5064 | `key` | 2 |
| `legacySnail` | L5065–5077 | `n, i, homes` | 3 |
| `migrateLegacy` | L5078–5178 | `data, now` | 1 |
| `dayNumber` | L5159–5159 | `value` | 2 |
| `parseSave` | L5179–5184 | `text, now=Date.now()` | 3 |
| `download` | L5185–5196 | `name, value` | 4 |
| `validSnapshot` | L5199–5209 | `value, slot='current'` | 4 |
| `recoverSnapshots` | L5210–5222 | `current, backup, checkpoint` | 2 |
| `openStore` | L5223–5232 | `indexedDB` | 1 |
| `onupgradeneeded` | L5227–5227 | — | 0 |
| `onerror` | L5228–5228 | — | 0 |
| `onblocked` | L5229–5229 | — | 0 |
| `onsuccess` | L5230–5230 | — | 0 |
| `indexedRepository` | L5233–5302 | `db` | 1 |
| `onversionchange` | L5234–5234 | — | 0 |
| `load` | L5236–5272 | — | 2 |
| `oncomplete` | L5243–5243 | — | 0 |
| `onabort` | L5244–5244 | — | 0 |
| `onsuccess` | L5245–5270 | — | 0 |
| `onsuccess` | L5253–5269 | — | 0 |
| `onabort` | L5266–5266 | — | 0 |
| `read` | L5273–5280 | `which='current'` | 1 |
| `onerror` | L5277–5277 | — | 0 |
| `onsuccess` | L5278–5278 | — | 0 |
| `commit` | L5281–5300 | `expected, next, previousId=next.saveId, checkpoint=false, erase=false` | 10 |
| `oncomplete` | L5286–5286 | — | 0 |
| `onabort` | L5287–5287 | — | 0 |
| `onsuccess` | L5288–5298 | — | 0 |
| `localRepository` | L5303–5335 | `ls` | 1 |
| `load` | L5305–5322 | — | 2 |
| `restore` | L5306–5320 | — | 3 |
| `read` | L5323–5323 | `which='current'` | 1 |
| `commit` | L5324–5333 | `expected, next, previousId=next.saveId, checkpoint=false, erase=false` | 10 |
| `save` | L5325–5331 | — | 4 |
| `repository` | L5336–5375 | — | 1 |
| `canFallback` | L5348–5348 | `error` | 2 |
| `preserveError` | L5349–5349 | `error` | 2 |
| `oldLocalSave` | L5376–5388 | — | 2 |

### ui

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `escapeHtml` | L5406–5406 | `v` | 82 |
| `numericLocale` | L5407–5407 | — | 4 |
| `format` | L5408–5408 | `n` | 37 |
| `short` | L5409–5409 | `n` | 24 |
| `dec` | L5410–5410 | `n, d=2` | 15 |
| `timer` | L5411–5415 | `ms` | 3 |
| `span` | L5416–5416 | `sec` | 0 |
| `spanRange` | L5417–5421 | `[a,b]` | 1 |
| `u` | L5418–5418 | `t` | 2 |
| `islandWeather` | L5427–5430 | `s, now` | 1 |
| `eggLabel` | L5432–5432 | `k` | 4 |
| `trailOf` | L5435–5435 | `n` | 4 |
| `power` | L5438–5438 | `n` | 19 |
| `btn` | L5440–5441 | `action, label, value='', enabled=true, css='', aria=''` | 164 |
| `cur` | L5442–5442 | `kind, n` | 26 |
| `header` | L5443–5444 | `label, summary='', extras=''` | 32 |
| `image` | L5445–5445 | `path, alt='', lazy=true` | 24 |
| `snailPic` | L5446–5446 | `snail, lazy=true` | 14 |
| `popHead` | L5447–5447 | `title, summary=''` | 6 |
| `info` | L5448–5448 | `text` | 82 |
| `pnl` | L5449–5449 | `inner, css=''` | 70 |
| `prow` | L5450–5450 | `title, right=''` | 46 |
| `bar` | L5451–5451 | `value, max, css=''` | 7 |
| `card` | L5452–5453 | `title, meta, actions='', media='', css=''` | 4 |
| `countdown` | L5454–5454 | `when, ready='Spremno'` | 8 |
| `incubationProgress` | L5455–5455 | `start, end, now` | 2 |
| `options` | L5456–5457 | `list, selectedId, label=n=>snailName(n)+' · '+power(n), empty=''` | 6 |
| `homeIndex` | L5458–5458 | `s, id` | 2 |
| `occupancy` | L5459–5459 | `s, home` | 3 |
| `totalSeats` | L5460–5460 | `s` | 2 |
| `builtState` | L5461–5467 | `s, id, go, subtitle=''` | 6 |
| `sec1` | L5473–5473 | `v` | 5 |
| `trailNumbers` | L5474–5486 | `n` | 1 |
| `trailBox` | L5487–5496 | `n, s, css='', withWeak=false, mode='both', fullLabels=false` | 5 |
| `statCells` | L5497–5500 | `n, keys=['hp','atk','speed','weight','beauty']` | 5 |
| `snailRow` | L5501–5516 | `n, s, withHome=true` | 2 |
| `upgrades` | L5518–5525 | `n, s` | 1 |
| `iconBtn` | L5527–5528 | `tab, label, active, extra=''` | 3 |
| `snailElement` | L5529–5529 | `n` | 5 |
| `snailShareText` | L5530–5534 | `n` | 1 |
| `snailPopup` | L5536–5561 | `n, s, view` | 3 |
| `name` | L5540–5541 | — | 0 |
| `home` | L5542–5543 | — | 0 |
| `up` | L5544–5544 | — | 0 |
| `info` | L5545–5547 | — | 82 |
| `habitatTiles` | L5564–5568 | `s, now, action='habitat-open'` | 1 |
| `nextExpansion` | L5569–5579 | `s` | 1 |
| `name` | L5580–5580 | `a, b` | 0 |
| `power` | L5580–5580 | `a, b` | 19 |
| `prod` | L5581–5581 | `a, b` | 0 |
| `hp` | L5581–5581 | `a, b` | 0 |
| `atk` | L5581–5581 | `a, b` | 0 |
| `speed` | L5581–5581 | `a, b` | 0 |
| `beauty` | L5581–5581 | `a, b` | 0 |
| `weight` | L5581–5581 | `a, b` | 0 |
| `sortedSnails` | L5584–5587 | `list, key, dir=sortDirection` | 2 |
| `sortBar` | L5588–5590 | `view` | 2 |
| `snailList` | L5592–5596 | `list, s, view, withHome=true` | 2 |
| `masteryPanel` | L5598–5606 | `s` | 1 |
| `tree` | L5607–5626 | `s, view, now` | 1 |
| `habitat` | L5629–5675 | `s, view, now` | 1 |
| `eggCard` | L5678–5695 | `e, s, now` | 3 |
| `dailyPanel` | L5696–5704 | `s` | 1 |
| `incubator` | L5705–5712 | `s, now` | 1 |
| `reservoirPanel` | L5715–5725 | `s, now` | 1 |
| `reservoir` | L5726–5731 | `s, now` | 1 |
| `timebreaker` | L5734–5743 | `s, now` | 1 |
| `weatherControls` | L5748–5758 | `s, now` | 2 |
| `shop` | L5759–5817 | `s, view, now` | 1 |
| `catalogGrid` | L5821–5842 | `s, view` | 1 |
| `tile` | L5831–5838 | `n` | 0 |
| `collection` | L5843–5870 | `s, view` | 1 |
| `sel` | L5862–5863 | `id, label, opts, value` | 4 |
| `races` | L5875–5898 | `s, view` | 1 |
| `runnerCard` | L5899–5904 | `n, s` | 1 |
| `fighterCard` | L5907–5912 | `n, s` | 1 |
| `arenaDefaults` | L5913–5918 | `s, view` | 2 |
| `arena` | L5919–5959 | `s, view` | 1 |
| `fighter` | L5940–5948 | `n, enemy` | 2 |
| `breedingPreview` | L5962–5968 | `s, a, b` | 1 |
| `parentCard` | L5969–5972 | `n, s` | 2 |
| `breeding` | L5973–5986 | `s, view` | 1 |
| `weeklyPanel` | L5989–5996 | `s, now` | 1 |
| `meteorPanel` | L5997–6003 | `s, now` | 2 |
| `crater` | L6004–6017 | `s, now` | 1 |
| `pageants` | L6020–6039 | `s, view` | 1 |
| `cell` | L6026–6026 | `k, v` | 24 |
| `expeditionsScreen` | L6042–6062 | `s, view, now` | 1 |
| `feedbackPanel` | L6066–6074 | `view` | 1 |
| `progress` | L6075–6090 | `s, now, view` | 1 |
| `trophyRoom` | L6091–6100 | `s, now` | 1 |
| `loginPanel` | L6101–6110 | `s, now` | 1 |
| `profilePanel` | L6111–6117 | `s` | 1 |
| `cloudPanel` | L6118–6145 | `view` | 1 |
| `dimensionPanel` | L6146–6151 | `s` | 1 |
| `wheatPanel` | L6152–6211 | `s, now, field` | 1 |
| `more` | L6213–6231 | `s, now` | 1 |
| `card` | L6216–6219 | `id, label, asset, sub, action='open'` | 4 |
| `settings` | L6233–6261 | `s, view` | 1 |
| `sec` | L6235–6235 | `title, inner` | 9 |
| `anBars` | L6276–6279 | `rows, key, names` | 3 |
| `anCurrency` | L6280–6288 | `an, k` | 1 |
| `graphCanvas` | L6289–6291 | `points, label, kind` | 2 |
| `anSpark` | L6292–6300 | `an` | 1 |
| `anRaceFrameGraph` | L6301–6308 | `values` | 1 |
| `analytics` | L6309–6363 | `s, view` | 1 |
| `shown` | L6316–6316 | `value` | 13 |
| `cell` | L6317–6317 | `v, l` | 24 |
| `help` | L6364–6369 | — | 1 |
| `wrap` | L6372–6380 | `html, key` | 1 |
| `renderPanel` | L6381–6388 | `key, s, view, now, moveKey` | 1 |
| `screen` | L6389–6421 | `key, s, view, now` | 1 |
| `updateClockNodes` | L6422–6433 | `root, now` | 1 |
| `modal` | L6435–6437 | `title, message, actions` | 5 |
| `hatchPanel` | L6438–6444 | `{name,species:speciesId,kind}, levelUp=false` | 1 |
| `resultPanel` | L6445–6457 | `value, race, pending=false` | 2 |
| `quickSlot` | L6459–6468 | `p, i, snail, badge=''` | 2 |
| `quickResultPanel` | L6469–6490 | `value, race, snail, trace=[]` | 1 |
| `badge` | L6478–6478 | `k` | 1 |
| `discardResultPanel` | L6491–6492 | — | 1 |
| `pausePanel` | L6493–6502 | `lost=false, o={}` | 5 |
| `importPanel` | L6503–6509 | `parsed` | 1 |
| `releasePanel` | L6510–6511 | `n` | 1 |
| `resetPanel` | L6512–6513 | — | 1 |
| `erasePanel` | L6514–6516 | — | 1 |

### metrics

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `rounded` | L6522–6522 | `n, d=1` | 9 |
| `summarize` | L6523–6528 | `values` | 5 |
| `pick` | L6526–6526 | `p` | 4 |
| `createMetrics` | L6529–6595 | — | 1 |
| `addStall` | L6539–6542 | `source, duration` | 2 |
| `start` | L6553–6555 | `track, mode, backend, size, raceType, camera` | 1 |
| `frame` | L6556–6564 | `gap, cpu, calls, upload` | 1 |
| `end` | L6565–6574 | `status` | 26 |
| `islandDraw` | L6575–6579 | `cpu` | 1 |
| `mapReturn` | L6580–6580 | `samples` | 4 |
| `markLoading` | L6581–6581 | `name, ms` | 6 |
| `report` | L6582–6593 | `renderer` | 1 |

### cloud

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `originOk` | L6605–6606 | — | 4 |
| `library` | L6607–6611 | — | 2 |
| `getClient` | L6612–6620 | — | 2 |
| `identity` | L6621–6635 | `create=false` | 4 |
| `status` | L6636–6645 | `create=false` | 2 |
| `upload` | L6646–6661 | `save, expected, exists=false` | 5 |
| `deleteCopy` | L6662–6671 | `expected` | 1 |
| `signOut` | L6672–6676 | — | 2 |
| `download` | L6677–6686 | — | 4 |

### i18n

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `current` | L6702–6702 | — | 3 |
| `setLanguage` | L6703–6707 | `value` | 2 |
| `translate` | L6708–6726 | `value` | 14 |
| `rememberText` | L6727–6732 | `node, source` | 1 |
| `apply` | L6733–6756 | `root` | 3 |

### app

| Ime | Linije | Parametri | Poziva po imenu |
|---|---|---|---:|
| `$` | L6772–6772 | `id` | 101 |
| `watchTransient` | L6792–6798 | `animation` | 4 |
| `done` | L6794–6794 | — | 0 |
| `clearTransientFx` | L6799–6803 | — | 3 |
| `testing` | L6808–6808 | — | 17 |
| `set` | L6815–6815 | `element, value` | 58 |
| `selected` | L6816–6816 | `key` | 20 |
| `nowBound` | L6817–6817 | — | 10 |
| `baseTime` | L6818–6818 | — | 19 |
| `toast` | L6819–6828 | `text` | 56 |
| `settingsWrite` | L6829–6829 | — | 4 |
| `analyticsSave` | L6841–6845 | — | 4 |
| `analyticsLog` | L6846–6856 | `type, before, after` | 1 |
| `measureReport` | L6857–6872 | — | 2 |
| `updateStatus` | L6873–6902 | — | 10 |
| `activityBadge` | L6904–6907 | `now=Date.now()` | 3 |
| `traceRow` | L6911–6911 | `run` | 2 |
| `playQuickBars` | L6912–6939 | `run, trace` | 1 |
| `paint` | L6914–6921 | `idx` | 3 |
| `finish` | L6923–6929 | — | 2 |
| `tick` | L6931–6937 | `now` | 0 |
| `quickRace` | L6940–6964 | — | 2 |
| `arenaLoop` | L6966–6979 | — | 4 |
| `meteorFall` | L6983–6992 | `rain` | 1 |
| `applyTheme` | L6993–6993 | — | 2 |
| `markMap` | L6995–7002 | — | 12 |
| `showSheet` | L7005–7030 | `html, layout='popup'` | 15 |
| `dismiss` | L7031–7036 | — | 12 |
| `signatures` | L7037–7040 | `time` | 2 |
| `openScreen` | L7041–7068 | `key, {keepScroll=false}={}` | 11 |
| `refreshBreeding` | L7069–7078 | — | 1 |
| `updatePanel` | L7079–7081 | — | 38 |
| `tickClocks` | L7082–7154 | — | 6 |
| `commit` | L7155–7177 | `type, fields={}` | 10 |
| `replaceSave` | L7178–7190 | `next, erase=false` | 3 |
| `showImport` | L7191–7194 | `text` | 4 |
| `selectRatio` | L7195–7195 | — | 1 |
| `resize` | L7196–7206 | — | 3 |
| `startMetricSegment` | L7207–7211 | — | 4 |
| `updateRaceHud` | L7212–7241 | `now, force=false` | 4 |
| `startRace` | L7242–7274 | `snailId=selected('race-snail')` | 2 |
| `saveReward` | L7275–7285 | — | 2 |
| `finishRace` | L7286–7290 | `now` | 1 |
| `returnMap` | L7291–7309 | `inputAt=null` | 2 |
| `pauseRace` | L7310–7315 | — | 4 |
| `pauseOptions` | L7316–7316 | — | 5 |
| `resumeRace` | L7317–7320 | — | 3 |
| `toggleCamera` | L7321–7327 | — | 2 |
| `schedule` | L7328–7328 | — | 15 |
| `loop` | L7329–7397 | `now` | 0 |
| `zoomAt` | L7398–7409 | `value, point` | 3 |
| `mapTap` | L7410–7451 | `point` | 1 |
| `attachInput` | L7452–7526 | — | 2 |
| `coords` | L7455–7462 | `x, y, refresh=false` | 5 |
| `soundToggle` | L7527–7538 | — | 1 |
| `cloudAction` | L7539–7634 | `action, value=''` | 2 |
| `openShare` | L7635–7641 | `title, text` | 3 |
| `submitShare` | L7642–7653 | `native` | 2 |
| `flyReward` | L7656–7680 | `key` | 1 |
| `oncancel` | L7671–7671 | — | 0 |
| `onfinish` | L7672–7678 | — | 0 |
| `celebrate` | L7683–7696 | `level` | 4 |
| `devMarkup` | L7698–7719 | — | 1 |
| `b` | L7699–7700 | `action, label, value='', on=false, disabled=false, title=''` | 18 |
| `renderDev` | L7720–7729 | — | 11 |
| `devApply` | L7730–7747 | `change` | 8 |
| `devAction` | L7748–7810 | `action, value` | 2 |
| `shift` | L7766–7774 | `next, ms` | 7 |
| `picks` | L7812–7816 | `name` | 2 |
| `keepPicks` | L7817–7820 | `name, key` | 3 |
| `closeEditor` | L7822–7825 | — | 3 |
| `refreshEditor` | L7826–7842 | `redraw=true` | 4 |
| `openEditor` | L7843–7867 | `key` | 2 |
| `controls` | L7868–8152 | `action, value, inputAt=null` | 5 |
| `attachUI` | L8153–8242 | — | 1 |
| `again` | L8168–8168 | — | 6 |
| `settleClock` | L8243–8259 | — | 2 |
| `boot` | L8260–8348 | — | 1 |
| `onLoss` | L8267–8283 | — | 1 |
| `onRestore` | L8284–8288 | — | 2 |
| `onFallback` | L8289–8294 | — | 1 |
