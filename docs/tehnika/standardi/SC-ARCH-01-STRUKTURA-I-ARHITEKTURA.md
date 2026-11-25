# SC-ARCH-01 — Struktura fajlova, funkcija i sistema (test1 0.8.92)

> **Izdanje za `tihidon/test1`.** Revizija 1.0 je projektni dokument (24.11.2026) pisan nad ZIP-om 0.8.93; ovde su njegova pravila prenesena, a sve činjenice o kodu (linije, putanje, tabela paketa) **ponovo izmerene nad test1** `main` `2d66e55`, `index.html` SHA-256 `c19cc1ac…`, 25.11.2026. Linije iz 0.8.93 su uklonjene jer ovde ne važe. GameMaker deo je sveden na jednu rečenicu (odluka vlasnika: projekat nema GML koda). Pregled svih dokumenata: [docs/README.md](../../README.md).

**Revizija 1.1 (test1) | 25.11.2026 | Obavezni standard za agente i developere**

Status: dokument za usvajanje; nije izmena igre niti release PASS. Dopunjuje [SC-AGENT-01](./SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md) i [SSOT](./PRAVILO-JEDAN-IZVOR-ISTINE.md), ne zamenjuje ih. Aktivni proizvod je HTML/CSS/JavaScript PWA sa WebGL rendererom, lokalnim IndexedDB i opcionim cloud sistemom.

## Sadržaj

1. [Autoritet i opseg](#1-autoritet-i-opseg)
2. [Fizička struktura distribucije](#2-fizička-struktura-distribucije)
3. [Vizuelni jezik dokumentacije](#3-vizuelni-jezik-dokumentacije)
4. [Logička struktura index.html](#4-logička-struktura-indexhtml)
5. [Registar ključnih funkcija](#5-registar-ključnih-funkcija)
6. [Tok podataka i transakcija](#6-tok-podataka-i-transakcija)
7. [Grafika, koordinate i resursi](#7-grafika-koordinate-i-resursi)
8. [Vreme, scene, trka i borba](#8-vreme-scene-trka-i-borba)
9. [PWA, save i hosting su odvojeni slojevi](#9-pwa-save-i-hosting-su-odvojeni-slojevi)
10. [Statički audit paketa](#10-statički-audit-paketa)
11. [Kontrola promena i QA](#11-kontrola-promena-i-qa)
12. [Izvori](#12-izvori)

## 1. Autoritet i opseg

1. Identifikuj tačan commit, `VERSION`, SW cache i origin. Izvršni kod tog builda je autoritet za trenutno ponašanje; odobrena dokumentacija za ciljno ponašanje i postupak ([SC-RAD-01 §2](./SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md#2-hijerarhija-autoriteta)).
2. Pre izmene pronađi postojeći fajl, modul, funkciju, čitaoce, pisce, zavisnosti i testove. Proširi postojećeg vlasnika. Zabranjeni su paralelni autoriteti za podatke, cene, koordinate, kolizije, CSS, render, vreme, save i lifecycle.
3. Dokument je navigacioni indeks, ne runtime konfiguracija. Ne kopirati konstante i formule iz njega u drugi sistem. Linije ispod važe samo za commit `2d66e55`.
4. Nema automatskog refaktorisanja, migracije foldera, novog frameworka ili bundlera. Odstupanje zahteva obrazloženje, minimalni diff, QA i odobrenje vlasnika.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 2. Fizička struktura distribucije

Stvarno stablo test1 (provereno `ls`, 25.11.2026); poklapa se sa ciljnom strukturom izvedenom iz referentnog 0.8.90:

```text
<repo root = publish root>/
├── index.html               # izvršna igra: HTML, CSS, JS, ugrađeni asseti (7.404.866 B)
├── sw.js                    # jedan SW za scope aplikacije
├── manifest.webmanifest     # PWA identitet, start_url "./", scope "./", ikonice iz img/
├── _headers                 # Netlify MIME i cache policy
├── privacy.html             # privatnost
├── delete-account.html      # brisanje naloga
├── img/
│   ├── icon-192.png
│   ├── icon-512.png
│   └── icon-maskable.png
└── docs/                    # dokumentacija (vidi upozorenje ispod)
```

- `version.json` **ne postoji** u test1. Nije obavezan runtime fajl; ako se uvede, mora biti izveden iz odobrenog identiteta izdanja i ulazi u verzijske tačke (danas šest mesta u `index.html` i `sw.js`) ([SC-RAD-01 §3](./SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md#3-činjenice-o-kodu-koje-agent-mora-znati)).
- **Upozorenje:** repo nema `netlify.toml`, pa ako Netlify objavljuje koren repoa, `docs/` je javno dostupan na sajtu. Ne utiče na offline rad (`docs/` nije u `CORE_PATHS`), ali dokumentacija postaje javna. Publish directory nije proveren u Netlify podešavanjima (NIJE PROVERENO). Ne premeštati fajlove bez odluke vlasnika.

`_headers` u test1 (doslovno, isti kao referentni iz 0.8.90):

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

Netlify obrađuje `_headers` u publish direktorijumu; ne dodavati konkurentna pravila u `netlify.toml` bez pregleda. `no-cache` znači revalidacija, ne zabrana skladištenja. Ovaj fajl nije zamena za SW offline cache. Pre premeštanja proveriti sve HTML/JS/CSS URL-ove, manifest, SW `CORE_PATHS`, scope, start URL, pravne stranice i stvarne HTTPS odgovore. Ne prihvatati HTML fallback kao PNG, manifest ili JS.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 3. Vizuelni jezik dokumentacije

Svaki prikaz ima naslov, verziju/commit ili oznaku PREDLOG, legendu, granicu sistema i jasne odnose. Fizički folderi se prikazuju stablom; logički moduli zasebnim stablom; pozivi i tok podataka usmerenim strelicama; stanja dijagramom stanja; poređenje staro/novo u dva poravnata stabla ili tabeli. Ne predstavljati logički modul kao fizički JS fajl ako je u `index.html`.

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

Boja je dopunska; tekstualna oznaka je obavezna. Prikaz mora biti čitljiv na mobilnom uređaju. Bez dekorativnih strelica koje glume pozive. Za svaku promenu navesti šta je ostalo isto. Tehnički dijagram nije screenshot igre.

Obrazac inventara: `putanja/simbol | tip | vlasnik | odgovornost | čita | piše | zavisnosti | test | status | dokaz`. Obrazac poređenja: `pre → posle | razlog | uticaj | rollback`. Nepoznato označiti `NIJE PROVERENO`, ne popunjavati pretpostavkama.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 4. Logička struktura index.html

Linije dodele `modules.*` u test1 (`grep -noE 'modules\.[A-Za-z0-9]+ *='`, 17 modula). Grupisanje služi za navigaciju; ne tvrdi da su to zasebni fajlovi ili potpun graf zavisnosti.

```text
index.html
├── HTML / CSS (1 <style>) / ugrađeni resursi
├── #sc-startup-trace         L8     dijagnostika pokretanja
├── #sc-pwa-bootstrap         L66    rana registracija jedinog SW-a
├── SC_LEGACY_CLOUD           L1747  URL i javni sb_publishable ključ starog projekta
└── modules (glavni blok od L1920)
    ├── Podaci i pravila
    │   ├── catalog          L1924
    │   ├── progression      L1930
    │   ├── islandEvents     L2056
    │   ├── playerProgress   L2146
    │   └── domain           L2204
    ├── Grafika i simulacija
    │   ├── frames           L3164
    │   ├── physics          L3169
    │   ├── race             L3267
    │   ├── renderer         L3488
    │   ├── sceneManager     L4068
    │   └── scenes           L4150
    ├── Podrška i interfejs
    │   ├── storage          L4891
    │   ├── ui               L5392
    │   ├── metrics          L6520
    │   ├── cloud            L6599
    │   └── i18n             L6690
    └── app                  L6759
```

Vlasništvo (proveriti implementaciju pre zahvata): catalog — definicije sadržaja; progression/playerProgress — postojeći proračuni napretka; islandEvents — događaji ostrva; domain — stanje i transakcije; frames — grafički frejmovi; physics/race — simulacija i pravila trke; renderer — GPU resursi i prikaz; sceneManager/scenes — scene, projekcija i geometrija; storage — validacija i trajno lokalno stanje; ui — prikaz i unos; metrics — merenje; cloud — sinhronizacija; i18n — tekstovi; app — orkestracija. Ne zaključivati javni API samo iz naziva modula.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 5. Registar ključnih funkcija

Lokacije ključnih funkcija i potpuni generisani registar: [SC-FUNC-01 §4–§5](./SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md#4-ključne-funkcije). Ne voditi drugu listu linija u ovom dokumentu (SSOT). Razlikovati istoimene funkcije u različitim modulima, npr. `app` `commit` i storage `commit`.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 6. Tok podataka i transakcija

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

Tačan redosled prikaza, potvrde i trajnog upisa proveriti u konkretnoj komandi; dijagram ne znači atomsku transakciju svih sistema. Ne potvrditi uspeh korisniku pre predviđenog rezultata upisa. Odbijena komanda ne naplaćuje resurse. Dupli klik i konflikt revizije ne smeju napraviti duplu nagradu. UI ne poseduje jedinu kopiju stanja. Cloud nije uslov za lokalni offline napredak. Ne izlagati tajne ključeve (javni `sb_publishable` ključ u `SC_LEGACY_CLOUD` je namenjen klijentu, nije tajna).

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 7. Grafika, koordinate i resursi

```text
Ekran / CSS px / DPR → postojeća projekcija → svet → grid ćelija
                                      │
                         stvarna osnova objekta
                                      ▼
                        postojeća maska i validacija
                          ├─ preview
                          └─ potvrda postavljanja
```

Ista logika za prikaz, klik, touch, zoom/pan i potvrdu. Put, ivica, fontana, bazen i vodopad eksplicitno kroz postojeće pravilo terena (`FIELD.rows` → `forbiddenCell`). Proveriti stvarnu masku, ne pretpostavljati je po slici. Renderer koristi postojeće teksture i atlas, ne duplira GPU resurse, ne vrši gameplay transakcije. Bez nepotrebnih alokacija po frejmu; contextlost/restored i cleanup prema vlasništvu ([SC-REND-01](./SC-REND-01-CIST-KOD-I-RENDER.md)). CSS: postojeća kaskada, jedan vlasnik stilskog pravila; PL-01 i CSS-01 obavezni. Poštovati `prefers-reduced-motion`, fokus, tastaturu i relevantni WCAG AA; ne uklanjati funkcionalni sadržaj radi performansi.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 8. Vreme, scene, trka i borba

Sačuvani realni rokovi i postojeći `settle` su autoritet za inkubaciju, žetvu i resurse; vreme igre u `app` daje `nowBound()` (vidi SC-REND-01 T01 i N01). Animacije, rAF i intervali nisu autoritet offline vremena. Testirati povratak iz trke, zatvaranje, negativno vreme i promenu sata. Scene ulaze/izlaze kroz postojeći `sceneManager`/`app`; suspendovati nerelevantni UI i rad, ne praviti drugi manager. Statistike trke/borbe proizlaze iz stvarnih podataka puža, bez alternativnih tabela. Ne izmišljati nazive funkcija borbe: pronaći ih u kodu. GameMaker pravila ne važe za ovaj build.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 9. PWA, save i hosting su odvojeni slojevi

```text
Git → Netlify publish → HTTP odgovor → browser / SW → app shell
                                            │
                                 Cache Storage (resursi)

App domain → storage → IndexedDB (napredak) ↔ postojeći cloud adapter
```

Jedan SW po aplikativnom scope-u; jedan kontrolisani cache namespace. U test1: `CACHE_NAME = 'snail-city-shell-0.8.92-css-unified-p1-r2'`, `OWNED_PREFIXES = ['snail-city-08', 'snail-city-shell-']`, sedam `CORE_PATHS` (index, manifest, tri ikonice iz `img/`, privacy, delete-account), budžeti `CORE_SIZE_LIMIT` 16 MiB i `PER_RESOURCE_LIMIT` 12 MiB (`sw.js`). Budžeti su postojeći kod; ne uvoditi kopiju konstanti. Ne ublažavati MIME/size validaciju radi prolaska instalacije. Prekinuta instalacija ne sme obrisati validan stari shell niti korisnički save. Cache Storage nije IndexedDB. Ne koristiti Clear site data, unregister ili reset profila kao rutinsku popravku. HTTPS ili localhost za SW.

Obavezna verifikacija: inventar Git → deploy stablo → direktni HTTP status, MIME i decoded body SHA-256 → browser sa i bez SW presretanja → kompletan online boot → offline cold relaunch → sačuvani identitet/revizija → reconnect/upgrade/rollback. Status 200 ili aktivan SW sam po sebi nije PASS. Stanje PW-01 za ovaj build: [PW-01-STANJE-0.8.92](../pwa-offline/PW-01-STANJE-0.8.92.md).

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 10. Statički audit paketa

Kolone 0.8.90, 0.8.92 ZIP i 0.8.93 su iz revizije 1.0 (priloženi ZIP-ovi, 24.11.2026). Kolona test1 je izmerena 25.11.2026.

| Stavka | 0.8.90 | 0.8.92 ZIP | 0.8.93 | **test1 (0.8.92)** |
|---|---:|---:|---:|---:|
| `index.html` bajtovi | 7.018.536 | 7.404.866 | 7.225.560 | **7.404.866** (isti SHA-256 kao 0.8.92 ZIP) |
| `<script>` tagovi | 20 | 21 | 21 | **21** (5 izvršnih) |
| `<style>` blokovi | 9 | 1 | 1 | **1** |
| `_headers` | postoji | nedostaje | nedostaje | **postoji** |
| Ikonice | `img/` | `img/` | root | **`img/`** |
| SW i manifest očekuju | `img/` | `img/` | `img/` | **`img/`** — slaže se |
| SW cache (`snail-city-shell-` …) | `0.8.90-r2` | `0.8.92-css-unified-p1-r1` | `0.8.93-deco-webp-r1` | **`0.8.92-css-unified-p1-r2`** |

CRC i izgled paketa ne dokazuju stabilnost igre. test1 nema statička odstupanja putanja iz ove tabele; stvarni HTTPS odgovori nisu provereni.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 11. Kontrola promena i QA

PRE: cilj, potrebni rezultati, ciljni identitet, vlasnik funkcije, stablo pre/posle, reference, nedostajući podaci, rizik, rollback. TOKOM: jedan minimalan diff, bez duplikata, provera sintakse i svih zavisnosti; brisanje samo po [SC-RAD-01 §6](./SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md#6-brisanje-dokaz-po-vrsti). POSLE: G0–G7 prema relevantnosti ([SC-AGENT-01 §14](./SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md#14-sc-a14--obavezna-qa-matrica-i-release-gate)), konkretni dokazi i odluka vlasnika. Za izmenu grafike stvarni Chromium screenshot pre/posle, za animaciju GIF iz realnih frejmova („Pogledaj kretanje“). Za optimizaciju A/B/R na istom uređaju i stanju, p50/p95/max. Fizički Android za mobilni release. PW-01 na testnom profilu. Bez merge/deploy-a bez odobrenja.

| Kontrola | Način | Alat | Kriterijum |
|---|---|---|---|
| Fajlovi | inventar i reference | git tree, `git grep` | nema obavezne nedostajuće putanje |
| Funkcije | deklaracije, pozivi, read/write | `git grep` + [SC-FUNC-01](./SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md) | jedan vlasnik, bez paralelnih pravila |
| HTTP | status, MIME, SHA-256 decoded body | curl / DevTools | tačan sadržaj i tip |
| PWA | lifecycle i cold offline | Chromium Application + fizički Android | PW-01 bez gubitka sejva |
| Grafika | stvarni render i interakcije | Chromium, screenshot, realni GIF | očekivan prikaz i funkcija |
| Performanse | ponovljeno merenje | DevTools Performance | bez regresije |

Statusi: URAĐENO / DELIMIČNO / NIJE URAĐENO za isporuke; PASS / FAIL / BLOCKED / NIJE TESTIRANO za testove. Ne mešati. Izveštaj navodi šta nije dirano. Relevantan P0/P1 neuspeh blokira release.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 12. Izvori

- Kod: `tihidon/test1` `main` `2d66e55` (`index.html`, `sw.js`, `manifest.webmanifest`, `_headers`), provereno 25.11.2026.
- Revizija 1.0: projektni dokument `SC-ARCH-01-STRUKTURA-I-ARHITEKTURA.md` (claude.ai projekat „APP SC 0.8.92-css-unified“), 24.11.2026.
- Eksterni: [Netlify custom headers](https://docs.netlify.com/manage/routing/headers/), [MDN Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers), [MDN WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices), [Chrome Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance), [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Web Vitals](https://web.dev/articles/vitals) — preneti iz revizije 1.0, nisu ponovo čitani u ovoj isporuci.

<sub>[↑ Sadržaj](#sadržaj)</sub>
