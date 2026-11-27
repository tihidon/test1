# Snail City — zajednička dokumentacija test1 / test-cl1

Poslednja izmena indeksa: 2026-11-27

**P0 — kanonski autoritet:** `tihidon/test1` je primarni razvojni repo; `snail-city-test` je istorijski izvor. Aktivna pravila se održavaju ovde. P1/P3/P10 podaci ispod su istorijski snapshotovi, ne dokaz za aktuelni checkout ili novo izvršno merenje.

Istorijski indeks dokumenata za P3 (nije trenutni runtime dokaz): `tihidon/test1` `main` `5b4b030` (PR #13), `index.html` SHA-256 `594026b9ffab62ceb8dbbfa181c887edea3f903ff84a27151a2330fb978dc58a`, `const VERSION = '0.8.92-css-unified-p3'`, SW `snail-city-shell-0.8.92-css-unified-p3-r2`. Kopije označene „`2d66e55` / `c19cc1ac…`“ proverene su samo nad p1 commit-om i nisu ponovo proverene nad p3. Svaki dokument je pre prenosa proveren prema ovom kodu 25.11.2026; netačne tvrdnje su ispravljene ili dokument nije prenet (§3).

### DOC-003 — aktuelni Agent Team registar (snapshot 26.11.2026)

Provereno 28.11.2026. [Snail City Agent Team](https://chatgpt.com/plugins/plugins_6b07821ba2488191803130852db1560a) **0.7.7**, izdanje `pluginrel_6b0a0b385834819194b9eb31670f2401`. Oba manifesta navode 0.7.7. Svih 16 profila navodi internu proveru D7 i odluku vlasnika D8. Provera obuhvata objavljene instrukcije.

| Profil u Team paketu | Pročitana verzija |
|---|---|
| `coordinate-team` | 0.5.13 |
| `team-agent-conduct` | 0.1.2 |
| `team-architecture` | 0.5.10 |
| `team-chromium-qa` | 0.5.7 |
| `team-defensive-auditor` | 0.1.3 |
| `team-engineering` | 0.5.9 |
| `team-handoff` | 0.5.7 |
| `team-legal` | 0.1.2 |
| `team-marketing` | 0.3.3 |
| `team-qa-assurance` | 0.5.8 |
| `team-qa-planning` | 0.5.7 |
| `team-qa-release` | 0.5.7 |
| `team-reliability` | 0.5.8 |
| `team-rendering` | 0.5.8 |
| `team-stress-test` | 0.5.8 |
| `team-visual-design` | 0.5.12 |

SC-PRO-01/SC-KG-01: odobrena primena postojećeg governance-a, ne blanket odobrenje novih predloga. Izvršavanje scenarija K1–K10 nije potvrđeno u ovom pregledu. SC-INTEGRITY-01/INT-APPROVAL-01 ostaju kandidati prema sopstvenom standardu, bez tvrdnje o aktivnom platform enforcement-u. Repo snapshot pregleda: test1 `15add8492e830c1ca98f22d9a8ef9d8facf0621c`, test-cl1 `8731439629947d5a502af5c9ef0ef228a26f07fd`; razlike u AGENTS.md, docs/README.md i dva dokumenta nezavisnog kandidata zahtevaju zaseban pregled pre prenosa, ne prepisivanje. U 11 repo SKILL.md devet navodi SC-BEH-01; marketing i visual-design ne navode ga eksplicitno. Nijedan ne navodi oba SC-PRO-01/SC-KG-01 direktno; postojeći kanonski AGENTS.md već propisuje njihovu primenu svim ulogama. Predlog dopune ulaznih referenci nije dokaz izvršavanja. SC-DEC-01, DOC-VER-01 i PMV ostaju obavezni.

### Interni D7 i Provera izvršnih dokaza — 27.11.2026.

[SC-DEC-01](tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md#automatska-provera-izvršnih-dokaza) u test1 main sadrži interni postupak, prioritete P0–P4 i postupanje pri poplavi događaja. [PR #83](https://github.com/tihidon/test1/pull/83) je spojen kao `7b453697`. [PR CI #106](https://github.com/tihidon/test1/actions/runs/46063984212) je PASS za head `d121722f`. CI za tačan merge SHA ovde nije potvrđen.

Izvršeni piloti su sintetički. QA prijem i stvarni zapisi igre još nisu provereni ovom metodom. Eksterni kontrolor, eksterna slepa proba i obavezno odobrenje nezavisnog agenta su ukinuti. Interna provera originalnih dokaza ostaje u D7, a odluka vlasnika u D8. Formalni interni D7 revizije `b559a871…` ostaje BLOCKED. Identitet objavljenog Team paketa evidentiran je u DOC-003 iznad.

### Istorijski DOC-003 snapshot — paket 0.7.2

Read-back 27.11.2026 CET (26.11. UTC), preko autorizovanog Plugin Creator konektora. Tadašnji [Snail City Agent Team](https://chatgpt.com/plugins/plugins_6b07821ba2488191803130852db1560a) bio je **0.7.2**, release `pluginrel_6b08bb6baf108191ac666b7a64f19df1`; oba manifesta 0.7.2, USER/PRIVATE, 34 fajla i 16 skillova u inventaru. Usklađeni Coordinator i zajednički behavior guide sa SC-PRO-01/SC-KG-01; ostali skill headeri ostaju na stvarno pročitanim verzijama. Pravila važe za sve uloge kroz SC-BEH-01 i zajednički vodič; stvarna aktivacija u pojedinačnoj sesiji i ponašanje nisu dokazani read-backom.

| Profil u Team paketu | Pročitana verzija |
|---|---|
| `coordinate-team` | 0.5.10 |
| `team-agent-conduct` | 0.1.0 |
| `team-architecture` | 0.5.8 |
| `team-chromium-qa` | 0.5.5 |
| `team-defensive-auditor` | 0.1.1 |
| `team-engineering` | 0.5.7 |
| `team-handoff` | 0.5.5 |
| `team-legal` | 0.1.0 |
| `team-marketing` | 0.3.1 |
| `team-qa-assurance` | 0.5.6 |
| `team-qa-planning` | 0.5.5 |
| `team-qa-release` | 0.5.5 |
| `team-reliability` | 0.5.6 |
| `team-rendering` | 0.5.6 |
| `team-stress-test` | 0.5.6 |
| `team-visual-design` | 0.5.9 |

Vlasnik je eksplicitno autorizovao korišćenje dogovorenih pravila. To nije nezavisni D7 dokaz niti blanket odobrenje budućih predloga, novih dozvola, troškova ili objava. Governance PR [test1 #62](https://github.com/tihidon/test1/pull/62) merge `41ca10af378265a34dcf4a93362e20e6084cd3a3`, [test-cl1 #10](https://github.com/tihidon/test-cl1/pull/10) merge `def076ac44a338f92e9e5d20e78cc5b67600c141`; originalni main push [CI test1](https://github.com/tihidon/test1/actions/runs/45908609505) i [CI test-cl1](https://github.com/tihidon/test-cl1/actions/runs/45908633343) success, attempt 1, po 25 tooling i 16 chromium-runtime koraka success; po 4 neistekla artefakta evidentirana. Sirovi logovi i sadržaj ZIP-ova nisu ponovo pregledani ovim zapisom. Tri dokumenta identični blobovi u oba repoa, HTML/SW nepromenjeni. PMV MERGED/CI PASS/D7 PENDING, K1–K10 behavioral NOT RUN. Bez tvrdnje o produkcionom deploy-u. Prethodni release `pluginrel_6b08b3dcb5f0819187b8779ffe0e4d12` (0.7.1) ostaje istorijski rollback referenca, ne aktivna verzija.

### Istorijski DOC-003 snapshot — paket 0.7.1

Provereno 26.11.2026. Tadašnji Snail City Agent Team na sajtu je **0.7.1**. U izdanju je 16 timskih profila. Tri nova profila pokrivaju pravnu procenu, defanzivni audit i kontrolu rada agenata. Lokalni profili i njihove verzije vode se u [AGENTS.md](../AGENTS.md) i pripadajućim `SKILL.md` fajlovima. Provera sadržaja izdanja i evaluacija ponašanja agenata imaju odvojene dokaze.

| Profil u Team paketu | Verzija |
|---|---|
| `coordinate-team` | 0.5.9 |
| `team-agent-conduct` | 0.1.0 |
| `team-architecture` | 0.5.8 |
| `team-chromium-qa` | 0.5.5 |
| `team-defensive-auditor` | 0.1.1 |
| `team-engineering` | 0.5.7 |
| `team-handoff` | 0.5.5 |
| `team-legal` | 0.1.0 |
| `team-marketing` | 0.3.1 |
| `team-qa-assurance` | 0.5.6 |
| `team-qa-planning` | 0.5.5 |
| `team-qa-release` | 0.5.5 |
| `team-reliability` | 0.5.6 |
| `team-rendering` | 0.5.6 |
| `team-stress-test` | 0.5.6 |
| `team-visual-design` | 0.5.9 |

Za predaju nalaza koristi [SC-DEC-01](tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md), a za procenu ozbiljnosti i eskalaciju [SC-BEH-01](tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md).

### Istorijski DOC-003 snapshot — paket 0.5.7

ChatGPT read-back 26.11.2026. Tadašnji [Snail City Agent Team](https://chatgpt.com/plugins/plugins_6b07821ba2488191803130852db1560a) je **0.5.7**, release `pluginrel_6b0865f75ac8819189d12ed145696811`. Verzije ispod su pročitane iz pojedinačnih SKILL.md, a profile opisuje AGENTS.md i uputstvo odgovarajuće uloge. Read-back potvrđuje sadržaj i identitet paketa. Izvršne QA i D7 tvrdnje zahtevaju zaseban dokaz.

| Skill u Team paketu | Pročitana verzija |
|---|---|
| `coordinate-team` | 0.5.6 |
| `team-architecture` | 0.5.7 |
| `team-chromium-qa` | 0.5.5 |
| `team-engineering` | 0.5.6 |
| `team-handoff` | 0.5.4 |
| `team-qa-assurance` | 0.5.5 |
| `team-qa-planning` | 0.5.5 |
| `team-qa-release` | 0.5.5 |
| `team-reliability` | 0.5.5 |
| `team-rendering` | 0.5.6 |
| `team-stress-test` | 0.5.6 |

### Istorijski DOC-003 snapshot — paket 0.5.5

Kanonski registar je ovaj odeljak u test1; test-cl1 održava njegovu identičnu kopiju. Istorijski snail-city-test se ne prepisuje. Izvor: ChatGPT Plugin Creator, `get_plugin_files` (oba manifesta i svih 11 SKILL.md metapodataka) i `list_plugin_releases`, pročitani 26.11.2026. Tadašnji paket Snail City Agent Team `plugins_6b07821ba2488191803130852db1560a` ima verziju **0.5.5**, release `pluginrel_6b084da02a108191a574be055071a73c`, tada označen kao current. Istorijski paket **0.5.1**, release `pluginrel_6b07f9c0261c8191b6b53456bcd512cc`, i dalje je u istoriji, nije current. Ne prepisivati QA-001 i ranijih 28 fixture testova kao dokaz za 0.5.5.

| Skill u Team paketu | Pročitana verzija |
|---|---|
| `coordinate-team` | 0.5.5 |
| `team-architecture` | 0.5.5 |
| `team-chromium-qa` | 0.5.5 |
| `team-engineering` | 0.5.5 |
| `team-handoff` | 0.5.4 |
| `team-qa-assurance` | 0.5.5 |
| `team-qa-planning` | 0.5.5 |
| `team-qa-release` | 0.5.5 |
| `team-reliability` | 0.5.5 |
| `team-rendering` | 0.5.5 |
| `team-stress-test` | 0.5.5 |

Team release, verzija pojedinačnog skilla, verzija samostalnog plugina, repo skill i verzija igre/SW su odvojeni identiteti. Ovo je read-back metapodataka Team paketa, ne inventar drugih samostalno instaliranih plugina, lokalne aktivacije ili dokaz nezavisne delegacije. D7/behavioral eval nije potvrđen ovim pregledom. `team-handoff` 0.5.4 je opaženo stanje, ne razlog za automatski bump. Pravilo [DOC-VER-01](tehnika/standardi/SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md#doc-ver-01--identitet-i-istorija-verzija) važi za sve uloge. Ponovo proveriti stvarni release pri svakom update-u; novi snapshot dodati uz očuvanje prethodnog. DOC-003 zatvaranje zahteva odobren merge i SC-PMV-01 na oba repoa; ovaj zapis nije potvrda merge-a.

### Aktuelni zajednički status — 26.11.2026.

- Kanonski razvojni repo: `tihidon/test1`; referentni main `e51b1e6cba31bedd61ad0bbb269c90f065117279`. Cloudflare testni repo: `tihidon/test-cl1`; referentni main `8d9fec8405674cbfcc97dd97224bb3a8de596c15`. Istorija test1 je povezana kroz `3f5ca38e2e79d1f2f98b27130204addac9a473ff`; zamrznuti CI baseline nije resetovan. Ovi SHA su snapshot dokaza, ne tvrdnja o budućem HEAD-u.
- Zajednički build `0.8.92-css-unified-p11`, HTML blob `f730698c8251c30c91d798ea816986a91e189a01`, 7606179 B, SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a`; SW blob `2f57bfd2fd38f8d220af090caa5c55c7580007f3`, cache `snail-city-shell-0.8.92-css-unified-p11-r2`. Family labels ostaju 0.8.92. Oba repoa imaju identične src, HTML, SW i zajedničke CI workflow-e.
- test1: [post-merge CI PR #54](https://github.com/tihidon/test1/actions/runs/45812765115) success; Netlify publish gate sprečava različite src/root bajtove. [Origin probe](https://github.com/tihidon/test1/actions/runs/45813275480) vratio HTTP 503 za 9 URL-ova; vlasnik prijavio potrošene kredite. Netlify produkcijski identitet nije potvrđen.
- test-cl1: [post-merge engineering](https://github.com/tihidon/test-cl1/actions/runs/45836823254) success; B01–B06 51/51, QA-003 67/67 kroz 5 scenarija, obe Cloudflare publish kontrole PASS; [MCP push](https://github.com/tihidon/test-cl1/actions/runs/45836823391) success (sintetički click/trace/PNG, ne gameplay/performance). Prvi neuspešni CI zbog nedostajuće istorije [45832281916](https://github.com/tihidon/test-cl1/actions/runs/45832281916) ostaje dokaz incidenta.
- Cloudflare build `2a7682f6-dee9-4ce2-8b9b-227e3ff58dfd`, deployment `f6ca2f98-9969-41aa-b45e-63771d596006`, version `420b108e-3fcf-4fed-9c62-77f123e4f8c9` 100%; vlasnik potvrdio 7 koraka fizičkog offline testa. Opseg i ograničenja dokaza u kanonskom [PW-01](tehnika/pwa-offline/PW-01-STANJE-0.8.92.md). Public HTTP byte/MIME identitet, potpuni fizički dokaz i nezavisni D7 nisu potvrđeni; PMV/release zatvaranje nije VERIFIED.
- Cloudflare-specifični fajlovi samo u test-cl1: `wrangler.toml`, `_redirects`, `tools/cloudflare-build.sh`, `tools/agent/test_cloudflare_publish.py`. Netlify koristi postojeći netlify.toml; Cloudflare build koristi isti kanonski whitelist/identity ugovor i dodaje rutiranje. Ne kopirati hosting konfiguracije automatski između repoa. Origin-i imaju odvojeni IndexedDB i keš.
- Održavanje: zajednička pravila, registri i dokazi najpre se usklađuju u test1, zatim se kontrolisano prenose u test-cl1 uz byte diff i CI. Hosting-specifične promene idu samo u odgovarajući repo; evidencija mora navesti repo/ref/origin. Bez paralelnih standarda, resetovanja istorijskih baseline-a ili automatske objave. P1/P3/P10 i prethodni kandidat zapisi u nastavku ostaju istorijski; funkcijski registri nisu ponovo generisani ovim docs-only zadatkom.

## Sadržaj

1. [Odakle početi](#1-odakle-početi)
2. [Dokumenti i status provere](#2-dokumenti-i-status-provere)
3. [Šta nije preneto i zašto](#3-šta-nije-preneto-i-zašto)
4. [Ispravke nađene pri proveri](#4-ispravke-nađene-pri-proveri)
5. [Održavanje kopija](#5-održavanje-kopija)
6. [Otvoreno](#6-otvoreno)

## 1. Odakle početi

1. [SC-RAD-01 §2–§3](./tehnika/standardi/SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md#2-hijerarhija-autoriteta): redosled važenja izvora i činjenice o ovom kodu.
2. [SC-AGENT-01](./tehnika/standardi/SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md): obavezni postupak rada i QA gate-ovi G0–G7.
3. Za konkretnu izmenu: standard njene oblasti iz tabele ispod.

Kad se dokument i kod ne slažu, važi kod; neslaganje se upisuje, ne rešava pretpostavkom.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 2. Dokumenti i status provere

**Kopija** = prenet iz drugog izvora uz proveru i ispravke za test1. **Izdanje za test1** = pravila iz izvora, činjenice ponovo izmerene. **Novo** = napisano nad test1.

### Standardi (`tehnika/standardi/`)

| Dokument | Oblast | Vrsta i izvor | Provera prema test1 |
|---|---|---|---|
| [SC-AGENT-01](./tehnika/standardi/SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md) | postupak rada agenata, QA gate | izdanje za test1; projekat (rev. 1.0, 0.8.93) | identitet buildova, lista brzina, CSS blok, ikonice ispravljeni; GML deo uklonjen |
| [SC-ARCH-01](./tehnika/standardi/SC-ARCH-01-STRUKTURA-I-ARHITEKTURA.md) | struktura fajlova i modula, PWA slojevi | izdanje za test1; projekat (rev. 1.0, 0.8.93) | stablo, `_headers`, linije 17 modula, `sw.js` vrednosti i tabela paketa izmereni nad test1 |
| [SC-FUNC-01](./tehnika/standardi/SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md) | registar funkcija, K01–K08 | izdanje za test1; projekat (rev. 1.0, 0.8.93) | registar regenerisan (983 čvora); K01, K02 ne važe za test1, K03–K08 potvrđeni |
| [SSOT — jedan izvor istine](./tehnika/standardi/PRAVILO-JEDAN-IZVOR-ISTINE.md) | vlasnici podataka | kopija; `snail-city-test@1e3258f` | svih 19 vlasnika postoji; red verzije dopunjen |
| [SC-PL-01 / CSS-01](./tehnika/standardi/SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md) | layout, canvas resize, velike slike u CSS promenljivama | kopija; `snail-city-test@1e3258f` | tabela CSS-01 potvrđena; dodata peta vrednost `--sc174-snail-art`; trace brojevi su iz 0.8.90 |
| [SC-CODE-01](./tehnika/standardi/SC-CODE-01-CSS-DOM-FUNKCIJE.md) | pisanje CSS, DOM, funkcija; ratchet | kopija; `snail-city-test@12f986c` (PR #12, spojen `f32b290`) | ratchet PASS, 0 razlika prema baseline 0.8.92; dodato pokretanje alata |
| [SC-RAD-01](./tehnika/standardi/SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md) | postavka, izmena, brisanje koda | kopija; `snail-city-test@12f986c` (PR #12, spojen `f32b290`) | §3 prepisan za test1; R04, R05 prilagođeni |
| [SC-REND-01](./tehnika/standardi/SC-REND-01-CIST-KOD-I-RENDER.md) | render, vreme, keš, invalidacija | kopija; `snail-city-test@12f986c` (PR #12, spojen `f32b290`; pisan nad test1) | ratchet PASS; N01, N12 potvrđeni; dva podatka ispravljena (§4) |
| [SC-BRISANJE-3-PROVERE](./tehnika/standardi/SC-BRISANJE-3-PROVERE.md) | presedan brisanja CSS-a | kopija; `snail-city-test@1e3258f` | **ne opisuje test1**: `.map-controls` ovde i dalje postoji (označeno) |

### PWA, QA i alati

| Dokument | Vrsta | Provera |
|---|---|---|
| [PW-01 — stanje u 0.8.92](./tehnika/pwa-offline/PW-01-STANJE-0.8.92.md) | novo | 12 elemenata PW-01 mehanizma iz 0.8.90 potvrđeno u kodu; uređaj nije testiran |
| [Animacije — inventar 0.8.92](./qa/SC-ANIMACIJE-0.8.92-INVENTAR.md) | novo | 26 `@keyframes` popisano; veza sa 37 istorijskih imena |
| [docs/alati](./alati/README.md) | novo | generator registra za SC-FUNC-01 |

### Dokumenti koji su već bili u test1 (nisu menjani)

| Dokument | Šta je |
|---|---|
| [SC-v0.8.92-P1-CSS-SINGLE-SOURCE-AUDIT.md](./SC-v0.8.92-P1-CSS-SINGLE-SOURCE-AUDIT.md) i [JSON](./SC-v0.8.92-P1-static-audit.json) | audit kandidata 0.8.92 (23.11.2026); isti `index.html` SHA-256 kao ovaj build; jedina razlika je `CACHE_NAME` `…-r1` u auditu, `…-r2` ovde (PR #2). Kao izvor CSS pravila zamenjen je SC-CODE-01 |

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 3. Šta nije preneto i zašto

| Dokument (izvor) | Razlog |
|---|---|
| `Snail-City-0.8.93-SOURCES.md` (projekat) | opisuje drugi build (0.8.93 u test-2); linije ne važe za test1. Njegova pravila su u SC-AGENT-01 i SSOT, mapa koda u SC-ARCH-01 i SC-FUNC-01 |
| `Snail-City-Faza-4-detaljna-revizija-v2.md` (projekat) | cilj je 0.8.87, a izvršni kod tada nije bio pročitan; matrica 42 animacije koristi imena iz v174 koja u test1 uglavnom ne postoje. Zamenjen [inventarom animacija](./qa/SC-ANIMACIJE-0.8.92-INVENTAR.md); ekonomske stavke EC-01–EC-10 ostaju otvorene u projektu |
| `Snail-City-P1-izolacija-zastoja.md`, `Snail-City-P1-prodavnica.md` (projekat) | merenja na buildu `0.8.90-p1-startup-probe`; ne mogu se ponovo proveriti bez tadašnjih trace-ova i priloga. Zaključci su već u PL-01/CSS-01 |
| `PW-01-MIGRATION-AND-QA.md` (projekat) | istorija 0.8.90; ono što je i dalje tačno za 0.8.92 provereno je u [PW-01 stanje](./tehnika/pwa-offline/PW-01-STANJE-0.8.92.md) |
| `claude/dokument-promena.md` (projekat) | jedan dnevnik promena; dupla kopija bi se razišla |
| Istorijski izveštaji `snail-city-test/docs` (arhitektura 0.8.21–0.8.87, PW-01 0.8.88–0.8.90, cloud v1.0.7, IndexedDB 0.8.87) | opisuju starije buildove; dostupni u [snail-city-test/docs](https://github.com/tihidon/snail-city-test/tree/1e3258f/docs) |
| `AGENTS.md` (`snail-city-test`) | zadatak je bio `docs/`; vidi §6 |

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 4. Ispravke nađene pri proveri

Netačne tvrdnje u izvornim dokumentima, provereno nad kodom 25.11.2026:

| Tvrdnja u izvoru | Stvarno stanje | Gde je ispravljeno |
|---|---|---|
| „verzijske tačke: 4 sa `version.json`“ (SC-RAD-01), „3 tačke“ za test1 (SC-REND-01) | **šest mesta**: build tag u `#sc-startup-trace`, `SC_PWA_STATUS.version`, `<title>`, `const VERSION`, komentar i `CACHE_NAME` u `sw.js`. `SC_PWA_STATUS.version` postoji i u 0.8.90 i alat ga ne proverava | SC-RAD-01 §3, SSOT, SC-REND-01, SC-CODE-01 §9 |
| „build tag ne postoji“ | postoji: `build:'0.8.92-css-unified-p1'` u `#sc-startup-trace` | SC-RAD-01 §1, §8 |
| „samo 2 od 26 `@keyframes` van compositora“ | 3: i `logo-fill` animira `clip-path` | SC-REND-01 §6 |
| lista brzina `[…,60]` (SC-AGENT-01) | `[10,20,30,40,50,55]` | SC-AGENT-01 §2 |
| linije modula i funkcija iz 0.8.93 | u test1 su drugačije (npr. `applyCommand` L2678, ne L2690) | SC-ARCH-01 §4, SC-FUNC-01 §4 |
| K01 ikonice, K02 `_headers` (0.8.93) | u test1 rešeno | SC-FUNC-01 §3 |
| šest `.map-controls` deklaracija obrisano | u test1 selektor i dalje postoji u 2 grupna pravila | SC-BRISANJE-3-PROVERE (napomena) |

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 5. Održavanje kopija

- Opšta pravila (SSOT, PL-01, SC-CODE-01, SC-RAD-01, SC-REND-01) održavaju se kanonski u `tihidon/test1`. Istorijske izvore i commit reference sačuvati; nema obaveznog prenosa iz starog repoa.
- Činjenice o ovom buildu (linije, verzije, putanje) važe za `2d66e55`. Posle izmene `index.html` regenerisati [SC-FUNC-01](./tehnika/standardi/SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md) (SC-F08) i ažurirati SC-RAD-01 §3 i SC-ARCH-01 §4 u istom PR-u.
- Mesto u kodu se navodi imenom funkcije ili sidrom; broj linije samo uz commit.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 6. Otvoreno

1. **Javnost `docs/`:** konfiguracija u repozitorijumu objavljuje whitelist fajlova iz `dist/`. Stvarni Netlify deploy i podešavanja sajta nisu provereni u ovom pregledu.
2. **`AGENTS.md` u korenu test1:** dodat u PR #4 (spojen); sadrži redosled čitanja i ključna pravila sa vezom na ovaj indeks.
3. **`verify_edit.py` K2:** ispravka (šest tačaka, `version.json` opcion) je u PR #13 `snail-city-test`, istorijski status PR-a, nije aktuelna potvrda. Ranije provereno: test1 PASS, build tag 0.8.91 u kopiji FAIL.
4. **`snail-city-test` SC-RAD-01 §3:** broj verzijskih tačaka ispravljen na šest u PR #13 (istorijski status, nije aktuelna potvrda).
5. PW-01 na uređaju, vizuelni QA i animacije za 0.8.92: NIJE TESTIRANO.
6. PR #12 u `snail-city-test` (SC-REND-01, SC-CODE-01, SC-RAD-01) spojen je 25.11.2026 kao `f32b290`. Kopije u ovom repou su rađene sa `12f986c`, koji je sadržan u tom spajanju.

<sub>[↑ Sadržaj](#sadržaj)</sub>

## 7. Agent upgrade v1.1.0 (25.11.2026)

- [SC-BUILD-01](tehnika/standardi/SC-BUILD-01-PYTHON-BUILD.md) — izolovani istorijski round-trip, current-source gate, build/publish identitet.
- [SC-LOOP-01](tehnika/standardi/SC-LOOP-01-LOOP-I-BUG-AUDIT.md) — AST kandidati, watchdog, lifecycle, PL-01, agent retry.
- [SC-CLI-01](alati/SC-CLI-01-AGENT-INSTALACIJA.md) — projektna instalacija, zavisnosti, komande, eval.
- [SKILL.md](../.agents/skills/snail-city-engineering/SKILL.md) — operativni ulaz, postojeći standardi ostaju kanonski.

Novi standardi su pripremljeni na osnovu commita 360efc7a88897c50a7d58305e1cbef0794191c53; stariji identiteti u odeljcima 1–6 nisu trenutna verifikacija. Netlify konfiguracija sada postoji i objavljuje whitelist u dist/; ne menja se u ovom upgrade-u. Python/JS i official CLI rezultate vezati za tačan commit i izvršne logove. Originalne projektne priloge i raniji overlay ZIP nije bilo moguće ponovo pročitati u ovom okruženju; postojeća test1 izdanja standarda sačuvana su bez prepisivanja. Ne tvrditi byte-identical prenos kompletnog v1.0.0/v1.1.0 paketa.

## 8. Chromium Runtime QA — kandidat v1.0.0

[SC-QA-02](tehnika/standardi/SC-QA-02-CHROMIUM-RUNTIME.md) i [skill](../.agents/skills/chromium-runtime-qa/SKILL.md). Testni alati tools/qa/; zaseban CI job. Baseline 325ff6a9965a4081bda55f55eb7a35a1881b2e10. Scope: shell identity, worker/cache, offline navigation, external watchdog, trace and CPU sample; gameplay/state/device and actual agent activation remain separate. No game version or publish changes.

## 9. QA v1.0.1 i Agent Reliability v1.0.0

[SC-QA-02](tehnika/standardi/SC-QA-02-CHROMIUM-RUNTIME.md): CI incident Ubuntu 26.04/Playwright 1.56, pin browser runner 24.04 i setup diagnostics. [SC-REL-01](tehnika/standardi/SC-REL-01-AGENT-RELIABILITY.md): nezavisni evidence contract, checker fixtures i behavioral eval katalog. [Agent Reliability skill](../.agents/skills/agent-reliability/SKILL.md). Stvarno ponašanje agenta još NOT RUN. Bez promene igre.

## 10. Shared Decision Chain
[SC-DEC-01](tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md), zajednički D0–D8, tools/reliability/check_decision.py i regression fixtures; postojeći CI discovery pokriva nove testove. Verzije skillova 1.2.0 / 1.1.0 / 1.1.0. Runtime igre nepromenjen. Trace(2).zip analiza BLOCKED, stvarni agent eval NOT RUN.

## 11. Executable complexity controls
[SC-CODE-02](tehnika/standardi/SC-CODE-02-IZVRSNA-KONTROLA-KOMPLEKSNOSTI.md): canonical SC-CODE-01 tools installed, historical baseline preserved, current ratchet and locations, loop inventory and Chromium fixtures/live DOM. CI candidate; no runtime game changes.

## SC-DEBUG-01 phase A
[Pouzdano debugovanje](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md): selected lint ratchet, exact AST duplicates, separate CDP counts/CSS deltas and shared specialist handoff. Candidate; game unchanged.

## SC-DEBUG-01 phase B
Functional contract in [SC-DEBUG-01](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md#phase-b--functional-contract-and-scope-candidate). Six real UI/IDB cases, 10 contract fixtures; desktop CI PASS za B01–B06 (vidi §15). No production change. B06 fixture not natural progression, cold offline desktop not Android.

## 12. Team coordination (26.11.2026)

Snapshot koordinacije 26.11.2026: commit `5d57b32919477b6636c9093b2f81b9f8ae897e16`; root `index.html` Git blob `57ff0991646cff4e63c8c74868168905d1004b62`; `src/js/block-00.js` startup build `0.8.92-css-unified-p10`; `sw.js` cache `snail-city-shell-0.8.92-css-unified-p10-r1`. `SC_PWA_STATUS.version` je family `0.8.92`, ne dokaz punog build identiteta. Netlify kopira whitelist root fajlova u `dist/`. SHA-256 HTML-a, svih šest tačaka verzije, build/publish jednakost i runtime nisu ponovo izvršno provereni u ovom docs-only zadatku; ne proglašavati ih PASS. Svaki budući zadatak ponovo utvrđuje identitet iz checkout-a.

[Rendering Performance kandidat](../.agents/skills/snail-city-rendering-performance/SKILL.md) je novo lokalno uputstvo, ne potvrđena kopija zasebnog instaliranog skilla. Koristi postojeći [SC-DEC-01](tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md). Team plugin v0.2.0 ažuriran i ponovo pročitan; agent behavioral eval i nezavisna delegacija NOT RUN/BLOCKED. Bez runtime/SW/deploy izmene.

## 13. Team CI coverage correction (26.11.2026)

PR #38 merged at `f422312`. Run [45738038440](https://github.com/tihidon/test1/actions/runs/45738038440) tooling job passed but its explicit skill list did not include Rendering Performance. Add the existing rendering candidate to `skills-ref validate` and `to-prompt`; do not weaken any existing gate. Correct historical P3 labels in SC-RAD-01 and SC-AGENT-01 without changing normative rules. CI za PR #39 je prošao (vidi §15); nezavisan pregled ostaje otvoren; no game/SW/deploy configuration changes. Official skill validation is not behavioral agent evaluation.

## 14. Model Spec — SC-BEH-01 (26.11.2026)

Istorijski predlog (naknadno odobrena primena; vidi DOC-003): [SC-PRO-01 i SC-KG-01](tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md#sc-pro-01--obavezna-proaktivnost-u-odobrenom-opsegu) — obavezna proaktivnost u opsegu i karantin/pregled/odobrenje pre trajnog usvajanja znanja i tehnologija. Ne menja DOC-003 aktuelne verzije, izvršni kod ili dozvole. Nezavisni D7 i behavioral evaluacija nisu izvršeni; aktivacija i release odvojeni od odobrenja pripreme kandidata.

[Zajedničko ponašanje agenata](tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md), povezano iz AGENTS.md. Koordinator v0.3.0. Jedini evaluacioni katalog proširen na 26 REL/TEAM/BEH slučajeva; behavioral NOT RUN. Bez runtime/SW/deploy izmene.

## 15. Stanje dokaza tima (26.11.2026)

Dokumentacija pregledana na `test1@d82f17e2149c4c9ec5ed8e950c373eb7487f78de`. Različite verzije repo uputstava i ChatGPT paketa imaju zasebne izvore i cikluse provere.

| Oblast | Potvrda i granica |
|---|---|
| CLI, statička analiza, build/publish | `tooling` PASS u [CI za PR #39](https://github.com/tihidon/test1/actions/runs/45738292152), uključujući proveru build/publish bajtova i validaciju strukture uputstava. Rezultat je vezan za taj run. |
| Funkcionalni desktop Chromium | B01–B06 PASS u istom runu. Obuhvata UI, trajnost sejva i hladno offline pokretanje sa prekidom transporta do lokalnog origina. Detalji i raniji B04 FAIL u [SC-DEBUG-01](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md#b04-qa-infrastructure-correction-26112026). |
| Ponašanje agenata | [SC-BEH-01](tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md) definiše 26 slučajeva. Izvršna evaluacija kataloga NOT RUN. D7 nezavisan pregled nije potvrđen. |
| Android, produkcija i performanse | Sveže izvršavanje za ovaj pregled NOT RUN. Za tvrdnju o uzroku zastoja potrebni su originalni trace, konkretan poziv, prvo odstupanje i uporediv kontrolni scenario. |
| Noćni zadatak | Prijavljeno 0/10 ispravki i 0 commitova iz tog zadatka. Lokalni Git bio je blokiran DNS-om. Raniji CI prolazi pripadaju zasebnim PR-ovima. |

## 16. SC-TEAM-004 — infrastructure lesson (26.11.2026)
See [SC-DEBUG-01 infrastructure strategy pivot](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md#infrastructure-strategy-pivot--sc-team-004-26112026). The authenticated API tree was accessible at `8ed4417a6d2e423800a88436b4465a7a28f1dcab`; full local snapshot and runtime were not verified. Engineering/Architecture and AGENTS entry points refer to the same rule. External Coordinator package update and behavioral evaluation remain separate. NS01 oracle is defined in the canonical standard; no game fix claimed.

## 17. Istorijski zapis — Central QA / PMV-01 (26.11.2026)

> Dokazi v0.5.1 pripadaju istorijskom izdanju; aktuelne verzije vidi u DOC-003 registru na početku.

[SC-PMV-01](tehnika/standardi/SC-PMV-01-POST-MERGE-VERIFICATION-STANDARD.md) — mandatory closure gate for all agents, extending existing G0–G7 and D0–D8. QA-001 found no automatic main-push workflow; proposed existing workflow extension, preserved ratchets and exact checkout verification. ChatGPT Coordinator v0.5.1 package read back; 28 helper fixture tests PASS, independent agent eval not run. Actual post-merge CI and release remain unverified until original evidence exists. No game/SW/deploy change.

## 18. QA-002 — save oracle

[SC-DEBUG-01 QA-002](tehnika/standardi/SC-DEBUG-01-POUZDANO-DEBUGOVANJE.md#qa-002--committed-save-oracle-hardening-26112026) records four reproduced false accepts and candidate oracle corrections. 28 local fixture methods passed; real candidate Chromium and independent review remain pending. No production save or game change.

## 19. Chrome DevTools MCP qualification — candidate

PR #51 merged at `1b3ecbd`. [PR MCP run 45798818665](https://github.com/tihidon/test1/actions/runs/45798818665) actually initialized MCP 1.14.0, discovered tools and read synthetic Chrome DOM; no trace, heap or actual game scenario executed by that smoke. [Main engineering run 45799727773](https://github.com/tihidon/test1/actions/runs/45799727773) passed; MCP-specific push evidence missing. New candidate extends the existing isolated fixture to native click, frozen positive/negative marker oracle, parsed nonempty trace and PNG artifact with SHA-256, checks actual server schema, and adds path-scoped main push trigger and exact checkout assertion. No game/SW/deploy change. Candidate CI and D7 pending. Tool qualification is not Snail City gameplay or agent behavioral certification.

### MCP qualification artifact path correction

Run [45805792394](https://github.com/tihidon/test1/actions/runs/45805792394) failed at performance_stop_trace because RUNNER_TEMP is outside the server default filesystem roots; seven unit tests passed. Use the tagged v1.14.0 documented `--filesystem-root` with only the newly created resolved output directory. No unrestricted paths, no relaxed URL allowlist, no changed click/trace oracle. Re-run actual MCP CI; candidate remains unverified. Source: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/chrome-devtools-mcp-v1.14.0/docs/configuration.md


### P0 recovery after PR #49 (26.11.2026)
- Merged commit `9b5658db2bde10b2c1a938212429d4a26eb55f6d`: source P11, root HTML P10; post-merge tooling run [45807116303](https://github.com/tihidon/test1/actions/runs/45807116303) failed build/publish equality. Expected P11 SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a` from independent CI assembly.
- Corrective candidate: regenerate root HTML using existing Python build, verify exact digest and existing build gate. Advance CACHE_NAME to `snail-city-shell-0.8.92-css-unified-p11-r2` because r1 may contain old HTML. Retain existing collision guard, all game sources, family labels (title/status/SW comment 0.8.92), no save/economy changes. No Netlify configuration change. Actual deployed origin/ID unknown; no release claim.
- Candidate PR and CI required; D7 and post-merge PMV pending. Revert candidate only under owner approval; never delete player data or manually clear caches.

Recovery evidence: [run 45808612656](https://github.com/tihidon/test1/actions/runs/45808612656), job 139870295474, generated commit `bcd3c6e658f1684649fb26dabcca7c0fb8a0cdd5`, HTML blob `f730698c8251c30c91d798ea816986a91e189a01`, SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a`, 7606179 bytes, independent assembly/syntax and root equality PASS. Temporary write-enabled recovery workflow removed before PR. Full PR CI, D7 and exact-SHA PMV remain pending. No deploy claim.

## Istorijski zapis — Cloudflare Workers static hosting kandidat (26.11.2026)

> Status ovog kandidata je naknadno promenjen; aktuelni dokazi su u zajedničkom statusu na početku dokumenta.

Canonical development: tihidon/test1 at e51b1e6cba31bedd61ad0bbb269c90f065117279; test-cl1 import f6c2b4d91f489e497ead625fda2e437437bf1a16 contains identical P11-r2 runtime/source and 193 matching blobs, but lacks two CI workflow files and all ancestral Git commits (root import). Restore both workflows byte-for-byte; historical ESLint ratchet commit cd79662b45b2477d2d53aba000e60f90fefc8662 is absent (API 404). Full engineering CI cannot be qualified until source history is imported by authorized Git fetch/merge; do not weaken or reset the frozen baseline. Cloudflare candidate only: wrangler.toml static assets ./dist, no server-side script, html_handling none, no wildcard fallback; _redirects exact / -> /index.html 200 internal proxy. Build uses existing Netlify whitelist/identity command, then adds _redirects; Python >=3.11 for tomllib. Dashboard build command: bash tools/cloudflare-build.sh; deploy command: npx wrangler deploy; root /. Keep builds disabled until reviewed and approved. New tests exercise exact whitelist and stale root rejection, not actual Cloudflare routing. Validate live exact URL status/MIME/bytes and no redirects on all SW core resources, private path 404s, physical PWA and synthetic save persistence. No changes to test1, game HTML, SW, save, or cache version. New origin has separate storage. Actual hosting configuration and deploy not accessible here; D7, CI and PMV pending.
Sources: https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/ ; https://developers.cloudflare.com/workers/static-assets/redirects/ ; https://developers.cloudflare.com/workers/ci-cd/builds/configuration/


## SC-INTEGRITY-01 — predlog P0 (27.11.2026)

[Zaštita integriteta projekta](tehnika/standardi/SC-INTEGRITY-01-ZASTITA-INTEGRITETA-PROJEKTA.md) — incident test-cl1 PR #11, 18 rizika, izvršni ugovor i 10 grupa kvalifikacionih testova. Predlog dokumentacije; implementacija i nezavisna verifikacija otvorene.


## SC-INTEGRITY-01 — implementacioni kandidat 0.2

[Standard](tehnika/standardi/SC-INTEGRITY-01-ZASTITA-INTEGRITETA-PROJEKTA.md), checker tools/agent/check_integrity.py, negativni fixture i read-only base-controlled workflow. Oba repoa isti checker/testovi; platform enforcement, nezavisni deploy guard i D7 otvoreni. Status ZADRŽI ZA QA.

### SC-EQ-01 — organizacioni kandidat (27.11.2026)

[SC-EQ-01](tehnika/standardi/SC-EQ-01-KVALIFIKACIJA-EVALUATORA.md): jedan kanonski predlog za sve evaluatore; javni pilot, slepi ispit, odvojeni oracle, ograničeno ovlašćenje i obnova. E0–E7 NOT RUN, nezavisni D7 BLOCKED, sertifikat nije izdat. Odluka i referenca na dokaz u SC-DEC-01; DOC-003 ostaje indeks, ne novi registar. Nema promene Team release-a.
