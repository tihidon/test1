# SC-ARCH-01 — Struktura fajlova, funkcija i sistema

**Snail City 0.8.93 | Revizija 1.0 | 24.11.2026 | Obavezni predlog standarda za agente i developere**

Status: dokument za usvajanje; nije izmena igre niti release PASS. Dopunjuje SC-AGENT-01 i SSOT, ne zamenjuje ih. Aktivni proizvod je HTML/CSS/JavaScript PWA sa WebGL rendererom, lokalnim IndexedDB i opcionim cloud sistemom. GameMaker/GML pravila važe samo za stvarni port.

## 1. Autoritet i opseg

1. Identifikuj tačan ZIP, granu, commit, blob, VERSION, SW cache i origin. Izvršni kod tog kandidata je autoritet za trenutno ponašanje; odobrena dokumentacija za ciljno ponašanje i postupak.
2. Pre izmene pronađi postojeći fajl, modul, funkciju, čitaoce, pisce, zavisnosti i testove. Proširi postojećeg vlasnika. Zabranjeni paralelni autoriteti za podatke, cene, koordinate, kolizije, CSS, render, vreme, save i lifecycle.
3. Dokument je navigacioni indeks, ne runtime konfiguracija. Ne kopirati konstante i formule iz njega u drugi sistem. Linije ispod važe samo za priloženi 0.8.93 ZIP.
4. Nema automatskog refaktorisanja, migracije foldera, novog frameworka, bundlera ili GML implementacije. Odstupanje zahteva obrazloženje, minimalni diff, QA i odobrenje vlasnika.

## 2. SC-ARCH-01.01 — Fizička struktura distribucije

Ciljna struktura (projektna odluka izvedena iz referentnog 0.8.90, ne univerzalni web standard):

```text
<publish-root>/
├── index.html               # izvršna igra: HTML, CSS, JS, ugrađeni asseti
├── sw.js                    # jedan SW za scope aplikacije
├── manifest.webmanifest     # PWA identitet, start_url, scope, ikonice
├── _headers                 # Netlify MIME i cache policy
├── privacy.html             # privatnost
├── delete-account.html      # brisanje naloga
└── img/
    ├── icon-192.png
    ├── icon-512.png
    └── icon-maskable.png
```

Repo root i publish root nisu nužno isti. Dopušten je postojeći layout `.` ili `public/`, nikad dva konkurentna deploy stabla. Pre promene evidentirati Netlify publish directory. Dokumentaciju, QA, arhive i razvojne alate držati izvan javne distribucije kada layout to omogućava; ne uvoditi migraciju samo zbog ovog pravila. `version.json` postoji u 0.8.90, ali nije obavezan novi runtime fajl u 0.8.93. Ako se koristi, mora biti izveden iz odobrenog identiteta izdanja.

Referentni `_headers` iz 0.8.90 (doslovno):

```text
/sw.js
  Cache-Control: no-cache, max-age=0, must-revalidate
  Content-Type: application/javascript; charset=utf-8
/index.html
  Cache-Control: no-cache, max-age=0, must-revalidate
/
  Cache-Control: no-cache, max-age=0, must-revalidate
/manifest.webmanifest
  Content-Type: application/manifest+json
  Cache-Control: no-cache, max-age=0, must-revalidate
```

Netlify obrađuje `_headers` u publish direktorijumu; ne dodavati konkurentna pravila u `netlify.toml` bez pregleda. `no-cache` znači revalidacija, ne zabrana skladištenja. Ovaj fajl nije zamena za SW offline cache. Pre premeštanja proveriti sve HTML/JS/CSS URL-ove, manifest, SW CORE_PATHS, scope, start URL, pravne stranice, backend callback URL ako je pogođen i stvarne HTTPS odgovore. Ne prihvatati HTML fallback kao PNG/manifest/JS.

## 3. SC-ARCH-01.02 — Vizuelni jezik dokumentacije (za svaki sistem)

Svaki prikaz ima naslov, verziju/commit ili oznaku PREDLOG, legendu, granicu sistema i jasne odnose. Fizički folderi se prikazuju stablom; logički moduli zasebnim stablom; pozivi i tok podataka usmerenim strelicama; stanja dijagramom stanja; poređenje staro/novo u dva poravnata stabla ili tabeli. Ne predstavljati logički modul kao fizički JS fajl ako je u index.html.

| Simbol | Značenje |
|---|---|
| 📁 | direktorijum |
| 📄 | fajl |
| ƒ | funkcija |
| ▣ | modul ili vlasnik sistema |
| ◉ | skladište podataka |
| → | smer konkretnog poziva ili toka; obavezno imenovati tip |
| + / − / ~ / = | dodato / uklonjeno / izmenjeno / nepromenjeno |
| ✓ / ! / × / ? | provereno / odstupanje / nedostaje / nije provereno |

Boja je dopunska: neutralno za postojeće, plavo za kod, žuto za foldere, zeleno za potvrđeno, narandžasto za odstupanje, crveno za grešku. Tekstualna oznaka obavezna; boja sama nije dokaz. Prikaz mora biti čitljiv na mobilnom uređaju; kod širokog stabla koristi vertikalni raspored ili monospace tekst. Bez dekorativnih strelica koje glume pozive. Za svaku promenu navesti šta je ostalo isto. Tehnički dijagram nije screenshot igre.

Obrazac inventara: `putanja/simbol | tip | vlasnik | odgovornost | čita | piše | zavisnosti | test | status | dokaz`. Obrazac poređenja: `pre → posle | razlog | uticaj | rollback`. Nepoznato označiti `NIJE PROVERENO`, ne popunjavati pretpostavkama.

## 4. SC-ARCH-01.03 — Logička struktura postojećeg index.html

Statički pronađene deklaracije `modules.*` u ZIP 0.8.93 (17 modula). Grupisanje ispod služi za navigaciju; ne tvrdi da su to zasebni fajlovi ili potpun graf zavisnosti.

```text
index.html
├── HTML / CSS / ugrađeni resursi / PWA bootstrap
└── modules
    ├── Podaci i pravila
    │   ├── catalog          L1936
    │   ├── progression      L1942
    │   ├── islandEvents     L2068
    │   ├── playerProgress   L2158
    │   └── domain           L2216
    ├── Grafika i simulacija
    │   ├── frames           L3176
    │   ├── physics          L3181
    │   ├── race             L3279
    │   ├── renderer         L3500
    │   ├── sceneManager     L4080
    │   └── scenes           L4162
    ├── Podrška i interfejs
    │   ├── storage          L4903
    │   ├── ui               L5404
    │   ├── metrics          L6532
    │   ├── cloud            L6611
    │   └── i18n             L6702
    └── app                 L6771
```

Vlasništvo (obavezna granica, proveriti implementaciju pre zahvata): catalog — definicije sadržaja; progression/playerProgress — postojeći proračuni napretka; islandEvents — događaji ostrva; domain — stanje i transakcije; frames — grafički frejmovi; physics/race — simulacija i pravila trke; renderer — GPU resursi i prikaz; sceneManager/scenes — scene, projekcija i postojeća geometrija; storage — validacija i trajno lokalno stanje; ui — prikaz i unos; metrics — merenje; cloud — postojeća sinhronizacija; i18n — tekstovi; app — orkestracija. Ne zaključivati tačan javni API samo iz naziva modula.

## 5. SC-ARCH-01.04 — Registar ključnih funkcija

| Sistem | Postojeći simboli i lokacija u 0.8.93 | Obavezna granica |
|---|---|---|
| Domen | `newGame`, `settle` L2542, `applyCommand` L2690 | Validacija, napredak i transakcije; UI ne menja ekonomiju direktno |
| Mapa | `FIELD`, `SC_STRUCTURE`, `supportFootprint` L4292, `forbiddenCell`, `fitsTerrain`, `placementRules`, `canPlace` L4496 | Jedna maska, stvarni oslonac, ista validacija preview i potvrde |
| Prikaz mape | `mapRect` L4504, `scBuildVisualInstances` L4526, `paintMap` L4615, `mapView` | Ista projekcija za prikaz i hit test |
| Trka | `integrate`, `step`, `createRace` L3312, `advanceRace` L3449, `createProjection` L3466, `paintRace` L4735 | Jedna fizika, stvarne statistike, renderer bez nagrada |
| Save | `parseSave` L5191, `openStore` L5235, storage commit | Validacija, revizija, konflikt, bez tihog resetovanja |
| App | `openScreen` L7053, `tickClocks` L7094, `commit` L7167, `resize` L7208, `schedule` L7340, `loop` L7341 | Jedna orkestracija i glavna RAF petlja; pomoćne animacije proveriti zasebno |

Ovo je početni indeks, ne iscrpan popis svih funkcija. Svaki agent dopunjava relevantni deo postojećeg registra pre izmene, bez pravljenja paralelnog registra. Razlikovati istoimene funkcije u različitim modulima, npr. app commit i storage commit.

Kartica funkcije (obavezan format za tehničko objašnjenje):

```text
Simbol: modules.<vlasnik> / <funkcija>
Lokacija: fajl + commit/blob + linija
Svrha / preduslovi:
Ulaz / jedinice / validacija:
Izlaz / greške:
Čita / piše / side effects:
Poziva / pozivaju (proverene reference):
Lifecycle / resursi / cleanup:
Pozitivan, negativan i regresioni test:
Status / dokaz:
```

## 6. SC-ARCH-01.05 — Tok podataka i transakcija

Normativni tok odgovornosti, ne potvrđeni graf svih poziva:

```text
Miš / touch / tastatura
          │ namera
          ▼
UI + app orkestracija
          │ validirana komanda
          ▼
Domen (applyCommand / settle) ── koristi postojeće kataloge i pravila
          │ rezultat / stanje
          ├──► storage commit ──► IndexedDB (saveId / revision)
          └──► UI / scene / renderer ──► vidljivi rezultat
                    cloud: opciona sinhronizacija kroz postojeći adapter
```

Tačan redosled prikaza, potvrde i trajnog upisa proveriti u konkretnoj komandi; ne pretpostavljati da dijagram znači atomsku transakciju svih sistema. Ne potvrditi uspeh korisniku pre predviđenog rezultata upisa. Odbijena komanda ne naplaćuje resurse. Dupli klik i konflikt revizije ne smeju napraviti duplu nagradu. UI ne poseduje jedinu kopiju stanja. Cloud nije uslov za lokalni offline napredak; proveriti postojeći režim autentikacije, konflikte i migracije. Ne izlagati tajne ključeve.

## 7. SC-ARCH-01.06 — Grafika, koordinate i resursi

```text
Ekran / CSS px / DPR → postojeća projekcija → svet → grid ćelija
                                      │
                         stvarna osnova objekta
                                      ▼
                        postojeća maska i validacija
                          ├─ preview
                          └─ potvrda postavljanja
```

Ista logika za prikaz, klik, touch, zoom/pan i potvrdu. Put, ivica, fontana, bazen i vodopad eksplicitno kroz postojeće pravilo terena. Proveriti stvarnu masku, ne pretpostavljati je po slici. Renderer koristi postojeće teksture/atlas, ne duplira GPU resurse, ne vrši gameplay transakcije. Bez nepotrebnih alokacija po frejmu; contextlost/restored i cleanup prema vlasništvu. CSS: postojeća kaskada, jedan vlasnik stilskog pravila; PL-01 i CSS-01 obavezni. Poštovati prefers-reduced-motion, fokus, tastaturu i relevantni WCAG AA; ne uklanjati funkcionalni sadržaj radi performansi.

## 8. SC-ARCH-01.07 — Vreme, scene, trka i borba

Sačuvani realni rokovi i postojeći `settle`/`Date.now()` su autoritet za inkubaciju, žetvu i resurse. Animacije, RAF i intervali nisu autoritet offline vremena. Testirati povratak iz trke, zatvaranje, negativno vreme i promenu sata. Scene ulaze/izlaze kroz postojeći sceneManager/app; suspendovati nerelevantni UI i rad, ne praviti drugi manager. Statistike trke/borbe proizlaze iz stvarnih podataka puža, bez alternativnih tabela. Ne izmišljati nazive funkcija borbe: pronaći u ciljanom kodu. Za stvarni GML port važe global.game_data, persistent obj_game_manager, GAME_STATE, real-time datumi, save/load i Clean Up iz SC-AGENT-01; to nije trenutna web implementacija.

## 9. SC-ARCH-01.08 — PWA, save i hosting su odvojeni slojevi

```text
Git / ZIP → Netlify publish → HTTP odgovor → browser / SW → app shell
                                                 │
                                      Cache Storage (resursi)

App domain → storage → IndexedDB (napredak) ↔ postojeći cloud adapter
```

Jedan SW po aplikativnom scope-u; jedan kontrolisani cache namespace. CORE_PATHS u 0.8.93: index, manifest, tri ikonice, privacy, delete-account; budžeti 16 MiB ukupno i 12 MiB po resursu. Budžeti su postojeći kod, ne uvoditi kopiju konstanti. Ne ublažavati MIME/size validaciju radi prolaska instalacije. Prekinuta instalacija ne sme obrisati validan stari shell niti korisnički save. Cache Storage nije IndexedDB. Ne koristiti Clear site data, unregister ili reset profila kao rutinsku popravku bez plana i saglasnosti; testirati na posebnom profilu. HTTPS ili localhost za SW, odgovarajući scope. Ne cache-ovati privatne API odgovore mimo odobrenog sistema.

Obavezna verifikacija: inventar ZIP/Git → deploy stablo → direktni HTTP status/MIME/decoded body SHA-256 → browser sa i bez SW presretanja → kompletan online boot → offline cold relaunch → sačuvani identitet/revizija → reconnect/upgrade/rollback. Status 200 ili aktivan SW sam po sebi nije PASS. Ako se bajtovi ili script blokovi razlikuju, izolovati sloj koji menja sadržaj; ne kriviti browser/hosting bez dokaza.

## 10. SC-ARCH-01.09 — Statički audit priloženih paketa

| Stavka | 0.8.90 | 0.8.92 | 0.8.93 |
|---|---:|---:|---:|
| ZIP CRC test | PASS | PASS | PASS |
| index.html bajtovi | 7.018.536 | 7.404.866 | 7.225.560 |
| script tagovi | 20 | 21 | 21 |
| _headers | postoji | nedostaje | nedostaje |
| Ikonice | img/ | img/ | root |
| SW i manifest očekuju | img/ | img/ | img/ |
| SW cache | 0.8.90-r2 | 0.8.92-css-unified-p1-r1 | 0.8.93-deco-webp-r1 |

Cache prefiks `snail-city-shell-` skraćen radi čitljivosti. CRC PASS dokazuje čitljivost paketa, ne stabilnost igre. Korisnik navodi da su sva tri stabilna; to nije novi runtime dokaz. 0.8.93 ima statičko odstupanje putanja i oba novija paketa nemaju referentni `_headers`. To opravdava ciljni standard, ne dokazuje da je svaki online problem uzrokovan tim odstupanjima.

## 11. SC-ARCH-01.10 — Kontrola promena i QA

PRE: cilj, potrebni rezultati, ciljni identitet, vlasnik funkcije, stablo pre/posle, reference, nedostajući podaci, rizik, rollback. DURING: jedan minimalan diff, bez duplikata, proveri sintaksu i sve zavisnosti; brisanje samo uz tri provere iz SC-AGENT-01. POSLE: G0–G7 prema relevantnosti, konkretni dokazi i odluka vlasnika. Za izmenu grafike stvarni Chromium screenshot pre/posle, za animaciju GIF iz realnih frejmova (Pogledaj kretanje). Za optimizaciju A/B/R isti uređaj i stanje, p50/p95/max; INP/LCP/CLS prema SC-AGENT-01. Fizički Android za mobilni release. PW-01 na testnom profilu, mreže isključene, zatvaranje/ponovno pokretanje, saveId/revision/level, upgrade i rollback. Bez merge/deploy bez odobrenja.

| Kontrola | Način | Alat | Kriterijum |
|---|---|---|---|
| Fajlovi | inventar i reference | ZIP/CRC, git tree, rg | nema obavezne nedostajuće putanje |
| Funkcije | deklaracije, pozivi, read/write | rg + pregled koda | jedan vlasnik, bez paralelnih pravila |
| HTTP | status, MIME, SHA-256 decoded body | curl/DevTools | tačan sadržaj i tip |
| PWA | lifecycle i cold offline | Chromium Application + fizički Android | PW-01 bez gubitka save |
| Grafika | stvarni render i interakcije | Chromium, screenshot, realni GIF | očekivan prikaz i funkcija |
| Performanse | ponovljeno merenje | DevTools Performance | bez regresije prema odobrenom budžetu |

Statusi: URAĐENO / DELIMIČNO / NIJE URAĐENO za isporuke; PASS / FAIL / BLOCKED / NIJE TESTIRANO za testove. Ne mešati. Izveštaj mora navesti šta nije dirano. Relevantan P0/P1 neuspeh blokira release.

## 12. Izvori i primena

Projektni izvori direktno pročitani: `Snail-City-0.8.93-SOURCES.md`, `SC-0.8.93-OBAVEZNI-STANDARD-AGENATA.md`, tri priložena ZIP-a (inventar, CRC, manifest, SW deklaracije, _headers i ključne deklaracije index.html). Projektni linkovi: [SSOT](https://github.com/tihidon/snail-city-test/blob/main/docs/tehnika/standardi/PRAVILO-JEDAN-IZVOR-ISTINE.md), [docs](https://github.com/tihidon/snail-city-test/tree/main/docs), [test-2](https://github.com/tihidon/test-2). Linkovi su referentni; živi privatni repo nije ponovo auditovan u ovoj isporuci.

Eksterni izvori: [Netlify custom headers](https://docs.netlify.com/manage/routing/headers/), [Netlify build configuration](https://docs.netlify.com/build/configure-builds/overview/), [MDN Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers), [MDN WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices), [Chrome Modern Web Guidance](https://developer.chrome.com/docs/modern-web-guidance) — konsultovani rezultati 24.11.2026. Dodatne referentne smernice iz SC-AGENT-01: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Web Vitals](https://web.dev/articles/vitals), [Chrome forced reflow](https://developer.chrome.com/docs/performance/insights/forced-reflow). Projektna organizacija i vizuelna legenda su lokalni standard, ne zahtev W3C/MDN. Za konkretan patch agent ponovo proverava relevantan standard i kompatibilnost.

Predložena lokacija u dokumentacionom repozitorijumu: `docs/tehnika/standardi/SC-ARCH-01-STRUKTURA-I-ARHITEKTURA.md`; postojeći indeks docs i AGENTS treba samo da referenciraju ovaj dokument nakon odobrenja, bez kopiranja sadržaja.

## 13. Status ove isporuke

| Stavka | Status |
|---|---|
| Čitanje projektnih standarda i tri ZIP-a | URAĐENO |
| Standard fizičke/logičke strukture | URAĐENO |
| Vizuelni jezik i obrazac dokumentovanja funkcija | URAĐENO |
| Ključni moduli i početni registar funkcija | URAĐENO |
| Potpun graf poziva i svih handlera | DELIMIČNO — nije predmet potpunog statičkog audita |
| Live Git/Netlify i Chromium test | NIJE URAĐENO — dokumentaciona isporuka |
| Izmene igre, Git-a, deploy-a ili profila | NIJE URAĐENO — namerno |
