# SC-FUNC-01 — Registar funkcija, poziva i kontradikcija

**Snail City 0.8.93 | revizija 1.0 | 24.11.2026 | statički inventar + normativni dodatak**

## 1. Identitet i opseg

- Izvor: `snail-city-source-0.8.93-deco-webp.zip`; SHA-256 `5604811213bf14af0dd1e4600a7dcc6959945928ede2683df06e3ab214a69efb`. CRC: PASS.
- `index.html`: SHA-256 `74dc364a2be81ad947f745268ebf037917b72e58f91ab06fd840f13dd7c4cca0`; Git blob `96805d08148be75189dd1c4a19d4f75f468620df`.
- `sw.js`: SHA-256 `ee59c1b7ec4e08f4c946e3260ef54dacc424232b3fb5b4012c4c04d1bd182686`.
- SC-ARCH-01, SC-AGENT-01 i SOURCES su projektni standardi; ovaj dokument je izvedeni indeks, ne novi runtime autoritet. Live Git/Netlify nisu auditovani.

## 2. Metod i značenje rezultata
TypeScript AST i checker, bez izvršavanja aplikacije. Pet izvršnih inline JS blokova i SW, bez JSON/asset blokova; privacy/delete-account nemaju script tag. Sintaksna dijagnostika 0 za svih šest jedinica. Obuhvaćene deklaracije, arrow funkcije, metode, get/set i anonimni callbackovi; implicitni konstruktori i runtime generisane funkcije nisu deklaracije. Poziv uključuje call i new; ne uključuje implicitno izvršavanje gettera, event dispatch ili poziv iz eksternog SDK. Lokacije su originalne linije, ID je stabilan samo za ovaj inventar.

**996 funkcijskih čvorova, 5046 mesta poziva/konstrukcije, 2192 statički povezano sa indeksiranim deklaracijama, 330 dodatnih kandidata po modulskim aliasima, 2524 bez lokalno utvrđenog cilja.** Poslednja grupa uključuje browser API, biblioteke i dinamičke pozive, nije lista grešaka. Checker veza ne dokazuje runtime izvršenje; kandidat (~) je pomoć za pregled, ne potvrđena veza. Poziv preko event handlera kao argumenta može biti bez direktnog incoming poziva. Ne proglašavati mrtav kod na osnovu nule.

## 3. Mapa modula
| Modul | AST funkcije | Odgovornost (SC-ARCH-01) |
|---|---:|---|
| bootstrap | 23 | startup, PWA registracija i katalog bootstrap |
| catalog | 1 | katalog |
| progression | 16 | sezona, liga, napredak |
| islandEvents | 16 | događaji ostrva |
| playerProgress | 5 | napredak igrača |
| domain | 168 | stanje, komande, ekonomija |
| frames | 1 | atlas frejmovi |
| physics | 6 | fizika |
| race | 27 | trka i projekcija |
| renderer | 53 | GPU i Canvas resursi |
| sceneManager | 12 | životni ciklus scena |
| scenes | 80 | mapa, kolizije, prikaz |
| storage | 113 | validacija, migracija, save adapteri |
| ui | 259 | paneli i prikaz |
| metrics | 15 | merenje |
| cloud | 11 | sinhronizacija |
| i18n | 11 | prevodi |
| app | 164 | orkestracija, unos, lifecycle |
| SW | 15 | offline shell i HTTP presretanje |

## 4. Obavezni standard funkcija
- SC-F01: identifikuj vlasnika, potpis, pozivaoce, callback registracije, alias/destructuring, string dispatch, ulaz, izlaz, mutacije i greške pre izmene. Funkcija sa istim imenom u različitom scope-u nije sama po sebi duplikat.
- SC-F02: jedan autoritet za teren, oslonac, projekciju, ekonomiju, fiziku, vreme, save i RAF. Izvedeni keš je dozvoljen uz invalidaciju.
- SC-F03: UI šalje nameru; reducer odlučuje; storage potvrđuje trajnost; renderer ne vrši gameplay transakciju. Proveri stvarni redosled, ne kopiraj normativni dijagram u kod.
- SC-F04: ulazi imaju jedinice, preduslove, granice, validaciju; greška ne ostavlja delimičnu transakciju. Kod Promise-a proveri reject, cleanup i paralelne pozive.
- SC-F05: svaki listener, interval, RAF, GPU resurs i observer ima vlasnika i lifecycle; ne uvoditi paralelni manager.
- SC-F06: pre brisanja proveri direktne reference, dinamičke reference i runtime scenarije; 0 statičkih poziva nije dokaz nekorišćenja.
- SC-F07: svi relevantni G0–G7 iz SC-AGENT-01, Chromium screenshot/GIF za grafiku, PW-01 za save/PWA, A/B/R za performanse.
- SC-F08: nakon odobrenog patch-a regeneriši indeks prema novom hash-u; ne ručno menjati izvedene linije i ID.

## 5. Kontradikcije, odstupanja i rizici
| ID | Dokaz | Klasifikacija | Postupak |
|---|---|---|---|
| K01 | SW L8–11 i manifest očekuju img/, ZIP ikonice u root-u | potvrđeno statičko odstupanje P0 | uskladiti odobreni publish layout i reference; proveriti HTTPS i offline |
| K02 | ZIP nema _headers; 0.8.90 referenca SC-ARCH-01 §2 ga ima | potvrđeno odstupanje od projektnog standarda; live MIME nije testiran | vratiti referentnu politiku samo u dogovorenom patch-u |
| K03 | index L3286–3287: [10,20,30,40,50,55], normalna 30; stariji SSOT navodi 60 | potvrđen konflikt verzija, nije automatski bug | ne menjati balans bez vlasnika; UI L6511, handler L8007–8009 i loop L7348 čitaju postojeći izvor |
| K04 | SW L55–65 network-first za navigaciju prihvata live.ok bez provere sadržaja; install L33–41 proverava tip i budžet | rizik: 200 HTML ne garantuje izvršnu igru; nije dokaz uzroka ranijeg splash-a | proveriti decoded SHA-256 i kompletan boot, ne slabiti MIME gate |
| K05 | indexedRepository.commit L5293 i localRepository.commit L5336, app.commit L7167 | namerno različiti slojevi/adapteri, ne dokaz SSOT konflikta | proveriti izbor jednog adaptera i ugovor revizije |
| K06 | boot L8314–8323 čeka saved/atlas/mapArt u Promise.all | rizik: neuspeh jedne grane sprečava nastavak boot-a | testirati svaku granu i postojeći catch; ne zaključivati uzrok bez trace-a |
| K07 | scBuildVisualInstances L4526–4532 keš po identitetu objects | rizik stale keša samo ako se niz menja bez invalidacije; nije potvrđen kvar | proveriti sve mutacije i rebuild |
| K08 | SC-ARCH-01 propisuje web PWA; projektne GML instrukcije za port | razlika platformi, ne kontradikcija koda | ne uvoditi global.game_data/GML alarm u JS aplikaciju |

## 6. Ručno pregledane ključne funkcije
Svrha i ugovor su izvedeni iz tela funkcije; testovi su predloženi kriterijumi, nisu izvršeni. Za potpuni read/write audit relevantne funkcije pročitati ceo opseg pre patch-a.

### F0126 · domain.newGame
`index.html:L2417–2425` · parametri: `now=Date.now(), id=uuid()`

**Svrha:** Kreira početni profil sa identitetom, revizijom i početnim stanjem.

**Kriterijum provere:** Novi profil samo kada politika oporavka to dozvoljava; oštećen save nije automatski nov profil.

### F0144 · domain.settle
`index.html:L2542–2574` · parametri: `s, now, random`

**Svrha:** Obračunava proteklo realno vreme, koristi efektivno vreme i ograničava elapsed na DAY. Menja prosleđeno stanje.

**Kriterijum provere:** Negativno vreme, offline povratak, ponavljanje bez dvostrukih resursa.

### F0185 · domain.applyCommand
`index.html:L2690–3170` · parametri: `current, cmd, now=Date.now(), random=Math.random`

**Svrha:** Centralni reducer: proverava komandu i ID, obrađuje stanje, beleži completed i povećava revision.

**Kriterijum provere:** Dupli ID, nevalidna komanda, nedovoljna sredstva, rollback i revizija.

### F0235 · physics.integrate
`index.html:L3188–3269` · parametri: `rs, dt, onImpact`

**Svrha:** Izvršava korak fizike igrača, kontakata i cooldowna.

**Kriterijum provere:** Sudari, deterministički koraci, granice i validan dt.

### F0236 · physics.step
`index.html:L3270–3274` · parametri: `rs, dt, onImpact`

**Svrha:** Deli pozitivan dt na podkorake najviše MAX_STEP i poziva integrate.

**Kriterijum provere:** Veliki dt, pause/resume i različit FPS.

### F0240 · race.createRace
`index.html:L3312–3334` · parametri: `snail, key, seed, id=uuid(), mode='league', trophies=0, keeperLevel=1`

**Svrha:** Kreira trku iz puža, staze, seed-a i režima; odbija nedostupnu stazu ili zauzetog puža.

**Kriterijum provere:** Isti seed i ulaz; nevalidna staza, busy puž.

### F0257 · race.advanceRace
`index.html:L3449–3462` · parametri: `race, seconds`

**Svrha:** Napreduje simulaciju ako nije pauzirana ili završena, uz ograničen catch-up.

**Kriterijum provere:** Pauza, cilj, povratak iz backgrounda i duple nagrade.

### F0260 · race.createProjection
`index.html:L3466–3496` · parametri: `width, height, race`

**Svrha:** Izvodi perspektivu trke iz dimenzija i režima kamere.

**Kriterijum provere:** Portrait/landscape, promene kamere.

### F0347 · scenes.supportFootprint
`index.html:L4292–4296` · parametri: `key, gx, gy`

**Svrha:** Izvodi stajnu osnovu iz groundProfile i donjeg sidra.

**Kriterijum provere:** Preview, hit-test i potvrda moraju imati isti oslonac.

### F0352 · scenes.forbiddenCell
`index.html:L4315–4315` · parametri: `x, y`

**Svrha:** Vraća true kada FIELD.rows[y]?.[x] nije f, uključujući nedostajuće ćelije.

**Kriterijum provere:** Granice, put, voda, fontana, svaka zabranjena ćelija.

### F0353 · scenes.fitsTerrain
`index.html:L4316–4332` · parametri: `taken, key, gx, gy, s=null`

**Svrha:** Proverava geometriju, granice i teren/zauzeće za predloženi položaj.

**Kriterijum provere:** Nevalidan grid, delimični izlaz, preklapanje i dozvoljeni položaj.

### F0377 · scenes.placementRules
`index.html:L4473–4494` · parametri: `s, now, key`

**Svrha:** Priprema pravilo za konkretnu građevinu/pomeranje, proverava uslove i rezervisane ćelije, vraća closure ili null.

**Kriterijum provere:** Trošak i uslovi identični reduceru; invalidacija preview pri promeni stanja.

### F0381 · scenes.canPlace
`index.html:L4496–4499` · parametri: `s, now, key, gx, gy`

**Svrha:** Proverava tip ključa i delegira na placementRules; podrazumevano false.

**Kriterijum provere:** Isti rezultat pri potvrdi kao u preview.

### F0382 · scenes.mapRect
`index.html:L4504–4521` · parametri: `obj, view, frames`

**Svrha:** Izračunava vizuelni pravougaonik objekta prema footprint/projekciji.

**Kriterijum provere:** DPR, zoom, pan, sidro i hit-test.

### F0383 · scenes.scBuildVisualInstances
`index.html:L4526–4532` · parametri: `objects, renderer`

**Svrha:** Gradi Map vizuelnih pravougaonika i koristi keš po identitetu objects.

**Kriterijum provere:** Promena pozicije/objekata mora invalidirati keš; bez stale rendera.

### F0395 · scenes.paintMap
`index.html:L4615–4693` · parametri: `renderer, s, camera, objects, now, editor`

**Svrha:** Iscrtava ostrvo kroz renderer i vremensku fazu.

**Kriterijum provere:** Stvarni Chromium screenshot, prikaz bez naplate ili save transakcije.

### F0404 · scenes.paintRace
`index.html:L4735–4898` · parametri: `renderer, race, motion=true`

**Svrha:** Prikazuje trku preko postojećeg renderer.begin i atlasa staze.

**Kriterijum provere:** Screenshot i stvarni GIF; renderer ne dodaje nagradu.

### F0425 · storage.validateSave
`index.html:L4958–5071` · parametri: `s`

**Svrha:** Validira format, schemaVersion, identitet i strukturu save-a.

**Kriterijum provere:** Nevalidan JSON, nepoznata šema, oštećen ili nepotpun zapis.

### F0482 · storage.parseSave
`index.html:L5191–5196` · parametri: `text, now=Date.now()`

**Svrha:** Ograničava veličinu tekstualnog JSON-a, parsira i validira ili migrira legacy format.

**Kriterijum provere:** Prevelik, oštećen i legacy save; bez destruktivne zamene.

### F0488 · storage.openStore
`index.html:L5235–5244` · parametri: `indexedDB`

**Svrha:** Otvara IndexedDB i obrađuje događaje otvaranja.

**Kriterijum provere:** Blocked, upgrade, versionchange i greška otvaranja.

### F0494 · storage.indexedRepository
`index.html:L5245–5314` · parametri: `db`

**Svrha:** Formira IndexedDB adapter load/read/commit i zatvara DB na versionchange.

**Kriterijum provere:** Konflikt revizije, abort, recovery, checkpoint.

### F0512 · storage.localRepository
`index.html:L5315–5347` · parametri: `ls`

**Svrha:** Rezervni adapter localStorage sa istim ugovorom i navigator.locks kada je dostupan.

**Kriterijum provere:** Konflikt, oštećen JSON, režim bez locks; nije paralelni save autoritet.

### F0864 · app.openScreen
`index.html:L7053–7080` · parametri: `key, {keepScroll=false}={}`

**Svrha:** Otvara postojeći ekran, ne radi kada je race aktivan.

**Kriterijum provere:** Povratak, scroll, tastatura i bez gradskog UI u trci.

### F0871 · app.tickClocks
`index.html:L7094–7166` · parametri: `—`

**Svrha:** Osvežava prikaz rokova i faza iz nowBound i postojećeg stanja.

**Kriterijum provere:** Nije autoritet obračuna ekonomije; vidljivost i povratak.

### F0876 · app.commit
`index.html:L7167–7189` · parametri: `type, fields={}`

**Svrha:** Zaključava savePending, poziva applyCommand, čeka repo.commit pre zamene s, zatim osvežava status i mapu; hvata grešku.

**Kriterijum provere:** Dupli klik, neuspeh upisa, isti saveId/revision, test režim.

### F0877 · app.replaceSave
`index.html:L7190–7202` · parametri: `next, erase=false`

**Svrha:** Validira zamenski save, čuva reviziju, poziva adapter sa checkpoint/erase parametrima i menja stanje tek nakon upisa.

**Kriterijum provere:** Uvoz, reset, eksplicitno odobrenje, backup i test režim.

### F0893 · app.schedule
`index.html:L7340–7340` · parametri: `—`

**Svrha:** Zakazuje requestAnimationFrame samo ako raf nije aktivan i dokument nije skriven.

**Kriterijum provere:** Jedan glavni RAF, hidden/resume.

### F0894 · app.loop
`index.html:L7341–7409` · parametri: `now`

**Svrha:** Glavna RAF petlja: simulacija, uslovno crtanje, metrički podaci i provere renderer/lost/hidden.

**Kriterijum provere:** FPS, pause/resume, context loss, bez duplog loop-a.

### F0975 · app.boot
`index.html:L8272–8360` · parametri: `—`

**Svrha:** Pokreće renderer i sceneManager, paralelno čeka save/atlas/mapArt, validira stanje, hidrira UI i registruje lifecycle.

**Kriterijum provere:** Greška svake od tri paralelne grane, oporavak save-a i first frame.

### F0983 · SW.isWithinScope
`sw.js:L22–22` · parametri: `url`

**Svrha:** Proverava isti origin i prefiks scope putanje.

**Kriterijum provere:** Tuđi origin i van scope-a ne presretati.

### F0984 · SW.isCore
`sw.js:L23–23` · parametri: `url`

**Svrha:** Proverava da li je URL tačan član CORE mape.

**Kriterijum provere:** Query varijante i API nisu core.

### F0985 · SW.isEntryNavigation
`sw.js:L24–26` · parametri: `url`

**Svrha:** Prepoznaje scope root ili index.html putanju.

**Kriterijum provere:** Root i index offline; nepoznate rute ne prepisivati.

## 7. Potpuni statički registar (dodatak A)
Svaki AST funkcijski čvor ima zaseban ID, uključujući anonimne callbackove. Kratak isečak tela je doslovan izvorni trag (skraćen), ne potpuna semantička analiza. Odlazni pozivi su direktno unutar funkcije, bez poziva unutar njenog ugnježdenog callbacka; taj callback ima svoj ID. L je linija u fajlu funkcije; dolazne reference uključuju fajl i vlasnika. Znak ~ znači kandidat; — znači cilj nije lokalno razrešen. Za povratne vrednosti, čitanja/pisanja i cleanup koji nisu ručno pregledani status je NIJE PROVERENO.

### bootstrap — startup, PWA registracija i katalog bootstrap

**F0001 · anonimna** — `index.html:L9–63` · FunctionExpression · parent —.  
Ulaz: `—`.  
Trag tela: `{ 'use strict'; // Diagnostic only: bounded in-memory timings, never stores/uploads player data. const events=[],longTasks=[];const CAP=220,`.  
Poziva: `Object.defineProperty` L51 → —; `api.mark` L52 → —; `new PerformanceObserver(list=>{ for(const e of list.getEntries()){ if(longTasks.length>=LT_CAP)break; longTasks.push({startMs:+e.startTime.t` L54 → —; `PerformanceObserver` L54 → —; `document.addEventListener` L61 → —; `window.addEventListener` L62 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0002 · now** — `index.html:L13–13` · ArrowFunction · parent F0001.  
Ulaz: `—`.  
Trag tela: `performance.now()`.  
Poziva: `performance.now` L13 → —.  
Pozivaju: index.html:L16 (F0003); index.html:L28 (F0004); index.html:L29 (F0005); index.html:L30 (F0006); index.html:L35 (F0007); index.html:L37 (F0009); index.html:L38 (F0010).

**F0003 · emit** — `index.html:L14–26` · FunctionDeclaration · parent F0001.  
Ulaz: `kind, label, start, end, detail`.  
Trag tela: `{ if(events.length>=CAP)return; const t=Number.isFinite(start)?start:now(); const row={kind,label,startMs:+t.toFixed(2)}; if(Number.isFinite`.  
Poziva: `Number.isFinite` L16 → —; `now` L16 → F0002; `t.toFixed` L17 → —; `Number.isFinite` L18 → —; `(end-t).toFixed` L18 → —; `String(detail).slice` L19 → —; `String` L19 → —; `events.push` L20 → —; `Number.isFinite` L21 → —; `performance.measure` L22 → —; `performance.mark` L24 → —.  
Pozivaju: index.html:L29 (F0005); index.html:L30 (F0006); index.html:L37 (F0009); index.html:L38 (F0010).

**F0004 · begin** — `index.html:L28–28` · ArrowFunction · parent F0001.  
Ulaz: `—`.  
Trag tela: `now()`.  
Poziva: `now` L28 → F0002.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0005 · mark** — `index.html:L29–29` · ArrowFunction · parent F0001.  
Ulaz: `label, detail`.  
Trag tela: `emit('mark',label,now(),undefined,detail)`.  
Poziva: `emit` L29 → F0003; `now` L29 → F0002.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0006 · end** — `index.html:L30–30` · ArrowFunction · parent F0001.  
Ulaz: `label, begin, detail`.  
Trag tela: `emit('span',label,begin,now(),detail)`.  
Poziva: `emit` L30 → F0003; `now` L30 → F0002.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0007 · probeDecode** — `index.html:L33–39` · ArrowFunction · parent F0001.  
Ulaz: `image, label`.  
Trag tela: `{ if(!location.search.includes('scP1Decode=1')||typeof image?.decode!=='function')return; const begin=now(); Promise.resolve().then(()=>imag`.  
Poziva: `location.search.includes` L34 → —; `now` L35 → F0002; `Promise.resolve().then(()=>image.decode()) .then(()=>emit('span','decode.promiseLatency.'+label,begin,now(),'opt-in;may-perturb')) .catch` L36 → —; `Promise.resolve().then(()=>image.decode()) .then` L36 → —; `Promise.resolve().then` L36 → —; `Promise.resolve` L36 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0008 · callback Promise.resolve().then** — `index.html:L36–36` · ArrowFunction · parent F0007.  
Ulaz: `—`.  
Trag tela: `image.decode()`.  
Poziva: `image.decode` L36 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0009 · callback Promise.resolve().then(()=>image.decode()) .then** — `index.html:L37–37` · ArrowFunction · parent F0007.  
Ulaz: `—`.  
Trag tela: `emit('span','decode.promiseLatency.'+label,begin,now(),'opt-in;may-perturb')`.  
Poziva: `emit` L37 → F0003; `now` L37 → F0002.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0010 · callback Promise.resolve().then(()=>image.decode()) .then(()=>emit('span','decode.promiseLatency.'+label,begin,now(),'opt-in;may-perturb')) .catch** — `index.html:L38–38` · ArrowFunction · parent F0007.  
Ulaz: `—`.  
Trag tela: `emit('mark','decode.rejected.'+label,now())`.  
Poziva: `emit` L38 → F0003; `now` L38 → F0002.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0011 · export** — `index.html:L40–49` · ArrowFunction · parent F0001.  
Ulaz: `—`.  
Trag tela: `({schema:1,build:'0.8.93-deco-webp-p1',timeOrigin:performance.timeOrigin, timings:events.slice(),longTasks:longTasks.slice(), navigation:per`.  
Poziva: `events.slice` L41 → —; `longTasks.slice` L41 → —; `performance.getEntriesByType('navigation').map` L42 → —; `performance.getEntriesByType` L42 → —; `performance.getEntriesByType('paint').map` L48 → —; `performance.getEntriesByType` L48 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0012 · callback performance.getEntriesByType('navigation').map** — `index.html:L42–47` · ArrowFunction · parent F0011.  
Ulaz: `e`.  
Trag tela: `({ type:e.type,fetchStart:+e.fetchStart.toFixed(1),responseEnd:+e.responseEnd.toFixed(1), domInteractive:+e.domInteractive.toFixed(1),domCon`.  
Poziva: `e.fetchStart.toFixed` L43 → —; `e.responseEnd.toFixed` L43 → —; `e.domInteractive.toFixed` L44 → —; `e.domContentLoadedEventEnd.toFixed` L44 → —; `e.loadEventEnd.toFixed` L45 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0013 · callback performance.getEntriesByType('paint').map** — `index.html:L48–48` · ArrowFunction · parent F0011.  
Ulaz: `e`.  
Trag tela: `({name:e.name,startMs:+e.startTime.toFixed(1)})`.  
Poziva: `e.startTime.toFixed` L48 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0014 · anonimna** — `index.html:L54–59` · ArrowFunction · parent F0001.  
Ulaz: `list`.  
Trag tela: `{ for(const e of list.getEntries()){ if(longTasks.length>=LT_CAP)break; longTasks.push({startMs:+e.startTime.toFixed(1),durationMs:+e.durati`.  
Poziva: `list.getEntries` L55 → —; `longTasks.push` L57 → —; `e.startTime.toFixed` L57 → —; `e.duration.toFixed` L57 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0015 · callback document.addEventListener** — `index.html:L61–61` · ArrowFunction · parent F0001.  
Ulaz: `—`.  
Trag tela: `api.mark('document.domContentLoaded')`.  
Poziva: `api.mark` L61 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0016 · callback window.addEventListener** — `index.html:L62–62` · ArrowFunction · parent F0001.  
Ulaz: `—`.  
Trag tela: `api.mark('window.load')`.  
Poziva: `api.mark` L62 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0017 · anonimna** — `index.html:L69–93` · FunctionExpression · parent —.  
Ulaz: `—`.  
Trag tela: `{ 'use strict'; var diagnostic={version:'0.8.93',state:'unsupported',ready:false,controlled:false,error:null}; window.SC_PWA_STATUS=diagnost`.  
Poziva: `globalThis.Capacitor?.isNativePlatform` L75 → —; `Boolean` L78 → —; `nav.addEventListener` L79 → —; `nav.register('./sw.js',{scope:'./',updateViaCache:'none'}).then(function(reg){ diagnostic.state='registered'; diagnostic.scope=reg.scope; re` L80 → —; `nav.register('./sw.js',{scope:'./',updateViaCache:'none'}).then(function(reg){ diagnostic.state='registered'; diagnostic.scope=reg.scope; re` L80 → —; `nav.register('./sw.js',{scope:'./',updateViaCache:'none'}).then` L80 → —; `nav.register` L80 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0018 · callback nav.addEventListener** — `index.html:L79–79` · FunctionExpression · parent F0017.  
Ulaz: `—`.  
Trag tela: `{diagnostic.controlled=Boolean(nav.controller);}`.  
Poziva: `Boolean` L79 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0019 · callback nav.register('./sw.js',{scope:'./',updateViaCache:'none'}).then** — `index.html:L80–84` · FunctionExpression · parent F0017.  
Ulaz: `reg`.  
Trag tela: `{ diagnostic.state='registered'; diagnostic.scope=reg.scope; return nav.ready; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0020 · callback nav.register('./sw.js',{scope:'./',updateViaCache:'none'}).then(function(reg){ diagnostic.state='registered'; diagnostic.scope=reg.scope; re** — `index.html:L84–89` · FunctionExpression · parent F0017.  
Ulaz: `—`.  
Trag tela: `{ diagnostic.ready=true; diagnostic.controlled=Boolean(nav.controller); diagnostic.state='offline-ready'; console.info('[Snail City] PW-01 o`.  
Poziva: `Boolean` L86 → —; `console.info` L88 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0021 · callback nav.register('./sw.js',{scope:'./',updateViaCache:'none'}).then(function(reg){ diagnostic.state='registered'; diagnostic.scope=reg.scope; re** — `index.html:L89–92` · FunctionExpression · parent F0017.  
Ulaz: `err`.  
Trag tela: `{ diagnostic.state='failed';diagnostic.error=String(err&&err.message||err); console.error('[Snail City] PW-01 offline installation failed:',`.  
Poziva: `String` L90 → —; `console.error` L91 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0022 · anonimna** — `index.html:L1885–1918` · ArrowFunction · parent —.  
Ulaz: `—`.  
Trag tela: `{ // Content imported from the v174.103 catalog. const catalog = {"species":[{"id":0,"sr":"Plamenko","en":"Pyre-Snail","elements":["fire"],"`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0023 · anonimna** — `index.html:L1935–8365` · ArrowFunction · parent —.  
Ulaz: `—`.  
Trag tela: `{ const modules={}; modules.catalog=(()=>{ if(!globalThis.SnailCatalog)throw new Error('catalog.js nije učitan'); const catalog = globalThis`.  
Poziva: `(()=>{ if(!globalThis.SnailCatalog)throw new Error('catalog.js nije učitan'); const catalog = globalThis.SnailCatalog.catalog; return {catal` L1936 → —; `(()=>{ const WEEK_MS = 7 * 86400000, DAY_MS = 86400000; const divisions = [ ['Bronza III',0,0], ['Bronza II',100,0], ['Bronza I',200,0], ['S` L1942 → —; `(()=>{ const { catalog }=modules.catalog; const HOUR=3600000, DAY=24*HOUR; const diamondPools={care:6,meteor:12,activities:18,tasks:9}; cons` L2068 → —; `(()=>{ const HOUR=3600000; const loginRewards={ 1:{hours:1},2:{tokens:1,diamonds:1},3:{hours:2},4:{tokens:1,diamonds:3}, 5:{hours:1,tokens:1` L2158 → —; `(()=>{ const { catalog }=modules.catalog; const { getLogin, creditLogin, queueReturnGift, creditMuseum }=modules.playerProgress; const { SUM` L2216 → —; `(()=>{ const frames = {"island":{"island":[0.0013020833333333333,0.0013020833333333333,0.81640625,0.81640625,1],"sky-day":[0.001302083333333` L3176 → —; `(()=>{ // Collision and motion rules reused from the supplied v174.103 race-physics module. 'use strict'; const LANE_W=3.90, RADIUS=1.86, MA` L3181 → —; `(()=>{ const { clip, dimensionOf, rng, species, tracks, uuid }=modules.domain; const { step }=modules.physics; const { leagueOf }=modules.pr` L3279 → —; `(()=>{ const { frames }=modules.frames; const vertexSource = ˋ attribute vec2 point; attribute vec2 uv; attribute vec4 tint; uniform vec2 vi` L3500 → —; `(()=>{ /** * The only scene ownership layer. Both scenes use the same renderer and canvas. * CPU image assets remain decoded; only inactive ` L4080 → —; `(()=>{ const { defaultHomes, buildings, habitatPrice, weatherFor, trackAtlas, clip, WHEAT_FIELDS, wheatStage, reserveAt, reservoirCapacity }` L4162 → —; `(()=>{ const { AUTO_HOME_STATS }=modules.domain; const { FORMAT, newGame, dayKey, makeDaily, buildings, species, tracks, capacity, clip, exp` L4903 → —; `(()=>{ const { VERSION, DAY, buildings, tracks, species, snailName, eggNames, eggAssets, eggCosts, eggLevels, eggCapacity, incubatorUsed, cr` L5404 → —; `(()=>{ const { VERSION }=modules.domain; const rounded = (n,d=1) => Math.round(n*10**d)/10**d; function summarize(values) { if(!values.lengt` L6532 → —; `(()=>{ // Single opt-in cloud backup adapter for the existing local save format. // Publishable frontend key only; Row Level Security enforc` L6611 → —; `(()=>{ const EN_DICTIONARY=Object.freeze({"Privremena sesija: prethodni HTTPS sejv nije učitan. Napredak se ovde NE čuva. Otvori igru preko ` L6702 → —; `(()=>{ const { VERSION, WHEAT_LEVEL, WHEAT_FIELDS, wheatStage, ACTIVE_MS, newGame, eggAssets, applyCommand, available, uuid, reserveAt, rese` L6771 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### catalog — katalog

**F0024 · anonimna** — `index.html:L1936–1941` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ if(!globalThis.SnailCatalog)throw new Error('catalog.js nije učitan'); const catalog = globalThis.SnailCatalog.catalog; return {catalog}; `.  
Poziva: `Error` L1937 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### progression — sezona, liga, napredak

**F0025 · anonimna** — `index.html:L1942–2067` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const WEEK_MS = 7 * 86400000, DAY_MS = 86400000; const divisions = [ ['Bronza III',0,0], ['Bronza II',100,0], ['Bronza I',200,0], ['Srebro`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0026 · divisionOf** — `index.html:L1948–1948` · ArrowFunction · parent F0025.  
Ulaz: `trophies`.  
Trag tela: `divisions.findLastIndex(entry => trophies >= entry[1])`.  
Poziva: `divisions.findLastIndex` L1948 → —.  
Pozivaju: index.html:L1949 (F0028); index.html:L1958 (F0030); ~index.html:L6104 (F0709).

**F0027 · callback divisions.findLastIndex** — `index.html:L1948–1948` · ArrowFunction · parent F0026.  
Ulaz: `entry`.  
Trag tela: `trophies >= entry[1]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0028 · leagueOf** — `index.html:L1949–1949` · ArrowFunction · parent F0025.  
Ulaz: `trophies`.  
Trag tela: `Math.max(0,divisionOf(trophies)-2)`.  
Poziva: `Math.max` L1949 → —; `divisionOf` L1949 → F0026.  
Pozivaju: ~index.html:L2667 (F0181); ~index.html:L2953 (F0185); ~index.html:L3323 (F0240).

**F0029 · previousReward** — `index.html:L1950–1951` · ArrowFunction · parent F0025.  
Ulaz: `prev`.  
Trag tela: `prev && prev.matches>=40 && !prev.claimed ? Math.round(divisions[prev.division][2]*(prev.wins>=25?1.5:prev.wins>=15?1:.5)) : 0`.  
Poziva: `Math.round` L1951 → —.  
Pozivaju: ~index.html:L2899 (F0185); ~index.html:L6105 (F0709).

**F0030 · getSeason** — `index.html:L1952–1960` · FunctionDeclaration · parent F0025.  
Ulaz: `save, now`.  
Trag tela: `{ const week=Math.floor(now/WEEK_MS); const day=Math.floor(now/DAY_MS); const old=save.season; if(!old)return {week,matches:0,wins:0,previou`.  
Poziva: `Math.floor` L1953 → —; `Math.floor` L1954 → —; `divisionOf` L1958 → F0026.  
Pozivaju: ~index.html:L2424 (F0126); ~index.html:L2696 (F0185); ~index.html:L5780 (F0627); ~index.html:L6003 (F0686); ~index.html:L6028 (F0689); ~index.html:L6104 (F0709); ~index.html:L6114 (F0711).

**F0031 · weeklyTasks** — `index.html:L1961–1961` · ArrowFunction · parent F0025.  
Ulaz: `level`.  
Trag tela: `level>=33?['race','arena','polish','expedition']:['race','arena','polish']`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L1965 (F0033); ~index.html:L6005 (F0686).

**F0032 · cosmicTradeCost** — `index.html:L1962–1962` · ArrowFunction · parent F0025.  
Ulaz: `rate`.  
Trag tela: `Math.max(50000000,Math.round(rate*48*3600))`.  
Poziva: `Math.max` L1962 → —; `Math.round` L1962 → —.  
Pozivaju: ~index.html:L2991 (F0185); ~index.html:L6021 (F0689).

**F0033 · creditWeekly** — `index.html:L1963–1973` · FunctionDeclaration · parent F0025.  
Ulaz: `save, key`.  
Trag tela: `{ if(save.level<11)return; const expected=weeklyTasks(save.level); const season=save.season; const done=season.missions??=[]; if(!expected.i`.  
Poziva: `weeklyTasks` L1965 → F0031; `expected.includes` L1968 → —; `done.includes` L1968 → —; `done.push` L1969 → —; `expected.every` L1970 → —.  
Pozivaju: ~index.html:L2676 (F0181); ~index.html:L2857 (F0185); ~index.html:L2957 (F0185); ~index.html:L3068 (F0185).

**F0034 · callback expected.every** — `index.html:L1970–1970` · ArrowFunction · parent F0033.  
Ulaz: `v`.  
Trag tela: `done.includes(v)`.  
Poziva: `done.includes` L1970 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0035 · packAmount** — `index.html:L1979–1982` · FunctionDeclaration · parent F0025.  
Ulaz: `key, rate`.  
Trag tela: `{ const amount=exchanges[key][0]; return key.startsWith('sliz')?Math.max(2000*amount,Math.round(rate*3600*amount)):amount; }`.  
Poziva: `key.startsWith` L1981 → —; `Math.max` L1981 → —; `Math.round` L1981 → —.  
Pozivaju: ~index.html:L2877 (F0185); ~index.html:L5783 (F0629).

**F0036 · inheritedTrait** — `index.html:L1985–1985` · ArrowFunction · parent F0025.  
Ulaz: `prop`.  
Trag tela: `Object.hasOwn({hp:1,atk:1,speed:1,weight:1,prod:1,beauty:1},prop)`.  
Poziva: `Object.hasOwn` L1985 → —.  
Pozivaju: ~index.html:L4929 (F0416); ~index.html:L5075 (F0462).

**F0037 · upgradeInfo** — `index.html:L1990–2024` · FunctionDeclaration · parent F0025.  
Ulaz: `n, s, key`.  
Trag tela: `{ let cost, currency='dust', blocked=''; switch(key){ case 'snail-level': { const sl=n.sl??1; cost=wheatBase[n.cls]+15*(sl-1);currency='whea`.  
Poziva: `Math.min` L1997 → —; `tempering.includes` L1998 → —; `Math.floor` L2003 → —; `Math.max` L2010 → —; `Math.round` L2010 → —.  
Pozivaju: ~index.html:L2853 (F0185); ~index.html:L5516 (F0565); ~index.html:L5533 (F0568).

**F0038 · inheritedStat** — `index.html:L2025–2029` · FunctionDeclaration · parent F0025.  
Ulaz: `snail, key`.  
Trag tela: `{ if(key==='weight')return snail.originalWeight??snail.weight; if(key==='beauty')return snail.originalBeauty??Math.max(0,snail.beauty-snail.`.  
Poziva: `Math.max` L2027 → —.  
Pozivaju: ~index.html:L2791 (F0189).

**F0039 · improveSnail** — `index.html:L2030–2064` · FunctionDeclaration · parent F0025.  
Ulaz: `n, key`.  
Trag tela: `{ switch(key){ case 'snail-level': { const sl=n.sl??1; const base=n.baseStats??=Object.fromEntries(foundation.map(prop=>[prop,n[prop]])); if`.  
Poziva: `Object.fromEntries` L2034 → —; `foundation.map` L2034 → —; `tempering.includes` L2035 → —; `next.toFixed` L2039 → —; `Math.round` L2039 → —; `Math.max` L2044 → —; `Math.max` L2049 → —; `Math.round` L2049 → —; `Math.min` L2049 → —; `Math.round` L2049 → —; `restored.toFixed` L2057 → —; `Math.round` L2057 → —; `Math.round` L2058 → —; `Math.round` L2059 → —.  
Pozivaju: ~index.html:L2856 (F0185).

**F0040 · callback foundation.map** — `index.html:L2034–2034` · ArrowFunction · parent F0039.  
Ulaz: `prop`.  
Trag tela: `[prop,n[prop]]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### islandEvents — događaji ostrva

**F0041 · anonimna** — `index.html:L2068–2157` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const { catalog }=modules.catalog; const HOUR=3600000, DAY=24*HOUR; const diamondPools={care:6,meteor:12,activities:18,tasks:9}; const SUM`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0042 · timeBreakCost** — `index.html:L2076–2076` · ArrowFunction · parent F0041.  
Ulaz: `production`.  
Trag tela: `Math.max(300,Math.round(production*3600/10)*10)`.  
Poziva: `Math.max` L2076 → —; `Math.round` L2076 → —.  
Pozivaju: ~index.html:L2823 (F0185); ~index.html:L5747 (F0624).

**F0043 · craterPrice** — `index.html:L2077–2077` · ArrowFunction · parent F0041.  
Ulaz: `state`.  
Trag tela: `state.craterPrice??70`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: ~index.html:L2576 (F0151); ~index.html:L6020 (F0689).

**F0044 · nextCraterPrice** — `index.html:L2078–2078` · ArrowFunction · parent F0041.  
Ulaz: `level`.  
Trag tela: `Math.max(70,Math.min(200,70+3*(level-20)))`.  
Poziva: `Math.max` L2078 → —; `Math.min` L2078 → —.  
Pozivaju: ~index.html:L2579 (F0151).

**F0045 · summonChoices** — `index.html:L2079–2080` · ArrowFunction · parent F0041.  
Ulaz: `phase`.  
Trag tela: `Object.keys(catalog.weather).filter(id=> id!=='starfall'&&id!=='calm'&&(!catalog.weather[id].ph||catalog.weather[id].ph.includes(phase)))`.  
Poziva: `Object.keys(catalog.weather).filter` L2079 → —; `Object.keys` L2079 → —.  
Pozivaju: ~index.html:L2984 (F0185); ~index.html:L5762 (F0625).

**F0046 · callback Object.keys(catalog.weather).filter** — `index.html:L2079–2080` · ArrowFunction · parent F0045.  
Ulaz: `id`.  
Trag tela: `id!=='starfall'&&id!=='calm'&&(!catalog.weather[id].ph||catalog.weather[id].ph.includes(phase))`.  
Poziva: `catalog.weather[id].ph.includes` L2080 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0047 · creditDiamonds** — `index.html:L2082–2088` · FunctionDeclaration · parent F0041.  
Ulaz: `state, pool, requested`.  
Trag tela: `{ const counts=state.daily.diamondPools??={}; const used=Object.values(counts).reduce((sum,n)=>sum+n,0); const received=Math.min(requested,d`.  
Poziva: `Object.values(counts).reduce` L2084 → —; `Object.values` L2084 → —; `Math.min` L2085 → —; `Math.max` L2087 → —.  
Pozivaju: ~index.html:L2669 (F0181); ~index.html:L2763 (F0185); ~index.html:L2779 (F0185); ~index.html:L2965 (F0185); ~index.html:L2979 (F0185); ~index.html:L3004 (F0185); ~index.html:L3091 (F0185).

**F0048 · callback Object.values(counts).reduce** — `index.html:L2084–2084` · ArrowFunction · parent F0047.  
Ulaz: `sum, n`.  
Trag tela: `sum+n`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0049 · canCare** — `index.html:L2090–2091` · ArrowFunction · parent F0041.  
Ulaz: `egg, now`.  
Trag tela: `!egg.cared&&egg.careAt!==null&&egg.careEnd!==null&& egg.careEnd>=now&&egg.readyAt>now`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2094 (F0050); index.html:L2102 (F0051); ~index.html:L2776 (F0185); ~index.html:L2816 (F0185); ~index.html:L5691 (F0612); ~index.html:L7113 (F0873); ~index.html:L8263 (F0974).

**F0050 · releaseExpiredHalf** — `index.html:L2093–2098` · FunctionDeclaration · parent F0041.  
Ulaz: `state, egg, now`.  
Trag tela: `{ if(egg.halfHeld&&!canCare(egg,now)){ egg.halfHeld=false; state.halfTokens=(state.halfTokens??0)+1; } }`.  
Poziva: `canCare` L2094 → F0049.  
Pozivaju: index.html:L2107 (F0051); ~index.html:L2565 (F0144).

**F0051 · accelerateEgg** — `index.html:L2100–2108` · FunctionDeclaration · parent F0041.  
Ulaz: `state, egg, now, ms`.  
Trag tela: `{ egg.readyAt=Math.max(now,egg.readyAt-ms); if(canCare(egg,now)&&egg.careAt>now){ const window=egg.careEnd-egg.careAt; egg.careAt=Math.max(n`.  
Poziva: `Math.max` L2101 → —; `canCare` L2102 → F0049; `Math.max` L2104 → —; `Math.min` L2104 → —; `Math.min` L2105 → —; `releaseExpiredHalf` L2107 → F0050.  
Pozivaju: ~index.html:L2778 (F0185); ~index.html:L2808 (F0185); ~index.html:L2815 (F0185).

**F0052 · tickMeteorRain** — `index.html:L2110–2120` · FunctionDeclaration · parent F0041.  
Ulaz: `state, now, random`.  
Trag tela: `{ if(state.level<11)return; if(state.rain){ if(now<state.rain.until)return; if(state.rain.caught>0&&random()<.04)state.craterQueue=(state.cr`.  
Poziva: `random` L2114 → —; `Math.floor` L2116 → —; `random` L2116 → —.  
Pozivaju: ~index.html:L2566 (F0144).

**F0053 · nextMeteor** — `index.html:L2122–2130` · FunctionDeclaration · parent F0041.  
Ulaz: `state, now`.  
Trag tela: `{ if(state.level<3)return null; const rain=state.rain; if(rain&&now<rain.until){ return rain.caught<RAIN_LIMIT&&now>=rain.readyAt?'rain':nul`.  
Poziva: `Math.floor` L2128 → —.  
Pozivaju: ~index.html:L2969 (F0185); ~index.html:L6014 (F0688); ~index.html:L7051 (F0860); ~index.html:L7145 (F0871).

**F0054 · creditPrestige** — `index.html:L2132–2147` · FunctionDeclaration · parent F0041.  
Ulaz: `state, snail`.  
Trag tela: `{ snail.showWins=(snail.showWins??0)+1; state.titles++; const tiers={ 5:['diamonds',2],15:['dust',5],30:['beauty',.03],60:['dust',10], 100:[`.  
Poziva: `Math.max` L2143 → —; `Math.round` L2144 → —.  
Pozivaju: ~index.html:L3096 (F0185).

**F0055 · prestigeBoost** — `index.html:L2149–2149` · ArrowFunction · parent F0041.  
Ulaz: `titles`.  
Trag tela: `Math.min(.05,Math.floor(titles/50)*.01)`.  
Poziva: `Math.min` L2149 → —; `Math.floor` L2149 → —.  
Pozivaju: ~index.html:L2513 (F0139).

**F0056 · showReference** — `index.html:L2150–2154` · FunctionDeclaration · parent F0041.  
Ulaz: `level`.  
Trag tela: `{ if(level<=44)return (92+.9*level)*1.1; if(level<=70)return (132-.2*(level-44))*1.1; return (127+1.5*(level-70))*1.1; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: ~index.html:L3086 (F0185).

### playerProgress — napredak igrača

**F0057 · anonimna** — `index.html:L2158–2215` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const HOUR=3600000; const loginRewards={ 1:{hours:1},2:{tokens:1,diamonds:1},3:{hours:2},4:{tokens:1,diamonds:3}, 5:{hours:1,tokens:1,diam`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0058 · getLogin** — `index.html:L2168–2176` · FunctionDeclaration · parent F0057.  
Ulaz: `season, production`.  
Trag tela: `{ const gap=season.rewardDay===null?Infinity:season.day-season.rewardDay; const grace=gap===2&&(season.streakGrace===undefined||season.day-s`.  
Poziva: `Math.max` L2172 → —; `Math.max` L2175 → —; `Math.round` L2175 → —.  
Pozivaju: ~index.html:L2891 (F0185); ~index.html:L6114 (F0711).

**F0059 · creditLogin** — `index.html:L2178–2184` · FunctionDeclaration · parent F0057.  
Ulaz: `save, plan`.  
Trag tela: `{ save.season.rewardDay=save.season.day; save.season.streak=plan.streak; if(plan.grace)save.season.streakGrace=save.season.day; for(const ke`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: ~index.html:L2893 (F0185).

**F0060 · queueReturnGift** — `index.html:L2186–2198` · FunctionDeclaration · parent F0057.  
Ulaz: `save, elapsed, random`.  
Trag tela: `{ const season=save.season; if(save.level<11||elapsed<20*HOUR||season.giftDay===season.day|| (season.fragmentsEarned??0)>=10||(season.giftsR`.  
Poziva: `random` L2192 → —; `Math.floor` L2192 → —; `random` L2192 → —; `Math.min` L2193 → —.  
Pozivaju: ~index.html:L2698 (F0185).

**F0061 · creditMuseum** — `index.html:L2203–2212` · FunctionDeclaration · parent F0057.  
Ulaz: `save, snail, name, at`.  
Trag tela: `{ const old=save.museumPoints??0; const points=specimenPoints[snail.cls]; save.museumPoints=old+points; save.museum=[...(save.museum??[]),{s`.  
Poziva: `[...(save.museum??[]),{species:snail.species,name,at}].slice` L2207 → —.  
Pozivaju: ~index.html:L2871 (F0185).

### domain — stanje, komande, ekonomija

**F0062 · anonimna** — `index.html:L2216–3175` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const { catalog }=modules.catalog; const { getLogin, creditLogin, queueReturnGift, creditMuseum }=modules.playerProgress; const { SUMMON_C`.  
Poziva: `Object.freeze` L2224 → —; `Object.freeze` L2322 → —; `Set` L2323 → —; `Set` L2455 → —; `Set` L2456 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0063 · wheatYield** — `index.html:L2227–2227` · FunctionDeclaration · parent F0062.  
Ulaz: `s`.  
Trag tela: `{return WHEAT_AMOUNT+30*(s.wheatRank??0);}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2729 (F0185); index.html:L2745 (F0185); ~index.html:L6165 (F0718).

**F0064 · wheatKey** — `index.html:L2231–2231` · ArrowFunction · parent F0062.  
Ulaz: `field`.  
Trag tela: `field===0?'wheat':'wheat:'+field`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2711 (F0185); index.html:L2727 (F0187); index.html:L2743 (F0185).

**F0065 · wheatBuilt** — `index.html:L2232–2232` · FunctionDeclaration · parent F0062.  
Ulaz: `s, field`.  
Trag tela: `{return Array.isArray(s.wheatBuilt)&&s.wheatBuilt.includes(field);}`.  
Poziva: `Array.isArray` L2232 → —; `s.wheatBuilt.includes` L2232 → —.  
Pozivaju: index.html:L2238 (F0067); index.html:L2706 (F0185); index.html:L2727 (F0187); index.html:L2743 (F0185).

**F0066 · wheatDeadline** — `index.html:L2234–2236` · FunctionDeclaration · parent F0062.  
Ulaz: `s, field=0`.  
Trag tela: `{ return (field===0?s.wheatReadyAt:s.wheatExtraReadyAt?.[field-1])??0; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2239 (F0067); ~index.html:L6170 (F0719).

**F0067 · wheatStage** — `index.html:L2237–2241` · FunctionDeclaration · parent F0062.  
Ulaz: `s, now, field=0`.  
Trag tela: `{ if(!(s.level>=WHEAT_FIELDS[field])||!wheatBuilt(s,field))return null; const left=wheatDeadline(s,field)-now; return left<=0?'ripe':left>WH`.  
Poziva: `wheatBuilt` L2238 → F0065; `wheatDeadline` L2239 → F0066.  
Pozivaju: index.html:L2727 (F0187); index.html:L2744 (F0185); ~index.html:L4213 (F0336); ~index.html:L6169 (F0719); ~index.html:L7010 (F0856); ~index.html:L7051 (F0863); ~index.html:L7098 (F0872).

**F0068 · expeditionFactor** — `index.html:L2262–2262` · ArrowFunction · parent F0062.  
Ulaz: `level`.  
Trag tela: `level<=15?2:level<=33?2-1.5*(level-15)/18:Math.max(.3,.5-(level-33)/55)`.  
Poziva: `Math.max` L2262 → —.  
Pozivaju: index.html:L2268 (F0070); ~index.html:L6061 (F0697).

**F0069 · snailPower** — `index.html:L2263–2263` · ArrowFunction · parent F0062.  
Ulaz: `n`.  
Trag tela: `Math.round(n.hp/5+n.atk*2+n.speed*1.5)`.  
Poziva: `Math.round` L2263 → —.  
Pozivaju: index.html:L2341 (F0102); index.html:L3059 (F0215); ~index.html:L7974 (F0948); ~index.html:L7974 (F0948).

**F0070 · expeditionSliz** — `index.html:L2265–2269` · FunctionDeclaration · parent F0062.  
Ulaz: `hours, power, production, skippedMs, level`.  
Trag tela: `{ const f=1-Math.min(1,(skippedMs||0)/(hours*HOUR)); const bonus=(expeditions.find(e=>e[2]===hours)?.[3]??2)-1; return Math.round(hours*powe`.  
Poziva: `Math.min` L2266 → —; `expeditions.find` L2267 → —; `Math.round` L2268 → —; `expeditionFactor` L2268 → F0068.  
Pozivaju: index.html:L3059 (F0185).

**F0071 · callback expeditions.find** — `index.html:L2267–2267` · ArrowFunction · parent F0070.  
Ulaz: `e`.  
Trag tela: `e[2]===hours`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0072 · trackAtlas** — `index.html:L2277–2277` · ArrowFunction · parent F0062.  
Ulaz: `key`.  
Trag tela: `tracks[key]?.art??'race'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: ~index.html:L4737 (F0404); ~index.html:L7265 (F0883); ~index.html:L7273 (F0883).

**F0073 · dimensionOf** — `index.html:L2286–2286` · ArrowFunction · parent F0062.  
Ulaz: `level`.  
Trag tela: `dimensions.findLast(item=>level>=item.level)??null`.  
Poziva: `dimensions.findLast` L2286 → —.  
Pozivaju: index.html:L2287 (F0075); index.html:L2434 (F0131); index.html:L2501 (F0135); index.html:L2518 (F0141); index.html:L2557 (F0144); index.html:L2976 (F0185); index.html:L3109 (F0185); ~index.html:L3316 (F0240); ~index.html:L5890 (F0655); ~index.html:L6159 (F0716).

**F0074 · callback dimensions.findLast** — `index.html:L2286–2286` · ArrowFunction · parent F0073.  
Ulaz: `item`.  
Trag tela: `level>=item.level`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0075 · incubationRate** — `index.html:L2287–2287` · ArrowFunction · parent F0062.  
Ulaz: `level`.  
Trag tela: `dimensionOf(level)?.id==='chronos'?2:1`.  
Poziva: `dimensionOf` L2287 → F0073.  
Pozivaju: index.html:L2397 (F0122); index.html:L3145 (F0185); index.html:L3145 (F0185).

**F0076 · expeditionTeam** — `index.html:L2288–2288` · ArrowFunction · parent F0062.  
Ulaz: `e`.  
Trag tela: `e.team??[e.snail]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L3040 (F0185); ~index.html:L5013 (F0441); ~index.html:L5013 (F0441); ~index.html:L5013 (F0441); ~index.html:L5014 (F0441); ~index.html:L5014 (F0441); ~index.html:L5014 (F0441); ~index.html:L5047 (F0455); ~index.html:L5048 (F0456); ~index.html:L6065 (F0700).

**F0077 · capacity** — `index.html:L2296–2296` · ArrowFunction · parent F0062.  
Ulaz: `level`.  
Trag tela: `[3,6,9,12][level-1]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2331 (F0099); index.html:L2584 (F0153); index.html:L2831 (F0185); index.html:L3020 (F0185); index.html:L3052 (F0185); ~index.html:L5043 (F0451); ~index.html:L5049 (F0425); ~index.html:L5122 (F0464); ~index.html:L5472 (F0558); ~index.html:L5578 (F0580); ~index.html:L5586 (F0581); ~index.html:L5586 (F0581); ~index.html:L5665 (F0604); ~index.html:L5675 (F0604); ~index.html:L5741 (F0623).

**F0078 · baseXp** — `index.html:L2298–2298` · ArrowFunction · parent F0062.  
Ulaz: `level`.  
Trag tela: `30 + level*22 + 9*Math.max(0,level-10)**2`.  
Poziva: `Math.max` L2298 → —.  
Pozivaju: index.html:L2299 (F0079); index.html:L2668 (F0181); index.html:L2668 (F0181); index.html:L2759 (F0185); index.html:L2955 (F0185); index.html:L2965 (F0185).

**F0079 · xpNeeded** — `index.html:L2299–2299` · ArrowFunction · parent F0062.  
Ulaz: `level`.  
Trag tela: `Math.round(baseXp(level)*(level<66?1:level<70?1.5:level<80?1.5+.09*(level-70):level<87?2.4:5.8))`.  
Poziva: `Math.round` L2299 → —; `baseXp` L2299 → F0078.  
Pozivaju: index.html:L2438 (F0131); index.html:L2441 (F0131); ~index.html:L6093 (F0708); ~index.html:L6093 (F0708); ~index.html:L6892 (F0837).

**F0080 · reservoirHours** — `index.html:L2305–2305` · ArrowFunction · parent F0062.  
Ulaz: `level`.  
Trag tela: `level>=33?24:level>=22?16:level>=11?12:6`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2307 (F0081); ~index.html:L5735 (F0621).

**F0081 · reservoirCapacity** — `index.html:L2306–2307` · ArrowFunction · parent F0062.  
Ulaz: `s`.  
Trag tela: `Math.max(600 + 600*s.homes.reduce((sum,home)=>sum+home.level,0) + 200*s.level, Math.round(rate(s,s.lastAt,false)*reservoirHours(s.level)*360`.  
Poziva: `Math.max` L2306 → —; `s.homes.reduce` L2306 → —; `Math.round` L2307 → —; `rate` L2307 → F0139; `reservoirHours` L2307 → F0080.  
Pozivaju: index.html:L2531 (F0142); index.html:L2758 (F0185); ~index.html:L4609 (F0394); ~index.html:L5728 (F0621); ~index.html:L7117 (F0871); ~index.html:L7808 (F0931).

**F0082 · callback s.homes.reduce** — `index.html:L2306–2306` · ArrowFunction · parent F0081.  
Ulaz: `sum, home`.  
Trag tela: `sum+home.level`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0083 · masteryOpen** — `index.html:L2310–2310` · ArrowFunction · parent F0062.  
Ulaz: `s`.  
Trag tela: `s.homes.length>=2&&s.homes.every(home=>home.level>=4)`.  
Poziva: `s.homes.every` L2310 → —.  
Pozivaju: index.html:L3134 (F0185); ~index.html:L5611 (F0597).

**F0084 · callback s.homes.every** — `index.html:L2310–2310` · ArrowFunction · parent F0083.  
Ulaz: `home`.  
Trag tela: `home.level>=4`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0085 · tourists** — `index.html:L2311–2314` · FunctionDeclaration · parent F0062.  
Ulaz: `s`.  
Trag tela: `{ const beauty=s.snails.filter(n=>n.home&&!n.busy).reduce((sum,n)=>sum+(n.beauty||0),0); return beauty<30?0:Math.min(.2,.1+(beauty-30)/1000)`.  
Poziva: `s.snails.filter(n=>n.home&&!n.busy).reduce` L2312 → —; `s.snails.filter` L2312 → —; `Math.min` L2313 → —.  
Pozivaju: index.html:L2513 (F0139); ~index.html:L5632 (F0599).

**F0086 · callback s.snails.filter** — `index.html:L2312–2312` · ArrowFunction · parent F0085.  
Ulaz: `n`.  
Trag tela: `n.home&&!n.busy`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0087 · callback s.snails.filter(n=>n.home&&!n.busy).reduce** — `index.html:L2312–2312` · ArrowFunction · parent F0085.  
Ulaz: `sum, n`.  
Trag tela: `sum+(n.beauty||0)`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0088 · eggCapacity** — `index.html:L2315–2315` · ArrowFunction · parent F0062.  
Ulaz: `s`.  
Trag tela: `2+Math.floor(s.level/11)`.  
Poziva: `Math.floor` L2315 → —.  
Pozivaju: index.html:L2609 (F0167); index.html:L2769 (F0185); index.html:L3003 (F0185); ~index.html:L5718 (F0618); ~index.html:L5720 (F0618); ~index.html:L5820 (F0632); ~index.html:L5824 (F0627); ~index.html:L5992 (F0680); ~index.html:L6100 (F0708).

**F0089 · incubatorUsed** — `index.html:L2316–2316` · ArrowFunction · parent F0062.  
Ulaz: `s`.  
Trag tela: `s.eggs.filter(e=>e.kind!==8).length`.  
Poziva: `s.eggs.filter` L2316 → —.  
Pozivaju: index.html:L2609 (F0167); index.html:L2769 (F0185); index.html:L3003 (F0185); ~index.html:L5718 (F0618); ~index.html:L5720 (F0618); ~index.html:L5820 (F0632); ~index.html:L5824 (F0627); ~index.html:L5992 (F0680); ~index.html:L6100 (F0708).

**F0090 · callback s.eggs.filter** — `index.html:L2316–2316` · ArrowFunction · parent F0089.  
Ulaz: `e`.  
Trag tela: `e.kind!==8`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0091 · craterUsed** — `index.html:L2317–2317` · ArrowFunction · parent F0062.  
Ulaz: `s`.  
Trag tela: `s.eggs.some(e=>e.kind===8)`.  
Poziva: `s.eggs.some` L2317 → —.  
Pozivaju: index.html:L2609 (F0167); index.html:L2995 (F0185); ~index.html:L5720 (F0618); ~index.html:L5723 (F0618).

**F0092 · callback s.eggs.some** — `index.html:L2317–2317` · ArrowFunction · parent F0091.  
Ulaz: `e`.  
Trag tela: `e.kind===8`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0093 · clip** — `index.html:L2318–2318` · ArrowFunction · parent F0062.  
Ulaz: `value, min, max`.  
Trag tela: `Math.min(max,Math.max(min,value))`.  
Poziva: `Math.min` L2318 → —; `Math.max` L2318 → —.  
Pozivaju: index.html:L2529 (F0142); index.html:L2534 (F0142); index.html:L2544 (F0144); index.html:L2606 (F0167); ~index.html:L3318 (F0240); ~index.html:L3318 (F0240); ~index.html:L3337 (F0243); ~index.html:L3345 (F0245); ~index.html:L3391 (F0253); ~index.html:L3404 (F0253); ~index.html:L3434 (F0253); ~index.html:L3438 (F0253); ~index.html:L3443 (F0253); ~index.html:L3452 (F0257); ~index.html:L3472 (F0260); ~index.html:L3479 (F0261); ~index.html:L4869 (F0404); ~index.html:L4870 (F0404); ~index.html:L4876 (F0404); ~index.html:L4910 (F0410); ~index.html:L4911 (F0411).

**F0094 · usable** — `index.html:L2319–2319` · ArrowFunction · parent F0062.  
Ulaz: `snail`.  
Trag tela: `Boolean(snail && !snail.busy)`.  
Poziva: `Boolean` L2319 → —.  
Pozivaju: index.html:L2320 (F0095); index.html:L2558 (F0147); index.html:L3106 (F0222).

**F0095 · available** — `index.html:L2320–2321` · ArrowFunction · parent F0062.  
Ulaz: `s, snail`.  
Trag tela: `usable(snail)&& !(!s.arena?.done&&s.arena?.team.some(member=>member.id===snail.id))`.  
Poziva: `usable` L2320 → F0094; `s.arena?.team.some` L2321 → —.  
Pozivaju: index.html:L2337 (F0097); index.html:L2339 (F0101); index.html:L2586 (F0154); index.html:L2603 (F0167); index.html:L2603 (F0167); index.html:L2828 (F0185); index.html:L3021 (F0205); ~index.html:L5518 (F0565); ~index.html:L5535 (F0568); ~index.html:L5549 (F0573); ~index.html:L5890 (F0656); ~index.html:L5926 (F0664); ~index.html:L5988 (F0681); ~index.html:L6035 (F0692); ~index.html:L6057 (F0698); ~index.html:L6955 (F0847); ~index.html:L7257 (F0883); ~index.html:L7973 (F0947).

**F0096 · callback s.arena?.team.some** — `index.html:L2321–2321` · ArrowFunction · parent F0095.  
Ulaz: `member`.  
Trag tela: `member.id===snail.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0097 · assignBestHomes** — `index.html:L2327–2355` · FunctionDeclaration · parent F0062.  
Ulaz: `s, now, stat=s.autoStat??'prod'`.  
Trag tela: `{ requireThat(AUTO_HOME_STATS.includes(stat),'Nepoznat atribut automatskog rasporeda.'); const before=rate(s,now),original=new Map(s.snails.`.  
Poziva: `requireThat` L2328 → F0128; `AUTO_HOME_STATS.includes` L2328 → —; `rate` L2329 → F0139; `Map` L2329 → —; `s.snails.map` L2329 → —; `s.homes.map` L2330 → —; `Map` L2332 → —; `groups.map` L2332 → —; `available` L2337 → F0095; `byId.has` L2337 → —; `byId.get` L2337 → —; `s.snails.filter` L2339 → —; `movable.sort` L2343 → —; `groups.sort` L2344 → —; `Math.max` L2347 → —; `s.snails.filter` L2352 → —; `s.snails.filter` L2353 → —; `rate` L2354 → F0139; `Boolean` L2354 → —.  
Pozivaju: index.html:L2837 (F0185); index.html:L2844 (F0185); index.html:L3161 (F0185).

**F0098 · callback s.snails.map** — `index.html:L2329–2329` · ArrowFunction · parent F0097.  
Ulaz: `n`.  
Trag tela: `[n.id,n.home]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0099 · callback s.homes.map** — `index.html:L2330–2331` · ArrowFunction · parent F0097.  
Ulaz: `h, index`.  
Trag tela: `({id:h.id,level:h.level,index, capacity:capacity(h.level),fixed:0})`.  
Poziva: `capacity` L2331 → F0077.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0100 · callback groups.map** — `index.html:L2332–2332` · ArrowFunction · parent F0097.  
Ulaz: `g`.  
Trag tela: `[g.id,g]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0101 · callback s.snails.filter** — `index.html:L2339–2339` · ArrowFunction · parent F0097.  
Ulaz: `n`.  
Trag tela: `available(s,n)`.  
Poziva: `available` L2339 → F0095.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0102 · primary** — `index.html:L2340–2341` · ArrowFunction · parent F0097.  
Ulaz: `n`.  
Trag tela: `stat==='prod'?n.prod*economyMultiplier(s,n,now,true): stat==='power'?snailPower(n):(n[stat]??0)`.  
Poziva: `economyMultiplier` L2340 → F0135; `snailPower` L2341 → F0069.  
Pozivaju: index.html:L2343 (F0103); index.html:L2343 (F0103).

**F0103 · callback movable.sort** — `index.html:L2343–2343` · ArrowFunction · parent F0097.  
Ulaz: `a, b`.  
Trag tela: `primary(b)-primary(a)||b.prod-a.prod||a.id.localeCompare(b.id)`.  
Poziva: `primary` L2343 → F0102; `primary` L2343 → F0102; `a.id.localeCompare` L2343 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0104 · callback groups.sort** — `index.html:L2344–2344` · ArrowFunction · parent F0097.  
Ulaz: `a, b`.  
Trag tela: `b.level-a.level||a.index-b.index`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0105 · callback s.snails.filter** — `index.html:L2352–2352` · ArrowFunction · parent F0097.  
Ulaz: `n`.  
Trag tela: `n.home!==original.get(n.id)`.  
Poziva: `original.get` L2352 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0106 · callback s.snails.filter** — `index.html:L2353–2353` · ArrowFunction · parent F0097.  
Ulaz: `n`.  
Trag tela: `n.home&&!n.busy`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0107 · snailName** — `index.html:L2356–2356` · ArrowFunction · parent F0062.  
Ulaz: `snail, lang='sr'`.  
Trag tela: `snail.name || species[snail.species]?.[lang] || (lang==='en'?'Hybrid':'Hibrid')`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2804 (F0185); index.html:L2871 (F0185); index.html:L3113 (F0228); ~index.html:L5468 (F0551); ~index.html:L5521 (F0565); ~index.html:L5522 (F0565); ~index.html:L5543 (F0572); ~index.html:L5553 (F0575); ~index.html:L5561 (F0573); ~index.html:L5563 (F0573); ~index.html:L5592 (F0584); ~index.html:L5592 (F0584); ~index.html:L5868 (F0650); ~index.html:L5902 (F0660); ~index.html:L5912 (F0661); ~index.html:L5920 (F0662); ~index.html:L5946 (F0671); ~index.html:L5982 (F0679); ~index.html:L6041 (F0696); ~index.html:L6065 (F0701); ~index.html:L6071 (F0705); ~index.html:L6474 (F0767); ~index.html:L6522 (F0778).

**F0108 · dayKey** — `index.html:L2357–2357` · ArrowFunction · parent F0062.  
Ulaz: `now`.  
Trag tela: `Math.floor(now/DAY)`.  
Poziva: `Math.floor` L2357 → —.  
Pozivaju: index.html:L2423 (F0126); index.html:L2547 (F0144); index.html:L2547 (F0144); ~index.html:L5145 (F0464).

**F0109 · idOk** — `index.html:L2360–2360` · ArrowFunction · parent F0062.  
Ulaz: `id`.  
Trag tela: `typeof id === 'string' && /^[A-Za-z0-9_-]{1,100}$/.test(id)`.  
Poziva: `/^[A-Za-z0-9_-]{1,100}$/.test` L2360 → —.  
Pozivaju: index.html:L2691 (F0185); index.html:L2948 (F0185).

**F0110 · uuid** — `index.html:L2361–2363` · FunctionDeclaration · parent F0062.  
Ulaz: `—`.  
Trag tela: `{ return globalThis.crypto?.randomUUID?.() ?? String(Date.now())+'-'+Math.floor(Math.random()*1e12); }`.  
Poziva: `globalThis.crypto?.randomUUID` L2362 → —; `String` L2362 → —; `Date.now` L2362 → —; `Math.floor` L2362 → —; `Math.random` L2362 → —.  
Pozivaju: index.html:L2417 (F0126); ~index.html:L3312 (F0240); ~index.html:L6959 (F0847); ~index.html:L7171 (F0876); ~index.html:L7272 (F0883); ~index.html:L7817 (F0934).

**F0111 · rng** — `index.html:L2364–2367` · FunctionDeclaration · parent F0062.  
Ulaz: `seed`.  
Trag tela: `{ let n=seed>>>0; return () => ((n=(Math.imul(1664525,n)+1013904223)>>>0)/4294967296); }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2369 (F0113); ~index.html:L3315 (F0240); ~index.html:L3317 (F0240).

**F0112 · anonimna** — `index.html:L2366–2366` · ArrowFunction · parent F0111.  
Ulaz: `—`.  
Trag tela: `((n=(Math.imul(1664525,n)+1013904223)>>>0)/4294967296)`.  
Poziva: `Math.imul` L2366 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0113 · seedDay** — `index.html:L2368–2370` · FunctionDeclaration · parent F0062.  
Ulaz: `day`.  
Trag tela: `{ return rng((day*2654435761)>>>0); }`.  
Poziva: `rng` L2369 → F0111.  
Pozivaju: index.html:L2372 (F0114).

**F0114 · makeDaily** — `index.html:L2371–2376` · FunctionDeclaration · parent F0062.  
Ulaz: `level, day`.  
Trag tela: `{ const rand=seedDay(day); const targets=dailyDefs.filter(item=>item[2]<=Math.max(3,level)).map(item=>({key:item[0],rank:rand()})); targets.`.  
Poziva: `seedDay` L2372 → F0113; `dailyDefs.filter(item=>item[2]<=Math.max(3,level)).map` L2373 → —; `dailyDefs.filter` L2373 → —; `targets.sort` L2374 → —; `targets.slice(0,3).map` L2375 → —; `targets.slice` L2375 → —.  
Pozivaju: index.html:L2423 (F0126); index.html:L2547 (F0144); ~index.html:L5145 (F0464).

**F0115 · callback dailyDefs.filter** — `index.html:L2373–2373` · ArrowFunction · parent F0114.  
Ulaz: `item`.  
Trag tela: `item[2]<=Math.max(3,level)`.  
Poziva: `Math.max` L2373 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0116 · callback dailyDefs.filter(item=>item[2]<=Math.max(3,level)).map** — `index.html:L2373–2373` · ArrowFunction · parent F0114.  
Ulaz: `item`.  
Trag tela: `({key:item[0],rank:rand()})`.  
Poziva: `rand` L2373 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0117 · callback targets.sort** — `index.html:L2374–2374` · ArrowFunction · parent F0114.  
Ulaz: `a, b`.  
Trag tela: `a.rank-b.rank`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0118 · callback targets.slice(0,3).map** — `index.html:L2375–2375` · ArrowFunction · parent F0114.  
Ulaz: `v`.  
Trag tela: `v.key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0119 · newSnail** — `index.html:L2377–2394` · FunctionDeclaration · parent F0062.  
Ulaz: `id, i, random=()=>.5, traits=false`.  
Trag tela: `{ const type=species[i], b=catalog.base[type.cls], w=type.weight; const vary=()=>.85+random()*.30; const snail={id,species:i,cls:type.cls,na`.  
Poziva: `Math.round` L2381 → —; `vary` L2381 → F0121; `Math.round` L2381 → —; `vary` L2381 → F0121; `Math.max` L2381 → —; `Math.round` L2381 → —; `Math.sqrt` L2381 → —; `vary` L2381 → F0121; `Math.max` L2382 → —; `Math.round` L2382 → —; `vary` L2382 → F0121; `(b.prod*type.production*vary()).toFixed` L2382 → —; `vary` L2382 → F0121; `Math.round` L2383 → —; `vary` L2383 → F0121; `Math.floor` L2386 → —; `random` L2386 → —; `Math.floor` L2388 → —; `random` L2388 → —; `(snail[key]*mul).toFixed` L2390 → —; `Math.max` L2390 → —; `Math.round` L2390 → —.  
Pozivaju: index.html:L2421 (F0126); index.html:L2421 (F0126); index.html:L2786 (F0185).

**F0120 · anonimna** — `index.html:L2377–2377` · ArrowFunction · parent F0119.  
Ulaz: `—`.  
Trag tela: `.5`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0121 · vary** — `index.html:L2379–2379` · ArrowFunction · parent F0119.  
Ulaz: `—`.  
Trag tela: `.85+random()*.30`.  
Poziva: `random` L2379 → —.  
Pozivaju: index.html:L2381 (F0119); index.html:L2381 (F0119); index.html:L2381 (F0119); index.html:L2382 (F0119); index.html:L2382 (F0119); index.html:L2383 (F0119).

**F0122 · newEgg** — `index.html:L2395–2400` · FunctionDeclaration · parent F0062.  
Ulaz: `id, kind, now, level, random, parents=null, recipe=null`.  
Trag tela: `{ const [min,max]=catalog.durations[kind]; const span=Math.round(min+(max-min)*random())*1000/incubationRate(level); return {id,kind,started`.  
Poziva: `Math.round` L2397 → —; `random` L2397 → —; `incubationRate` L2397 → F0075; `Math.floor` L2398 → —; `Math.floor` L2399 → —.  
Pozivaju: index.html:L2422 (F0126); index.html:L2772 (F0185); index.html:L2943 (F0185); index.html:L2998 (F0185); index.html:L3004 (F0185).

**F0123 · hatchExperience** — `index.html:L2401–2407` · FunctionDeclaration · parent F0062.  
Ulaz: `e, level`.  
Trag tela: `{ const minimum=level<5?0:level<11?1:level<16?2:level<24?3:level<28?4:level<36?5:6; const first=[5,11,16,24,28,36,999,999,999][e.kind]; cons`.  
Poziva: `Number.isInteger` L2404 → —; `Math.round` L2406 → —.  
Pozivaju: index.html:L2803 (F0185); ~index.html:L5692 (F0612); ~index.html:L5820 (F0632).

**F0124 · habitatPrice** — `index.html:L2409–2409` · ArrowFunction · parent F0062.  
Ulaz: `i`.  
Trag tela: `[null,[4,25000],[9,600000],[22,800000],[33,1500000]][i]??null`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2920 (F0185); ~index.html:L4485 (F0377); ~index.html:L5588 (F0581); ~index.html:L5642 (F0604); ~index.html:L5644 (F0604); ~index.html:L5651 (F0604).

**F0125 · upgradePrice** — `index.html:L2410–2416` · FunctionDeclaration · parent F0062.  
Ulaz: `home`.  
Trag tela: `{ if(home.id==='h1'&&home.level===1)return [2,3000,0]; if(home.level===1)return [5,300000,0]; if(home.level===2)return [16,1200000,1]; if(ho`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2931 (F0185); ~index.html:L5583 (F0582); ~index.html:L5665 (F0604).

**F0126 · newGame** — `index.html:L2417–2425` · FunctionDeclaration · parent F0062.  
Ulaz: `now=Date.now(), id=uuid()`.  
Trag tela: `{ return {format:FORMAT,schemaVersion:1,saveId:id,revision:0,lastAt:now,createdAt:now, level:1,xp:0,xpFraction:0,sliz:300000,diamonds:10,tok`.  
Poziva: `Date.now` L2417 → —; `uuid` L2417 → F0110; `newSnail` L2421 → F0119; `newSnail` L2421 → F0119; `newEgg` L2422 → F0122; `makeDaily` L2423 → F0114; `dayKey` L2423 → F0108; `getSeason` L2424 → ~F0030.  
Pozivaju: ~index.html:L5095 (F0464); ~index.html:L5233 (F0486); ~index.html:L7790 (F0924); ~index.html:L8075 (F0943); ~index.html:L8077 (F0943); ~index.html:L8328 (F0975).

**F0127 · callback newEgg** — `index.html:L2422–2422` · ArrowFunction · parent F0126.  
Ulaz: `—`.  
Trag tela: `.5`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0128 · requireThat** — `index.html:L2426–2426` · FunctionDeclaration · parent F0062.  
Ulaz: `ok, message`.  
Trag tela: `{if(!ok)throw Error(message);}`.  
Poziva: `Error` L2426 → —.  
Pozivaju: index.html:L2328 (F0097); index.html:L2427 (F0129); index.html:L2586 (F0154); index.html:L2590 (F0157); index.html:L2591 (F0159); index.html:L2618 (F0169); index.html:L2619 (F0169); index.html:L2621 (F0169); index.html:L2691 (F0185); index.html:L2705 (F0185); index.html:L2707 (F0185); index.html:L2719 (F0185); index.html:L2725 (F0185); index.html:L2728 (F0185); index.html:L2730 (F0185); index.html:L2740 (F0185); index.html:L2742 (F0185); index.html:L2743 (F0185); index.html:L2744 (F0185); index.html:L2746 (F0185); index.html:L2757 (F0185); index.html:L2768 (F0185); index.html:L2769 (F0185); index.html:L2770 (F0185); index.html:L2776 (F0185); index.html:L2784 (F0185); index.html:L2807 (F0185); index.html:L2812 (F0185); index.html:L2813 (F0185); index.html:L2822 (F0185); index.html:L2828 (F0185); index.html:L2830 (F0185); index.html:L2831 (F0185); index.html:L2840 (F0185); index.html:L2842 (F0185); index.html:L2849 (F0185); index.html:L2854 (F0185); index.html:L2855 (F0185); index.html:L2861 (F0185); index.html:L2864 (F0185); index.html:L2868 (F0185); index.html:L2875 (F0185); index.html:L2879 (F0185); index.html:L2882 (F0185); index.html:L2885 (F0185); index.html:L2892 (F0185); index.html:L2896 (F0185); index.html:L2900 (F0185); index.html:L2905 (F0185); index.html:L2907 (F0185); index.html:L2915 (F0185); index.html:L2921 (F0185); index.html:L2923 (F0185); index.html:L2924 (F0185); index.html:L2932 (F0185); index.html:L2937 (F0185); index.html:L2940 (F0185); index.html:L2948 (F0185); index.html:L2950 (F0185); index.html:L2964 (F0185); index.html:L2970 (F0185); index.html:L2983 (F0185); index.html:L2984 (F0185); index.html:L2990 (F0185); index.html:L2995 (F0185); index.html:L3000 (F0185); index.html:L3003 (F0185); index.html:L3009 (F0185); index.html:L3011 (F0185); index.html:L3031 (F0185); index.html:L3039 (F0185); index.html:L3079 (F0185); index.html:L3080 (F0185); index.html:L3081 (F0185); index.html:L3102 (F0185); index.html:L3103 (F0185); index.html:L3108 (F0185); index.html:L3125 (F0185); index.html:L3128 (F0185); index.html:L3134 (F0185); index.html:L3140 (F0185).

**F0129 · pay** — `index.html:L2427–2427` · FunctionDeclaration · parent F0062.  
Ulaz: `s, amount, key='sliz'`.  
Trag tela: `{requireThat(s[key]>=amount,'Nedovoljno resursa.');s[key]-=amount;}`.  
Poziva: `requireThat` L2427 → F0128.  
Pozivaju: index.html:L2577 (F0151); index.html:L2709 (F0185); index.html:L2720 (F0185); index.html:L2771 (F0185); index.html:L2771 (F0185); index.html:L2808 (F0185); index.html:L2823 (F0185); index.html:L2823 (F0185); index.html:L2856 (F0185); index.html:L2880 (F0185); index.html:L2883 (F0185); index.html:L2886 (F0185); index.html:L2887 (F0185); index.html:L2909 (F0185); index.html:L2925 (F0185); index.html:L2933 (F0185); index.html:L2933 (F0185); index.html:L2941 (F0185); index.html:L2942 (F0185); index.html:L2985 (F0185); index.html:L2988 (F0185); index.html:L2991 (F0185); index.html:L3001 (F0185); index.html:L3032 (F0185); index.html:L3135 (F0185).

**F0130 · hit** — `index.html:L2428–2428` · FunctionDeclaration · parent F0062.  
Ulaz: `s, key, n=1`.  
Trag tela: `{s.daily.counts[key]=(s.daily.counts[key]||0)+n;}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2676 (F0181); index.html:L2761 (F0185); index.html:L2780 (F0185); index.html:L2803 (F0185); index.html:L2857 (F0185); index.html:L2943 (F0185); index.html:L2956 (F0185); index.html:L2980 (F0185); index.html:L3027 (F0185); index.html:L3092 (F0185).

**F0131 · addXp** — `index.html:L2430–2443` · FunctionDeclaration · parent F0062.  
Ulaz: `s, amount`.  
Trag tela: `{ if(s.level>=11){ const healing=s.snails.filter(n=>n.trail==='healing'&&!n.busy).length; const bonus=Math.min(.15,.03*healing); const sign=`.  
Poziva: `s.snails.filter` L2432 → —; `Math.min` L2433 → —; `dimensionOf` L2434 → F0073; `xpNeeded` L2438 → F0079; `xpNeeded` L2441 → F0079.  
Pozivaju: index.html:L2555 (F0144); index.html:L2672 (F0181); index.html:L2760 (F0185); index.html:L2803 (F0185); index.html:L2956 (F0185); index.html:L2965 (F0185); index.html:L2980 (F0185); index.html:L3063 (F0185); index.html:L3099 (F0185).

**F0132 · callback s.snails.filter** — `index.html:L2432–2432` · ArrowFunction · parent F0131.  
Ulaz: `n`.  
Trag tela: `n.trail==='healing'&&!n.busy`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0133 · trackDay** — `index.html:L2444–2447` · FunctionDeclaration · parent F0062.  
Ulaz: `now`.  
Trag tela: `{ const seconds=(now/1000)%43200; return seconds<3600?'dawn':seconds<21600?'day':seconds<25200?'dusk':'night'; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2449 (F0134); index.html:L2569 (F0148); index.html:L2984 (F0185).

**F0134 · weatherFor** — `index.html:L2448–2452` · FunctionDeclaration · parent F0062.  
Ulaz: `state, now`.  
Trag tela: `{ const hour=trackDay(now); const condition=state.weather&&state.weather.until>now?catalog.weather[state.weather.id]:null; return {hour,cond`.  
Poziva: `trackDay` L2449 → F0133.  
Pozivaju: index.html:L2460 (F0135); ~index.html:L4616 (F0395); ~index.html:L5440 (F0533); ~index.html:L5762 (F0625); ~index.html:L6088 (F0708); ~index.html:L7137 (F0871).

**F0135 · economyMultiplier** — `index.html:L2458–2505` · FunctionDeclaration · parent F0062.  
Ulaz: `s, snail, now, applyEvents=true`.  
Trag tela: `{ if(s.level<11)return 1; const {hour,condition}=applyEvents?weatherFor(s,now):{hour:null,condition:null}; const weather=condition?.id??(app`.  
Poziva: `weatherFor` L2460 → F0134; `Math.min` L2465 → —; `Math.max` L2466 → —; `NIGHT_SPECIES.has` L2468 → —; `DAY_SPECIES.has` L2469 → —; `condition?.boost.some` L2471 → —; `type.elements.includes` L2473 → —; `Array.from(String(snail.id??'0')).reduce` L2481 → —; `Array.from` L2481 → —; `String` L2481 → —; `Math.floor` L2482 → —; `condition?.hurt.some` L2489 → —; `NIGHT_SPECIES.has` L2490 → —; `DAY_SPECIES.has` L2491 → —; `dimensionOf` L2501 → F0073; `Math.min` L2504 → —; `Math.min` L2504 → —.  
Pozivaju: index.html:L2340 (F0102); index.html:L2511 (F0139); index.html:L3022 (F0206); index.html:L3022 (F0206).

**F0136 · callback condition?.boost.some** — `index.html:L2471–2471` · ArrowFunction · parent F0135.  
Ulaz: `el`.  
Trag tela: `type.elements.includes(el)`.  
Poziva: `type.elements.includes` L2471 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0137 · callback Array.from(String(snail.id??'0')).reduce** — `index.html:L2481–2481` · ArrowFunction · parent F0135.  
Ulaz: `h, c`.  
Trag tela: `(h*31+c.charCodeAt(0))>>>0`.  
Poziva: `c.charCodeAt` L2481 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0138 · callback condition?.hurt.some** — `index.html:L2489–2489` · ArrowFunction · parent F0135.  
Ulaz: `el`.  
Trag tela: `type.elements.includes(el)`.  
Poziva: `type.elements.includes` L2489 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0139 · rate** — `index.html:L2506–2514` · FunctionDeclaration · parent F0062.  
Ulaz: `s, now, applyWeather=true, homeId=null`.  
Trag tela: `{ const homeLevels=new Map(s.homes.map(h=>[h.id,h.level])); let value=0; for(const snail of s.snails){ if(!snail.home||snail.busy||homeId!==`.  
Poziva: `Map` L2507 → —; `s.homes.map` L2507 → —; `homeLevels.get` L2511 → —; `economyMultiplier` L2511 → F0135; `prestigeBoost` L2513 → ~F0055; `tourists` L2513 → F0085.  
Pozivaju: index.html:L2307 (F0081); index.html:L2329 (F0097); index.html:L2354 (F0097); index.html:L2533 (F0142); index.html:L2535 (F0142); index.html:L2535 (F0142); index.html:L2823 (F0185); index.html:L2877 (F0185); index.html:L2891 (F0185); index.html:L2991 (F0185); ~index.html:L5579 (F0580); ~index.html:L5622 (F0599); ~index.html:L5665 (F0604); ~index.html:L5672 (F0604); ~index.html:L5728 (F0621); ~index.html:L5741 (F0623); ~index.html:L5747 (F0624); ~index.html:L5780 (F0627); ~index.html:L6021 (F0689); ~index.html:L6114 (F0711); ~index.html:L7811 (F0933).

**F0140 · callback s.homes.map** — `index.html:L2507–2507` · ArrowFunction · parent F0139.  
Ulaz: `h`.  
Trag tela: `[h.id,h.level]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0141 · silverDiamondChance** — `index.html:L2517–2527` · FunctionDeclaration · parent F0062.  
Ulaz: `s, now`.  
Trag tela: `{ if(s.level<11||dimensionOf(s.level)?.id==='antimatter')return 0; const weather=s.weather?.until>now?s.weather.id:null; let chance=0; for(c`.  
Poziva: `dimensionOf` L2518 → F0073; `Math.min` L2523 → —; `Math.min` L2526 → —.  
Pozivaju: index.html:L2763 (F0185).

**F0142 · reserveAt** — `index.html:L2528–2536` · FunctionDeclaration · parent F0062.  
Ulaz: `s, now`.  
Trag tela: `{ const elapsed=clip(now-s.lastAt,0,DAY); const live=Math.min(elapsed,60000); const cap=reservoirCapacity(s); if(!elapsed||s.reserve>=cap)re`.  
Poziva: `clip` L2529 → F0093; `Math.min` L2530 → —; `reservoirCapacity` L2531 → F0081; `Math.min` L2532 → —; `rate` L2533 → F0139; `clip` L2534 → F0093; `Math.min` L2534 → —; `Math.min` L2535 → —; `rate` L2535 → F0139; `rate` L2535 → F0139.  
Pozivaju: index.html:L2545 (F0144); ~index.html:L4610 (F0394); ~index.html:L5728 (F0621); ~index.html:L7103 (F0871).

**F0143 · startWeather** — `index.html:L2537–2541` · FunctionDeclaration · parent F0062.  
Ulaz: `s, id, now`.  
Trag tela: `{ const duration=catalog.weather[id].dur*1000; s.weather={id,until:now+duration}; s.weatherAt=now+duration+25*60000; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2572 (F0144); index.html:L2986 (F0185).

**F0144 · settle** — `index.html:L2542–2574` · FunctionDeclaration · parent F0062.  
Ulaz: `s, now, random`.  
Trag tela: `{ const effective=Math.max(s.lastAt,now); const elapsed=clip(effective-s.lastAt,0,DAY); s.reserve=reserveAt(s,effective); s.lastAt=effective`.  
Poziva: `Math.max` L2543 → —; `clip` L2544 → F0093; `reserveAt` L2545 → F0142; `dayKey` L2547 → F0108; `makeDaily` L2547 → F0114; `dayKey` L2547 → F0108; `s.snails.filter(n=>!n.busy).reduce` L2551 → —; `s.snails.filter` L2551 → —; `Math.floor` L2553 → —; `addXp` L2555 → F0131; `dimensionOf` L2557 → F0073; `Math.min` L2558 → —; `s.snails.filter` L2558 → —; `Math.min` L2560 → —; `Math.floor` L2560 → —; `releaseExpiredHalf` L2565 → ~F0050; `tickMeteorRain` L2566 → ~F0052; `Object.entries(catalog.weather).filter` L2569 → —; `Object.entries` L2569 → —; `random` L2570 → —; `entries.reduce` L2570 → —; `entries.find` L2571 → —; `startWeather` L2572 → F0143.  
Pozivaju: index.html:L2697 (F0185).

**F0145 · callback s.snails.filter** — `index.html:L2551–2551` · ArrowFunction · parent F0144.  
Ulaz: `n`.  
Trag tela: `!n.busy`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0146 · callback s.snails.filter(n=>!n.busy).reduce** — `index.html:L2551–2551` · ArrowFunction · parent F0144.  
Ulaz: `sum, n`.  
Trag tela: `sum+(n.beauty??0)`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0147 · callback s.snails.filter** — `index.html:L2558–2558` · ArrowFunction · parent F0144.  
Ulaz: `n`.  
Trag tela: `usable(n)&&n.trail==='crystalline'`.  
Poziva: `usable` L2558 → F0094.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0148 · callback Object.entries(catalog.weather).filter** — `index.html:L2569–2569` · ArrowFunction · parent F0144.  
Ulaz: `[,w]`.  
Trag tela: `!w.ph||w.ph.includes(trackDay(effective))`.  
Poziva: `w.ph.includes` L2569 → —; `trackDay` L2569 → F0133.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0149 · callback entries.reduce** — `index.html:L2570–2570` · ArrowFunction · parent F0144.  
Ulaz: `acc, [,w]`.  
Trag tela: `acc+w.w`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0150 · callback entries.find** — `index.html:L2571–2571` · ArrowFunction · parent F0144.  
Ulaz: `[,w]`.  
Trag tela: `(r-=w.w)<0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0151 · queueCosmic** — `index.html:L2575–2580` · FunctionDeclaration · parent F0062.  
Ulaz: `s`.  
Trag tela: `{ const price=craterPrice(s); pay(s,price,'fragments'); s.craterQueue=(s.craterQueue??0)+1; s.craterPrice=nextCraterPrice(s.level); }`.  
Poziva: `craterPrice` L2576 → ~F0043; `pay` L2577 → F0129; `nextCraterPrice` L2579 → ~F0044.  
Pozivaju: index.html:L2993 (F0185); index.html:L2996 (F0185).

**F0152 · freeHome** — `index.html:L2581–2585` · FunctionDeclaration · parent F0062.  
Ulaz: `s`.  
Trag tela: `{ const map={}; for (const snail of s.snails)map[snail.home]=(map[snail.home]||0)+1; return s.homes.find(home=>(map[home.id]||0)<capacity(ho`.  
Poziva: `s.homes.find` L2584 → —.  
Pozivaju: index.html:L2800 (F0185).

**F0153 · callback s.homes.find** — `index.html:L2584–2584` · ArrowFunction · parent F0152.  
Ulaz: `home`.  
Trag tela: `(map[home.id]||0)<capacity(home.level)`.  
Poziva: `capacity` L2584 → F0077.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0154 · findSnail** — `index.html:L2586–2586` · FunctionDeclaration · parent F0062.  
Ulaz: `s, id`.  
Trag tela: `{const n=s.snails.find(v=>v.id===id);requireThat(available(s,n),'Puž je trenutno zauzet ili nedostupan.');return n;}`.  
Poziva: `s.snails.find` L2586 → —; `requireThat` L2586 → F0128; `available` L2586 → F0095.  
Pozivaju: index.html:L2827 (F0185); index.html:L2848 (F0185); index.html:L2853 (F0185); index.html:L2867 (F0185); index.html:L2938 (F0185); index.html:L2938 (F0185); index.html:L2946 (F0185); index.html:L3012 (F0200); index.html:L3082 (F0185); index.html:L3104 (F0220).

**F0155 · callback s.snails.find** — `index.html:L2586–2586` · ArrowFunction · parent F0154.  
Ulaz: `v`.  
Trag tela: `v.id===id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0156 · countLeague** — `index.html:L2587–2589` · FunctionDeclaration · parent F0062.  
Ulaz: `s, won`.  
Trag tela: `{ s.season.matches++;if(won)s.season.wins++; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L2666 (F0181); index.html:L2956 (F0185).

**F0157 · findEgg** — `index.html:L2590–2590` · FunctionDeclaration · parent F0062.  
Ulaz: `s, id`.  
Trag tela: `{const egg=s.eggs.find(e=>e.id===id);requireThat(egg,'Jaje nije pronađeno.');return egg;}`.  
Poziva: `s.eggs.find` L2590 → —; `requireThat` L2590 → F0128.  
Pozivaju: index.html:L2775 (F0185); index.html:L2783 (F0185); index.html:L2807 (F0185); index.html:L2811 (F0185).

**F0158 · callback s.eggs.find** — `index.html:L2590–2590` · ArrowFunction · parent F0157.  
Ulaz: `e`.  
Trag tela: `e.id===id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0159 · checkBuilding** — `index.html:L2591–2591` · FunctionDeclaration · parent F0062.  
Ulaz: `s, id`.  
Trag tela: `{requireThat(s.built.includes(id),'Prvo izgradi objekat.');}`.  
Poziva: `requireThat` L2591 → F0128; `s.built.includes` L2591 → —.  
Pozivaju: index.html:L2936 (F0185); index.html:L2946 (F0185); index.html:L2993 (F0185); index.html:L2995 (F0185); index.html:L3007 (F0185); index.html:L3076 (F0185); index.html:L3102 (F0185).

**F0160 · pickSpecies** — `index.html:L2592–2601` · FunctionDeclaration · parent F0062.  
Ulaz: `s, kind, random`.  
Trag tela: `{ let pool=species.filter(n=>n.cls===kind&&n.level<=s.level&&!n.special); if(!pool.length)pool=species.filter(n=>n.cls===Math.max(1,kind)&&!`.  
Poziva: `species.filter` L2593 → —; `species.filter` L2594 → —; `species.filter` L2595 → —; `pool.map` L2598 → —; `random` L2599 → —; `weights.reduce` L2599 → —; `pool.find` L2600 → —.  
Pozivaju: index.html:L2785 (F0185).

**F0161 · callback species.filter** — `index.html:L2593–2593` · ArrowFunction · parent F0160.  
Ulaz: `n`.  
Trag tela: `n.cls===kind&&n.level<=s.level&&!n.special`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0162 · callback species.filter** — `index.html:L2594–2594` · ArrowFunction · parent F0160.  
Ulaz: `n`.  
Trag tela: `n.cls===Math.max(1,kind)&&!n.special`.  
Poziva: `Math.max` L2594 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0163 · callback species.filter** — `index.html:L2595–2595` · ArrowFunction · parent F0160.  
Ulaz: `n`.  
Trag tela: `n.cls===1&&n.level<=s.level`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0164 · callback pool.map** — `index.html:L2598–2598` · ArrowFunction · parent F0160.  
Ulaz: `n`.  
Trag tela: `(s.seen.includes(n.id)?1:2)/(1+(owned[n.id]||0))**2`.  
Poziva: `s.seen.includes` L2598 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0165 · callback weights.reduce** — `index.html:L2599–2599` · ArrowFunction · parent F0160.  
Ulaz: `a, b`.  
Trag tela: `a+b`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0166 · callback pool.find** — `index.html:L2600–2600` · ArrowFunction · parent F0160.  
Ulaz: `_, i`.  
Trag tela: `(selection-=weights[i])<0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0167 · breedPlan** — `index.html:L2602–2611` · FunctionDeclaration · parent F0062.  
Ulaz: `s, a, b`.  
Trag tela: `{ if(!available(s,a)||!available(s,b)||a.id===b.id)return null; const recipe=Object.entries(catalog.recipes).find(([,pair])=>pair[0]!==pair[`.  
Poziva: `available` L2603 → F0095; `available` L2603 → F0095; `Object.entries(catalog.recipes).find` L2604 → —; `Object.entries` L2604 → —; `clip` L2606 → F0093; `Math.round` L2606 → —; `Math.round` L2608 → —; `s.built.includes` L2609 → —; `craterUsed` L2609 → F0091; `incubatorUsed` L2609 → F0089; `eggCapacity` L2609 → F0088.  
Pozivaju: index.html:L2939 (F0185); ~index.html:L5975 (F0676).

**F0168 · callback Object.entries(catalog.recipes).find** — `index.html:L2604–2604` · ArrowFunction · parent F0167.  
Ulaz: `[,pair]`.  
Trag tela: `pair[0]!==pair[1]&&pair.includes(a.species)&&pair.includes(b.species)`.  
Poziva: `pair.includes` L2604 → —; `pair.includes` L2604 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0169 · battleTurn** — `index.html:L2615–2659` · FunctionDeclaration · parent F0062.  
Ulaz: `duel, action, target`.  
Trag tela: `{ const actor=duel.team.slice(duel.round%duel.team.length).concat(duel.team.slice(0,duel.round%duel.team.length)).find(n=>n.hp>0); const ene`.  
Poziva: `duel.team.slice(duel.round%duel.team.length).concat(duel.team.slice(0,duel.round%duel.team.length)).find` L2616 → —; `duel.team.slice(duel.round%duel.team.length).concat` L2616 → —; `duel.team.slice` L2616 → —; `duel.team.slice` L2616 → —; `duel.foes.find` L2617 → —; `duel.foes.find` L2617 → —; `requireThat` L2618 → F0128; `requireThat` L2619 → F0128; `['attack','guard','trail'].includes` L2619 → —; `requireThat` L2621 → F0128; `Math.min` L2624 → —; `Math.min` L2626 → —; `duel.team.filter(n=>n.hp>0).sort` L2629 → —; `duel.team.filter` L2629 → —; `Math.max` L2630 → —; `Math.round` L2630 → —; `Math.min` L2630 → —; `Math.max` L2633 → —; `Math.round` L2633 → —; `Math.max` L2634 → —; `Math.round` L2634 → —; `Math.max` L2635 → —; `Math.max` L2637 → —; `Math.round` L2637 → —; `Math.min` L2638 → —; `duel.foes.find` L2642 → —; `Math.max` L2644 → —; `Math.round` L2644 → —; `Math.max` L2645 → —; `Math.max` L2646 → —; `duel.foes.some` L2650 → —; `duel.team.some` L2651 → —; `share` L2655 → F0178; `share` L2655 → F0178.  
Pozivaju: index.html:L2686 (F0183); index.html:L3129 (F0185).

**F0170 · callback duel.team.slice(duel.round%duel.team.length).concat(duel.team.slice(0,duel.round%duel.team.length)).find** — `index.html:L2616–2616` · ArrowFunction · parent F0169.  
Ulaz: `n`.  
Trag tela: `n.hp>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0171 · callback duel.foes.find** — `index.html:L2617–2617` · ArrowFunction · parent F0169.  
Ulaz: `n`.  
Trag tela: `n.id===target&&n.hp>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0172 · callback duel.foes.find** — `index.html:L2617–2617` · ArrowFunction · parent F0169.  
Ulaz: `n`.  
Trag tela: `n.hp>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0173 · callback duel.team.filter** — `index.html:L2629–2629` · ArrowFunction · parent F0169.  
Ulaz: `n`.  
Trag tela: `n.hp>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0174 · callback duel.team.filter(n=>n.hp>0).sort** — `index.html:L2629–2629` · ArrowFunction · parent F0169.  
Ulaz: `a, b`.  
Trag tela: `a.hp/a.maxHp-b.hp/b.maxHp`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0175 · callback duel.foes.find** — `index.html:L2642–2642` · ArrowFunction · parent F0169.  
Ulaz: `n`.  
Trag tela: `n.hp>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0176 · callback duel.foes.some** — `index.html:L2650–2650` · ArrowFunction · parent F0169.  
Ulaz: `n`.  
Trag tela: `n.hp>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0177 · callback duel.team.some** — `index.html:L2651–2651` · ArrowFunction · parent F0169.  
Ulaz: `n`.  
Trag tela: `n.hp>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0178 · share** — `index.html:L2653–2654` · ArrowFunction · parent F0169.  
Ulaz: `team`.  
Trag tela: `team.reduce((sum,n)=>sum+Math.max(0,n.hp),0)/ Math.max(1,team.reduce((sum,n)=>sum+n.maxHp,0))`.  
Poziva: `team.reduce` L2653 → —; `Math.max` L2654 → —; `team.reduce` L2654 → —.  
Pozivaju: index.html:L2655 (F0169); index.html:L2655 (F0169).

**F0179 · callback team.reduce** — `index.html:L2653–2653` · ArrowFunction · parent F0178.  
Ulaz: `sum, n`.  
Trag tela: `sum+Math.max(0,n.hp)`.  
Poziva: `Math.max` L2653 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0180 · callback team.reduce** — `index.html:L2654–2654` · ArrowFunction · parent F0178.  
Ulaz: `sum, n`.  
Trag tela: `sum+n.maxHp`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0181 · settleArenaResult** — `index.html:L2661–2680` · FunctionDeclaration · parent F0062.  
Ulaz: `s`.  
Trag tela: `{ const won=s.arena.done==='win'; const eligible=s.daily.arena<ARENA_REWARD_LIMIT; const result={eligible,sliz:0,xp:0,diamonds:0,trophies:0}`.  
Poziva: `countLeague` L2666 → F0156; `Math.round` L2667 → —; `leagueOf` L2667 → ~F0028; `Math.max` L2668 → —; `Math.round` L2668 → —; `baseXp` L2668 → F0078; `Math.max` L2668 → —; `Math.round` L2668 → —; `baseXp` L2668 → F0078; `creditDiamonds` L2669 → ~F0047; `Math.max` L2670 → —; `addXp` L2672 → F0131; `Set` L2674 → —; `s.arena.team.map` L2674 → —; `members.has` L2675 → —; `hit` L2676 → F0130; `creditWeekly` L2676 → ~F0033.  
Pozivaju: index.html:L2688 (F0183); index.html:L3129 (F0185).

**F0182 · callback s.arena.team.map** — `index.html:L2674–2674` · ArrowFunction · parent F0181.  
Ulaz: `member`.  
Trag tela: `member.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0183 · playAutomaticTurns** — `index.html:L2681–2689` · FunctionDeclaration · parent F0062.  
Ulaz: `s`.  
Trag tela: `{ // Bounded batches keep very high-HP imported teams responsive. for(let turn=0;turn<ARENA_MAX_ROUNDS&&!s.arena.done;turn++){ const members`.  
Poziva: `members.slice(offset).concat(members.slice(0,offset)).find` L2685 → —; `members.slice(offset).concat` L2685 → —; `members.slice` L2685 → —; `members.slice` L2685 → —; `battleTurn` L2686 → F0169; `settleArenaResult` L2688 → F0181.  
Pozivaju: index.html:L3121 (F0185); index.html:L3126 (F0185).

**F0184 · callback members.slice(offset).concat(members.slice(0,offset)).find** — `index.html:L2685–2685` · ArrowFunction · parent F0183.  
Ulaz: `n`.  
Trag tela: `n.hp>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0185 · applyCommand** — `index.html:L2690–3170` · FunctionDeclaration · parent F0062.  
Ulaz: `current, cmd, now=Date.now(), random=Math.random`.  
Trag tela: `{ requireThat(current&&Number.isFinite(now)&&idOk(cmd.id),'Komanda nije validna.'); if(current.completed.includes(cmd.id))return {state:curr`.  
Poziva: `Date.now` L2690 → —; `requireThat` L2691 → F0128; `Number.isFinite` L2691 → —; `idOk` L2691 → F0109; `current.completed.includes` L2692 → —; `current.completed.includes` L2693 → —; `structuredClone` L2694 → —; `Math.max` L2695 → —; `getSeason` L2696 → ~F0030; `settle` L2697 → F0144; `queueReturnGift` L2698 → ~F0060; `modules.scenes.prepareIsland` L2699 → ~F0370; `requireThat` L2705 → F0128; `Number.isInteger` L2705 → —; `wheatBuilt` L2706 → F0065; `requireThat` L2707 → F0128; `modules.scenes.canPlace` L2707 → ~F0381; `pay` L2709 → F0129; `wheatKey` L2711 → F0064; `requireThat` L2719 → F0128; `pay` L2720 → F0129; `requireThat` L2725 → F0128; `WHEAT_FIELDS.map((gate,i)=>({gate,i})).filter` L2726 → —; `WHEAT_FIELDS.map` L2726 → —; `requireThat` L2728 → F0128; `wheatYield` L2729 → F0063; `requireThat` L2730 → F0128; `requireThat` L2740 → F0128; `requireThat` L2742 → F0128; `Number.isInteger` L2742 → —; `requireThat` L2743 → F0128; `wheatBuilt` L2743 → F0065; `wheatKey` L2743 → F0064; `requireThat` L2744 → F0128; `wheatStage` L2744 → F0067; `wheatYield` L2745 → F0063; `requireThat` L2746 → F0128; `Math.floor` L2756 → —; `requireThat` L2757 → F0128; `Math.max` L2758 → —; `reservoirCapacity` L2758 → F0081; `Math.max` L2759 → —; `Math.round` L2759 → —; `baseXp` L2759 → F0078; `addXp` L2760 → F0131; `hit` L2761 → F0130; `random` L2763 → —; `silverDiamondChance` L2763 → F0141; `creditDiamonds` L2763 → ~F0047; `requireThat` L2768 → F0128; `Number.isInteger` L2768 → —; `requireThat` L2769 → F0128; `incubatorUsed` L2769 → F0089; `eggCapacity` L2769 → F0088; `requireThat` L2770 → F0128; `pay` L2771 → F0129; `pay` L2771 → F0129; `s.eggs.push` L2772 → —; `newEgg` L2772 → F0122; `findEgg` L2775 → F0157; `requireThat` L2776 → F0128; `canCare` L2776 → ~F0049; `accelerateEgg` L2778 → ~F0051; `creditDiamonds` L2779 → ~F0047; `hit` L2780 → F0130; `findEgg` L2783 → F0157; `requireThat` L2784 → F0128; `pickSpecies` L2785 → F0160; `newSnail` L2786 → F0119; `Number.isInteger` L2787 → —; `String` L2788 → —; `e.parents.map` L2789 → —; `e.parents.map` L2791 → —; `((a+b)*(.47+.12*random())).toFixed` L2792 → —; `random` L2792 → —; `Math.max` L2793 → —; `e.parents.slice().sort` L2795 → —; `e.parents.slice` L2795 → —; `(snail[key]*1.15).toFixed` L2798 → —; `(snail.prod*1.05).toFixed` L2799 → —; `freeHome` L2800 → F0152; `s.snails.push` L2800 → —; `s.eggs.filter` L2801 → —; `s.seen.includes` L2802 → —; `s.seen.push` L2802 → —; `hit` L2803 → F0130; `addXp` L2803 → F0131; `hatchExperience` L2803 → F0123; `snailName` L2804 → F0107; `findEgg` L2807 → F0157; `requireThat` L2807 → F0128; `pay` L2808 → F0129; `accelerateEgg` L2808 → ~F0051; `findEgg` L2811 → F0157; `requireThat` L2812 → F0128; `requireThat` L2813 → F0128; `accelerateEgg` L2815 → ~F0051; `canCare` L2816 → ~F0049; `Boolean` L2819 → —; `requireThat` L2822 → F0128; `pay` L2823 → F0129; `pay` L2823 → F0129; `timeBreakCost` L2823 → ~F0042; `rate` L2823 → F0139; `findSnail` L2827 → F0154; `requireThat` L2828 → F0128; `available` L2828 → F0095; `s.homes.find` L2829 → —; `requireThat` L2830 → F0128; `Boolean` L2830 → —; `requireThat` L2831 → F0128; `s.snails.filter` L2831 → —; `capacity` L2831 → F0077; `assignBestHomes` L2837 → F0097; `requireThat` L2840 → F0128; `requireThat` L2842 → F0128; `AUTO_HOME_STATS.includes` L2842 → —; `assignBestHomes` L2844 → F0097; `s.snails.filter` L2844 → —; `findSnail` L2848 → F0154; `requireThat` L2849 → F0128; `cmd.name.trim` L2849 → —; `cmd.name.trim` L2850 → —; `findSnail` L2853 → F0154; `upgradeInfo` L2853 → ~F0037; `requireThat` L2854 → F0128; `requireThat` L2855 → F0128; `pay` L2856 → F0129; `improveSnail` L2856 → ~F0039; `hit` L2857 → F0130; `creditWeekly` L2857 → ~F0033; `requireThat` L2861 → F0128; `cmd.name.trim` L2861 → —; `cmd.name.trim` L2862 → —; `requireThat` L2864 → F0128; `s.seen.includes` L2864 → —; `findSnail` L2867 → F0154; `requireThat` L2868 → F0128; `Math.round` L2869 → —; `Math.min` L2869 → —; `Math.min` L2869 → —; `s.snails.filter` L2870 → —; `creditMuseum` L2871 → ~F0061; `snailName` L2871 → F0107; `requireThat` L2875 → F0128; `Object.hasOwn` L2875 → —; `packAmount` L2877 → ~F0035; `rate` L2877 → F0139; `key.startsWith` L2878 → —; `requireThat` L2879 → F0128; `pay` L2880 → F0129; `key.startsWith` L2881 → —; `requireThat` L2882 → F0128; `pay` L2883 → F0129; `requireThat` L2885 → F0128; `pay` L2886 → F0129; `pay` L2887 → F0129; `getLogin` L2891 → ~F0058; `rate` L2891 → F0139; `requireThat` L2892 → F0128; `creditLogin` L2893 → ~F0059; `requireThat` L2896 → F0128; `previousReward` L2899 → ~F0029; `requireThat` L2900 → F0128; `requireThat` L2905 → F0128; `s.built.includes` L2905 → —; `requireThat` L2907 → F0128; `modules.scenes.canPlace` L2907 → ~F0381; `pay` L2909 → F0129; `s.built.push` L2910 → —; `requireThat` L2915 → F0128; `modules.scenes.canPlace` L2915 → ~F0381; `habitatPrice` L2920 → F0124; `requireThat` L2921 → F0128; `Number` L2922 → —; `requireThat` L2923 → F0128; `Number.isInteger` L2923 → —; `s.homes.some` L2923 → —; `requireThat` L2924 → F0128; `modules.scenes.canPlace` L2924 → ~F0381; `pay` L2925 → F0129; `s.homes.push` L2925 → —; `s.homes.find` L2930 → —; `upgradePrice` L2931 → F0125; `requireThat` L2932 → F0128; `pay` L2933 → F0129; `pay` L2933 → F0129; `checkBuilding` L2936 → F0159; `requireThat` L2937 → F0128; `findSnail` L2938 → F0154; `findSnail` L2938 → F0154; `breedPlan` L2939 → F0167; `requireThat` L2940 → F0128; `pay` L2941 → F0129; `pay` L2942 → F0129; `s.eggs.push` L2943 → —; `newEgg` L2943 → F0122; `hit` L2943 → F0130; `checkBuilding` L2946 → F0159; `findSnail` L2946 → F0154; `requireThat` L2948 → F0128; `idOk` L2948 → F0109; `Number.isInteger` L2948 → —; `Number.isFinite` L2948 → —; `s.completed.push` L2949 → —; `requireThat` L2950 → F0128; `leagueOf` L2953 → ~F0028; `Math.round` L2954 → —; `Math.max` L2955 → —; `Math.round` L2955 → —; `baseXp` L2955 → F0078; `hit` L2956 → F0130; `countLeague` L2956 → F0156; `Math.max` L2956 → —; `addXp` L2956 → F0131; `creditWeekly` L2957 → ~F0033; `dailyDefs.find` L2963 → —; `requireThat` L2964 → F0128; `s.daily.keys.includes` L2964 → —; `s.daily.claimed.includes` L2964 → —; `s.daily.claimed.push` L2965 → —; `creditDiamonds` L2965 → ~F0047; `addXp` L2965 → F0131; `Math.max` L2965 → —; `Math.round` L2965 → —; `baseXp` L2965 → F0078; `nextMeteor` L2969 → ~F0053; `requireThat` L2970 → F0128; `Math.min` L2975 → —; `s.snails.filter` L2975 → —; `dimensionOf` L2976 → F0073; `Math.max` L2977 → —; `Math.floor` L2977 → —; `random` L2977 → —; `creditDiamonds` L2979 → ~F0047; `addXp` L2980 → F0131; `hit` L2980 → F0130; `requireThat` L2983 → F0128; `requireThat` L2984 → F0128; `summonChoices(trackDay(effective)).includes` L2984 → —; `summonChoices` L2984 → ~F0045; `trackDay` L2984 → F0133; `pay` L2985 → F0129; `startWeather` L2986 → F0143; `pay` L2988 → F0129; `requireThat` L2990 → F0128; `pay` L2991 → F0129; `cosmicTradeCost` L2991 → ~F0032; `rate` L2991 → F0139; `checkBuilding` L2993 → F0159; `queueCosmic` L2993 → F0151; `checkBuilding` L2995 → F0159; `requireThat` L2995 → F0128; `craterUsed` L2995 → F0091; `queueCosmic` L2996 → F0151; `s.eggs.push` L2998 → —; `newEgg` L2998 → F0122; `requireThat` L3000 → F0128; `pay` L3001 → F0129; `requireThat` L3003 → F0128; `incubatorUsed` L3003 → F0089; `eggCapacity` L3003 → F0088; `s.eggs.push` L3004 → —; `newEgg` L3004 → F0122; `creditDiamonds` L3004 → ~F0047; `checkBuilding` L3007 → F0159; `requireThat` L3009 → F0128; `requireThat` L3011 → F0128; `Array.isArray` L3011 → —; `Set` L3011 → —; `ids.map` L3012 → —; `team.map` L3015 → —; `team.forEach` L3016 → —; `s.homes.find` L3019 → —; `s.snails.filter` L3020 → —; `capacity` L3020 → F0077; `s.snails.filter(n=>available(s,n)&&!n.home) .sort` L3021 → —; `s.snails.filter` L3021 → —; `s.expeditions.push` L3025 → —; `hit` L3027 → F0130; `s.expeditions.find` L3030 → —; `requireThat` L3031 → F0128; `pay` L3032 → F0129; `Math.min` L3033 → —; `s.expeditions.find` L3038 → —; `requireThat` L3039 → F0128; `expeditionTeam(exp).map` L3040 → —; `expeditionTeam` L3040 → F0076; `s.snails.find` L3047 → —; `s.homes.find` L3048 → —; `s.snails.find` L3050 → —; `s.snails.filter` L3052 → —; `capacity` L3052 → F0077; `expeditionSliz` L3059 → F0070; `team.reduce` L3059 → —; `team.reduce` L3059 → —; `Math.max` L3061 → —; `Math.min` L3061 → —; `addXp` L3063 → F0131; `Math.round` L3063 → —; `Math.max` L3063 → —; `creditWeekly` L3068 → ~F0033; `random` L3069 → —; `s.expeditions.filter` L3072 → —; `checkBuilding` L3076 → F0159; `requireThat` L3079 → F0128; `requireThat` L3080 → F0128; `requireThat` L3081 → F0128; `findSnail` L3082 → F0154; `Math.round` L3085 → —; `random` L3085 → —; `showReference` L3086 → ~F0056; `Array.from` L3087 → —; `opponents.filter` L3088 → —; `creditDiamonds` L3091 → ~F0047; `hit` L3092 → F0130; `creditPrestige` L3096 → ~F0054; `addXp` L3099 → F0131; `checkBuilding` L3102 → F0159; `requireThat` L3102 → F0128; `requireThat` L3103 → F0128; `Array.isArray` L3103 → —; `Set` L3103 → —; `cmd.team.map` L3104 → —; `s.snails.filter(n=>usable(n)&&!cmd.team.includes(n.id)).sort` L3106 → —; `s.snails.filter` L3106 → —; `picked.concat` L3107 → —; `remaining.slice` L3107 → —; `requireThat` L3108 → F0128; `dimensionOf` L3109 → F0073; `members.map(n=>[n,random()]).sort((a,b)=>a[1]-b[1]).map` L3110 → —; `members.map(n=>[n,random()]).sort` L3110 → —; `members.map` L3110 → —; `members.sort` L3111 → —; `ordered.map` L3112 → —; `team.map` L3115 → —; `Math.min` L3119 → —; `playAutomaticTurns` L3121 → F0183; `requireThat` L3125 → F0128; `playAutomaticTurns` L3126 → F0183; `requireThat` L3128 → F0128; `['attack','guard','trail'].includes` L3128 → —; `battleTurn` L3129 → F0169; `settleArenaResult` L3129 → F0181; `requireThat` L3134 → F0128; `masteryOpen` L3134 → F0083; `pay` L3135 → F0129; `requireThat` L3140 → F0128; `Error` L3141 → —; `Math.round` L3144 → —; `incubationRate` L3145 → F0075; `incubationRate` L3145 → F0075; `Math.round` L3149 → —; `AUTO_HOME_REBALANCE.has` L3161 → —; `assignBestHomes` L3161 → F0097; `Number.isFinite` L3163 → —; `Math.max` L3164 → —; `Math.min` L3164 → —; `Math.floor` L3164 → —; `s.completed.push` L3165 → —; `s.completed.slice` L3166 → —; `modules.scenes.prepareIsland` L3168 → ~F0370.  
Pozivaju: ~index.html:L7171 (F0876).

**F0186 · callback WHEAT_FIELDS.map** — `index.html:L2726–2726` · ArrowFunction · parent F0185.  
Ulaz: `gate, i`.  
Trag tela: `({gate,i})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0187 · callback WHEAT_FIELDS.map((gate,i)=>({gate,i})).filter** — `index.html:L2726–2727` · ArrowFunction · parent F0185.  
Ulaz: `{gate,i}`.  
Trag tela: `s.level>=gate&&wheatBuilt(s,i)&&Boolean(s.islandPositions[wheatKey(i)])&&wheatStage(s,effective,i)==='ripe'`.  
Poziva: `wheatBuilt` L2727 → F0065; `Boolean` L2727 → —; `wheatKey` L2727 → F0064; `wheatStage` L2727 → F0067.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0188 · callback e.parents.map** — `index.html:L2789–2789` · ArrowFunction · parent F0185.  
Ulaz: `p`.  
Trag tela: `p.species`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0189 · callback e.parents.map** — `index.html:L2791–2791` · ArrowFunction · parent F0185.  
Ulaz: `parent`.  
Trag tela: `inheritedStat(parent,key)`.  
Poziva: `inheritedStat` L2791 → ~F0038.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0190 · callback e.parents.slice().sort** — `index.html:L2795–2795` · ArrowFunction · parent F0185.  
Ulaz: `a, b`.  
Trag tela: `b.beauty-a.beauty`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0191 · callback s.eggs.filter** — `index.html:L2801–2801` · ArrowFunction · parent F0185.  
Ulaz: `v`.  
Trag tela: `v.id!==e.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0192 · callback s.homes.find** — `index.html:L2829–2829` · ArrowFunction · parent F0185.  
Ulaz: `h`.  
Trag tela: `h.id===cmd.home`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0193 · callback s.snails.filter** — `index.html:L2831–2831` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `n.home===home.id&&n.id!==snail.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0194 · callback s.snails.filter** — `index.html:L2844–2844` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `n.home&&!n.busy`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0195 · callback s.snails.filter** — `index.html:L2870–2870` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `n.id!==snail.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0196 · callback s.homes.some** — `index.html:L2923–2923` · ArrowFunction · parent F0185.  
Ulaz: `h`.  
Trag tela: `h.slot===slot`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0197 · callback s.homes.find** — `index.html:L2930–2930` · ArrowFunction · parent F0185.  
Ulaz: `v`.  
Trag tela: `v.id===cmd.home`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0198 · callback dailyDefs.find** — `index.html:L2963–2963` · ArrowFunction · parent F0185.  
Ulaz: `item`.  
Trag tela: `item[0]===cmd.goal`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0199 · callback s.snails.filter** — `index.html:L2975–2975` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `n.trail==='starry'&&!n.busy`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0200 · callback ids.map** — `index.html:L3012–3012` · ArrowFunction · parent F0185.  
Ulaz: `snail`.  
Trag tela: `findSnail(s,snail)`.  
Poziva: `findSnail` L3012 → F0154.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0201 · callback team.map** — `index.html:L3015–3015` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `({snailId:n.id,homeId:n.home??null,substituteId:null})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0202 · callback team.forEach** — `index.html:L3016–3016` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `{n.busy=id;n.home=null;}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0203 · callback s.homes.find** — `index.html:L3019–3019` · ArrowFunction · parent F0185.  
Ulaz: `h`.  
Trag tela: `h.id===slot.homeId`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0204 · callback s.snails.filter** — `index.html:L3020–3020` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `n.home===home.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0205 · callback s.snails.filter** — `index.html:L3021–3021` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `available(s,n)&&!n.home`.  
Poziva: `available` L3021 → F0095.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0206 · callback s.snails.filter(n=>available(s,n)&&!n.home) .sort** — `index.html:L3022–3022` · ArrowFunction · parent F0185.  
Ulaz: `a, b`.  
Trag tela: `b.prod*economyMultiplier(s,b,effective)-a.prod*economyMultiplier(s,a,effective)||a.id.localeCompare(b.id)`.  
Poziva: `economyMultiplier` L3022 → F0135; `economyMultiplier` L3022 → F0135; `a.id.localeCompare` L3022 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0207 · callback s.expeditions.find** — `index.html:L3030–3030` · ArrowFunction · parent F0185.  
Ulaz: `x`.  
Trag tela: `x.id===cmd.expedition`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0208 · callback s.expeditions.find** — `index.html:L3038–3038` · ArrowFunction · parent F0185.  
Ulaz: `x`.  
Trag tela: `x.id===cmd.expedition`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0209 · callback expeditionTeam(exp).map** — `index.html:L3040–3040` · ArrowFunction · parent F0185.  
Ulaz: `member`.  
Trag tela: `s.snails.find(n=>n.id===member)`.  
Poziva: `s.snails.find` L3040 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0210 · callback s.snails.find** — `index.html:L3040–3040` · ArrowFunction · parent F0209.  
Ulaz: `n`.  
Trag tela: `n.id===member`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0211 · callback s.snails.find** — `index.html:L3047–3047` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `n.id===slot.snailId`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0212 · callback s.homes.find** — `index.html:L3048–3048` · ArrowFunction · parent F0185.  
Ulaz: `h`.  
Trag tela: `h.id===slot.homeId`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0213 · callback s.snails.find** — `index.html:L3050–3050` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `n.id===slot.substituteId&&n.home===home.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0214 · callback s.snails.filter** — `index.html:L3052–3052` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `n.home===home.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0215 · callback team.reduce** — `index.html:L3059–3059` · ArrowFunction · parent F0185.  
Ulaz: `sum, n`.  
Trag tela: `sum+snailPower(n)`.  
Poziva: `snailPower` L3059 → F0069.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0216 · callback team.reduce** — `index.html:L3059–3059` · ArrowFunction · parent F0185.  
Ulaz: `sum, n`.  
Trag tela: `sum+n.prod`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0217 · callback s.expeditions.filter** — `index.html:L3072–3072` · ArrowFunction · parent F0185.  
Ulaz: `v`.  
Trag tela: `v.id!==exp.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0218 · callback Array.from** — `index.html:L3087–3087` · ArrowFunction · parent F0185.  
Ulaz: `—`.  
Trag tela: `Math.round(base*((cosmic?1.05:.95)+random()*.40))`.  
Poziva: `Math.round` L3087 → —; `random` L3087 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0219 · callback opponents.filter** — `index.html:L3088–3088` · ArrowFunction · parent F0185.  
Ulaz: `v`.  
Trag tela: `v>score`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0220 · callback cmd.team.map** — `index.html:L3104–3104` · ArrowFunction · parent F0185.  
Ulaz: `member`.  
Trag tela: `findSnail(s,member)`.  
Poziva: `findSnail` L3104 → F0154.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0221 · power** — `index.html:L3105–3105` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `n.atk*3+n.hp+n.speed*2`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L3106 (F0223); index.html:L3106 (F0223).

**F0222 · callback s.snails.filter** — `index.html:L3106–3106` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `usable(n)&&!cmd.team.includes(n.id)`.  
Poziva: `usable` L3106 → F0094; `cmd.team.includes` L3106 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0223 · callback s.snails.filter(n=>usable(n)&&!cmd.team.includes(n.id)).sort** — `index.html:L3106–3106` · ArrowFunction · parent F0185.  
Ulaz: `a, b`.  
Trag tela: `power(b)-power(a)`.  
Poziva: `power` L3106 → F0221; `power` L3106 → F0221.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0224 · callback members.map** — `index.html:L3110–3110` · ArrowFunction · parent F0185.  
Ulaz: `n`.  
Trag tela: `[n,random()]`.  
Poziva: `random` L3110 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0225 · callback members.map(n=>[n,random()]).sort** — `index.html:L3110–3110` · ArrowFunction · parent F0185.  
Ulaz: `a, b`.  
Trag tela: `a[1]-b[1]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0226 · callback members.map(n=>[n,random()]).sort((a,b)=>a[1]-b[1]).map** — `index.html:L3110–3110` · ArrowFunction · parent F0185.  
Ulaz: `[n]`.  
Trag tela: `n`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0227 · callback members.sort** — `index.html:L3111–3111` · ArrowFunction · parent F0185.  
Ulaz: `a, b`.  
Trag tela: `dimension==='antimatter'?a.speed-b.speed:b.speed-a.speed`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0228 · callback ordered.map** — `index.html:L3112–3113` · ArrowFunction · parent F0185.  
Ulaz: `v`.  
Trag tela: `({id:v.id, name:snailName(v),hp:v.hp,maxHp:v.hp,atk:v.atk,trail:v.trail,species:v.species,weight:v.weight,infusion:v.infusion??0,energy:0})`.  
Poziva: `snailName` L3113 → F0107.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0229 · callback team.map** — `index.html:L3115–3118` · ArrowFunction · parent F0185.  
Ulaz: `v, i`.  
Trag tela: `({...v,id:'rival-'+i,name:'Rival '+(i+1), atk:Math.max(1,Math.round(v.atk*(.96+random()*.08))), hp:Math.max(1,Math.round(v.hp*(.96+random()*`.  
Poziva: `Math.max` L3116 → —; `Math.round` L3116 → —; `random` L3116 → —; `Math.max` L3117 → —; `Math.round` L3117 → —; `random` L3117 → —; `Math.max` L3118 → —; `Math.round` L3118 → —; `random` L3118 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### frames — atlas frejmovi

**F0230 · anonimna** — `index.html:L3176–3180` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const frames = {"island":{"island":[0.0013020833333333333,0.0013020833333333333,0.81640625,0.81640625,1],"sky-day":[0.0013020833333333333,`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### physics — fizika

**F0231 · anonimna** — `index.html:L3181–3278` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ // Collision and motion rules reused from the supplied v174.103 race-physics module. 'use strict'; const LANE_W=3.90, RADIUS=1.86, MAX_STE`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0232 · clamp** — `index.html:L3185–3185` · ArrowFunction · parent F0231.  
Ulaz: `v, a, b`.  
Trag tela: `Math.max(a,Math.min(b,v))`.  
Poziva: `Math.max` L3185 → —; `Math.min` L3185 → —.  
Pozivaju: index.html:L3186 (F0233); index.html:L3191 (F0235); index.html:L3195 (F0235); index.html:L3196 (F0235); index.html:L3201 (F0235); index.html:L3204 (F0235); index.html:L3214 (F0235); index.html:L3242 (F0235); index.html:L3242 (F0235); index.html:L3248 (F0235); index.html:L3253 (F0235); index.html:L3253 (F0235); index.html:L3254 (F0235); index.html:L3258 (F0235); index.html:L3258 (F0235); index.html:L3260 (F0235).

**F0233 · mass** — `index.html:L3186–3186` · ArrowFunction · parent F0231.  
Ulaz: `p`.  
Trag tela: `clamp(3+Number(p.wt||10)*0.85,4,105)`.  
Poziva: `clamp` L3186 → F0232; `Number` L3186 → —.  
Pozivaju: index.html:L3235 (F0235); index.html:L3235 (F0235); index.html:L3247 (F0235); index.html:L3247 (F0235); index.html:L3256 (F0235).

**F0234 · pairs** — `index.html:L3187–3187` · ArrowFunction · parent F0231.  
Ulaz: `ps`.  
Trag tela: `{const all=[];for(let i=0;i<ps.length;i++)for(let j=i+1;j<ps.length;j++)all.push([i,j]);return all;}`.  
Poziva: `all.push` L3187 → —.  
Pozivaju: index.html:L3219 (F0235).

**F0235 · integrate** — `index.html:L3188–3269` · FunctionDeclaration · parent F0231.  
Ulaz: `rs, dt, onImpact`.  
Trag tela: `{ const ps=rs.players,gravity=rs.g||EARTH_G,contact=rs.contacts||(rs.contacts=new Set()),cooldowns=rs.cooldowns||(rs.cooldowns=new Map()); c`.  
Poziva: `Set` L3189 → —; `Map` L3189 → —; `clamp` L3191 → F0232; `Number` L3194 → —; `Math.max` L3194 → —; `clamp` L3195 → F0232; `clamp` L3196 → F0232; `Math.exp` L3200 → —; `clamp` L3201 → F0232; `clamp` L3204 → F0232; `clamp` L3214 → F0232; `Set` L3217 → —; `touching.clear` L3218 → —; `pairs` L3219 → F0234; `Math.hypot` L3226 → —; `touching.add` L3231 → —; `Math.hypot` L3232 → —; `mass` L3235 → F0233; `mass` L3235 → F0233; `clamp` L3242 → F0232; `clamp` L3242 → F0232; `contact.has` L3243 → —; `cooldowns.get` L3243 → —; `Math.max` L3245 → —; `contact.add` L3246 → —; `mass` L3247 → F0233; `mass` L3247 → F0233; `clamp` L3248 → F0232; `Math.abs` L3248 → —; `clamp` L3253 → F0232; `clamp` L3253 → F0232; `clamp` L3254 → F0232; `Math.sqrt` L3256 → —; `mass` L3256 → F0233; `Math.sqrt` L3257 → —; `Math.max` L3257 → —; `clamp` L3258 → F0232; `Math.min` L3258 → —; `Math.max` L3258 → —; `clamp` L3258 → F0232; `Math.max` L3260 → —; `clamp` L3260 → F0232; `onImpact` L3262 → —; `contact.add` L3264 → —; `cooldowns.set` L3264 → —; `touching.has` L3268 → —; `contact.delete` L3268 → —.  
Pozivaju: index.html:L3273 (F0236).

**F0236 · step** — `index.html:L3270–3274` · FunctionDeclaration · parent F0231.  
Ulaz: `rs, dt, onImpact`.  
Trag tela: `{ if(!rs||!Array.isArray(rs.players)||!(dt>0))return; const steps=Math.ceil(dt/MAX_STEP),h=dt/steps; for(let i=0;i<steps;i++)integrate(rs,h,`.  
Poziva: `Array.isArray` L3271 → —; `Math.ceil` L3272 → —; `integrate` L3273 → F0235.  
Pozivaju: ~index.html:L3417 (F0253).

### race — trka i projekcija

**F0237 · anonimna** — `index.html:L3279–3499` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const { clip, dimensionOf, rng, species, tracks, uuid }=modules.domain; const { step }=modules.physics; const { leagueOf }=modules.progres`.  
Poziva: `Object.freeze` L3286 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0238 · cycleCamera** — `index.html:L3303–3305` · FunctionDeclaration · parent F0237.  
Ulaz: `mode`.  
Trag tela: `{ return mode==='chase'?'first':mode==='first'?'back':'chase'; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: ~index.html:L7335 (F0892); ~index.html:L8014 (F0943).

**F0239 · participant** — `index.html:L3307–3311` · FunctionDeclaration · parent F0237.  
Ulaz: `data, lane, isMe, speed`.  
Trag tela: `{ return {id:data.id,species:data.species,cls:data.cls,trail:data.trail,isMe,speed,wt:data.weight,atk:data.atk,infusion:data.infusion??0,bea`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L3324 (F0240); index.html:L3324 (F0242).

**F0240 · createRace** — `index.html:L3312–3334` · FunctionDeclaration · parent F0237.  
Ulaz: `snail, key, seed, id=uuid(), mode='league', trophies=0, keeperLevel=1`.  
Trag tela: `{ const course=tracks[key]; if(!course||!snail||snail.busy)throw Error('Trka ili puž nisu dostupni.'); const random=rng(seed); const dimensi`.  
Poziva: `uuid` L3312 → ~F0110; `Error` L3314 → —; `rng` L3315 → ~F0111; `dimensionOf` L3316 → ~F0073; `rng(seed^0x6e656275)` L3317 → —; `rng` L3317 → ~F0111; `clip` L3318 → ~F0093; `Math.pow` L3318 → —; `clip` L3318 → ~F0093; `[0,1,3].map` L3319 → —; `leagueOf` L3323 → ~F0028; `participant` L3324 → F0239; `others.map` L3324 → —; `random` L3326 → —; `Math.floor` L3327 → —; `random` L3327 → —; `random` L3327 → —; `objects.push` L3328 → —; `objects.push` L3329 → —; `random` L3329 → —; `Math.floor` L3329 → —; `random` L3329 → —.  
Pozivaju: ~index.html:L6959 (F0847); ~index.html:L7272 (F0883).

**F0241 · callback [0,1,3].map** — `index.html:L3319–3322` · ArrowFunction · parent F0240.  
Ulaz: `v, i`.  
Trag tela: `{ const s=species[(snail.species+1+Math.floor(random()*9)+i)%species.length]; return {id:'rival-'+v,species:s.id,cls:s.cls,weight:snail.weig`.  
Poziva: `Math.floor` L3320 → —; `random` L3320 → —; `random` L3321 → —; `random` L3321 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0242 · callback others.map** — `index.html:L3324–3324` · ArrowFunction · parent F0240.  
Ulaz: `n, i`.  
Trag tela: `participant(n,lanes[i+1],false,base*(.92+random()*.16)*rivalFactor)`.  
Poziva: `participant` L3324 → F0239; `random` L3324 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0243 · laneCommand** — `index.html:L3335–3338` · FunctionDeclaration · parent F0237.  
Ulaz: `race, delta`.  
Trag tela: `{ if(race.ready>0||race.paused||race.finish)return; race.queuedLane=clip(race.queuedLane+delta,-3,3); }`.  
Poziva: `clip` L3337 → ~F0093.  
Pozivaju: ~index.html:L7526 (F0903); ~index.html:L7941 (F0943); ~index.html:L7942 (F0943); ~index.html:L8234 (F0970).

**F0244 · boostCommand** — `index.html:L3339–3342` · FunctionDeclaration · parent F0237.  
Ulaz: `race`.  
Trag tela: `{ if(race.ready>0||race.paused||race.finish||race.energy<100)return false; race.queuedBoost=true;return true; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: ~index.html:L6962 (F0847); ~index.html:L7943 (F0943); ~index.html:L8236 (F0970).

**F0245 · activateTrail** — `index.html:L3343–3365` · FunctionDeclaration · parent F0237.  
Ulaz: `race, me`.  
Trag tela: `{ const unlocked=race.keeperLevel>=11; const strength=unlocked?clip(trailPower[me.cls]*(1+Math.min(.3,me.beauty/1000))*(1+.04*me.infusion),.`.  
Poziva: `clip` L3345 → ~F0093; `Math.min` L3345 → —; `race.players.slice(1).filter` L3352 → —; `race.players.slice` L3352 → —; `slow` L3355 → F0247; `slow` L3357 → F0247; `rivals.filter(rival=>rival.dist>=me.dist).sort` L3359 → —; `rivals.filter` L3359 → —; `rivals.sort` L3360 → —; `slow` L3361 → F0247; `['healing','sandy','starry'].includes` L3362 → —.  
Pozivaju: index.html:L3396 (F0253).

**F0246 · callback race.players.slice(1).filter** — `index.html:L3352–3352` · ArrowFunction · parent F0245.  
Ulaz: `racer`.  
Trag tela: `racer.finished===null`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0247 · slow** — `index.html:L3353–3353` · ArrowFunction · parent F0245.  
Ulaz: `racer, seconds`.  
Trag tela: `{racer.slowTo=Math.max(racer.slowTo,race.elapsed+seconds*strength);}`.  
Poziva: `Math.max` L3353 → —.  
Pozivaju: index.html:L3355 (F0245); index.html:L3357 (F0245); index.html:L3361 (F0245).

**F0248 · callback rivals.filter** — `index.html:L3359–3359` · ArrowFunction · parent F0245.  
Ulaz: `rival`.  
Trag tela: `rival.dist>=me.dist`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0249 · callback rivals.filter(rival=>rival.dist>=me.dist).sort** — `index.html:L3359–3359` · ArrowFunction · parent F0245.  
Ulaz: `a, b`.  
Trag tela: `a.dist-b.dist`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0250 · callback rivals.sort** — `index.html:L3360–3360` · ArrowFunction · parent F0245.  
Ulaz: `a, b`.  
Trag tela: `b.dist-a.dist`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0251 · recordWake** — `index.html:L3366–3375` · FunctionDeclaration · parent F0237.  
Ulaz: `race, me`.  
Trag tela: `{ if(race.trailEffect?.until<=race.elapsed||!race.trailEffect)return; const traveled=me.dist-race.wakeDist; if(traveled<4)return; const d=ra`.  
Poziva: `race.wake.push` L3372 → —; `race.wake.shift` L3374 → —.  
Pozivaju: index.html:L3425 (F0253).

**F0252 · recordRivalWake** — `index.html:L3377–3387` · FunctionDeclaration · parent F0237.  
Ulaz: `race, p`.  
Trag tela: `{ p.wakeDist??=p.dist;p.wakeX??=p.x; const traveled=p.dist-p.wakeDist; if(traveled<4)return; const d=p.wakeDist+4; const x=p.wakeX+(p.x-p.wa`.  
Poziva: `list.push` L3384 → —; `list.shift` L3386 → —.  
Pozivaju: index.html:L3426 (F0253).

**F0253 · tickRace** — `index.html:L3388–3448` · FunctionDeclaration · parent F0237.  
Ulaz: `race`.  
Trag tela: `{ const me=race.players[0]; if(race.queuedLane){ me.lane=clip(me.lane+race.queuedLane,0,3); race.commands.push([race.tick,me.lane]); race.qu`.  
Poziva: `clip` L3391 → ~F0093; `race.commands.push` L3392 → —; `activateTrail` L3396 → F0245; `race.commands.push` L3397 → —; `race.objects.find` L3403 → —; `race.random` L3404 → —; `clip` L3404 → ~F0093; `race.random` L3404 → —; `race.random` L3405 → —; `step` L3417 → ~F0236; `recordWake` L3425 → F0251; `recordRivalWake` L3426 → F0252; `Math.abs` L3432 → —; `clip` L3434 → ~F0093; `Math.max` L3435 → —; `clip` L3438 → ~F0093; `Math.max` L3438 → —; `clip` L3443 → ~F0093; `race.players.slice(1).filter` L3445 → —; `race.players.slice` L3445 → —.  
Pozivaju: index.html:L3459 (F0257).

**F0254 · callback race.objects.find** — `index.html:L3403–3403` · ArrowFunction · parent F0253.  
Ulaz: `o`.  
Trag tela: `o.type!=='drop'&&o.lane===p.lane&&o.d>p.dist&&o.d-p.dist<40`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0255 · callback step** — `index.html:L3417–3424` · ArrowFunction · parent F0253.  
Ulaz: `hit`.  
Trag tela: `{ race.impacts++; // v174 visual-only record of the collision (recoil, contact ring, BONG/KRC notice); the impulse itself is untouched for(c`.  
Poziva: `(race.hits??=[]).push` L3421 → —; `hit.broken.some` L3421 → —; `race.hits.shift` L3422 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0256 · callback race.players.slice(1).filter** — `index.html:L3445–3445` · ArrowFunction · parent F0253.  
Ulaz: `p`.  
Trag tela: `p.finished!==null&&p.finished<me.finished`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0257 · advanceRace** — `index.html:L3449–3462` · FunctionDeclaration · parent F0237.  
Ulaz: `race, seconds`.  
Trag tela: `{ if(race.paused||race.finish)return; // One rAF; bounded catch-up using the existing .01 s physics; at most MAX_FRAME/STEP ticks per call. `.  
Poziva: `Math.min` L3452 → —; `clip` L3452 → ~F0093; `Math.min` L3453 → —; `Math.max` L3454 → —; `Math.min` L3455 → —; `tickRace` L3459 → F0253.  
Pozivaju: ~index.html:L6963 (F0847); ~index.html:L7348 (F0894).

**F0258 · rankOf** — `index.html:L3463–3465` · FunctionDeclaration · parent F0237.  
Ulaz: `race`.  
Trag tela: `{ return race.finish?.place??(1+race.players.slice(1).filter(p=>p.dist>race.players[0].dist).length); }`.  
Poziva: `race.players.slice(1).filter` L3464 → —; `race.players.slice` L3464 → —.  
Pozivaju: ~index.html:L7227 (F0882).

**F0259 · callback race.players.slice(1).filter** — `index.html:L3464–3464` · ArrowFunction · parent F0258.  
Ulaz: `p`.  
Trag tela: `p.dist>race.players[0].dist`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0260 · createProjection** — `index.html:L3466–3496` · FunctionDeclaration · parent F0237.  
Ulaz: `width, height, race`.  
Trag tela: `{ const driver=race.cameraMode==='first',back=race.cameraMode==='back'; const portrait=width<=height; const nearY=height*(driver?.93:portrai`.  
Poziva: `clip` L3472 → ~F0093; `Math.min` L3477 → —.  
Pozivaju: ~index.html:L4738 (F0404).

**F0261 · row** — `index.html:L3478–3484` · FunctionDeclaration · parent F0260.  
Ulaz: `y, out=null`.  
Trag tela: `{ const scale=clip((y-horizon)/span,0,1.75); const offset=Math.sin(camera*.012+(1-scale)*2.35)*width*(portrait?.085:.14)*(1-Math.min(1,scale`.  
Poziva: `clip` L3479 → ~F0093; `Math.sin` L3480 → —; `Math.min` L3480 → —; `Math.max` L3481 → —.  
Pozivaju: index.html:L3491 (F0262).

**F0262 · at** — `index.html:L3485–3493` · FunctionDeclaration · parent F0260.  
Ulaz: `distance, lane`.  
Trag tela: `{ const ahead=(distance-camera)*direction; if(ahead< -11||ahead>560)return null; const ratio=26/(26+ahead); const y=horizon+span*ratio; if(y`.  
Poziva: `row` L3491 → F0261.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0263 · distanceAt** — `index.html:L3494–3494` · FunctionDeclaration · parent F0260.  
Ulaz: `y`.  
Trag tela: `{return camera+direction*26*(span/Math.max(1,y-horizon)-1);}`.  
Poziva: `Math.max` L3494 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### renderer — GPU i Canvas resursi

**F0264 · anonimna** — `index.html:L3500–4079` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const { frames }=modules.frames; const vertexSource = ˋ attribute vec2 point; attribute vec2 uv; attribute vec4 tint; uniform vec2 viewpor`.  
Poziva: `Map` L3558 → —; `Map` L3641 → —; `Map` L3642 → —; `Map` L3643 → —; `Float32Array` L3651 → —; `canvas.getContext` L3654 → —; `this.initGL` L3655 → F0281; `this.useCanvasFallback` L3659 → F0280; `this.canvas.getContext` L3662 → —; `Error` L3663 → —; `this.canvas.addEventListener` L3665 → —; `this.canvas.addEventListener` L3671 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0265 · colorOf** — `index.html:L3559–3567` · FunctionDeclaration · parent F0264.  
Ulaz: `hex`.  
Trag tela: `{ let color=COLORS.get(hex); if(color)return color; const value=hex.replace('#',''); color=[0,2,4].map(i=>parseInt(value.slice(i,i+2),16)/25`.  
Poziva: `COLORS.get` L3560 → —; `hex.replace` L3562 → —; `[0,2,4].map` L3563 → —; `color.push` L3564 → —; `parseInt` L3564 → —; `value.slice` L3564 → —; `COLORS.set` L3565 → —.  
Pozivaju: index.html:L3915 (F0295); index.html:L3959 (F0299); index.html:L3972 (F0298); index.html:L3973 (F0298); index.html:L3997 (F0300); index.html:L4059 (F0311); index.html:L4059 (F0311).

**F0266 · callback [0,2,4].map** — `index.html:L3563–3563` · ArrowFunction · parent F0265.  
Ulaz: `i`.  
Trag tela: `parseInt(value.slice(i,i+2),16)/255`.  
Poziva: `parseInt` L3563 → —; `value.slice` L3563 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0267 · shaderProgram** — `index.html:L3568–3580` · FunctionDeclaration · parent F0264.  
Ulaz: `gl`.  
Trag tela: `{ const compile=(type,source)=>{ const shader=gl.createShader(type);gl.shaderSource(shader,source);gl.compileShader(shader); if(!gl.getShade`.  
Poziva: `gl.createProgram` L3576 → —; `compile` L3576 → F0268; `compile` L3576 → F0268; `gl.attachShader` L3577 → —; `gl.attachShader` L3577 → —; `gl.linkProgram` L3577 → —; `gl.deleteShader` L3577 → —; `gl.deleteShader` L3577 → —; `gl.getProgramParameter` L3578 → —; `Error` L3578 → —; `gl.getProgramInfoLog` L3578 → —.  
Pozivaju: index.html:L3714 (F0281).

**F0268 · compile** — `index.html:L3569–3575` · ArrowFunction · parent F0267.  
Ulaz: `type, source`.  
Trag tela: `{ const shader=gl.createShader(type);gl.shaderSource(shader,source);gl.compileShader(shader); if(!gl.getShaderParameter(shader,gl.COMPILE_ST`.  
Poziva: `gl.createShader` L3570 → —; `gl.shaderSource` L3570 → —; `gl.compileShader` L3570 → —; `gl.getShaderParameter` L3571 → —; `gl.getShaderInfoLog` L3572 → —; `gl.deleteShader` L3572 → —; `Error` L3572 → —.  
Pozivaju: index.html:L3576 (F0267); index.html:L3576 (F0267).

**F0269 · imageHealth** — `index.html:L3585–3585` · FunctionDeclaration · parent F0264.  
Ulaz: `—`.  
Trag tela: `{return {...scImageHealth,missing:scImageHealth.missing.slice()};}`.  
Poziva: `scImageHealth.missing.slice` L3585 → —.  
Pozivaju: ~index.html:L6873 (F0836).

**F0270 · scImageName** — `index.html:L3586–3590` · FunctionDeclaration · parent F0264.  
Ulaz: `url`.  
Trag tela: `{ if(/^(data:|blob:)/.test(url))return 'ugrađena atlas slika'; try{return new URL(url,location.href).pathname.split('/').pop().slice(0,72)||`.  
Poziva: `/^(data:|blob:)/.test` L3587 → —; `new URL(url,location.href).pathname.split('/').pop().slice` L3588 → —; `new URL(url,location.href).pathname.split('/').pop` L3588 → —; `new URL(url,location.href).pathname.split` L3588 → —; `URL` L3588 → —.  
Pozivaju: index.html:L3606 (F0275).

**F0271 · loadImage** — `index.html:L3591–3615` · FunctionDeclaration · parent F0264.  
Ulaz: `url`.  
Trag tela: `{ return new Promise((resolve,reject)=>{ const external=/^(https?:|\.\.?\/|\/)/.test(url); let failures=0; const attempt=()=>{ const image=n`.  
Poziva: `Promise` L3592 → —.  
Pozivaju: index.html:L3739 (F0282); index.html:L3755 (F0285); index.html:L3763 (F0285); index.html:L3774 (F0285).

**F0272 · anonimna** — `index.html:L3592–3614` · ArrowFunction · parent F0271.  
Ulaz: `resolve, reject`.  
Trag tela: `{ const external=/^(https?:|\.\.?\/|\/)/.test(url); let failures=0; const attempt=()=>{ const image=new Image(); image.onload=()=>{if(failur`.  
Poziva: `/^(https?:|\.\.?\/|\/)/.test` L3593 → —; `attempt` L3613 → F0273.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0273 · attempt** — `index.html:L3595–3612` · ArrowFunction · parent F0272.  
Ulaz: `—`.  
Trag tela: `{ const image=new Image(); image.onload=()=>{if(failures)scImageHealth.recovered++;resolve(image);}; image.onerror=()=>{ scImageHealth.error`.  
Poziva: `Image` L3596 → —.  
Pozivaju: index.html:L3613 (F0272).

**F0274 · image.onload** — `index.html:L3597–3597` · ArrowFunction · parent F0273.  
Ulaz: `—`.  
Trag tela: `{if(failures)scImageHealth.recovered++;resolve(image);}`.  
Poziva: `resolve` L3597 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0275 · image.onerror** — `index.html:L3598–3610` · ArrowFunction · parent F0273.  
Ulaz: `—`.  
Trag tela: `{ scImageHealth.errors++; if(external&&failures===0&&navigator.onLine!==false){ failures++;scImageHealth.retried++; // Avoid changing the im`.  
Poziva: `setTimeout` L3603 → —; `scImageName` L3606 → F0270; `scImageHealth.missing.includes` L3607 → —; `scImageHealth.missing.push` L3608 → —; `reject` L3609 → —; `Error` L3609 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0276 · assetGroup** — `index.html:L3616–3623` · FunctionDeclaration · parent F0264.  
Ulaz: `path`.  
Trag tela: `{ if(path==='island.webp')return 'startup'; if(path==='race.webp')return 'race'; if(path==='raceExtra.webp')return 'race-extra'; if(path==='`.  
Poziva: `path.startsWith` L3621 → —; `Math.floor` L3621 → —; `Number` L3621 → —; `path.slice` L3621 → —.  
Pozivaju: index.html:L3628 (F0277).

**F0277 · imagePath** — `index.html:L3624–3635` · FunctionDeclaration · parent F0264.  
Ulaz: `path`.  
Trag tela: `{ const assets=globalThis.SNAIL_ASSETS; if(!assets)return './assets/'+path; if(!Object.hasOwn(assets,path)){ const group=document.getElement`.  
Poziva: `Object.hasOwn` L3627 → —; `document.getElementById` L3628 → —; `assetGroup` L3628 → F0276; `Object.assign` L3630 → —; `JSON.parse` L3630 → —; `group.remove` L3631 → —.  
Pozivaju: index.html:L3739 (F0282); ~index.html:L5454 (F0538); ~index.html:L5457 (F0540); ~index.html:L5895 (F0655); ~index.html:L5900 (F0659); ~index.html:L7158 (F0871); ~index.html:L7541 (F0906); ~index.html:L7676 (F0911).

**F0278 · callback this.canvas.addEventListener** — `index.html:L3665–3670` · ArrowFunction · parent F0264.  
Ulaz: `event`.  
Trag tela: `{ event.preventDefault(); if(event.currentTarget!==this.canvas)return; this.lost=true; this.onLoss?.(); }`.  
Poziva: `event.preventDefault` L3666 → —; `this.onLoss` L3669 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0279 · callback this.canvas.addEventListener** — `index.html:L3671–3688` · ArrowFunction · parent F0264.  
Ulaz: `event`.  
Trag tela: `{ if(event.currentTarget!==this.canvas)return; try{ this.initGL(); this.gpuResets++; // Restore only the island and the current scene. Uploa`.  
Poziva: `this.initGL` L3674 → F0281; `Set` L3678 → —; `this.images.get` L3679 → —; `this.upload` L3680 → F0292; `this.uploadIllustratedMap` L3682 → F0286; `this.uploadDetachedAtlas` L3683 → F0287; `Object.entries` L3684 → —; `this.uploadSky` L3684 → F0289; `this.onRestore` L3686 → —; `this.useCanvasFallback` L3687 → F0280.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0280 · useCanvasFallback** — `index.html:L3691–3709` · MethodDeclaration · parent F0264.  
Ulaz: `—`.  
Trag tela: `{ const previous=this.canvas; const canvas=previous.cloneNode(false); const ctx=canvas.getContext('2d',{alpha:false}); if(!ctx)return false;`.  
Poziva: `previous.cloneNode` L3693 → —; `canvas.getContext` L3694 → —; `previous.replaceWith` L3696 → —; `this.textures.clear` L3699 → —; `this.onFallback` L3707 → —.  
Pozivaju: index.html:L3659 (F0264); index.html:L3687 (F0279).

**F0281 · initGL** — `index.html:L3710–3729` · MethodDeclaration · parent F0264.  
Ulaz: `—`.  
Trag tela: `{ const gl=this.gl; this.textures.clear(); this.mapTexture=null;this.detachedTexture=null;this.skyTextures={}; this.program=shaderProgram(gl`.  
Poziva: `this.textures.clear` L3712 → —; `shaderProgram` L3714 → F0267; `gl.createBuffer` L3715 → —; `gl.useProgram` L3716 → —; `gl.bindBuffer` L3716 → —; `gl.bufferData` L3717 → —; `gl.getAttribLocation` L3719 → —; `gl.enableVertexAttribArray` L3719 → —; `gl.vertexAttribPointer` L3720 → —; `gl.getUniformLocation` L3722 → —; `gl.getUniformLocation` L3723 → —; `gl.getUniformLocation` L3724 → —; `gl.getUniformLocation` L3725 → —; `gl.uniform1f` L3726 → —; `gl.uniform1i` L3727 → —; `gl.getUniformLocation` L3727 → —; `gl.enable` L3728 → —; `gl.blendFunc` L3728 → —.  
Pozivaju: index.html:L3655 (F0264); index.html:L3674 (F0279).

**F0282 · preload** — `index.html:L3730–3746` · MethodDeclaration · parent F0264.  
Ulaz: `key`.  
Trag tela: `{ const scT=globalThis.SC_STARTUP_TRACE,scAt=key==='island'?scT?.begin():undefined; if(this.images.has(key)){ // A previous race may have re`.  
Poziva: `scT?.begin` L3731 → —; `this.images.has` L3732 → —; `this.textures.has` L3735 → —; `this.upload` L3735 → F0292; `this.images.get` L3735 → —; `Promise.resolve` L3736 → —; `this.pending.has` L3738 → —; `this.pending.get` L3738 → —; `loadImage(imagePath(key+'.webp')).then(image=>{ if(scAt!==undefined){scT?.end('island.imageOnload',scAt);scT?.probeDecode(image,'island');} ` L3739 → —; `loadImage(imagePath(key+'.webp')).then` L3739 → —; `loadImage` L3739 → F0271; `imagePath` L3739 → F0277; `this.pending.set` L3744 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0283 · callback loadImage(imagePath(key+'.webp')).then** — `index.html:L3739–3743` · ArrowFunction · parent F0282.  
Ulaz: `image`.  
Trag tela: `{ if(scAt!==undefined){scT?.end('island.imageOnload',scAt);scT?.probeDecode(image,'island');} if(this.gl&&!this.lost)this.upload(key,image);`.  
Poziva: `scT?.end` L3740 → —; `scT?.probeDecode` L3740 → —; `this.upload` L3741 → F0292; `this.images.set` L3742 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0284 · callback loadImage(imagePath(key+'.webp')).then(image=>{ if(scAt!==undefined){scT?.end('island.imageOnload',scAt);scT?.probeDecode(image,'island');} ** — `index.html:L3743–3743` · ArrowFunction · parent F0282.  
Ulaz: `—`.  
Trag tela: `this.pending.delete(key)`.  
Poziva: `this.pending.delete` L3743 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0285 · preloadIllustratedMap** — `index.html:L3747–3779` · MethodDeclaration · parent F0264.  
Ulaz: `—`.  
Trag tela: `{ const scT=globalThis.SC_STARTUP_TRACE,scAll=scT?.begin(); const element=document.getElementById('illustrated-map-webp'); if(!element)throw`.  
Poziva: `scT?.begin` L3748 → —; `document.getElementById` L3749 → —; `Error` L3750 → —; `scT?.begin` L3751 → —; `element.textContent.trim` L3752 → —; `scT?.end` L3753 → —; `scT?.begin` L3754 → —; `loadImage` L3755 → F0271; `scT?.end` L3756 → —; `scT?.probeDecode` L3756 → —; `this.uploadIllustratedMap` L3758 → F0286; `document.getElementById` L3760 → —; `scT?.begin` L3762 → —; `loadImage` L3763 → F0271; `source.textContent.trim` L3763 → —; `scT?.end` L3764 → —; `scT?.probeDecode` L3764 → —; `this.uploadSky` L3766 → F0289; `document.getElementById` L3771 → —; `Error` L3772 → —; `scT?.begin` L3773 → —; `loadImage` L3774 → F0271; `atlasText.textContent.trim` L3774 → —; `scT?.end` L3775 → —; `scT?.probeDecode` L3775 → —; `this.uploadDetachedAtlas` L3777 → F0287; `scT?.end` L3778 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0286 · uploadIllustratedMap** — `index.html:L3780–3795` · MethodDeclaration · parent F0264.  
Ulaz: `—`.  
Trag tela: `{ if(!this.gl||!this.mapImage)return; const gl=this.gl; if(this.mapTexture)gl.deleteTexture(this.mapTexture); const texture=gl.createTexture`.  
Poziva: `gl.deleteTexture` L3783 → —; `gl.createTexture` L3784 → —; `Error` L3785 → —; `gl.bindTexture` L3786 → —; `globalThis.SC_STARTUP_TRACE?.begin` L3787 → —; `gl.texImage2D` L3788 → —; `globalThis.SC_STARTUP_TRACE?.end` L3789 → —; `gl.texParameteri` L3790 → —; `gl.texParameteri` L3791 → —; `gl.texParameteri` L3792 → —; `gl.texParameteri` L3793 → —.  
Pozivaju: index.html:L3682 (F0279); index.html:L3758 (F0285).

**F0287 · uploadDetachedAtlas** — `index.html:L3796–3811` · MethodDeclaration · parent F0264.  
Ulaz: `—`.  
Trag tela: `{ if(!this.gl||!this.detachedImage)return; const gl=this.gl; if(this.detachedTexture)gl.deleteTexture(this.detachedTexture); const texture=g`.  
Poziva: `gl.deleteTexture` L3799 → —; `gl.createTexture` L3800 → —; `Error` L3801 → —; `gl.bindTexture` L3802 → —; `globalThis.SC_STARTUP_TRACE?.begin` L3803 → —; `gl.texImage2D` L3804 → —; `globalThis.SC_STARTUP_TRACE?.end` L3805 → —; `gl.texParameteri` L3808 → —; `gl.bindTexture` L3810 → —; `this.textures.get` L3810 → —.  
Pozivaju: index.html:L3683 (F0279); index.html:L3777 (F0285).

**F0288 · drawDetachedObjects** — `index.html:L3812–3828` · MethodDeclaration · parent F0264.  
Ulaz: `draws`.  
Trag tela: `{ if(!this.detachedImage||!draws.length)return; this.flush(); const oldAtlas=this.atlas,oldImage=this.image; this.atlas=DETACHED_MAP_UV; thi`.  
Poziva: `this.flush` L3814 → F0296; `this.gl.bindTexture` L3820 → —; `this.sprite` L3823 → F0307; `this.flush` L3825 → F0296; `this.gl.bindTexture` L3827 → —; `this.textures.get` L3827 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0289 · uploadSky** — `index.html:L3831–3835` · MethodDeclaration · parent F0264.  
Ulaz: `key, image`.  
Trag tela: `{ if(!this.gl||this.lost)return; this.upload('sc-sky-'+key,image); this.skyTextures[key]=this.textures.get('sc-sky-'+key); }`.  
Poziva: `this.upload` L3833 → F0292; `this.textures.get` L3834 → —.  
Pozivaju: index.html:L3684 (F0279); index.html:L3766 (F0285).

**F0290 · drawSky** — `index.html:L3836–3853` · MethodDeclaration · parent F0264.  
Ulaz: `key`.  
Trag tela: `{ const art=this.skyImages[key]; if(!art)return false; const zoom=Math.max(this.width/art.width,this.height/art.height); const w=art.width*z`.  
Poziva: `Math.max` L3839 → —; `this.ctx.drawImage` L3842 → —; `this.flush` L3844 → F0296; `this.gl.bindTexture` L3847 → —; `this.sprite` L3848 → F0307; `this.flush` L3849 → F0296; `this.gl.bindTexture` L3851 → —; `this.textures.get` L3851 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0291 · drawIllustratedMap** — `index.html:L3854–3876` · MethodDeclaration · parent F0264.  
Ulaz: `x, y, w, h`.  
Trag tela: `{ if(!this.mapImage)return false; if(!this.gl){this.ctx.drawImage(this.mapImage,x,y,w,h);return true;} if(!this.mapTexture)return false; // `.  
Poziva: `this.ctx.drawImage` L3856 → —; `this.flush` L3859 → F0296; `this.gl.bindTexture` L3862 → —; `globalThis.matchMedia` L3865 → —; `this.gl.uniform1f` L3866 → —; `this.gl.uniform1f` L3867 → —; `performance.now` L3867 → —; `Math.min` L3868 → —; `this.gl.uniform1f` L3869 → —; `Math.max` L3869 → —; `this.sprite` L3870 → F0307; `this.flush` L3871 → F0296; `this.gl.uniform1f` L3872 → —; `this.gl.bindTexture` L3874 → —; `this.textures.get` L3874 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0292 · upload** — `index.html:L3877–3891` · MethodDeclaration · parent F0264.  
Ulaz: `key, image`.  
Trag tela: `{ const gl=this.gl; if(this.textures.has(key))gl.deleteTexture(this.textures.get(key)); const texture=gl.createTexture(); if(!texture)throw `.  
Poziva: `this.textures.has` L3879 → —; `gl.deleteTexture` L3879 → —; `this.textures.get` L3879 → —; `gl.createTexture` L3880 → —; `Error` L3881 → —; `gl.bindTexture` L3882 → —; `globalThis.SC_STARTUP_TRACE?.begin` L3883 → —; `gl.texImage2D` L3884 → —; `globalThis.SC_STARTUP_TRACE?.end` L3885 → —; `gl.texParameteri` L3886 → —; `gl.texParameteri` L3887 → —; `gl.texParameteri` L3888 → —; `gl.texParameteri` L3889 → —; `this.textures.set` L3890 → —.  
Pozivaju: index.html:L3680 (F0279); index.html:L3735 (F0282); index.html:L3741 (F0283); index.html:L3833 (F0289).

**F0293 · releaseTexture** — `index.html:L3892–3900` · MethodDeclaration · parent F0264.  
Ulaz: `key`.  
Trag tela: `{ // Island atlas stays hot so return from races never triggers a GPU upload. if(key==='island'||key===this.active||!this.gl||this.lost)retu`.  
Poziva: `this.textures.get` L3895 → —; `this.gl.deleteTexture` L3897 → —; `this.textures.delete` L3898 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0294 · resize** — `index.html:L3901–3906` · MethodDeclaration · parent F0264.  
Ulaz: `width, height, ratio`.  
Trag tela: `{ width=Math.max(1,Math.round(width));height=Math.max(1,Math.round(height)); if(width===this.width&&height===this.height&&ratio===this.dpr)r`.  
Poziva: `Math.max` L3902 → —; `Math.round` L3902 → —; `Math.max` L3902 → —; `Math.round` L3902 → —; `Math.round` L3905 → —; `Math.round` L3905 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0295 · begin** — `index.html:L3907–3928` · MethodDeclaration · parent F0264.  
Ulaz: `key, bg`.  
Trag tela: `{ const image=this.images.get(key); if(!image||this.lost)return false; this.active=key;this.at=0;this.stats.calls=0;this.stats.upload=0; thi`.  
Poziva: `this.images.get` L3908 → —; `this.textures.has` L3914 → —; `colorOf` L3915 → F0265; `gl.viewport` L3916 → —; `gl.useProgram` L3917 → —; `gl.bindBuffer` L3917 → —; `gl.uniform2f` L3918 → —; `gl.activeTexture` L3919 → —; `gl.bindTexture` L3920 → —; `this.textures.get` L3920 → —; `gl.clearColor` L3921 → —; `gl.clear` L3921 → —; `this.ctx.setTransform` L3923 → —; `this.ctx.fillRect` L3925 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0296 · flush** — `index.html:L3929–3936` · MethodDeclaration · parent F0264.  
Ulaz: `—`.  
Trag tela: `{ if(!this.gl||!this.at)return; const gl=this.gl; gl.bufferSubData(gl.ARRAY_BUFFER,0,this.data.subarray(0,this.at)); gl.drawArrays(gl.TRIANG`.  
Poziva: `gl.bufferSubData` L3932 → —; `this.data.subarray` L3932 → —; `gl.drawArrays` L3933 → —.  
Pozivaju: index.html:L3814 (F0288); index.html:L3825 (F0288); index.html:L3844 (F0290); index.html:L3849 (F0290); index.html:L3859 (F0291); index.html:L3871 (F0291); index.html:L3971 (F0298).

**F0297 · vertex** — `index.html:L3937–3943` · MethodDeclaration · parent F0264.  
Ulaz: `x, y, u, v, r, g, b, a`.  
Trag tela: `{ const out=this.data; let i=this.at; out[i++]=x;out[i++]=y;out[i++]=u;out[i++]=v; out[i++]=r;out[i++]=g;out[i++]=b;out[i++]=a; this.at=i; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L3975 (F0298); index.html:L3975 (F0298); index.html:L3975 (F0298); index.html:L3976 (F0298); index.html:L3976 (F0298); index.html:L3976 (F0298).

**F0298 · quad** — `index.html:L3944–3977` · MethodDeclaration · parent F0264.  
Ulaz: `x1, y1, x2, y2, x3, y3, x4, y4, asset, hex, alpha=1, flip=false, bottom=hex, bottomAlpha=alpha`.  
Trag tela: `{ const sprite=asset?this.atlas[asset]:null; if(asset&&!sprite)return; if(!this.gl){ const ctx=this.ctx; ctx.globalAlpha=alpha; if(sprite){ `.  
Poziva: `ctx.save` L3952 → —; `ctx.translate` L3952 → —; `ctx.scale` L3952 → —; `ctx.drawImage` L3953 → —; `ctx.restore` L3954 → —; `ctx.createLinearGradient` L3957 → —; `gradient.addColorStop` L3962 → —; `rgba` L3962 → F0299; `gradient.addColorStop` L3962 → —; `rgba` L3962 → F0299; `ctx.beginPath` L3966 → —; `ctx.moveTo` L3966 → —; `ctx.lineTo` L3966 → —; `ctx.lineTo` L3966 → —; `ctx.lineTo` L3966 → —; `ctx.closePath` L3966 → —; `ctx.fill` L3966 → —; `this.flush` L3971 → F0296; `colorOf` L3972 → F0265; `colorOf` L3973 → F0265; `this.vertex` L3975 → F0297; `this.vertex` L3975 → F0297; `this.vertex` L3975 → F0297; `this.vertex` L3976 → F0297; `this.vertex` L3976 → F0297; `this.vertex` L3976 → F0297.  
Pozivaju: index.html:L3986 (F0300); index.html:L4020 (F0305); index.html:L4037 (F0306); index.html:L4040 (F0307); index.html:L4051 (F0308); index.html:L4056 (F0310).

**F0299 · rgba** — `index.html:L3958–3961` · ArrowFunction · parent F0298.  
Ulaz: `key, opacity`.  
Trag tela: `{ const [r,g,b,a]=colorOf(key); return 'rgba('+[r*255,g*255,b*255,a*opacity].join(',')+')'; }`.  
Poziva: `colorOf` L3959 → F0265; `[r*255,g*255,b*255,a*opacity].join` L3960 → —.  
Pozivaju: index.html:L3962 (F0298); index.html:L3962 (F0298).

**F0300 · roadStrip** — `index.html:L3978–4015` · MethodDeclaration · parent F0264.  
Ulaz: `rows, colors, shoulder=false`.  
Trag tela: `{ const edge=(half,index)=>half+(shoulder?2+index*.23:0); const tint=index=>shoulder?'#544e3c':colors[index]; const opacity=index=>Math.min(`.  
Poziva: `edge` L3985 → F0301; `edge` L3985 → F0301; `this.quad` L3986 → F0298; `tint` L3986 → F0302; `opacity` L3986 → F0303; `tint` L3986 → F0302; `opacity` L3986 → F0303; `ctx.createLinearGradient` L3995 → —; `colorOf` L3997 → F0265; `tint` L3997 → F0302; `gradient.addColorStop` L3998 → —; `[r*255,g*255,b*255,opacity(i)].join` L3998 → —; `opacity` L3998 → F0303; `ctx.beginPath` L4004 → —; `edge` L4006 → F0301; `ctx.moveTo` L4007 → —; `ctx.lineTo` L4007 → —; `ctx.lineTo` L4011 → —; `edge` L4011 → F0301; `ctx.closePath` L4013 → —; `ctx.fill` L4014 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0301 · edge** — `index.html:L3979–3979` · ArrowFunction · parent F0300.  
Ulaz: `half, index`.  
Trag tela: `half+(shoulder?2+index*.23:0)`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L3985 (F0300); index.html:L3985 (F0300); index.html:L4006 (F0300); index.html:L4011 (F0300).

**F0302 · tint** — `index.html:L3980–3980` · ArrowFunction · parent F0300.  
Ulaz: `index`.  
Trag tela: `shoulder?'#544e3c':colors[index]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L3986 (F0300); index.html:L3986 (F0300); index.html:L3997 (F0300).

**F0303 · opacity** — `index.html:L3981–3981` · ArrowFunction · parent F0300.  
Ulaz: `index`.  
Trag tela: `Math.min(1,index/4)*(shoulder?.76:1)`.  
Poziva: `Math.min` L3981 → —.  
Pozivaju: index.html:L3986 (F0300); index.html:L3986 (F0300); index.html:L3998 (F0300).

**F0304 · shadow** — `index.html:L4016–4018` · MethodDeclaration · parent F0264.  
Ulaz: `x, y, rx, ry, opacity`.  
Trag tela: `{ this.sprite('snail-shadow',x-rx,y-ry,2*rx,2*ry,opacity); }`.  
Poziva: `this.sprite` L4017 → F0307.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0305 · fill** — `index.html:L4019–4021` · MethodDeclaration · parent F0264.  
Ulaz: `x, y, w, h, hex, alpha=1`.  
Trag tela: `{ this.quad(x,y,x+w,y,x+w,y+h,x,y+h,null,hex,alpha); }`.  
Poziva: `this.quad` L4020 → F0298.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0306 · gradient** — `index.html:L4022–4038` · MethodDeclaration · parent F0264.  
Ulaz: `x, y, w, h, top, bottom`.  
Trag tela: `{ if(!this.gl){ const ctx=this.ctx; let cached=this.backgroundGradient; if(!cached||cached.ctx!==ctx||cached.y!==y||cached.h!==h|| cached.dp`.  
Poziva: `ctx.createLinearGradient` L4028 → —; `gradient.addColorStop` L4029 → —; `gradient.addColorStop` L4030 → —; `ctx.fillRect` L4034 → —; `this.quad` L4037 → F0298.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0307 · sprite** — `index.html:L4039–4041` · MethodDeclaration · parent F0264.  
Ulaz: `name, x, y, w, h, alpha=1, flip=false`.  
Trag tela: `{ this.quad(x,y,x+w,y,x+w,y+h,x,y+h,name,'#ffffff',alpha,flip); }`.  
Poziva: `this.quad` L4040 → F0298.  
Pozivaju: index.html:L3823 (F0288); index.html:L3848 (F0290); index.html:L3870 (F0291); index.html:L4017 (F0304); index.html:L4044 (F0308); index.html:L4047 (F0308).

**F0308 · spriteTurned** — `index.html:L4043–4052` · MethodDeclaration · parent F0264.  
Ulaz: `name, px, py, left, top, w, h, angle, alpha=1, flip=false`.  
Trag tela: `{ if(!angle||!this.gl&&typeof this.ctx?.rotate!=='function'){this.sprite(name,px+left,py+top,w,h,alpha,flip);return;} if(!this.gl){ const ct`.  
Poziva: `this.sprite` L4044 → F0307; `ctx.save` L4046 → —; `ctx.translate` L4046 → —; `ctx.rotate` L4046 → —; `this.sprite` L4047 → F0307; `ctx.restore` L4047 → —; `Math.cos` L4049 → —; `Math.sin` L4049 → —; `at` L4050 → F0309; `at` L4050 → F0309; `at` L4050 → F0309; `at` L4050 → F0309; `this.quad` L4051 → F0298.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0309 · at** — `index.html:L4049–4049` · ArrowFunction · parent F0308.  
Ulaz: `x, y`.  
Trag tela: `[px+x*c-y*s,py+x*s+y*c]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L4050 (F0308); index.html:L4050 (F0308); index.html:L4050 (F0308); index.html:L4050 (F0308).

**F0310 · line** — `index.html:L4054–4057` · MethodDeclaration · parent F0264.  
Ulaz: `x1, y1, x2, y2, width, hex, alpha=1`.  
Trag tela: `{ const dx=x2-x1,dy=y2-y1,len=Math.hypot(dx,dy)||1,nx=-dy/len*width/2,ny=dx/len*width/2; this.quad(x1+nx,y1+ny,x2+nx,y2+ny,x2-nx,y2-ny,x1-nx`.  
Poziva: `Math.hypot` L4055 → —; `this.quad` L4056 → F0298.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0311 · tint** — `index.html:L4058–4061` · MethodDeclaration · parent F0264.  
Ulaz: `l, r, t`.  
Trag tela: `{ const a=colorOf(l),b=colorOf(r); return '#'+a.slice(0,3).map((v,i)=>Math.round((v+(b[i]-v)*t)*255).toString(16).padStart(2,'0')).join('');`.  
Poziva: `colorOf` L4059 → F0265; `colorOf` L4059 → F0265; `a.slice(0,3).map((v,i)=>Math.round((v+(b[i]-v)*t)*255).toString(16).padStart(2,'0')).join` L4060 → —; `a.slice(0,3).map` L4060 → —; `a.slice` L4060 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0312 · callback a.slice(0,3).map** — `index.html:L4060–4060` · ArrowFunction · parent F0311.  
Ulaz: `v, i`.  
Trag tela: `Math.round((v+(b[i]-v)*t)*255).toString(16).padStart(2,'0')`.  
Poziva: `Math.round((v+(b[i]-v)*t)*255).toString(16).padStart` L4060 → —; `Math.round((v+(b[i]-v)*t)*255).toString` L4060 → —; `Math.round` L4060 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0313 · estimate** — `index.html:L4062–4075` · MethodDeclaration · parent F0264.  
Ulaz: `—`.  
Trag tela: `{ const sizeOf=image=>image?image.width*image.height*4:0; // The illustrated island lives outside the atlas Map. Count it as a // decoded CP`.  
Poziva: `sizeOf` L4066 → F0314; `[...this.images.values()].reduce` L4068 → —; `this.images.values` L4068 → —; `sizeOf` L4068 → F0314; `[...this.textures.keys()].reduce` L4069 → —; `this.textures.keys` L4069 → —; `sizeOf` L4070 → F0314; `sizeOf` L4071 → F0314; `this.textures.keys` L4072 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0314 · sizeOf** — `index.html:L4063–4063` · ArrowFunction · parent F0313.  
Ulaz: `image`.  
Trag tela: `image?image.width*image.height*4:0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L4066 (F0313); index.html:L4068 (F0315); index.html:L4068 (F0313); index.html:L4069 (F0316); index.html:L4070 (F0313); index.html:L4071 (F0313).

**F0315 · callback [...this.images.values()].reduce** — `index.html:L4068–4068` · ArrowFunction · parent F0313.  
Ulaz: `sum, i`.  
Trag tela: `sum+sizeOf(i)`.  
Poziva: `sizeOf` L4068 → F0314.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0316 · callback [...this.textures.keys()].reduce** — `index.html:L4069–4069` · ArrowFunction · parent F0313.  
Ulaz: `sum, key`.  
Trag tela: `sum+sizeOf(this.images.get(key))`.  
Poziva: `sizeOf` L4069 → F0314; `this.images.get` L4069 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### sceneManager — životni ciklus scena

**F0317 · anonimna** — `index.html:L4080–4161` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ /** * The only scene ownership layer. Both scenes use the same renderer and canvas. * CPU image assets remain decoded; only inactive race `.  
Poziva: `globalThis.requestIdleCallback?.bind` L4087 → —; `globalThis.cancelIdleCallback?.bind` L4087 → —; `Set` L4096 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0318 · anonimna** — `index.html:L4087–4087` · ArrowFunction · parent F0317.  
Ulaz: `callback, delay`.  
Trag tela: `globalThis.setTimeout(callback,delay)`.  
Poziva: `globalThis.setTimeout` L4087 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0319 · anonimna** — `index.html:L4087–4087` · ArrowFunction · parent F0317.  
Ulaz: `id`.  
Trag tela: `globalThis.clearTimeout(id)`.  
Poziva: `globalThis.clearTimeout` L4087 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0320 · cancelCleanup** — `index.html:L4103–4107` · MethodDeclaration · parent F0317.  
Ulaz: `—`.  
Trag tela: `{ if(this.timer!==null){this.clearTimer(this.timer);this.timer=null;} if(this.idleJob!==null&&this.cancelIdle)this.cancelIdle(this.idleJob);`.  
Poziva: `this.clearTimer` L4104 → —; `this.cancelIdle` L4105 → —.  
Pozivaju: index.html:L4114 (F0321).

**F0321 · activate** — `index.html:L4108–4127` · MethodDeclaration · parent F0317.  
Ulaz: `kind, atlas`.  
Trag tela: `{ if(kind!=='island'&&kind!=='race')throw Error('Unknown scene: '+kind); if(this.renderer.lost&&kind==='race')throw Error('Grafički kontekst`.  
Poziva: `Error` L4109 → —; `Error` L4110 → —; `this.renderer.images.has` L4111 → —; `this.renderer.textures.has` L4111 → —; `Error` L4112 → —; `this.cancelCleanup` L4114 → F0320; `this.retiring.delete` L4119 → —; `this.retiring.add` L4121 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0322 · paintedMap** — `index.html:L4128–4138` · MethodDeclaration · parent F0317.  
Ulaz: `—`.  
Trag tela: `{ if(this.active!=='island'||!this.retiring.size||this.timer!==null||this.idleJob!==null)return; // Do not delete anything in the input hand`.  
Poziva: `this.setTimer` L4132 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0323 · callback this.setTimer** — `index.html:L4132–4137` · ArrowFunction · parent F0322.  
Ulaz: `—`.  
Trag tela: `{ this.timer=null; if(this.idle){ this.idleJob=this.idle(()=>{this.idleJob=null;this.cleanupOne();},{timeout:2000}); }else this.cleanupOne()`.  
Poziva: `this.idle` L4135 → —; `this.cleanupOne` L4136 → F0325.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0324 · callback this.idle** — `index.html:L4135–4135` · ArrowFunction · parent F0323.  
Ulaz: `—`.  
Trag tela: `{this.idleJob=null;this.cleanupOne();}`.  
Poziva: `this.cleanupOne` L4135 → F0325.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0325 · cleanupOne** — `index.html:L4139–4153` · MethodDeclaration · parent F0317.  
Ulaz: `—`.  
Trag tela: `{ if(this.active!=='island'||this.awaitingFirstMap||this.renderer.lost)return; const item=this.retiring.values().next(); if(item.done)return`.  
Poziva: `this.retiring.values().next` L4141 → —; `this.retiring.values` L4141 → —; `this.retiring.delete` L4144 → —; `this.renderer.releaseTexture` L4145 → —; `this.idle` L4148 → —; `this.setTimer` L4150 → —.  
Pozivaju: index.html:L4135 (F0324); index.html:L4136 (F0323); index.html:L4148 (F0326); index.html:L4150 (F0327).

**F0326 · callback this.idle** — `index.html:L4148–4148` · ArrowFunction · parent F0325.  
Ulaz: `—`.  
Trag tela: `{this.idleJob=null;this.cleanupOne();}`.  
Poziva: `this.cleanupOne` L4148 → F0325.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0327 · callback this.setTimer** — `index.html:L4150–4150` · ArrowFunction · parent F0325.  
Ulaz: `—`.  
Trag tela: `{this.timer=null;this.cleanupOne();}`.  
Poziva: `this.cleanupOne` L4150 → F0325.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0328 · stats** — `index.html:L4154–4157` · MethodDeclaration · parent F0317.  
Ulaz: `—`.  
Trag tela: `{ return {active:this.active,atlas:this.atlas,transitions:this.transitions,pendingGpuReleases:this.retiring.size, gpuReleases:this.released,`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### scenes — mapa, kolizije, prikaz

**F0329 · anonimna** — `index.html:L4162–4902` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const { defaultHomes, buildings, habitatPrice, weatherFor, trackAtlas, clip, WHEAT_FIELDS, wheatStage, reserveAt, reservoirCapacity }=modu`.  
Poziva: `newObstacleNames.entries` L4189 → —; `world` L4203 → F0330; `Object.freeze` L4235 → —; `Object.freeze` L4235 → —; `Object.freeze` L4271 → —; `Object.freeze` L4503 → —; `Set` L4592 → —; `islandBuildings.map` L4592 → —; `document.getElementById` L4593 → —; `scReservoirFx?.querySelector` L4595 → —; `document.querySelector` L4596 → —; `Array.from` L4695 → —; `Map` L4697 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0330 · world** — `index.html:L4166–4166` · ArrowFunction · parent F0329.  
Ulaz: `x, y, w`.  
Trag tela: `[(x-50)/1800,(y-120)/1800,w/1800]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L4203 (F0329).

**F0331 · mapView** — `index.html:L4195–4202` · FunctionDeclaration · parent F0329.  
Ulaz: `width, height, camera`.  
Trag tela: `{ // Native map aspect: never distort the island or change land via camera zoom. const ratio=1448/1086; const sizeX=Math.min(width*1.16,heig`.  
Poziva: `Math.min` L4198 → —.  
Pozivaju: index.html:L4619 (F0395); ~index.html:L7411 (F0896); ~index.html:L7414 (F0896); ~index.html:L7423 (F0897); ~index.html:L7493 (F0901).

**F0332 · baseIslandObjects** — `index.html:L4204–4221` · FunctionDeclaration · parent F0329.  
Ulaz: `s, now`.  
Trag tela: `{ // A building has a standing footprint ONLY after it has been constructed. // Build prices/level gates stay in the domain catalog; no ghos`.  
Poziva: `islandBuildings .filter(([screen])=>!buildings[screen]||s.built.includes(screen)) .map` L4207 → —; `islandBuildings .filter` L4207 → —; `[ ...facilities, ...WHEAT_FIELDS.filter((_,field)=>s.wheatBuilt?.includes(field)).map(level=>{const field=WHEAT_FIELDS.indexOf(level);return` L4210 → —; `WHEAT_FIELDS.filter((_,field)=>s.wheatBuilt?.includes(field)).map` L4212 → —; `WHEAT_FIELDS.filter` L4212 → —; `s.homes.map` L4217 → —.  
Pozivaju: index.html:L4225 (F0339); index.html:L4339 (F0354); index.html:L4361 (F0358); index.html:L4429 (F0370); index.html:L4452 (F0370); index.html:L4489 (F0377).

**F0333 · callback islandBuildings .filter** — `index.html:L4208–4208` · ArrowFunction · parent F0332.  
Ulaz: `[screen]`.  
Trag tela: `!buildings[screen]||s.built.includes(screen)`.  
Poziva: `s.built.includes` L4208 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0334 · callback islandBuildings .filter(([screen])=>!buildings[screen]||s.built.includes(screen)) .map** — `index.html:L4209–4209` · ArrowFunction · parent F0332.  
Ulaz: `[screen,name,x,y,w]`.  
Trag tela: `({asset:screen,screen,name,x,y,w,locked:false})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0335 · callback WHEAT_FIELDS.filter** — `index.html:L4212–4212` · ArrowFunction · parent F0332.  
Ulaz: `_, field`.  
Trag tela: `s.wheatBuilt?.includes(field)`.  
Poziva: `s.wheatBuilt?.includes` L4212 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0336 · callback WHEAT_FIELDS.filter((_,field)=>s.wheatBuilt?.includes(field)).map** — `index.html:L4212–4216` · ArrowFunction · parent F0332.  
Ulaz: `level`.  
Trag tela: `{const field=WHEAT_FIELDS.indexOf(level);return ({ asset:'wheat-'+(wheatStage(s,now,field)??'soil'),screen:'wheat',field, key:field===0?'whe`.  
Poziva: `WHEAT_FIELDS.indexOf` L4212 → —; `wheatStage` L4213 → ~F0067.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0337 · callback s.homes.map** — `index.html:L4217–4219` · ArrowFunction · parent F0332.  
Ulaz: `home`.  
Trag tela: `({asset:home.level>1?'habitat-'+home.level:'habitat',screen:'habitat', name:'Stanište',x:.20+home.slot*.14,y:.30+(home.slot%3)*.18,w:.1,id:h`.  
Poziva: `s.homes.indexOf` L4219 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0338 · callback [ ...facilities, ...WHEAT_FIELDS.filter((_,field)=>s.wheatBuilt?.includes(field)).map(level=>{const field=WHEAT_FIELDS.indexOf(level);return** — `index.html:L4220–4220` · ArrowFunction · parent F0332.  
Ulaz: `o`.  
Trag tela: `({...o,key:o.key??(o.id?'home:'+o.id:o.screen)})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0339 · mapObjects** — `index.html:L4222–4229` · FunctionDeclaration · parent F0329.  
Ulaz: `s, now`.  
Trag tela: `{ if(s.islandLayout!==9){s=structuredClone(s);prepareIsland(s);} const positions=s.islandPositions; return baseIslandObjects(s,now) .filter(`.  
Poziva: `structuredClone` L4223 → —; `prepareIsland` L4223 → F0370; `baseIslandObjects(s,now) .filter(o=>o.screen!=='wheat'||!o.locked&&positions[o.key]) .map(o=>atPosition(o,o.pos??positions[o.key])) .sort` L4225 → —; `baseIslandObjects(s,now) .filter(o=>o.screen!=='wheat'||!o.locked&&positions[o.key]) .map` L4225 → —; `baseIslandObjects(s,now) .filter` L4225 → —; `baseIslandObjects` L4225 → F0332.  
Pozivaju: index.html:L4487 (F0377); ~index.html:L7011 (F0855).

**F0340 · callback baseIslandObjects(s,now) .filter** — `index.html:L4226–4226` · ArrowFunction · parent F0339.  
Ulaz: `o`.  
Trag tela: `o.screen!=='wheat'||!o.locked&&positions[o.key]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0341 · callback baseIslandObjects(s,now) .filter(o=>o.screen!=='wheat'||!o.locked&&positions[o.key]) .map** — `index.html:L4227–4227` · ArrowFunction · parent F0339.  
Ulaz: `o`.  
Trag tela: `atPosition(o,o.pos??positions[o.key])`.  
Poziva: `atPosition` L4227 → F0343.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0342 · callback baseIslandObjects(s,now) .filter(o=>o.screen!=='wheat'||!o.locked&&positions[o.key]) .map(o=>atPosition(o,o.pos??positions[o.key])) .sort** — `index.html:L4228–4228` · ArrowFunction · parent F0339.  
Ulaz: `a, b`.  
Trag tela: `a.y-b.y`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0343 · atPosition** — `index.html:L4230–4234` · FunctionDeclaration · parent F0329.  
Ulaz: `o, pos`.  
Trag tela: `{ if(!pos)return o; const [w,h]=footprint(o.key); return {...o,x:(pos[0]+w/2)/30,y:(pos[1]+h)/30}; }`.  
Poziva: `footprint` L4232 → F0346.  
Pozivaju: index.html:L4227 (F0341); index.html:L4342 (F0356); index.html:L4378 (F0358); index.html:L4384 (F0363); index.html:L4388 (F0358); index.html:L4677 (F0395).

**F0344 · structureType** — `index.html:L4279–4284` · FunctionDeclaration · parent F0329.  
Ulaz: `key`.  
Trag tela: `{ if(key.startsWith('new-building:'))return key.slice('new-building:'.length); if(key==='new-home'||key.startsWith('home:'))return 'habitat'`.  
Poziva: `key.startsWith` L4280 → —; `key.slice` L4280 → —; `key.startsWith` L4281 → —; `/^wheat(?::[1-4])?$|^new-wheat:[0-4]$/.test` L4282 → —.  
Pozivaju: index.html:L4287 (F0345); index.html:L4289 (F0346); index.html:L4341 (F0356); index.html:L4507 (F0382); index.html:L4508 (F0382); index.html:L4683 (F0395).

**F0345 · groundProfile** — `index.html:L4287–4287` · ArrowFunction · parent F0329.  
Ulaz: `key`.  
Trag tela: `SC_STRUCTURE[structureType(key)]??[1.45,1.1,.3,2,2]`.  
Poziva: `structureType` L4287 → F0344.  
Pozivaju: index.html:L4293 (F0347); index.html:L4309 (F0349); index.html:L4362 (F0359); index.html:L4362 (F0359).

**F0346 · footprint** — `index.html:L4288–4291` · ArrowFunction · parent F0329.  
Ulaz: `key`.  
Trag tela: `{ const profile=SC_STRUCTURE[structureType(key)]; return profile?[profile[3],profile[4]]:null; }`.  
Poziva: `structureType` L4289 → F0344.  
Pozivaju: index.html:L4232 (F0343); index.html:L4317 (F0353); index.html:L4366 (F0358); index.html:L4436 (F0370); index.html:L4457 (F0370); index.html:L4505 (F0382); index.html:L4528 (F0384); index.html:L4676 (F0395).

**F0347 · supportFootprint** — `index.html:L4292–4296` · FunctionDeclaration · parent F0329.  
Ulaz: `key, gx, gy`.  
Trag tela: `{ const [gw,gh,,vw,vh]=groundProfile(key); // Draw, touch and collision use the same sprite footprint and bottom anchor. return {x:gx+(vw-gw`.  
Poziva: `groundProfile` L4293 → F0345.  
Pozivaju: index.html:L4320 (F0353); index.html:L4328 (F0353); index.html:L4656 (F0395); index.html:L4669 (F0395); ~index.html:L7429 (F0897); ~index.html:L7448 (F0897); ~index.html:L7496 (F0901).

**F0348 · movable** — `index.html:L4300–4305` · FunctionDeclaration · parent F0329.  
Ulaz: `o, s`.  
Trag tela: `{ if(o.locked)return false; if(o.screen==='habitat'||o.screen==='wheat')return true; return ['incubator','crater','reservoir','expeditions',`.  
Poziva: `['incubator','crater','reservoir','expeditions','races','arena', 'shop','tree','pageant','breeding','timebreaker'].includes` L4303 → —.  
Pozivaju: index.html:L4487 (F0378); ~index.html:L7067 (F0865); ~index.html:L7857 (F0942).

**F0349 · clearance** — `index.html:L4309–4309` · FunctionDeclaration · parent F0329.  
Ulaz: `key`.  
Trag tela: `{return groundProfile(key)[2];}`.  
Poziva: `groundProfile` L4309 → F0345.  
Pozivaju: index.html:L4329 (F0353); index.html:L4329 (F0353).

**F0350 · overlapBox** — `index.html:L4310–4313` · FunctionDeclaration · parent F0329.  
Ulaz: `a, b, margin`.  
Trag tela: `{ return a.x < b.x+b.w+margin && a.x+a.w+margin > b.x && a.y < b.y+b.h+margin && a.y+a.h+margin > b.y; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L4329 (F0353).

**F0351 · reserve** — `index.html:L4314–4314` · FunctionDeclaration · parent F0329.  
Ulaz: `taken, key, [gx,gy]`.  
Trag tela: `{taken.push({key,gx,gy});}`.  
Poziva: `taken.push` L4314 → —.  
Pozivaju: index.html:L4369 (F0358); index.html:L4439 (F0370); index.html:L4467 (F0370); index.html:L4491 (F0377).

**F0352 · forbiddenCell** — `index.html:L4315–4315` · FunctionDeclaration · parent F0329.  
Ulaz: `x, y`.  
Trag tela: `{return FIELD.rows[y]?.[x]!=='f';}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L4325 (F0353).

**F0353 · fitsTerrain** — `index.html:L4316–4332` · FunctionDeclaration · parent F0329.  
Ulaz: `taken, key, gx, gy, s=null`.  
Trag tela: `{ const visual=footprint(key); if(!visual||!Number.isInteger(gx)||!Number.isInteger(gy)||gx<0||gy<0|| gx+visual[0]>30||gy+visual[1]>30)retur`.  
Poziva: `footprint` L4317 → F0346; `Number.isInteger` L4318 → —; `Number.isInteger` L4318 → —; `supportFootprint` L4320 → F0347; `Math.floor` L4321 → —; `Math.floor` L4321 → —; `Math.ceil` L4322 → —; `Math.ceil` L4322 → —; `forbiddenCell` L4325 → F0352; `supportFootprint` L4328 → F0347; `overlapBox` L4329 → F0350; `Math.max` L4329 → —; `clearance` L4329 → F0349; `clearance` L4329 → F0349.  
Pozivaju: index.html:L4347 (F0354); index.html:L4387 (F0358); index.html:L4461 (F0376); index.html:L4493 (F0380).

**F0354 · nearestFree** — `index.html:L4335–4358` · FunctionDeclaration · parent F0329.  
Ulaz: `taken, key, preferred, s`.  
Trag tela: `{ // Fresh or missing placements only: rank already-legal sites by visual clarity. // This is NOT another collision rule. Every candidate fi`.  
Poziva: `Map` L4339 → —; `baseIslandObjects(s,s.lastAt).map` L4339 → —; `baseIslandObjects` L4339 → F0332; `taken.map` L4344 → —; `fitsTerrain` L4347 → F0353; `artAt` L4348 → F0356; `scRectOverlap` L4350 → F0387.  
Pozivaju: index.html:L4368 (F0358); index.html:L4438 (F0370).

**F0355 · callback baseIslandObjects(s,s.lastAt).map** — `index.html:L4339–4339` · ArrowFunction · parent F0354.  
Ulaz: `o`.  
Trag tela: `[o.key,o]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0356 · artAt** — `index.html:L4340–4343` · ArrowFunction · parent F0354.  
Ulaz: `id, gx, gy`.  
Trag tela: `{ const obj=specs.get(id)??{key:id,asset:structureType(id)}; return mapRect(atPosition(obj,[gx,gy]),SC_NATIVE_VIEW,modules.frames.frames.isl`.  
Poziva: `specs.get` L4341 → —; `structureType` L4341 → F0344; `mapRect` L4342 → F0382; `atPosition` L4342 → F0343.  
Pozivaju: index.html:L4344 (F0357); index.html:L4348 (F0354).

**F0357 · callback taken.map** — `index.html:L4344–4344` · ArrowFunction · parent F0354.  
Ulaz: `o`.  
Trag tela: `artAt(o.key,o.gx,o.gy)`.  
Poziva: `artAt` L4344 → F0356.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0358 · buildLayout** — `index.html:L4359–4400` · FunctionDeclaration · parent F0329.  
Ulaz: `s`.  
Trag tela: `{ const taken=[],positions={}; const objects=baseIslandObjects(s,s.lastAt).sort((a,b)=>{ const pa=groundProfile(a.key),pb=groundProfile(b.ke`.  
Poziva: `baseIslandObjects(s,s.lastAt).sort` L4361 → —; `baseIslandObjects` L4361 → F0332; `footprint` L4366 → F0346; `Math.floor` L4367 → —; `Math.ceil` L4367 → —; `nearestFree` L4368 → F0354; `reserve` L4369 → F0351; `mapRect` L4378 → F0382; `atPosition` L4378 → F0343; `Object.entries(positions).filter(([id])=>id!==o.key) .map` L4380 → —; `Object.entries(positions).filter` L4380 → —; `Object.entries` L4380 → —; `Map` L4383 → —; `objects.map` L4383 → —; `occupied.map` L4384 → —; `fitsTerrain` L4387 → F0353; `mapRect` L4388 → F0382; `atPosition` L4388 → F0343; `scRectOverlap` L4392 → F0387.  
Pozivaju: index.html:L4446 (F0370).

**F0359 · callback baseIslandObjects(s,s.lastAt).sort** — `index.html:L4361–4364` · ArrowFunction · parent F0358.  
Ulaz: `a, b`.  
Trag tela: `{ const pa=groundProfile(a.key),pb=groundProfile(b.key); return pb[0]*pb[1]-pa[0]*pa[1]; // large buildings first }`.  
Poziva: `groundProfile` L4362 → F0345; `groundProfile` L4362 → F0345.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0360 · callback Object.entries(positions).filter** — `index.html:L4380–4380` · ArrowFunction · parent F0358.  
Ulaz: `[id]`.  
Trag tela: `id!==o.key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0361 · callback Object.entries(positions).filter(([id])=>id!==o.key) .map** — `index.html:L4381–4381` · ArrowFunction · parent F0358.  
Ulaz: `[id,[gx,gy]]`.  
Trag tela: `({key:id,gx,gy})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0362 · callback objects.map** — `index.html:L4383–4383` · ArrowFunction · parent F0358.  
Ulaz: `item`.  
Trag tela: `[item.key,item]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0363 · callback occupied.map** — `index.html:L4384–4384` · ArrowFunction · parent F0358.  
Ulaz: `item`.  
Trag tela: `mapRect(atPosition(specs.get(item.key),[item.gx,item.gy]),SC_NATIVE_VIEW,frames)`.  
Poziva: `mapRect` L4384 → F0382; `atPosition` L4384 → F0343; `specs.get` L4384 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0364 · ensureWheatBuilt** — `index.html:L4402–4410` · FunctionDeclaration · parent F0329.  
Ulaz: `s`.  
Trag tela: `{ if(Array.isArray(s.wheatBuilt))return; // Historical version had auto-generated farms. Keep the previously used farms // when wheat was ev`.  
Poziva: `Array.isArray` L4403 → —; `(s.wheatExtraReadyAt??[]).some` L4408 → —; `WHEAT_FIELDS.map((gate,i)=>s.level>=gate?i:-1).filter` L4409 → —; `WHEAT_FIELDS.map` L4409 → —.  
Pozivaju: index.html:L4423 (F0370).

**F0365 · callback (s.wheatExtraReadyAt??[]).some** — `index.html:L4408–4408` · ArrowFunction · parent F0364.  
Ulaz: `v`.  
Trag tela: `v>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0366 · callback WHEAT_FIELDS.map** — `index.html:L4409–4409` · ArrowFunction · parent F0364.  
Ulaz: `gate, i`.  
Trag tela: `s.level>=gate?i:-1`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0367 · callback WHEAT_FIELDS.map((gate,i)=>s.level>=gate?i:-1).filter** — `index.html:L4409–4409` · ArrowFunction · parent F0364.  
Ulaz: `i`.  
Trag tela: `i>=0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0368 · stripUnbuiltWheat** — `index.html:L4411–4415` · FunctionDeclaration · parent F0329.  
Ulaz: `s`.  
Trag tela: `{ for(let i=0;i<WHEAT_FIELDS.length;i++){ if(!s.wheatBuilt.includes(i))delete s.islandPositions?.[i?'wheat:'+i:'wheat']; } }`.  
Poziva: `s.wheatBuilt.includes` L4413 → —.  
Pozivaju: index.html:L4426 (F0370).

**F0369 · stripUnbuiltFacilities** — `index.html:L4416–4421` · FunctionDeclaration · parent F0329.  
Ulaz: `s`.  
Trag tela: `{ // Migration: remove ONLY legacy ghost coordinates. Existing built placements stay intact. for(const key of Object.keys(buildings)){ if(!s`.  
Poziva: `Object.keys` L4418 → —; `s.built.includes` L4419 → —.  
Pozivaju: index.html:L4424 (F0370).

**F0370 · prepareIsland** — `index.html:L4422–4471` · FunctionDeclaration · parent F0329.  
Ulaz: `s`.  
Trag tela: `{ ensureWheatBuilt(s); stripUnbuiltFacilities(s); if(s.islandLayout===9&&s.islandPositions){ stripUnbuiltWheat(s); // Legacy saves can mark `.  
Poziva: `ensureWheatBuilt` L4423 → F0364; `stripUnbuiltFacilities` L4424 → F0369; `stripUnbuiltWheat` L4426 → F0368; `baseIslandObjects` L4429 → F0332; `builtObjects.filter` L4430 → —; `Set` L4432 → —; `builtObjects.map` L4432 → —; `Object.entries(s.islandPositions).filter(([key,pos])=>active.has(key)&& Array.isArray(pos)&&pos.length===2).map` L4433 → —; `Object.entries(s.islandPositions).filter` L4433 → —; `Object.entries` L4433 → —; `footprint` L4436 → F0346; `Math.floor` L4437 → —; `Math.ceil` L4437 → —; `nearestFree` L4438 → F0354; `reserve` L4439 → F0351; `structuredClone` L4445 → —; `buildLayout` L4446 → F0358; `Set` L4452 → —; `baseIslandObjects(s,s.lastAt).map` L4452 → —; `baseIslandObjects` L4452 → F0332; `Set` L4453 → —; `Object.keys` L4453 → —; `Object.keys` L4453 → —; `active.has` L4454 → —; `Array.isArray` L4456 → —; `Array.isArray` L4457 → —; `footprint` L4457 → F0346; `/^wheat(?::[1-4])?$/.test` L4458 → —; `s.wheatBuilt?.includes` L4458 → —; `Number` L4458 → —; `key.slice` L4458 → —; `Array.isArray` L4465 → —; `trySite` L4465 → F0376; `trySite` L4466 → F0376; `reserve` L4467 → F0351.  
Pozivaju: index.html:L4223 (F0339); index.html:L4474 (F0377); ~index.html:L2699 (F0185); ~index.html:L3168 (F0185); ~index.html:L7749 (F0923); ~index.html:L7790 (F0924); ~index.html:L8334 (F0975).

**F0371 · callback builtObjects.filter** — `index.html:L4430–4430` · ArrowFunction · parent F0370.  
Ulaz: `o`.  
Trag tela: `!s.islandPositions[o.key]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0372 · callback builtObjects.map** — `index.html:L4432–4432` · ArrowFunction · parent F0370.  
Ulaz: `o`.  
Trag tela: `o.key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0373 · callback Object.entries(s.islandPositions).filter** — `index.html:L4433–4434` · ArrowFunction · parent F0370.  
Ulaz: `[key,pos]`.  
Trag tela: `active.has(key)&& Array.isArray(pos)&&pos.length===2`.  
Poziva: `active.has` L4433 → —; `Array.isArray` L4434 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0374 · callback Object.entries(s.islandPositions).filter(([key,pos])=>active.has(key)&& Array.isArray(pos)&&pos.length===2).map** — `index.html:L4434–4434` · ArrowFunction · parent F0370.  
Ulaz: `[key,[gx,gy]]`.  
Trag tela: `({key,gx,gy})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0375 · callback baseIslandObjects(s,s.lastAt).map** — `index.html:L4452–4452` · ArrowFunction · parent F0370.  
Ulaz: `o`.  
Trag tela: `o.key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0376 · trySite** — `index.html:L4460–4464` · ArrowFunction · parent F0370.  
Ulaz: `x, y`.  
Trag tela: `{ if(!fitsTerrain(taken,key,x,y,s))return; const d=(x-preferred[0])**2+(y-preferred[1])**2; if(d<bestDistance){best=[x,y];bestDistance=d;} }`.  
Poziva: `fitsTerrain` L4461 → F0353.  
Pozivaju: index.html:L4465 (F0370); index.html:L4466 (F0370).

**F0377 · placementRules** — `index.html:L4473–4494` · FunctionDeclaration · parent F0329.  
Ulaz: `s, now, key`.  
Trag tela: `{ if(s.islandLayout!==9){s=structuredClone(s);prepareIsland(s);} const building=key.startsWith('new-building:')?key.slice('new-building:'.le`.  
Poziva: `structuredClone` L4474 → —; `prepareIsland` L4474 → F0370; `key.startsWith` L4475 → —; `key.slice` L4475 → —; `/^new-wheat:([0-4])$/.exec` L4476 → —; `s.built.includes` L4479 → —; `Number` L4481 → —; `s.wheatBuilt?.includes` L4482 → —; `habitatPrice` L4485 → ~F0124; `mapObjects(s,now).some` L4487 → —; `mapObjects` L4487 → F0339; `Set` L4489 → —; `baseIslandObjects(s,now).map` L4489 → —; `baseIslandObjects` L4489 → F0332; `Object.entries` L4490 → —; `active.has` L4491 → —; `reserve` L4491 → F0351.  
Pozivaju: index.html:L4498 (F0381); ~index.html:L7864 (F0941).

**F0378 · callback mapObjects(s,now).some** — `index.html:L4487–4487` · ArrowFunction · parent F0377.  
Ulaz: `o`.  
Trag tela: `o.key===key&&movable(o,s)`.  
Poziva: `movable` L4487 → F0348.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0379 · callback baseIslandObjects(s,now).map** — `index.html:L4489–4489` · ArrowFunction · parent F0377.  
Ulaz: `o`.  
Trag tela: `o.key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0380 · anonimna** — `index.html:L4493–4493` · ArrowFunction · parent F0377.  
Ulaz: `gx, gy`.  
Trag tela: `fitsTerrain(taken,key,gx,gy,s)`.  
Poziva: `fitsTerrain` L4493 → F0353.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0381 · canPlace** — `index.html:L4496–4499` · FunctionDeclaration · parent F0329.  
Ulaz: `s, now, key, gx, gy`.  
Trag tela: `{ if(typeof key!=='string')return false; return placementRules(s,now,key)?.(gx,gy)??false; }`.  
Poziva: `placementRules(s,now,key)` L4498 → —; `placementRules` L4498 → F0377.  
Pozivaju: ~index.html:L2707 (F0185); ~index.html:L2907 (F0185); ~index.html:L2915 (F0185); ~index.html:L2924 (F0185).

**F0382 · mapRect** — `index.html:L4504–4521` · FunctionDeclaration · parent F0329.  
Ulaz: `obj, view, frames`.  
Trag tela: `{ const span=footprint(obj.key); if(span){ const crop=structureType(obj.key)==='wheat'; const width=span[0]*(crop?1.12:structureType(obj.key`.  
Poziva: `footprint` L4505 → F0346; `structureType` L4507 → F0344; `structureType` L4508 → F0344; `Math.min` L4513 → —.  
Pozivaju: index.html:L4342 (F0356); index.html:L4378 (F0358); index.html:L4384 (F0363); index.html:L4388 (F0358); index.html:L4529 (F0385); index.html:L4535 (F0386); index.html:L4680 (F0395).

**F0383 · scBuildVisualInstances** — `index.html:L4526–4532` · FunctionDeclaration · parent F0329.  
Ulaz: `objects, renderer`.  
Trag tela: `{ if(scVisualCache.objects===objects)return scVisualCache.rects; const rects=new Map(objects.filter(o=>o.name&&footprint(o.key)) .map(o=>[o.`.  
Poziva: `Map` L4528 → —; `objects.filter(o=>o.name&&footprint(o.key)) .map` L4528 → —; `objects.filter` L4528 → —.  
Pozivaju: index.html:L4626 (F0395); ~index.html:L7442 (F0897).

**F0384 · callback objects.filter** — `index.html:L4528–4528` · ArrowFunction · parent F0383.  
Ulaz: `o`.  
Trag tela: `o.name&&footprint(o.key)`.  
Poziva: `footprint` L4528 → F0346.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0385 · callback objects.filter(o=>o.name&&footprint(o.key)) .map** — `index.html:L4529–4529` · ArrowFunction · parent F0383.  
Ulaz: `o`.  
Trag tela: `[o.key,mapRect(o,SC_NATIVE_VIEW,renderer.atlas)]`.  
Poziva: `mapRect` L4529 → F0382.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0386 · scMapArtRect** — `index.html:L4533–4540` · FunctionDeclaration · parent F0329.  
Ulaz: `o, view, renderer, artRects`.  
Trag tela: `{ const rect=artRects?.get(o.key); if(!rect)return mapRect(o,view,renderer.atlas); return {x:view.x+rect.x*view.sizeX/SC_NATIVE_VIEW.sizeX, `.  
Poziva: `artRects?.get` L4534 → —; `mapRect` L4535 → F0382.  
Pozivaju: index.html:L4566 (F0390); index.html:L4635 (F0395); ~index.html:L7452 (F0897).

**F0387 · scRectOverlap** — `index.html:L4541–4545` · FunctionDeclaration · parent F0329.  
Ulaz: `a, b`.  
Trag tela: `{ const w=Math.max(0,Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)); const h=Math.max(0,Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)); return w`.  
Poziva: `Math.max` L4542 → —; `Math.min` L4542 → —; `Math.max` L4542 → —; `Math.max` L4543 → —; `Math.min` L4543 → —; `Math.max` L4543 → —.  
Pozivaju: index.html:L4350 (F0354); index.html:L4392 (F0358); index.html:L4577 (F0388); index.html:L4580 (F0388).

**F0388 · scPaintMapSigns** — `index.html:L4550–4589` · FunctionDeclaration · parent F0329.  
Ulaz: `renderer, labels, artRects, view`.  
Trag tela: `{ // The island's translation does not change relative distances between labels. // Cache in island-local coordinates and translate at paint`.  
Poziva: `[renderer.width,renderer.height,view.sizeX,view.sizeY].join` L4553 → —; `labels.every` L4556 → —; `renderer.sprite` L4559 → —; `Math.max` L4564 → —; `Math.min` L4564 → —; `labels.map` L4566 → —; `boxes.find` L4569 → —; `Math.max` L4574 → —; `Math.min` L4574 → —; `Math.max` L4575 → —; `Math.min` L4575 → —; `Math.abs` L4576 → —; `Math.abs` L4576 → —; `scRectOverlap` L4577 → F0387; `scRectOverlap` L4580 → F0387; `accepted.push` L4585 → —; `renderer.sprite` L4586 → —; `labels.map` L4588 → —.  
Pozivaju: index.html:L4653 (F0395).

**F0389 · callback labels.every** — `index.html:L4556–4556` · ArrowFunction · parent F0388.  
Ulaz: `o, i`.  
Trag tela: `o.key===cached.keys[i]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0390 · callback labels.map** — `index.html:L4566–4566` · ArrowFunction · parent F0388.  
Ulaz: `o`.  
Trag tela: `({key:o.key,rect:scMapArtRect(o.obj,localView,renderer,artRects)})`.  
Poziva: `scMapArtRect` L4566 → F0386.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0391 · callback boxes.find** — `index.html:L4569–4569` · ArrowFunction · parent F0388.  
Ulaz: `b`.  
Trag tela: `b.key===o.key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0392 · callback labels.map** — `index.html:L4588–4588` · ArrowFunction · parent F0388.  
Ulaz: `o`.  
Trag tela: `o.key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0393 · callback islandBuildings.map** — `index.html:L4592–4592` · ArrowFunction · parent F0329.  
Ulaz: `[key]`.  
Trag tela: `key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0394 · scUpdateReservoirFx** — `index.html:L4600–4614` · FunctionDeclaration · parent F0329.  
Ulaz: `s, now, rect=null`.  
Trag tela: `{ if(!scReservoirFx||!s)return; if(rect){ // Rect is taken from map rendering and changes on camera pan/zoom, not a second projection. scRes`.  
Poziva: `Math.max` L4606 → —; `Math.max` L4607 → —; `reservoirCapacity` L4609 → ~F0081; `Math.max` L4610 → —; `Math.min` L4610 → —; `reserveAt` L4610 → ~F0142.  
Pozivaju: index.html:L4648 (F0395); ~index.html:L7097 (F0871); ~index.html:L8241 (F0971).

**F0395 · paintMap** — `index.html:L4615–4693` · FunctionDeclaration · parent F0329.  
Ulaz: `renderer, s, camera, objects, now, editor`.  
Trag tela: `{ const phase=weatherFor(s,now).hour,night=phase==='night'; if(!renderer.begin('island',night?'#151739':'#71a7a5'))return false; renderer.dr`.  
Poziva: `weatherFor` L4616 → ~F0134; `renderer.begin` L4617 → —; `renderer.drawSky` L4618 → —; `mapView` L4619 → F0331; `renderer.drawIllustratedMap` L4622 → —; `renderer.flush` L4623 → —; `scBuildVisualInstances` L4626 → F0383; `SC_RENDER_BUILDING_KEYS.has` L4633 → —; `scMapArtRect` L4635 → F0386; `SC_RENDER_BUILDING_KEYS.has` L4638 → —; `labels.push` L4640 → —; `independent.push` L4645 → —; `scUpdateReservoirFx` L4648 → F0394; `independent.sort` L4650 → —; `renderer.drawDetachedObjects` L4651 → —; `scPaintMapSigns` L4653 → F0388; `supportFootprint` L4656 → F0347; `Math.floor` L4662 → —; `renderer.fill` L4663 → —; `Math.max` L4664 → —; `Math.max` L4664 → —; `supportFootprint` L4669 → F0347; `renderer.fill` L4671 → —; `editor.fits` L4672 → —; `editor.fits` L4674 → —; `objects.find` L4675 → —; `footprint` L4676 → F0346; `atPosition` L4677 → F0343; `mapRect` L4680 → F0382; `editor.key.startsWith` L4683 → —; `structureType` L4683 → F0344; `renderer.drawDetachedObjects` L4685 → —; `renderer.drawDetachedObjects` L4687 → —; `renderer.sprite` L4688 → —; `renderer.flush` L4691 → —.  
Pozivaju: ~index.html:L7390 (F0894).

**F0396 · callback independent.sort** — `index.html:L4650–4650` · ArrowFunction · parent F0395.  
Ulaz: `a, b`.  
Trag tela: `(a.y+a.h)-(b.y+b.h)`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0397 · callback objects.find** — `index.html:L4675–4675` · ArrowFunction · parent F0395.  
Ulaz: `o`.  
Trag tela: `o.key===editor.key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0398 · callback Array.from** — `index.html:L4695–4695` · ArrowFunction · parent F0329.  
Ulaz: `—`.  
Trag tela: `[0,0,0]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0399 · roadPalette** — `index.html:L4698–4704` · FunctionDeclaration · parent F0329.  
Ulaz: `renderer, course, key`.  
Trag tela: `{ if(!roadPalettes.has(key)){ roadPalettes.set(key,Array.from({length:roadSteps+1},(_,i)=> renderer.tint(key==='meadow'?'#efd0a0':course.roa`.  
Poziva: `roadPalettes.has` L4699 → —; `roadPalettes.set` L4700 → —; `Array.from` L4700 → —; `roadPalettes.get` L4703 → —.  
Pozivaju: index.html:L4740 (F0404).

**F0400 · callback Array.from** — `index.html:L4700–4701` · ArrowFunction · parent F0399.  
Ulaz: `_, i`.  
Trag tela: `renderer.tint(key==='meadow'?'#efd0a0':course.road[0],key==='meadow'?'#e3b181':course.road[1],i/roadSteps*.8)`.  
Poziva: `renderer.tint` L4701 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0401 · laneSelect** — `index.html:L4705–4708` · FunctionDeclaration · parent F0329.  
Ulaz: `project, y, lane`.  
Trag tela: `{ const [center,half]=project.row(y); return center+(lane-1.5)*half/2*project.direction; }`.  
Poziva: `project.row` L4706 → —.  
Pozivaju: index.html:L4771 (F0404); index.html:L4771 (F0404).

**F0402 · segment** — `index.html:L4709–4711` · FunctionDeclaration · parent F0329.  
Ulaz: `r, a, b, x1, x2, w1, w2, ink, alpha=1, bottom=ink, bottomAlpha=alpha`.  
Trag tela: `{ r.quad(x1-w1,a,x1+w1,a,x2+w2,b,x2-w2,b,null,ink,alpha,false,bottom,bottomAlpha); }`.  
Poziva: `r.quad` L4710 → —.  
Pozivaju: index.html:L4770 (F0404); index.html:L4825 (F0404); index.html:L4836 (F0404).

**F0403 · paintLine** — `index.html:L4712–4726` · FunctionDeclaration · parent F0329.  
Ulaz: `renderer, projection, distance, height`.  
Trag tela: `{ const leading=projection.at(distance,1.5); if(!leading||leading.y>height+30||leading.scale<.045)return; for(let rank=0;rank<2;rank++){ con`.  
Poziva: `projection.at` L4713 → —; `projection.at` L4716 → —; `projection.at` L4717 → —; `projection.row` L4719 → —; `projection.row` L4719 → —; `renderer.quad` L4722 → —.  
Pozivaju: index.html:L4851 (F0404); index.html:L4852 (F0404).

**F0404 · paintRace** — `index.html:L4735–4898` · FunctionDeclaration · parent F0329.  
Ulaz: `renderer, race, motion=true`.  
Trag tela: `{ const {width:w,height:h}=renderer, course=race.course; if(!renderer.begin(trackAtlas(race.key),course.sky))return false; const projection=`.  
Poziva: `renderer.begin` L4737 → —; `trackAtlas` L4737 → ~F0072; `createProjection` L4738 → ~F0260; `roadPalette` L4740 → F0399; `Math.max` L4745 → —; `Math.sin` L4746 → —; `renderer.gradient` L4747 → —; `Math.sin` L4749 → —; `renderer.sprite` L4750 → —; `renderer.sprite` L4752 → —; `Math.sin` L4754 → —; `renderer.sprite` L4755 → —; `row` L4759 → —; `renderer.roadStrip` L4762 → —; `renderer.roadStrip` L4763 → —; `Math.max` L4764 → —; `Math.ceil` L4764 → —; `Math.min` L4765 → —; `Math.max` L4766 → —; `Math.ceil` L4766 → —; `Math.min` L4767 → —; `projection.at` L4768 → —; `projection.at` L4768 → —; `Math.abs` L4769 → —; `segment` L4770 → F0402; `laneSelect` L4771 → F0401; `laneSelect` L4771 → F0401; `Math.min` L4772 → —; `Math.floor` L4776 → —; `projection.at` L4779 → —; `Math.floor` L4782 → —; `Math.floor` L4783 → —; `Math.min` L4785 → —; `Math.min` L4788 → —; `Math.sin` L4790 → —; `renderer.sprite` L4791 → —; `projection.at` L4793 → —; `projection.at` L4795 → —; `renderer.quad` L4799 → —; `renderer.fill` L4803 → —; `renderer.fill` L4804 → —; `Math.max` L4809 → —; `Math.min` L4809 → —; `Math.ceil` L4810 → —; `Math.round` L4811 → —; `projection.at` L4812 → —; `Math.min` L4814 → —; `Math.sin` L4815 → —; `renderer.sprite` L4816 → —; `Math.min` L4816 → —; `projection.at` L4823 → —; `projection.at` L4823 → —; `Math.min` L4824 → —; `segment` L4825 → F0402; `race.players.slice` L4828 → —; `projection.at` L4834 → —; `projection.at` L4834 → —; `Math.min` L4835 → —; `segment` L4836 → F0402; `projection.at` L4841 → —; `Math.min` L4843 → —; `renderer.quad` L4844 → —; `renderer.quad` L4846 → —; `renderer.fill` L4848 → —; `Math.max` L4848 → —; `paintLine` L4851 → F0403; `paintLine` L4852 → F0403; `projection.at` L4858 → —; `players.push` L4860 → —; `players.sort` L4862 → —; `Math.min` L4864 → —; `Math.min` L4864 → —; `renderer.shadow` L4867 → —; `clip` L4869 → ~F0093; `clip` L4870 → ~F0093; `renderer.spriteTurned` L4873 → —; `renderer.sprite` L4874 → —; `clip` L4876 → ~F0093; `Math.cos` L4876 → —; `Math.sin` L4876 → —; `path.slice(1).map` L4879 → —; `path.slice` L4879 → —; `path.slice(1).map` L4879 → —; `path.slice` L4879 → —; `at` L4880 → F0406; `at` L4880 → F0406; `renderer.line` L4880 → —; `renderer.quad` L4883 → —; `projection.at` L4889 → —; `Math.min` L4890 → —; `Math.min` L4890 → —; `renderer.line` L4893 → —; `Math.cos` L4893 → —; `Math.sin` L4893 → —; `Math.cos` L4893 → —; `Math.sin` L4893 → —; `renderer.flush` L4896 → —.  
Pozivaju: ~index.html:L7353 (F0894); ~index.html:L7407 (F0894).

**F0405 · callback players.sort** — `index.html:L4862–4862` · ArrowFunction · parent F0404.  
Ulaz: `a, b`.  
Trag tela: `a[1].y-b[1].y`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0406 · at** — `index.html:L4877–4877` · ArrowFunction · parent F0404.  
Ulaz: `x, y`.  
Trag tela: `[pose.x+x*u*c-y*u*sn,footY+x*u*sn+y*u*c]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L4880 (F0404); index.html:L4880 (F0404).

**F0407 · callback path.slice(1).map** — `index.html:L4879–4879` · ArrowFunction · parent F0404.  
Ulaz: `q, i`.  
Trag tela: `[path[i],q]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0408 · callback path.slice(1).map** — `index.html:L4879–4879` · ArrowFunction · parent F0404.  
Ulaz: `q, i`.  
Trag tela: `[path[i],q]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### storage — validacija, migracija, save adapteri

**F0409 · anonimna** — `index.html:L4903–5403` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const { AUTO_HOME_STATS }=modules.domain; const { FORMAT, newGame, dayKey, makeDaily, buildings, species, tracks, capacity, clip, expediti`.  
Poziva: `Set` L4916 → —; `Map` L5210 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0410 · int** — `index.html:L4910–4910` · ArrowFunction · parent F0409.  
Ulaz: `value, fallback, min=0, max=1e12`.  
Trag tela: `Number.isFinite(Number(value))?clip(Math.floor(Number(value)),min,max):fallback`.  
Poziva: `Number.isFinite` L4910 → —; `Number` L4910 → —; `clip` L4910 → ~F0093; `Math.floor` L4910 → —; `Number` L4910 → —.  
Pozivaju: index.html:L4913 (F0413); index.html:L5078 (F0463); index.html:L5079 (F0463); index.html:L5079 (F0463); index.html:L5081 (F0463); index.html:L5081 (F0463); index.html:L5081 (F0463); index.html:L5081 (F0463); index.html:L5082 (F0463); index.html:L5082 (F0463); index.html:L5083 (F0463); index.html:L5084 (F0463); index.html:L5084 (F0463); index.html:L5084 (F0463); index.html:L5085 (F0463); index.html:L5085 (F0463); index.html:L5085 (F0463); index.html:L5086 (F0463); index.html:L5086 (F0463); index.html:L5097 (F0466); index.html:L5115 (F0468); index.html:L5127 (F0474); index.html:L5136 (F0474); index.html:L5136 (F0474); index.html:L5143 (F0464); index.html:L5148 (F0464); index.html:L5148 (F0464); index.html:L5151 (F0464); index.html:L5151 (F0464); index.html:L5153 (F0464); index.html:L5157 (F0477); index.html:L5160 (F0464); index.html:L5160 (F0464); index.html:L5161 (F0464); index.html:L5164 (F0464); index.html:L5167 (F0464); index.html:L5174 (F0464); index.html:L5178 (F0464); index.html:L5178 (F0464); index.html:L5180 (F0464); index.html:L5181 (F0464); index.html:L5181 (F0464); index.html:L5184 (F0464); index.html:L5185 (F0464); index.html:L5185 (F0464).

**F0411 · number** — `index.html:L4911–4911` · ArrowFunction · parent F0409.  
Ulaz: `value, fallback, min=0, max=1e12`.  
Trag tela: `Number.isFinite(Number(value))?clip(Number(value),min,max):fallback`.  
Poziva: `Number.isFinite` L4911 → —; `Number` L4911 → —; `clip` L4911 → ~F0093; `Number` L4911 → —.  
Pozivaju: index.html:L5082 (F0463); index.html:L5087 (F0463); index.html:L5087 (F0463); index.html:L5087 (F0463); index.html:L5087 (F0463); index.html:L5126 (F0474); index.html:L5132 (F0474); index.html:L5143 (F0464).

**F0412 · idOk** — `index.html:L4912–4912` · ArrowFunction · parent F0409.  
Ulaz: `v`.  
Trag tela: `typeof v==='string'&&/^[A-Za-z0-9_-]{1,100}$/.test(v)`.  
Poziva: `/^[A-Za-z0-9_-]{1,100}$/.test` L4912 → —.  
Pozivaju: index.html:L4919 (F0416); index.html:L4959 (F0425); index.html:L4980 (F0431); index.html:L5010 (F0441); index.html:L5018 (F0442); index.html:L5019 (F0442); index.html:L5043 (F0451); index.html:L5051 (F0425); index.html:L5060 (F0459).

**F0413 · epoch** — `index.html:L4913–4913` · ArrowFunction · parent F0409.  
Ulaz: `v`.  
Trag tela: `int(v,0,0,1e14)`.  
Poziva: `int` L4913 → F0410.  
Pozivaju: index.html:L4944 (F0423); index.html:L4965 (F0425); index.html:L4976 (F0429); index.html:L4989 (F0434); index.html:L4990 (F0425); index.html:L5008 (F0440); index.html:L5010 (F0441); index.html:L5012 (F0441); index.html:L5039 (F0425); index.html:L5040 (F0425); index.html:L5040 (F0425); index.html:L5130 (F0474); index.html:L5130 (F0474); index.html:L5161 (F0464); index.html:L5162 (F0464); index.html:L5162 (F0464); index.html:L5163 (F0464); index.html:L5164 (F0464).

**F0414 · arrayOk** — `index.html:L4914–4914` · ArrowFunction · parent F0409.  
Ulaz: `a, max`.  
Trag tela: `Array.isArray(a)&&a.length<=max`.  
Poziva: `Array.isArray` L4914 → —.  
Pozivaju: index.html:L4945 (F0421); index.html:L4979 (F0425); index.html:L4992 (F0425); index.html:L4992 (F0425); index.html:L4992 (F0425); index.html:L4996 (F0425); index.html:L4997 (F0425); index.html:L4998 (F0425); index.html:L5008 (F0425); index.html:L5010 (F0425); index.html:L5021 (F0425); index.html:L5021 (F0425); index.html:L5059 (F0425); index.html:L5059 (F0425); index.html:L5091 (F0464); index.html:L5091 (F0464); index.html:L5091 (F0464); index.html:L5094 (F0464); index.html:L5108 (F0468).

**F0415 · assert** — `index.html:L4915–4915` · ArrowFunction · parent F0409.  
Ulaz: `ok, m='Sejv je oštećen ili koristi nepodržan format.'`.  
Trag tela: `{if(!ok)throw Error(m);}`.  
Poziva: `Error` L4915 → —.  
Pozivaju: index.html:L4919 (F0416); index.html:L4920 (F0416); index.html:L4921 (F0416); index.html:L4922 (F0416); index.html:L4923 (F0416); index.html:L4924 (F0416); index.html:L4925 (F0416); index.html:L4926 (F0416); index.html:L4927 (F0416); index.html:L4928 (F0416); index.html:L4929 (F0416); index.html:L4931 (F0416); index.html:L4940 (F0421); index.html:L4942 (F0421); index.html:L4943 (F0421); index.html:L4945 (F0421); index.html:L4947 (F0421); index.html:L4948 (F0421); index.html:L4949 (F0421); index.html:L4951 (F0421); index.html:L4952 (F0421); index.html:L4953 (F0421); index.html:L4955 (F0421); index.html:L4959 (F0425); index.html:L4964 (F0425); index.html:L4965 (F0425); index.html:L4967 (F0425); index.html:L4968 (F0425); index.html:L4972 (F0425); index.html:L4973 (F0425); index.html:L4975 (F0425); index.html:L4976 (F0425); index.html:L4979 (F0425); index.html:L4980 (F0425); index.html:L4983 (F0425); index.html:L4984 (F0425); index.html:L4986 (F0425); index.html:L4987 (F0425); index.html:L4988 (F0425); index.html:L4990 (F0425); index.html:L4991 (F0425); index.html:L4992 (F0425); index.html:L4993 (F0425); index.html:L4994 (F0425); index.html:L4995 (F0425); index.html:L4996 (F0425); index.html:L4997 (F0425); index.html:L4998 (F0425); index.html:L4999 (F0425); index.html:L5000 (F0425); index.html:L5003 (F0425); index.html:L5005 (F0425); index.html:L5006 (F0425); index.html:L5007 (F0425); index.html:L5008 (F0425); index.html:L5010 (F0425); index.html:L5017 (F0425); index.html:L5021 (F0425); index.html:L5023 (F0425); index.html:L5024 (F0425); index.html:L5025 (F0425); index.html:L5027 (F0425); index.html:L5029 (F0425); index.html:L5030 (F0425); index.html:L5033 (F0425); index.html:L5034 (F0425); index.html:L5035 (F0425); index.html:L5037 (F0425); index.html:L5038 (F0425); index.html:L5039 (F0425); index.html:L5040 (F0425); index.html:L5043 (F0425); index.html:L5045 (F0425); index.html:L5047 (F0425); index.html:L5047 (F0425); index.html:L5048 (F0425); index.html:L5049 (F0425); index.html:L5051 (F0425); index.html:L5052 (F0425); index.html:L5053 (F0425); index.html:L5054 (F0425); index.html:L5056 (F0425); index.html:L5057 (F0425); index.html:L5059 (F0425); index.html:L5060 (F0425); index.html:L5062 (F0425); index.html:L5065 (F0425); index.html:L5091 (F0464); index.html:L5093 (F0464); index.html:L5094 (F0464); index.html:L5098 (F0464); index.html:L5107 (F0468); index.html:L5112 (F0469); index.html:L5117 (F0464); index.html:L5122 (F0464); index.html:L5135 (F0474); index.html:L5192 (F0482); index.html:L5340 (F0517).

**F0416 · checkSnail** — `index.html:L4918–4933` · FunctionDeclaration · parent F0409.  
Ulaz: `n`.  
Trag tela: `{ assert(n&&idOk(n.id)&&species[n.species]&&Number.isInteger(n.cls)&&n.cls>=0&&n.cls<=8); assert(typeof n.name==='string'&&n.name.length<=80`.  
Poziva: `assert` L4919 → F0415; `idOk` L4919 → F0412; `Number.isInteger` L4919 → —; `assert` L4920 → F0415; `validTrail.has` L4920 → —; `assert` L4921 → F0415; `['hp','atk','speed','weight','prod','beauty','polish'].every` L4921 → —; `assert` L4922 → F0415; `assert` L4923 → F0415; `Number.isInteger` L4923 → —; `assert` L4924 → F0415; `Number.isInteger` L4924 → —; `assert` L4925 → F0415; `Number.isFinite` L4925 → —; `assert` L4926 → F0415; `Number.isFinite` L4926 → —; `assert` L4927 → F0415; `Number.isSafeInteger` L4927 → —; `assert` L4928 → F0415; `Number.isInteger` L4928 → —; `assert` L4929 → F0415; `inheritedTrait` L4929 → ~F0036; `assert` L4931 → F0415; `['hp','atk','speed','prod'].every` L4931 → —.  
Pozivaju: index.html:L5047 (F0425).

**F0417 · callback ['hp','atk','speed','weight','prod','beauty','polish'].every** — `index.html:L4921–4921` · ArrowFunction · parent F0416.  
Ulaz: `k`.  
Trag tela: `Number.isFinite(n[k])&&n[k]>=0&&n[k]<=1e6`.  
Poziva: `Number.isFinite` L4921 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0418 · callback ['hp','atk','speed','prod'].every** — `index.html:L4931–4931` · ArrowFunction · parent F0416.  
Ulaz: `key`.  
Trag tela: `Number.isFinite(n.baseStats[key])&&n.baseStats[key]>=0&&n.baseStats[key]<=1e6`.  
Poziva: `Number.isFinite` L4931 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0419 · checkRecords** — `index.html:L4934–4937` · FunctionDeclaration · parent F0409.  
Ulaz: `records`.  
Trag tela: `{ return records&&typeof records==='object'&&Object.entries(records).every(([k,v])=> Object.hasOwn(tracks,k)&&v&&Number.isFinite(v.seconds)&`.  
Poziva: `Object.entries(records).every` L4935 → —; `Object.entries` L4935 → —.  
Pozivaju: index.html:L4999 (F0425); index.html:L4999 (F0425).

**F0420 · callback Object.entries(records).every** — `index.html:L4935–4936` · ArrowFunction · parent F0419.  
Ulaz: `[k,v]`.  
Trag tela: `Object.hasOwn(tracks,k)&&v&&Number.isFinite(v.seconds)&&v.seconds>=0&&[1,2,3,4].includes(v.place)`.  
Poziva: `Object.hasOwn` L4936 → —; `Number.isFinite` L4936 → —; `[1,2,3,4].includes` L4936 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0421 · checkSeason** — `index.html:L4938–4957` · FunctionDeclaration · parent F0409.  
Ulaz: `season`.  
Trag tela: `{ const integer=(value,max)=>Number.isSafeInteger(value)&&value>=0&&value<=max; assert(season&&integer(season.week,1e8)&&integer(season.day,`.  
Poziva: `assert` L4940 → F0415; `integer` L4940 → F0422; `integer` L4940 → F0422; `integer` L4940 → F0422; `integer` L4941 → F0422; `integer` L4941 → F0422; `integer` L4941 → F0422; `assert` L4942 → F0415; `integer` L4942 → F0422; `assert` L4943 → F0415; `Object.entries(season.slizBought).every` L4943 → —; `Object.entries` L4943 → —; `assert` L4945 → F0415; `arrayOk` L4945 → F0414; `Set` L4945 → —; `season.missions.every` L4946 → —; `assert` L4947 → F0415; `integer` L4947 → F0422; `assert` L4948 → F0415; `assert` L4949 → F0415; `integer` L4949 → F0422; `assert` L4951 → F0415; `integer` L4951 → F0422; `assert` L4952 → F0415; `integer` L4952 → F0422; `assert` L4953 → F0415; `integer` L4953 → F0422; `assert` L4955 → F0415; `integer` L4955 → F0422; `integer` L4955 → F0422; `integer` L4956 → F0422.  
Pozivaju: index.html:L5002 (F0425).

**F0422 · integer** — `index.html:L4939–4939` · ArrowFunction · parent F0421.  
Ulaz: `value, max`.  
Trag tela: `Number.isSafeInteger(value)&&value>=0&&value<=max`.  
Poziva: `Number.isSafeInteger` L4939 → —.  
Pozivaju: index.html:L4940 (F0421); index.html:L4940 (F0421); index.html:L4940 (F0421); index.html:L4941 (F0421); index.html:L4941 (F0421); index.html:L4941 (F0421); index.html:L4942 (F0421); index.html:L4947 (F0421); index.html:L4949 (F0421); index.html:L4951 (F0421); index.html:L4952 (F0421); index.html:L4953 (F0421); index.html:L4955 (F0421); index.html:L4955 (F0421); index.html:L4956 (F0421).

**F0423 · callback Object.entries(season.slizBought).every** — `index.html:L4943–4944` · ArrowFunction · parent F0421.  
Ulaz: `[key,at]`.  
Trag tela: `key.startsWith('sliz')&&Object.hasOwn(exchanges,key)&&at===epoch(at)`.  
Poziva: `key.startsWith` L4944 → —; `Object.hasOwn` L4944 → —; `epoch` L4944 → F0413.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0424 · callback season.missions.every** — `index.html:L4946–4946` · ArrowFunction · parent F0421.  
Ulaz: `key`.  
Trag tela: `['race','arena','polish','expedition'].includes(key)`.  
Poziva: `['race','arena','polish','expedition'].includes` L4946 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0425 · validateSave** — `index.html:L4958–5071` · FunctionDeclaration · parent F0409.  
Ulaz: `s`.  
Trag tela: `{ assert(s?.format===FORMAT&&s.schemaVersion===1&&idOk(s.saveId)); if(s.islandLayout!==undefined&&!Number.isInteger(s.islandLayout)) throw E`.  
Poziva: `assert` L4959 → F0415; `idOk` L4959 → F0412; `Number.isInteger` L4960 → —; `Error` L4961 → —; `Error` L4963 → —; `assert` L4964 → F0415; `Number.isSafeInteger` L4964 → —; `assert` L4965 → F0415; `Number.isFinite` L4965 → —; `epoch` L4965 → F0413; `assert` L4967 → F0415; `Array.isArray` L4967 → —; `assert` L4968 → F0415; `Object.entries(s.islandPositions).every` L4968 → —; `Object.entries` L4968 → —; `assert` L4972 → F0415; `[1,2,3,4,5,6,7,8,9].includes` L4972 → —; `Boolean` L4972 → —; `assert` L4973 → F0415; `Number.isSafeInteger` L4973 → —; `assert` L4975 → F0415; `Array.isArray` L4975 → —; `assert` L4976 → F0415; `Object.entries(s.gardenJobs).every` L4976 → —; `Object.entries` L4976 → —; `assert` L4979 → F0415; `arrayOk` L4979 → F0414; `Set` L4979 → —; `s.gardenDecor.map` L4979 → —; `assert` L4980 → F0415; `s.gardenDecor.every` L4980 → —; `assert` L4983 → F0415; `Number.isFinite` L4983 → —; `assert` L4984 → F0415; `Array.isArray` L4984 → —; `Set` L4985 → —; `s.wheatBuilt.every` L4985 → —; `assert` L4986 → F0415; `Number.isInteger` L4986 → —; `assert` L4987 → F0415; `Number.isSafeInteger` L4987 → —; `assert` L4988 → F0415; `Array.isArray` L4988 → —; `s.wheatExtraReadyAt.every` L4989 → —; `assert` L4990 → F0415; `Number.isSafeInteger` L4990 → —; `epoch` L4990 → F0413; `assert` L4991 → F0415; `saveFields.every` L4991 → —; `Number.isInteger` L4991 → —; `assert` L4992 → F0415; `arrayOk` L4992 → F0414; `arrayOk` L4992 → F0414; `arrayOk` L4992 → F0414; `assert` L4993 → F0415; `assert` L4994 → F0415; `AUTO_HOME_STATS.includes` L4994 → —; `assert` L4995 → F0415; `s.eggs.filter` L4995 → —; `assert` L4996 → F0415; `arrayOk` L4996 → F0414; `s.built.every` L4996 → —; `assert` L4997 → F0415; `arrayOk` L4997 → F0414; `s.seen.every` L4997 → —; `assert` L4998 → F0415; `arrayOk` L4998 → F0414; `s.completed.every` L4998 → —; `assert` L4999 → F0415; `checkRecords` L4999 → F0419; `Object.hasOwn` L4999 → —; `checkRecords` L4999 → F0419; `assert` L5000 → F0415; `Array.isArray` L5000 → —; `Object.entries(s.tutorial).every` L5001 → —; `Object.entries` L5001 → —; `checkSeason` L5002 → F0421; `assert` L5003 → F0415; `Number.isInteger` L5003 → —; `s.seen.includes` L5003 → —; `assert` L5005 → F0415; `Number.isSafeInteger` L5005 → —; `assert` L5006 → F0415; `assert` L5007 → F0415; `assert` L5008 → F0415; `arrayOk` L5008 → F0414; `s.museum.every` L5008 → —; `assert` L5010 → F0415; `arrayOk` L5010 → F0414; `s.expeditions.every` L5010 → —; `assert` L5017 → F0415; `Array.isArray` L5017 → —; `e.originalHomes.every` L5018 → —; `assert` L5021 → F0415; `Number.isInteger` L5021 → —; `arrayOk` L5021 → F0414; `arrayOk` L5021 → F0414; `assert` L5023 → F0415; `[...s.daily.keys,...s.daily.claimed,...Object.keys(s.daily.counts)].every` L5023 → —; `Object.keys` L5023 → —; `assert` L5024 → F0415; `['races','pageants','arena'].every` L5024 → —; `assert` L5025 → F0415; `Object.values(s.daily.counts).every` L5025 → —; `Object.values` L5025 → —; `assert` L5027 → F0415; `Array.isArray` L5027 → —; `Object.entries` L5028 → —; `assert` L5029 → F0415; `values.every` L5029 → —; `assert` L5030 → F0415; `values.reduce` L5030 → —; `assert` L5033 → F0415; `Number.isInteger` L5033 → —; `assert` L5034 → F0415; `Number.isSafeInteger` L5034 → —; `assert` L5035 → F0415; `Number.isInteger` L5035 → —; `assert` L5037 → F0415; `Number.isSafeInteger` L5037 → —; `assert` L5038 → F0415; `assert` L5039 → F0415; `epoch` L5039 → F0413; `assert` L5040 → F0415; `epoch` L5040 → F0413; `epoch` L5040 → F0413; `Number.isInteger` L5041 → —; `Set` L5042 → —; `s.homes.map` L5042 → —; `Set` L5042 → —; `s.homes.map` L5042 → —; `assert` L5043 → F0415; `s.homes.every` L5043 → —; `assert` L5045 → F0415; `unique` L5045 → F0452; `unique` L5045 → F0452; `unique` L5045 → F0452; `Map` L5046 → —; `s.snails.map` L5046 → —; `checkSnail` L5047 → F0416; `assert` L5047 → F0415; `homes.has` L5047 → —; `assert` L5047 → F0415; `s.expeditions.some` L5047 → —; `assert` L5048 → F0415; `s.expeditions.every` L5048 → —; `assert` L5049 → F0415; `s.snails.filter` L5049 → —; `capacity` L5049 → ~F0077; `assert` L5051 → F0415; `idOk` L5051 → F0412; `Number.isInteger` L5051 → —; `Number.isFinite` L5051 → —; `assert` L5052 → F0415; `Boolean` L5052 → —; `assert` L5053 → F0415; `assert` L5054 → F0415; `Array.isArray` L5054 → —; `e.parents.forEach` L5054 → —; `assert` L5056 → F0415; `Number.isFinite` L5056 → —; `Number.isFinite` L5056 → —; `assert` L5057 → F0415; `Number.isFinite` L5057 → —; `assert` L5059 → F0415; `arrayOk` L5059 → F0414; `arrayOk` L5059 → F0414; `assert` L5060 → F0415; `[...s.arena.team,...s.arena.foes].every` L5060 → —; `assert` L5062 → F0415; `['win','loss',null].includes` L5062 → —; `Number.isSafeInteger` L5062 → —; `assert` L5065 → F0415; `['sliz','xp','diamonds'].every` L5066 → —; `Number.isSafeInteger` L5067 → —.  
Pozivaju: index.html:L5189 (F0464); index.html:L5195 (F0482); index.html:L5213 (F0485); ~index.html:L7196 (F0877); ~index.html:L7603 (F0908); ~index.html:L7751 (F0923); ~index.html:L7772 (F0924); ~index.html:L8061 (F0943); ~index.html:L8328 (F0975).

**F0426 · callback Object.entries(s.islandPositions).every** — `index.html:L4968–4970` · ArrowFunction · parent F0425.  
Ulaz: `[key,pos]`.  
Trag tela: `(/^(breeding|wheat(?::[1-4])?|prop:(?:[0-9]|1[0-5]))$/.test(key)||[1,2,3,4,5,6,7,8,9].includes(s.islandLayout)&&(Object.hasOwn(buildings,key`.  
Poziva: `/^(breeding|wheat(?::[1-4])?|prop:(?:[0-9]|1[0-5]))$/.test` L4969 → —; `[1,2,3,4,5,6,7,8,9].includes` L4969 → —; `Object.hasOwn` L4969 → —; `['reservoir','incubator','tree','shop','timebreaker','mine','fountain'].includes` L4969 → —; `Object.hasOwn` L4969 → —; `key.startsWith` L4969 → —; `s.homes?.some` L4969 → —; `Array.isArray` L4970 → —; `pos.every` L4970 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0427 · callback s.homes?.some** — `index.html:L4969–4969` · ArrowFunction · parent F0426.  
Ulaz: `h`.  
Trag tela: `'home:'+h.id===key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0428 · callback pos.every** — `index.html:L4970–4970` · ArrowFunction · parent F0426.  
Ulaz: `n`.  
Trag tela: `Number.isInteger(n)&&n>=0&&n<30`.  
Poziva: `Number.isInteger` L4970 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0429 · callback Object.entries(s.gardenJobs).every** — `index.html:L4976–4976` · ArrowFunction · parent F0425.  
Ulaz: `[key,value]`.  
Trag tela: `Object.hasOwn(modules.scenes.naturalProps,key)&&Number.isSafeInteger(value)&&value===epoch(value)`.  
Poziva: `Object.hasOwn` L4976 → —; `Number.isSafeInteger` L4976 → —; `epoch` L4976 → F0413.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0430 · callback s.gardenDecor.map** — `index.html:L4979–4979` · ArrowFunction · parent F0425.  
Ulaz: `o`.  
Trag tela: `o?.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0431 · callback s.gardenDecor.every** — `index.html:L4980–4981` · ArrowFunction · parent F0425.  
Ulaz: `o`.  
Trag tela: `o&&idOk(o.id)&&['bush','flowers','rock'].includes(o.kind)&& (o.pos===null||Array.isArray(o.pos)&&o.pos.length===2&&o.pos.every(n=>Number.isI`.  
Poziva: `idOk` L4980 → F0412; `['bush','flowers','rock'].includes` L4980 → —; `Array.isArray` L4981 → —; `o.pos.every` L4981 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0432 · callback o.pos.every** — `index.html:L4981–4981` · ArrowFunction · parent F0431.  
Ulaz: `n`.  
Trag tela: `Number.isInteger(n)&&n>=0&&n<30`.  
Poziva: `Number.isInteger` L4981 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0433 · callback s.wheatBuilt.every** — `index.html:L4985–4985` · ArrowFunction · parent F0425.  
Ulaz: `i`.  
Trag tela: `Number.isInteger(i)&&i>=0&&i<5`.  
Poziva: `Number.isInteger` L4985 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0434 · callback s.wheatExtraReadyAt.every** — `index.html:L4989–4989` · ArrowFunction · parent F0425.  
Ulaz: `t`.  
Trag tela: `Number.isSafeInteger(t)&&t===epoch(t)`.  
Poziva: `Number.isSafeInteger` L4989 → —; `epoch` L4989 → F0413.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0435 · callback saveFields.every** — `index.html:L4991–4991` · ArrowFunction · parent F0425.  
Ulaz: `k`.  
Trag tela: `Number.isFinite(s[k])&&s[k]>=0&&s[k]<=1e12`.  
Poziva: `Number.isFinite` L4991 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0436 · callback s.eggs.filter** — `index.html:L4995–4995` · ArrowFunction · parent F0425.  
Ulaz: `e`.  
Trag tela: `e?.kind===8`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0437 · callback s.built.every** — `index.html:L4996–4996` · ArrowFunction · parent F0425.  
Ulaz: `k`.  
Trag tela: `Object.hasOwn(buildings,k)`.  
Poziva: `Object.hasOwn` L4996 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0438 · callback s.seen.every** — `index.html:L4997–4997` · ArrowFunction · parent F0425.  
Ulaz: `i`.  
Trag tela: `Boolean(species[i])`.  
Poziva: `Boolean` L4997 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0439 · callback Object.entries(s.tutorial).every** — `index.html:L5001–5001` · ArrowFunction · parent F0425.  
Ulaz: `[key,value]`.  
Trag tela: `['collected','hatched','raced','repeat'].includes(key)&&typeof value==='boolean'`.  
Poziva: `['collected','hatched','raced','repeat'].includes` L5001 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0440 · callback s.museum.every** — `index.html:L5008–5008` · ArrowFunction · parent F0425.  
Ulaz: `n`.  
Trag tela: `n&&species[n.species]&&typeof n.name==='string'&&n.name.length<=80&&n.at===epoch(n.at)`.  
Poziva: `epoch` L5008 → F0413.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0441 · callback s.expeditions.every** — `index.html:L5010–5014` · ArrowFunction · parent F0425.  
Ulaz: `e`.  
Trag tela: `e&&idOk(e.id)&&Number.isInteger(e.destination)&&Array.isArray(expeditions[e.destination])&&e.until>=0&&e.until===epoch(e.until)&& (e.hours==`.  
Poziva: `idOk` L5010 → F0412; `Number.isInteger` L5010 → —; `Array.isArray` L5010 → —; `epoch` L5010 → F0413; `Number.isInteger` L5011 → —; `epoch` L5012 → F0413; `Array.isArray` L5013 → —; `expeditionTeam` L5013 → ~F0076; `expeditionTeam` L5013 → ~F0076; `expeditionTeam` L5013 → ~F0076; `expeditionTeam` L5014 → ~F0076; `Set` L5014 → —; `expeditionTeam` L5014 → ~F0076; `expeditionTeam` L5014 → ~F0076.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0442 · callback e.originalHomes.every** — `index.html:L5018–5019` · ArrowFunction · parent F0425.  
Ulaz: `x`.  
Trag tela: `x&&idOk(x.snailId)&&(x.homeId===null||s.homes.some(h=>h.id===x.homeId))&& (x.substituteId===null||idOk(x.substituteId))`.  
Poziva: `idOk` L5018 → F0412; `s.homes.some` L5018 → —; `idOk` L5019 → F0412.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0443 · callback s.homes.some** — `index.html:L5018–5018` · ArrowFunction · parent F0442.  
Ulaz: `h`.  
Trag tela: `h.id===x.homeId`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0444 · callback [...s.daily.keys,...s.daily.claimed,...Object.keys(s.daily.counts)].every** — `index.html:L5023–5023` · ArrowFunction · parent F0425.  
Ulaz: `k`.  
Trag tela: `taskKeys.includes(k)`.  
Poziva: `taskKeys.includes` L5023 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0445 · callback ['races','pageants','arena'].every** — `index.html:L5024–5024` · ArrowFunction · parent F0425.  
Ulaz: `k`.  
Trag tela: `Number.isInteger(s.daily[k])&&s.daily[k]>=0&&s.daily[k]<=100`.  
Poziva: `Number.isInteger` L5024 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0446 · callback Object.values(s.daily.counts).every** — `index.html:L5025–5025` · ArrowFunction · parent F0425.  
Ulaz: `n`.  
Trag tela: `Number.isSafeInteger(n)&&n>=0`.  
Poziva: `Number.isSafeInteger` L5025 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0447 · callback values.every** — `index.html:L5029–5029` · ArrowFunction · parent F0425.  
Ulaz: `[key,n]`.  
Trag tela: `Object.hasOwn(diamondPools,key)&&Number.isInteger(n)&&n>=0&&n<=diamondPools[key]`.  
Poziva: `Object.hasOwn` L5029 → —; `Number.isInteger` L5029 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0448 · callback values.reduce** — `index.html:L5030–5030` · ArrowFunction · parent F0425.  
Ulaz: `sum, [,n]`.  
Trag tela: `sum+n`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0449 · callback s.homes.map** — `index.html:L5042–5042` · ArrowFunction · parent F0425.  
Ulaz: `h`.  
Trag tela: `h?.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0450 · callback s.homes.map** — `index.html:L5042–5042` · ArrowFunction · parent F0425.  
Ulaz: `h`.  
Trag tela: `h?.slot`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0451 · callback s.homes.every** — `index.html:L5043–5043` · ArrowFunction · parent F0425.  
Ulaz: `h`.  
Trag tela: `idOk(h.id)&&capacity(h.level)&&Number.isInteger(h.slot)&&h.slot>=0&&h.slot<5`.  
Poziva: `idOk` L5043 → F0412; `capacity` L5043 → ~F0077; `Number.isInteger` L5043 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0452 · unique** — `index.html:L5044–5044` · FunctionDeclaration · parent F0425.  
Ulaz: `arr`.  
Trag tela: `{return new Set(arr.map(v=>v?.id)).size===arr.length;}`.  
Poziva: `Set` L5044 → —; `arr.map` L5044 → —.  
Pozivaju: index.html:L5045 (F0425); index.html:L5045 (F0425); index.html:L5045 (F0425).

**F0453 · callback arr.map** — `index.html:L5044–5044` · ArrowFunction · parent F0452.  
Ulaz: `v`.  
Trag tela: `v?.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0454 · callback s.snails.map** — `index.html:L5046–5046` · ArrowFunction · parent F0425.  
Ulaz: `n`.  
Trag tela: `[n.id,n]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0455 · callback s.expeditions.some** — `index.html:L5047–5047` · ArrowFunction · parent F0425.  
Ulaz: `e`.  
Trag tela: `e.id===n.busy&&expeditionTeam(e).includes(n.id)`.  
Poziva: `expeditionTeam(e).includes` L5047 → —; `expeditionTeam` L5047 → ~F0076.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0456 · callback s.expeditions.every** — `index.html:L5048–5048` · ArrowFunction · parent F0425.  
Ulaz: `e`.  
Trag tela: `expeditionTeam(e).every(id=>snailById.get(id)?.busy===e.id)`.  
Poziva: `expeditionTeam(e).every` L5048 → —; `expeditionTeam` L5048 → ~F0076.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0457 · callback expeditionTeam(e).every** — `index.html:L5048–5048` · ArrowFunction · parent F0456.  
Ulaz: `id`.  
Trag tela: `snailById.get(id)?.busy===e.id`.  
Poziva: `snailById.get` L5048 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0458 · callback s.snails.filter** — `index.html:L5049–5049` · ArrowFunction · parent F0425.  
Ulaz: `n`.  
Trag tela: `n.home===h.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0459 · callback [...s.arena.team,...s.arena.foes].every** — `index.html:L5060–5061` · ArrowFunction · parent F0425.  
Ulaz: `n`.  
Trag tela: `n&&idOk(n.id)&&typeof n.name==='string'&&n.name.length<=80&& ['hp','maxHp','atk'].every(k=>Number.isFinite(n[k])&&n[k]>=0&&n[k]<=1e6)&&n.max`.  
Poziva: `idOk` L5060 → F0412; `['hp','maxHp','atk'].every` L5061 → —; `validTrail.has` L5061 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0460 · callback ['hp','maxHp','atk'].every** — `index.html:L5061–5061` · ArrowFunction · parent F0459.  
Ulaz: `k`.  
Trag tela: `Number.isFinite(n[k])&&n[k]>=0&&n[k]<=1e6`.  
Poziva: `Number.isFinite` L5061 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0461 · callback ['sliz','xp','diamonds'].every** — `index.html:L5066–5066` · ArrowFunction · parent F0425.  
Ulaz: `k`.  
Trag tela: `Number.isSafeInteger(result[k])&&result[k]>=0`.  
Poziva: `Number.isSafeInteger` L5066 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0462 · legacyTrait** — `index.html:L5073–5076` · FunctionDeclaration · parent F0409.  
Ulaz: `key`.  
Trag tela: `{ const name=key==='spd'?'speed':key==='wt'?'weight':key==='bea'?'beauty':key; return inheritedTrait(name)?name:null; }`.  
Poziva: `inheritedTrait` L5075 → ~F0036.  
Pozivaju: index.html:L5086 (F0463); index.html:L5086 (F0463).

**F0463 · legacySnail** — `index.html:L5077–5089` · FunctionDeclaration · parent F0409.  
Ulaz: `n, i, homes`.  
Trag tela: `{ const type=int(Number(n?.sp)>=0?n.sp:n?.pic,0,0,species.length-1); const snail={ id:'s-'+int(n?.id,i+1,1), species:type, cls:int(n?.cls,sp`.  
Poziva: `int` L5078 → F0410; `Number` L5078 → —; `int` L5079 → F0410; `int` L5079 → F0410; `String(n?.nm??(Number(n?.sp)<0?n?.name??('Hibrid '+(i+1)):'')).slice` L5080 → —; `String` L5080 → —; `Number` L5080 → —; `int` L5081 → F0410; `int` L5081 → F0410; `int` L5081 → F0410; `int` L5081 → F0410; `number` L5082 → F0411; `int` L5082 → F0410; `int` L5082 → F0410; `validTrail.has` L5083 → —; `int` L5083 → F0410; `int` L5084 → F0410; `int` L5084 → F0410; `int` L5084 → F0410; `int` L5085 → F0410; `Math.max` L5085 → —; `int` L5085 → F0410; `int` L5085 → F0410; `int` L5086 → F0410; `int` L5086 → F0410; `Boolean` L5086 → —; `legacyTrait` L5086 → F0462; `legacyTrait` L5086 → F0462; `number` L5087 → F0411; `number` L5087 → F0411; `number` L5087 → F0411; `number` L5087 → F0411.  
Pozivaju: index.html:L5099 (F0467); index.html:L5138 (F0474); index.html:L5138 (F0474).

**F0464 · migrateLegacy** — `index.html:L5090–5190` · FunctionDeclaration · parent F0409.  
Ulaz: `data, now`.  
Trag tela: `{ assert(data?.sv===2&&arrayOk(data.snails,4000)&&arrayOk(data.eggs,20)&&arrayOk(data.houses,5), 'Podržan je izvoz napretka v174.103 (sv: 2)`.  
Poziva: `assert` L5091 → F0415; `arrayOk` L5091 → F0414; `arrayOk` L5091 → F0414; `arrayOk` L5091 → F0414; `assert` L5093 → F0415; `data.eggs.some` L5093 → —; `assert` L5094 → F0415; `arrayOk` L5094 → F0414; `newGame` L5095 → ~F0126; `data.houses.map` L5097 → —; `assert` L5098 → F0415; `data.snails.map` L5099 → —; `Boolean` L5100 → —; `AUTO_HOME_STATS.includes` L5102 → —; `Set` L5104 → —; `(data.exps??[]).map` L5105 → —; `assert` L5117 → F0415; `data.snails.every` L5117 → —; `s.homes.find` L5120 → —; `assert` L5122 → F0415; `capacity` L5122 → ~F0077; `Object.hasOwn` L5124 → —; `Object.keys(buildings).filter` L5124 → —; `Object.keys` L5124 → —; `data.eggs.map` L5125 → —; `Object.entries` L5143 → —; `int` L5143 → F0410; `number` L5143 → F0411; `Set` L5144 → —; `s.snails.map` L5144 → —; `Object.keys(data.found??{}).map(Number).filter` L5144 → —; `Object.keys(data.found??{}).map` L5144 → —; `Object.keys` L5144 → —; `makeDaily` L5145 → ~F0114; `dayKey` L5145 → ~F0108; `new Date(now).toISOString().slice` L5146 → —; `new Date(now).toISOString` L5146 → —; `Date` L5146 → —; `int` L5148 → F0410; `int` L5148 → F0410; `int` L5151 → F0410; `int` L5151 → F0410; `int` L5153 → F0410; `Object.fromEntries` L5156 → —; `Object.entries({care:'care',meteor:'met',activities:'act',tasks:'task'}).map` L5156 → —; `Object.entries` L5156 → —; `int` L5160 → F0410; `int` L5160 → F0410; `int` L5161 → F0410; `epoch` L5161 → F0413; `epoch` L5162 → F0413; `epoch` L5162 → F0413; `epoch` L5163 → F0413; `epoch` L5164 → F0413; `int` L5164 → F0410; `String(data.pname??'').trim().slice` L5166 → —; `String(data.pname??'').trim` L5166 → —; `String` L5166 → —; `int` L5167 → F0410; `s.snails.find` L5168 → —; `s.seen.includes` L5169 → —; `Boolean` L5170 → —; `dayNumber` L5172 → F0479; `dayNumber` L5172 → F0479; `int` L5174 → F0410; `Number` L5177 → —; `int` L5178 → F0410; `int` L5178 → F0410; `Object.entries({race:'race',arena:'arena',pol:'polish',exp:'expedition'}).filter(([key])=>data.wk[key]).map` L5179 → —; `Object.entries({race:'race',arena:'arena',pol:'polish',exp:'expedition'}).filter` L5179 → —; `Object.entries` L5179 → —; `Boolean` L5180 → —; `Boolean` L5180 → —; `int` L5180 → F0410; `int` L5181 → F0410; `int` L5181 → F0410; `Number` L5183 → —; `int` L5184 → F0410; `int` L5185 → F0410; `int` L5185 → F0410; `Boolean` L5185 → —; `validateSave` L5189 → F0425.  
Pozivaju: index.html:L5195 (F0482).

**F0465 · callback data.eggs.some** — `index.html:L5093–5093` · ArrowFunction · parent F0464.  
Ulaz: `e`.  
Trag tela: `e?.type==='mix'||e?.hyb||e?.mix`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0466 · callback data.houses.map** — `index.html:L5097–5097` · ArrowFunction · parent F0464.  
Ulaz: `h, index`.  
Trag tela: `({id:'h'+(index+1),level:int(h?.l,1,1,4),slot:index})`.  
Poziva: `int` L5097 → F0410.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0467 · callback data.snails.map** — `index.html:L5099–5099` · ArrowFunction · parent F0464.  
Ulaz: `n, index`.  
Trag tela: `legacySnail(n,index,s.homes)`.  
Poziva: `legacySnail` L5099 → F0463.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0468 · callback (data.exps??[]).map** — `index.html:L5105–5116` · ArrowFunction · parent F0464.  
Ulaz: `e`.  
Trag tela: `{ const destination=oldHours.indexOf(Number(e?.h)); assert(Number.isInteger(e?.id)&&destination>=0&&Number.isFinite(Number(e.left))&&e.left>`.  
Poziva: `oldHours.indexOf` L5106 → —; `Number` L5106 → —; `assert` L5107 → F0415; `Number.isInteger` L5107 → —; `Number.isFinite` L5107 → —; `Number` L5107 → —; `Number` L5107 → —; `arrayOk` L5108 → F0414; `e.ids.map` L5110 → —; `Math.round` L5115 → —; `Number` L5115 → —; `Number` L5115 → —; `int` L5115 → F0410; `Number` L5115 → —; `Number` L5115 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0469 · callback e.ids.map** — `index.html:L5110–5114` · ArrowFunction · parent F0468.  
Ulaz: `member`.  
Trag tela: `{ const index=data.snails.findIndex(n=>Number(n.id)===Number(member)); assert(index>=0&&Number(data.snails[index].busy)===e.id&&!accepted.ha`.  
Poziva: `data.snails.findIndex` L5111 → —; `assert` L5112 → F0415; `Number` L5112 → —; `accepted.has` L5112 → —; `accepted.add` L5113 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0470 · callback data.snails.findIndex** — `index.html:L5111–5111` · ArrowFunction · parent F0469.  
Ulaz: `n`.  
Trag tela: `Number(n.id)===Number(member)`.  
Poziva: `Number` L5111 → —; `Number` L5111 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0471 · callback data.snails.every** — `index.html:L5117–5117` · ArrowFunction · parent F0464.  
Ulaz: `n, index`.  
Trag tela: `!Number(n.busy)||accepted.has(index)`.  
Poziva: `Number` L5117 → —; `accepted.has` L5117 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0472 · callback s.homes.find** — `index.html:L5120–5120` · ArrowFunction · parent F0464.  
Ulaz: `item`.  
Trag tela: `item.id===n.home`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0473 · callback Object.keys(buildings).filter** — `index.html:L5124–5124` · ArrowFunction · parent F0464.  
Ulaz: `k`.  
Trag tela: `data.built?.[k]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0474 · callback data.eggs.map** — `index.html:L5125–5140` · ArrowFunction · parent F0464.  
Ulaz: `e, index`.  
Trag tela: `{ const elapsed=number(e?.el,0)*1000; const span=int(e?.dur,30,1,24*60*60*14)*1000; const readyAt=now+Math.max(0,span-elapsed); let careAt=n`.  
Poziva: `number` L5126 → F0411; `int` L5127 → F0410; `Math.max` L5128 → —; `epoch` L5130 → F0413; `Math.min` L5130 → —; `epoch` L5130 → F0413; `Math.min` L5132 → —; `Math.max` L5132 → —; `number` L5132 → F0411; `Math.min` L5133 → —; `Math.max` L5133 → —; `assert` L5135 → F0415; `int` L5136 → F0410; `int` L5136 → F0410; `Boolean` L5137 → —; `legacySnail` L5138 → F0463; `legacySnail` L5138 → F0463; `Number.isInteger` L5139 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0475 · callback s.snails.map** — `index.html:L5144–5144` · ArrowFunction · parent F0464.  
Ulaz: `n`.  
Trag tela: `n.species`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0476 · callback Object.keys(data.found??{}).map(Number).filter** — `index.html:L5144–5144` · ArrowFunction · parent F0464.  
Ulaz: `id`.  
Trag tela: `Boolean(species[id])`.  
Poziva: `Boolean` L5144 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0477 · callback Object.entries({care:'care',meteor:'met',activities:'act',tasks:'task'}).map** — `index.html:L5156–5158` · ArrowFunction · parent F0464.  
Ulaz: `[key,from]`.  
Trag tela: `{ const n=int(data.ddc[from],0,0,Math.min(left,diamondPools[key]));left-=n;return [key,n]; }`.  
Poziva: `int` L5157 → F0410; `Math.min` L5157 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0478 · callback s.snails.find** — `index.html:L5168–5168` · ArrowFunction · parent F0464.  
Ulaz: `snail`.  
Trag tela: `snail.id==='s-'+data.pav`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0479 · dayNumber** — `index.html:L5171–5171` · ArrowFunction · parent F0464.  
Ulaz: `value`.  
Trag tela: `typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value)?Date.parse(value)/86400000:NaN`.  
Poziva: `/^\d{4}-\d{2}-\d{2}$/.test` L5171 → —; `Date.parse` L5171 → —.  
Pozivaju: index.html:L5172 (F0464); index.html:L5172 (F0464).

**F0480 · callback Object.entries({race:'race',arena:'arena',pol:'polish',exp:'expedition'}).filter** — `index.html:L5179–5179` · ArrowFunction · parent F0464.  
Ulaz: `[key]`.  
Trag tela: `data.wk[key]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0481 · callback Object.entries({race:'race',arena:'arena',pol:'polish',exp:'expedition'}).filter(([key])=>data.wk[key]).map** — `index.html:L5179–5179` · ArrowFunction · parent F0464.  
Ulaz: `[,key]`.  
Trag tela: `key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0482 · parseSave** — `index.html:L5191–5196` · FunctionDeclaration · parent F0409.  
Ulaz: `text, now=Date.now()`.  
Trag tela: `{ assert(typeof text==='string'&&text.length<2e6,'Sejv je prevelik ili nije tekstualni JSON.'); let data; try{data=JSON.parse(text);}catch{t`.  
Poziva: `Date.now` L5191 → —; `assert` L5192 → F0415; `JSON.parse` L5194 → —; `Error` L5194 → —; `validateSave` L5195 → F0425; `migrateLegacy` L5195 → F0464.  
Pozivaju: ~index.html:L7204 (F0878); ~index.html:L7577 (F0908); ~index.html:L7631 (F0908).

**F0483 · download** — `index.html:L5197–5208` · FunctionDeclaration · parent F0409.  
Ulaz: `name, value`.  
Trag tela: `{ const text=JSON.stringify(value,null,2); if(globalThis.Capacitor?.isNativePlatform?.()){ const exporter=globalThis.Capacitor.Plugins?.Save`.  
Poziva: `JSON.stringify` L5198 → —; `globalThis.Capacitor?.isNativePlatform` L5199 → —; `Error` L5201 → —; `exporter.save` L5202 → —; `Blob` L5204 → —; `URL.createObjectURL` L5205 → —; `document.createElement` L5206 → —; `a.click` L5206 → —; `setTimeout` L5207 → —.  
Pozivaju: ~index.html:L8046 (F0943); ~index.html:L8051 (F0943); ~index.html:L8061 (F0943).

**F0484 · callback setTimeout** — `index.html:L5207–5207` · ArrowFunction · parent F0483.  
Ulaz: `—`.  
Trag tela: `URL.revokeObjectURL(href)`.  
Poziva: `URL.revokeObjectURL` L5207 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0485 · validSnapshot** — `index.html:L5211–5221` · FunctionDeclaration · parent F0409.  
Ulaz: `value, slot='current'`.  
Trag tela: `{ if(value==null)return null; try{return validateSave(value);} catch(error){ const layout=Number.isInteger(value?.islandLayout)?value.island`.  
Poziva: `validateSave` L5213 → F0425; `Number.isInteger` L5215 → —; `String(error?.message??'Nepoznata validaciona greška').slice` L5216 → —; `String` L5216 → —; `scSaveErrors.set` L5217 → —; `console.warn` L5218 → —.  
Pozivaju: index.html:L5223 (F0486); index.html:L5226 (F0486); index.html:L5226 (F0486); index.html:L5260 (F0500).

**F0486 · recoverSnapshots** — `index.html:L5222–5234` · FunctionDeclaration · parent F0409.  
Ulaz: `current, backup, checkpoint`.  
Trag tela: `{ const valid=validSnapshot(current); if(valid)return {state:valid,recovered:false}; const savedExists=current!=null||backup!=null||checkpoi`.  
Poziva: `validSnapshot` L5223 → F0485; `validSnapshot` L5226 → F0485; `validSnapshot` L5226 → F0485; `[...scSaveErrors.entries()].map(([slot,e])=>slot+' (raspored '+e.layout+'): '+e.reason).join` L5230 → —; `[...scSaveErrors.entries()].map` L5230 → —; `scSaveErrors.entries` L5230 → —; `Error` L5231 → —; `newGame` L5233 → ~F0126.  
Pozivaju: index.html:L5268 (F0501); index.html:L5325 (F0514).

**F0487 · callback [...scSaveErrors.entries()].map** — `index.html:L5230–5230` · ArrowFunction · parent F0486.  
Ulaz: `[slot,e]`.  
Trag tela: `slot+' (raspored '+e.layout+'): '+e.reason`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0488 · openStore** — `index.html:L5235–5244` · FunctionDeclaration · parent F0409.  
Ulaz: `indexedDB`.  
Trag tela: `{ return new Promise((resolve,reject)=>{ const scT=globalThis.SC_STARTUP_TRACE;const scAt=scT?.begin(); const req=indexedDB.open('snail-city`.  
Poziva: `Promise` L5236 → —.  
Pozivaju: index.html:L5373 (F0518).

**F0489 · anonimna** — `index.html:L5236–5243` · ArrowFunction · parent F0488.  
Ulaz: `resolve, reject`.  
Trag tela: `{ const scT=globalThis.SC_STARTUP_TRACE;const scAt=scT?.begin(); const req=indexedDB.open('snail-city-rebuild',1); req.onupgradeneeded=()=>r`.  
Poziva: `scT?.begin` L5237 → —; `indexedDB.open` L5238 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0490 · req.onupgradeneeded** — `index.html:L5239–5239` · ArrowFunction · parent F0489.  
Ulaz: `—`.  
Trag tela: `req.result.createObjectStore('snapshots')`.  
Poziva: `req.result.createObjectStore` L5239 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0491 · req.onerror** — `index.html:L5240–5240` · ArrowFunction · parent F0489.  
Ulaz: `—`.  
Trag tela: `{scT?.end('idb.open',scAt,'error');reject(req.error);}`.  
Poziva: `scT?.end` L5240 → —; `reject` L5240 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0492 · req.onblocked** — `index.html:L5241–5241` · ArrowFunction · parent F0489.  
Ulaz: `—`.  
Trag tela: `{scT?.mark('idb.open.blocked');reject(Error('Zatvori druge kartice igre i pokušaj ponovo.'));}`.  
Poziva: `scT?.mark` L5241 → —; `reject` L5241 → —; `Error` L5241 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0493 · req.onsuccess** — `index.html:L5242–5242` · ArrowFunction · parent F0489.  
Ulaz: `—`.  
Trag tela: `{scT?.end('idb.open',scAt,'ok');resolve(req.result);}`.  
Poziva: `scT?.end` L5242 → —; `resolve` L5242 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0494 · indexedRepository** — `index.html:L5245–5314` · FunctionDeclaration · parent F0409.  
Ulaz: `db`.  
Trag tela: `{ db.onversionchange=()=>db.close(); return {type:'IndexedDB', load(){ return new Promise((resolve,reject)=>{ const scT=globalThis.SC_STARTU`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L5373 (F0518).

**F0495 · db.onversionchange** — `index.html:L5246–5246` · ArrowFunction · parent F0494.  
Ulaz: `—`.  
Trag tela: `db.close()`.  
Poziva: `db.close` L5246 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0496 · load** — `index.html:L5248–5284` · MethodDeclaration · parent F0494.  
Ulaz: `—`.  
Trag tela: `{ return new Promise((resolve,reject)=>{ const scT=globalThis.SC_STARTUP_TRACE,scTxAt=scT?.begin(); const tx=db.transaction('snapshots','rea`.  
Poziva: `Promise` L5249 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0497 · anonimna** — `index.html:L5249–5283` · ArrowFunction · parent F0496.  
Ulaz: `resolve, reject`.  
Trag tela: `{ const scT=globalThis.SC_STARTUP_TRACE,scTxAt=scT?.begin(); const tx=db.transaction('snapshots','readwrite'),store=tx.objectStore('snapshot`.  
Poziva: `scT?.begin` L5250 → —; `db.transaction` L5251 → —; `tx.objectStore` L5251 → —; `scT?.mark` L5252 → —; `store.get` L5253 → —; `store.get` L5253 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0498 · tx.oncomplete** — `index.html:L5255–5255` · ArrowFunction · parent F0497.  
Ulaz: `—`.  
Trag tela: `{scT?.end('idb.load.transaction',scTxAt,'complete');resolve(result);}`.  
Poziva: `scT?.end` L5255 → —; `resolve` L5255 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0499 · tx.onabort** — `index.html:L5256–5256` · ArrowFunction · parent F0497.  
Ulaz: `—`.  
Trag tela: `{scT?.end('idb.load.transaction',scTxAt,'abort');reject(tx.error??Error('Čitanje sejva je prekinuto.'));}`.  
Poziva: `scT?.end` L5256 → —; `reject` L5256 → —; `Error` L5256 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0500 · current.onsuccess** — `index.html:L5257–5282` · ArrowFunction · parent F0497.  
Ulaz: `—`.  
Trag tela: `{ scT?.mark('idb.load.currentReady'); const scValidateAt=scT?.begin(); const state=validSnapshot(current.result); scT?.end('idb.validateCurr`.  
Poziva: `scT?.mark` L5258 → —; `scT?.begin` L5259 → —; `validSnapshot` L5260 → F0485; `scT?.end` L5261 → —; `Boolean` L5262 → —; `scT?.mark` L5263 → —; `store.get` L5264 → —; `store.get` L5264 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0501 · checkpoint.onsuccess** — `index.html:L5265–5281` · ArrowFunction · parent F0500.  
Ulaz: `—`.  
Trag tela: `{ try{ const scRecoveryAt=scT?.begin(); result=recoverSnapshots(current.result,backup.result,checkpoint.result); scT?.end('idb.recovery',scR`.  
Poziva: `scT?.begin` L5267 → —; `recoverSnapshots` L5268 → F0486; `scT?.end` L5269 → —; `store.put` L5271 → —; `Date.now` L5271 → —; `store.put` L5274 → —; `tx.abort` L5279 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0502 · tx.onabort** — `index.html:L5278–5278` · ArrowFunction · parent F0501.  
Ulaz: `—`.  
Trag tela: `reject(error)`.  
Poziva: `reject` L5278 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0503 · read** — `index.html:L5285–5292` · MethodDeclaration · parent F0494.  
Ulaz: `which='current'`.  
Trag tela: `{ return new Promise((resolve,reject)=>{ const store=db.transaction('snapshots').objectStore('snapshots'); const req=store.get(which); req.o`.  
Poziva: `Promise` L5286 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0504 · anonimna** — `index.html:L5286–5291` · ArrowFunction · parent F0503.  
Ulaz: `resolve, reject`.  
Trag tela: `{ const store=db.transaction('snapshots').objectStore('snapshots'); const req=store.get(which); req.onerror=()=>reject(req.error); req.onsuc`.  
Poziva: `db.transaction('snapshots').objectStore` L5287 → —; `db.transaction` L5287 → —; `store.get` L5288 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0505 · req.onerror** — `index.html:L5289–5289` · ArrowFunction · parent F0504.  
Ulaz: `—`.  
Trag tela: `reject(req.error)`.  
Poziva: `reject` L5289 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0506 · req.onsuccess** — `index.html:L5290–5290` · ArrowFunction · parent F0504.  
Ulaz: `—`.  
Trag tela: `resolve(req.result??null)`.  
Poziva: `resolve` L5290 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0507 · commit** — `index.html:L5293–5312` · MethodDeclaration · parent F0494.  
Ulaz: `expected, next, previousId=next.saveId, checkpoint=false, erase=false`.  
Trag tela: `{ return new Promise((resolve,reject)=>{ const tx=db.transaction('snapshots','readwrite'); const store=tx.objectStore('snapshots'),get=store`.  
Poziva: `Promise` L5294 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0508 · anonimna** — `index.html:L5294–5311` · ArrowFunction · parent F0507.  
Ulaz: `resolve, reject`.  
Trag tela: `{ const tx=db.transaction('snapshots','readwrite'); const store=tx.objectStore('snapshots'),get=store.get('current'); let conflict=false; tx`.  
Poziva: `db.transaction` L5295 → —; `tx.objectStore` L5296 → —; `store.get` L5296 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0509 · tx.oncomplete** — `index.html:L5298–5298` · ArrowFunction · parent F0508.  
Ulaz: `—`.  
Trag tela: `resolve()`.  
Poziva: `resolve` L5298 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0510 · tx.onabort** — `index.html:L5299–5299` · ArrowFunction · parent F0508.  
Ulaz: `—`.  
Trag tela: `reject(conflict?Error('Sejv je promenjen u drugoj kartici. Osveži igru.'):tx.error??Error('Upis sejva je prekinut.'))`.  
Poziva: `reject` L5299 → —; `Error` L5299 → —; `Error` L5299 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0511 · get.onsuccess** — `index.html:L5300–5310` · ArrowFunction · parent F0508.  
Ulaz: `—`.  
Trag tela: `{ if((get.result?.revision??null)!==expected||(get.result&&get.result.saveId!==previousId)){ conflict=true;tx.abort();return; } if(erase)sto`.  
Poziva: `tx.abort` L5302 → —; `store.clear` L5304 → —; `store.put` L5306 → —; `store.put` L5307 → —; `store.put` L5309 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0512 · localRepository** — `index.html:L5315–5347` · FunctionDeclaration · parent F0409.  
Ulaz: `ls`.  
Trag tela: `{ return {type:'localStorage', async load(){ const restore=()=>{ const raw=ls.getItem(key); let saved; try{saved=JSON.parse(raw??'null');} c`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L5383 (F0518).

**F0513 · load** — `index.html:L5317–5334` · MethodDeclaration · parent F0512.  
Ulaz: `—`.  
Trag tela: `{ const restore=()=>{ const raw=ls.getItem(key); let saved; try{saved=JSON.parse(raw??'null');} catch{throw Error('Lokalni sejv nije isprava`.  
Poziva: `navigator.locks.request` L5333 → —; `restore` L5333 → F0514.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0514 · restore** — `index.html:L5318–5332` · ArrowFunction · parent F0513.  
Ulaz: `—`.  
Trag tela: `{ const raw=ls.getItem(key); let saved; try{saved=JSON.parse(raw??'null');} catch{throw Error('Lokalni sejv nije ispravan JSON. Originalni z`.  
Poziva: `ls.getItem` L5319 → —; `JSON.parse` L5321 → —; `Error` L5322 → —; `Array.isArray` L5323 → —; `Error` L5324 → —; `recoverSnapshots` L5325 → F0486; `ls.setItem` L5328 → —; `JSON.stringify` L5328 → —; `Date.now` L5329 → —; `Boolean` L5330 → —.  
Pozivaju: index.html:L5333 (F0513).

**F0515 · read** — `index.html:L5335–5335` · MethodDeclaration · parent F0512.  
Ulaz: `which='current'`.  
Trag tela: `{return JSON.parse(ls.getItem(key)||'null')?.[which]??null;}`.  
Poziva: `JSON.parse` L5335 → —; `ls.getItem` L5335 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0516 · commit** — `index.html:L5336–5345` · MethodDeclaration · parent F0512.  
Ulaz: `expected, next, previousId=next.saveId, checkpoint=false, erase=false`.  
Trag tela: `{ const save=()=>{ const saved=JSON.parse(ls.getItem(key)||'null'); const old=saved?.current??null; assert((old?.revision??null)===expected&`.  
Poziva: `navigator.locks.request` L5344 → —; `save` L5344 → F0517.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0517 · save** — `index.html:L5337–5343` · ArrowFunction · parent F0516.  
Ulaz: `—`.  
Trag tela: `{ const saved=JSON.parse(ls.getItem(key)||'null'); const old=saved?.current??null; assert((old?.revision??null)===expected&&(!old||old.saveI`.  
Poziva: `JSON.parse` L5338 → —; `ls.getItem` L5338 → —; `assert` L5340 → F0415; `ls.setItem` L5342 → —; `JSON.stringify` L5342 → —.  
Pozivaju: index.html:L5344 (F0516).

**F0518 · repository** — `index.html:L5348–5387` · FunctionDeclaration · parent F0409.  
Ulaz: `—`.  
Trag tela: `{ // Android document viewers can open downloaded HTML as content:// URLs. // Those URLs have no reliable web origin for IndexedDB/localStor`.  
Poziva: `globalThis.Capacitor?.isNativePlatform` L5354 → —; `canFallback` L5368 → F0519; `preserveError` L5368 → F0520; `indexedRepository` L5373 → F0494; `openStore` L5373 → F0488; `canFallback` L5376 → F0519; `preserveError` L5376 → F0520; `localRepository` L5383 → F0512.  
Pozivaju: ~index.html:L8310 (F0975).

**F0519 · canFallback** — `index.html:L5360–5360` · ArrowFunction · parent F0518.  
Ulaz: `error`.  
Trag tela: `['SecurityError','InvalidStateError','NotSupportedError'].includes(error?.name)`.  
Poziva: `['SecurityError','InvalidStateError','NotSupportedError'].includes` L5360 → —.  
Pozivaju: index.html:L5368 (F0518); index.html:L5376 (F0518).

**F0520 · preserveError** — `index.html:L5361–5361` · ArrowFunction · parent F0518.  
Ulaz: `error`.  
Trag tela: `Error('Ne mogu da otvorim skladište igre ('+(error?.name||'nepoznata greška')+'). Sejv nije obrisan. Ne resetuj profil; pokušaj ponovo preko`.  
Poziva: `Error` L5361 → —.  
Pozivaju: index.html:L5368 (F0518); index.html:L5376 (F0518).

**F0521 · oldLocalSave** — `index.html:L5388–5400` · FunctionDeclaration · parent F0409.  
Ulaz: `—`.  
Trag tela: `{ try { const storage=globalThis.localStorage; if(!storage)return null; for(const key of legacyKeys){ const raw=storage.getItem(key); if(raw`.  
Poziva: `storage.getItem` L5393 → —; `JSON.parse` L5395 → —.  
Pozivaju: ~index.html:L8069 (F0943); ~index.html:L8326 (F0975).

### ui — paneli i prikaz

**F0522 · anonimna** — `index.html:L5404–6531` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const { VERSION, DAY, buildings, tracks, species, snailName, eggNames, eggAssets, eggCosts, eggLevels, eggCapacity, incubatorUsed, craterU`.  
Poziva: `Object.keys` L5832 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0523 · escapeHtml** — `index.html:L5418–5418` · ArrowFunction · parent F0522.  
Ulaz: `v`.  
Trag tela: `String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))`.  
Poziva: `String(v??'').replace` L5418 → —; `String` L5418 → —.  
Pozivaju: index.html:L5452 (F0537); index.html:L5453 (F0537); index.html:L5455 (F0539); index.html:L5456 (F0539); index.html:L5457 (F0540); index.html:L5459 (F0542); index.html:L5459 (F0542); index.html:L5460 (F0543); index.html:L5464 (F0547); index.html:L5465 (F0547); index.html:L5466 (F0548); index.html:L5468 (F0550); index.html:L5469 (F0552); index.html:L5469 (F0552); index.html:L5476 (F0559); index.html:L5502 (F0562); index.html:L5503 (F0562); index.html:L5511 (F0564); index.html:L5517 (F0565); index.html:L5518 (F0565); index.html:L5519 (F0565); index.html:L5520 (F0565); index.html:L5521 (F0565); index.html:L5522 (F0565); index.html:L5522 (F0565); index.html:L5534 (F0568); index.html:L5550 (F0574); index.html:L5552 (F0575); index.html:L5553 (F0575); index.html:L5561 (F0573); index.html:L5563 (F0573); index.html:L5567 (F0573); index.html:L5569 (F0573); index.html:L5570 (F0573); index.html:L5571 (F0573); index.html:L5577 (F0580); index.html:L5659 (F0604); index.html:L5694 (F0612); index.html:L5713 (F0616); index.html:L5768 (F0626); index.html:L5797 (F0630); index.html:L5846 (F0641); index.html:L5847 (F0641); index.html:L5848 (F0641); index.html:L5864 (F0649); index.html:L5870 (F0645); index.html:L5900 (F0659); index.html:L5908 (F0655); index.html:L5912 (F0661); index.html:L5913 (F0661); index.html:L5920 (F0662); index.html:L5921 (F0662); index.html:L5958 (F0672); index.html:L5982 (F0679); index.html:L6038 (F0695); index.html:L6042 (F0691); index.html:L6064 (F0700); index.html:L6065 (F0700); index.html:L6068 (F0703); index.html:L6090 (F0708); index.html:L6125 (F0713); index.html:L6127 (F0714); index.html:L6132 (F0715); index.html:L6147 (F0715); index.html:L6160 (F0717); index.html:L6161 (F0717); index.html:L6229 (F0728); index.html:L6231 (F0728); index.html:L6231 (F0728); index.html:L6252 (F0730); index.html:L6290 (F0734); index.html:L6302 (F0744); index.html:L6302 (F0744); index.html:L6363 (F0749); index.html:L6365 (F0757); index.html:L6366 (F0757); index.html:L6369 (F0758); index.html:L6386 (F0760); index.html:L6396 (F0761); index.html:L6452 (F0765); index.html:L6478 (F0767); index.html:L6510 (F0775).

**F0524 · callback String(v??'').replace** — `index.html:L5418–5418` · ArrowFunction · parent F0523.  
Ulaz: `c`.  
Trag tela: `({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0525 · numericLocale** — `index.html:L5419–5419` · ArrowFunction · parent F0522.  
Ulaz: `—`.  
Trag tela: `modules.i18n?.current()==='en'?'en-US':'sr-Latn-RS'`.  
Poziva: `modules.i18n?.current` L5419 → —.  
Pozivaju: index.html:L5420 (F0526); index.html:L5421 (F0527); index.html:L5421 (F0527); index.html:L5422 (F0528).

**F0526 · format** — `index.html:L5420–5420` · ArrowFunction · parent F0522.  
Ulaz: `n`.  
Trag tela: `Math.floor(n).toLocaleString(numericLocale())`.  
Poziva: `Math.floor(n).toLocaleString` L5420 → —; `Math.floor` L5420 → —; `numericLocale` L5420 → F0525.  
Pozivaju: index.html:L5421 (F0527); index.html:L5476 (F0559); index.html:L5634 (F0599); index.html:L5655 (F0604); index.html:L5655 (F0604); index.html:L5658 (F0604); index.html:L5683 (F0604); index.html:L5731 (F0621); index.html:L5823 (F0632); index.html:L5967 (F0668); index.html:L5967 (F0668); index.html:L6093 (F0708); index.html:L6093 (F0708); index.html:L6093 (F0708); index.html:L6106 (F0709); index.html:L6107 (F0709); index.html:L6108 (F0710); index.html:L6116 (F0711); index.html:L6125 (F0713); index.html:L6181 (F0718); index.html:L6182 (F0718); index.html:L6184 (F0718); index.html:L6185 (F0718); index.html:L6187 (F0718); index.html:L6191 (F0718); index.html:L6221 (F0718); index.html:L6517 (F0777); ~index.html:L6889 (F0837); ~index.html:L6893 (F0837); ~index.html:L6893 (F0837); ~index.html:L7088 (F0869); ~index.html:L7105 (F0871); ~index.html:L7117 (F0871); ~index.html:L8153 (F0943); ~index.html:L8154 (F0943); ~index.html:L8155 (F0943); ~index.html:L8161 (F0943).

**F0527 · short** — `index.html:L5421–5421` · ArrowFunction · parent F0522.  
Ulaz: `n`.  
Trag tela: `n>=1e6?(+(n/1e6).toFixed(n>=1e7?0:1)).toLocaleString(numericLocale())+'M':n>=1e4?(+(n/1e3).toFixed(n>=1e5?0:1)).toLocaleString(numericLocale`.  
Poziva: `(+(n/1e6).toFixed(n>=1e7?0:1)).toLocaleString` L5421 → —; `(n/1e6).toFixed` L5421 → —; `numericLocale` L5421 → F0525; `(+(n/1e3).toFixed(n>=1e5?0:1)).toLocaleString` L5421 → —; `(n/1e3).toFixed` L5421 → —; `numericLocale` L5421 → F0525; `format` L5421 → F0526.  
Pozivaju: index.html:L5477 (F0559); index.html:L5519 (F0565); index.html:L5535 (F0568); index.html:L5616 (F0598); index.html:L5630 (F0599); index.html:L5660 (F0604); index.html:L5661 (F0604); index.html:L5671 (F0604); index.html:L5674 (F0604); index.html:L5729 (F0621); index.html:L5731 (F0621); index.html:L5734 (F0621); index.html:L5751 (F0624); index.html:L5752 (F0624); index.html:L5789 (F0629); index.html:L5798 (F0630); index.html:L5811 (F0631); index.html:L5823 (F0632); index.html:L5823 (F0632); index.html:L6028 (F0689); index.html:L6290 (F0734); index.html:L6297 (F0735); index.html:L6297 (F0735); index.html:L6297 (F0735).

**F0528 · dec** — `index.html:L5422–5422` · ArrowFunction · parent F0522.  
Ulaz: `n, d=2`.  
Trag tela: `(+n.toFixed(d)).toLocaleString(numericLocale())`.  
Poziva: `(+n.toFixed(d)).toLocaleString` L5422 → —; `n.toFixed` L5422 → —; `numericLocale` L5422 → F0525.  
Pozivaju: index.html:L5485 (F0560); index.html:L5493 (F0561); index.html:L5511 (F0564); index.html:L5579 (F0580); index.html:L5630 (F0599); index.html:L5671 (F0604); index.html:L5672 (F0604); index.html:L5734 (F0621); index.html:L5741 (F0623); index.html:L5901 (F0659); index.html:L6061 (F0697); index.html:L6069 (F0703); index.html:L6071 (F0705); index.html:L6309 (F0745); index.html:L6330 (F0749).

**F0529 · timer** — `index.html:L5423–5427` · FunctionDeclaration · parent F0522.  
Ulaz: `ms`.  
Trag tela: `{ const n=Math.max(0,Math.ceil(ms/1000)); return n>=3600?Math.floor(n/3600)+' h '+Math.floor(n/60)%60+' min': n>=60?Math.floor(n/60)+' min '`.  
Poziva: `Math.max` L5424 → —; `Math.ceil` L5424 → —; `Math.floor` L5425 → —; `Math.floor` L5425 → —; `Math.floor` L5426 → —.  
Pozivaju: index.html:L6437 (F0763); ~index.html:L7115 (F0871); ~index.html:L7135 (F0871).

**F0530 · span** — `index.html:L5428–5428` · ArrowFunction · parent F0522.  
Ulaz: `sec`.  
Trag tela: `sec<60?sec+' s':sec<3600?Math.round(sec/60)+' min':Math.round(sec/3600)+' h'`.  
Poziva: `Math.round` L5428 → —; `Math.round` L5428 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0531 · spanRange** — `index.html:L5429–5433` · ArrowFunction · parent F0522.  
Ulaz: `[a,b]`.  
Trag tela: `{ const u=t=>t<60?[t,'s']:t<3600?[Math.round(t/60),'min']:[Math.round(t/3600),'h']; const [x,xu]=u(a),[y,yu]=u(b); return a===b?x+' '+xu:xu=`.  
Poziva: `u` L5431 → F0532; `u` L5431 → F0532.  
Pozivaju: index.html:L5822 (F0632).

**F0532 · u** — `index.html:L5430–5430` · ArrowFunction · parent F0531.  
Ulaz: `t`.  
Trag tela: `t<60?[t,'s']:t<3600?[Math.round(t/60),'min']:[Math.round(t/3600),'h']`.  
Poziva: `Math.round` L5430 → —; `Math.round` L5430 → —.  
Pozivaju: index.html:L5431 (F0531); index.html:L5431 (F0531).

**F0533 · islandWeather** — `index.html:L5439–5442` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ const weather=weatherFor(s,now); return phaseNames[weather.hour]+(weather.condition&&s.weather?' · '+weatherNames[s.weather.id]:''); }`.  
Poziva: `weatherFor` L5440 → ~F0134.  
Pozivaju: ~index.html:L7127 (F0871).

**F0534 · eggLabel** — `index.html:L5444–5444` · ArrowFunction · parent F0522.  
Ulaz: `k`.  
Trag tela: `clsNames[k]+' jaje'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L5699 (F0612); index.html:L5823 (F0632); index.html:L5978 (F0676); index.html:L6451 (F0765).

**F0535 · trailOf** — `index.html:L5447–5447` · ArrowFunction · parent F0522.  
Ulaz: `n`.  
Trag tela: `trails[n.trail]??['Posebni','#ccace9','Ubrzanje puža.','']`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L5500 (F0562); index.html:L5545 (F0572); index.html:L6044 (F0691); index.html:L6473 (F0767).

**F0536 · power** — `index.html:L5450–5450` · ArrowFunction · parent F0522.  
Ulaz: `n`.  
Trag tela: `Math.round(n.hp/5+n.atk*2+n.speed*1.5)`.  
Poziva: `Math.round` L5450 → —.  
Pozivaju: index.html:L5468 (F0551); index.html:L5524 (F0565); index.html:L5570 (F0573); index.html:L5592 (F0585); index.html:L5592 (F0585); index.html:L5634 (F0603); index.html:L5683 (F0610); index.html:L5890 (F0657); index.html:L5890 (F0657); index.html:L5914 (F0661); index.html:L5922 (F0662); index.html:L5926 (F0665); index.html:L5926 (F0665); index.html:L5983 (F0679); index.html:L5988 (F0682); index.html:L5988 (F0682); index.html:L6043 (F0691).

**F0537 · btn** — `index.html:L5452–5453` · ArrowFunction · parent F0522.  
Ulaz: `action, label, value='', enabled=true, css='', aria=''`.  
Trag tela: `'<button type="button" class="btn '+css+'" data-action="'+action+'" data-value="'+escapeHtml(value)+'"'+ (aria?' aria-label="'+escapeHtml(ar`.  
Poziva: `escapeHtml` L5452 → F0523; `escapeHtml` L5453 → F0523.  
Pozivaju: index.html:L5477 (F0559); index.html:L5478 (F0559); index.html:L5535 (F0568); index.html:L5553 (F0575); index.html:L5555 (F0576); index.html:L5559 (F0578); index.html:L5602 (F0593); index.html:L5607 (F0595); index.html:L5616 (F0598); index.html:L5646 (F0604); index.html:L5648 (F0604); index.html:L5660 (F0604); index.html:L5674 (F0604); index.html:L5680 (F0604); index.html:L5681 (F0604); index.html:L5704 (F0612); index.html:L5705 (F0612); index.html:L5705 (F0612); index.html:L5706 (F0612); index.html:L5714 (F0616); index.html:L5719 (F0618); index.html:L5722 (F0618); index.html:L5723 (F0618); index.html:L5733 (F0621); index.html:L5742 (F0623); index.html:L5751 (F0624); index.html:L5752 (F0624); index.html:L5754 (F0624); index.html:L5769 (F0625); index.html:L5791 (F0629); index.html:L5793 (F0627); index.html:L5798 (F0630); index.html:L5798 (F0630); index.html:L5799 (F0627); index.html:L5810 (F0631); index.html:L5811 (F0631); index.html:L5815 (F0627); index.html:L5823 (F0632); index.html:L5826 (F0627); index.html:L5827 (F0627); index.html:L5849 (F0641); index.html:L5858 (F0646); index.html:L5897 (F0655); index.html:L5897 (F0655); index.html:L5903 (F0655); index.html:L5904 (F0655); index.html:L5905 (F0655); index.html:L5948 (F0668); index.html:L5949 (F0668); index.html:L5949 (F0668); index.html:L5959 (F0672); index.html:L5961 (F0668); index.html:L5962 (F0668); index.html:L5969 (F0668); index.html:L5969 (F0668); index.html:L5969 (F0668); index.html:L5970 (F0668); index.html:L5970 (F0668); index.html:L6014 (F0688); index.html:L6019 (F0689); index.html:L6025 (F0689); index.html:L6026 (F0689); index.html:L6028 (F0689); index.html:L6047 (F0691); index.html:L6066 (F0700); index.html:L6066 (F0700); index.html:L6072 (F0697); index.html:L6072 (F0697); index.html:L6073 (F0697); index.html:L6081 (F0707); index.html:L6084 (F0706); index.html:L6094 (F0708); index.html:L6094 (F0708); index.html:L6094 (F0708); index.html:L6094 (F0708); index.html:L6095 (F0708); index.html:L6096 (F0708); index.html:L6100 (F0708); index.html:L6101 (F0708); index.html:L6111 (F0709); index.html:L6111 (F0709); index.html:L6121 (F0711); index.html:L6121 (F0711); index.html:L6128 (F0713); index.html:L6128 (F0713); index.html:L6128 (F0713); index.html:L6135 (F0715); index.html:L6138 (F0715); index.html:L6140 (F0715); index.html:L6143 (F0715); index.html:L6144 (F0715); index.html:L6149 (F0715); index.html:L6150 (F0715); index.html:L6151 (F0715); index.html:L6152 (F0715); index.html:L6153 (F0715); index.html:L6155 (F0715); index.html:L6156 (F0715); index.html:L6162 (F0716); index.html:L6177 (F0718); index.html:L6178 (F0722); index.html:L6187 (F0718); index.html:L6191 (F0718); index.html:L6207 (F0725); index.html:L6216 (F0718); index.html:L6221 (F0718); index.html:L6242 (F0726); index.html:L6249 (F0730); index.html:L6253 (F0730); index.html:L6256 (F0730); index.html:L6257 (F0730); index.html:L6257 (F0730); index.html:L6259 (F0730); index.html:L6260 (F0730); index.html:L6261 (F0730); index.html:L6263 (F0730); index.html:L6264 (F0730); index.html:L6265 (F0730); index.html:L6265 (F0730); index.html:L6266 (F0730); index.html:L6267 (F0730); index.html:L6267 (F0730); index.html:L6268 (F0730); index.html:L6269 (F0730); index.html:L6269 (F0730); index.html:L6270 (F0730); index.html:L6270 (F0730); index.html:L6271 (F0730); index.html:L6271 (F0730); index.html:L6272 (F0730); index.html:L6334 (F0749); index.html:L6374 (F0749); index.html:L6374 (F0749); index.html:L6374 (F0749); index.html:L6374 (F0749); index.html:L6378 (F0759); index.html:L6379 (F0759); index.html:L6454 (F0765); index.html:L6455 (F0765); index.html:L6466 (F0766); index.html:L6467 (F0766); index.html:L6467 (F0766); index.html:L6468 (F0766); index.html:L6501 (F0768); index.html:L6501 (F0768); index.html:L6501 (F0768); index.html:L6504 (F0774); index.html:L6504 (F0774); index.html:L6508 (F0775); index.html:L6509 (F0775); index.html:L6510 (F0775); index.html:L6511 (F0776); index.html:L6513 (F0775); index.html:L6513 (F0775); index.html:L6520 (F0777); index.html:L6520 (F0777); index.html:L6523 (F0778); index.html:L6523 (F0778); index.html:L6525 (F0779); index.html:L6525 (F0779); index.html:L6525 (F0779); index.html:L6528 (F0780); index.html:L6528 (F0780); index.html:L6528 (F0780).

**F0538 · cur** — `index.html:L5454–5454` · ArrowFunction · parent F0522.  
Ulaz: `kind, n`.  
Trag tela: `'<span class="cur"><img src="'+imagePath('c_'+kind+'.webp')+'" alt="" draggable="false">'+n+'</span>'`.  
Poziva: `imagePath` L5454 → ~F0277.  
Pozivaju: index.html:L5477 (F0559); index.html:L5519 (F0565); index.html:L5535 (F0568); index.html:L5616 (F0598); index.html:L5660 (F0604); index.html:L5661 (F0604); index.html:L5674 (F0604); index.html:L5674 (F0604); index.html:L5705 (F0612); index.html:L5751 (F0624); index.html:L5752 (F0624); index.html:L5769 (F0625); index.html:L5791 (F0629); index.html:L5793 (F0627); index.html:L5798 (F0630); index.html:L5811 (F0631); index.html:L5823 (F0632); index.html:L5823 (F0632); index.html:L6025 (F0689); index.html:L6026 (F0689); index.html:L6028 (F0689); index.html:L6028 (F0689); index.html:L6066 (F0700); index.html:L6111 (F0709); index.html:L6184 (F0718); index.html:L6297 (F0735).

**F0539 · header** — `index.html:L5455–5456` · ArrowFunction · parent F0522.  
Ulaz: `label, summary='', extras=''`.  
Trag tela: `'<header class="scr-head"><h2 class="scr-plank">'+escapeHtml(label)+'</h2>'+ (extras?'<span class="scr-btns">'+extras+'</span>':'')+'</heade`.  
Poziva: `escapeHtml` L5455 → F0523; `escapeHtml` L5456 → F0523.  
Pozivaju: index.html:L5476 (F0559); index.html:L5626 (F0599); index.html:L5657 (F0604); index.html:L5668 (F0604); index.html:L5719 (F0618); index.html:L5739 (F0622); index.html:L5748 (F0624); index.html:L5826 (F0627); index.html:L5862 (F0645); index.html:L5869 (F0645); index.html:L5876 (F0645); index.html:L5894 (F0655); index.html:L5937 (F0668); index.html:L5963 (F0668); index.html:L5990 (F0680); index.html:L6019 (F0689); index.html:L6022 (F0689); index.html:L6039 (F0691); index.html:L6060 (F0697); index.html:L6089 (F0708); index.html:L6106 (F0709); index.html:L6118 (F0711); index.html:L6124 (F0713); index.html:L6132 (F0715); index.html:L6160 (F0716); index.html:L6175 (F0718); index.html:L6239 (F0726); index.html:L6330 (F0749); index.html:L6377 (F0759); index.html:L6427 (F0762); index.html:L6429 (F0762); index.html:L6431 (F0762).

**F0540 · image** — `index.html:L5457–5457` · ArrowFunction · parent F0522.  
Ulaz: `path, alt='', lazy=true`.  
Trag tela: `'<img src="'+imagePath(path)+'" alt="'+escapeHtml(alt)+'" draggable="false" '+(lazy?'loading="lazy"':'')+'>'`.  
Poziva: `imagePath` L5457 → ~F0277; `escapeHtml` L5457 → F0523.  
Pozivaju: index.html:L5458 (F0541); index.html:L5578 (F0580); index.html:L5670 (F0604); index.html:L5693 (F0612); index.html:L5719 (F0618); index.html:L5748 (F0624); index.html:L5750 (F0624); index.html:L5750 (F0624); index.html:L5750 (F0624); index.html:L5774 (F0628); index.html:L5789 (F0629); index.html:L5792 (F0627); index.html:L5797 (F0630); index.html:L5799 (F0627); index.html:L5808 (F0631); index.html:L5822 (F0632); index.html:L5826 (F0627); index.html:L5827 (F0627); index.html:L5957 (F0672); index.html:L6023 (F0689); index.html:L6089 (F0708); index.html:L6124 (F0713); index.html:L6230 (F0728); index.html:L6452 (F0765).

**F0541 · snailPic** — `index.html:L5458–5458` · ArrowFunction · parent F0522.  
Ulaz: `snail, lazy=true`.  
Trag tela: `image('snails/'+String(snail.species+1).padStart(3,'0')+'.webp','',lazy)`.  
Poziva: `image` L5458 → F0540; `String(snail.species+1).padStart` L5458 → —; `String` L5458 → —.  
Pozivaju: index.html:L5521 (F0565); index.html:L5563 (F0573); index.html:L5846 (F0641); index.html:L5864 (F0649); index.html:L5912 (F0661); index.html:L5920 (F0662); index.html:L5957 (F0672); index.html:L5982 (F0679); index.html:L6042 (F0691); index.html:L6089 (F0708); index.html:L6124 (F0713); index.html:L6451 (F0765); index.html:L6475 (F0767); index.html:L6475 (F0767).

**F0542 · popHead** — `index.html:L5459–5459` · ArrowFunction · parent F0522.  
Ulaz: `title, summary=''`.  
Trag tela: `'<header class="pop-head">'+(summary?'<p>'+escapeHtml(summary)+'</p>':'')+'<h2>'+escapeHtml(title)+'</h2></header>'`.  
Poziva: `escapeHtml` L5459 → F0523; `escapeHtml` L5459 → F0523.  
Pozivaju: index.html:L6248 (F0730); index.html:L6448 (F0764); index.html:L6451 (F0765); index.html:L6459 (F0766); index.html:L6493 (F0768); index.html:L6506 (F0775).

**F0543 · info** — `index.html:L5460–5460` · ArrowFunction · parent F0522.  
Ulaz: `text`.  
Trag tela: `'<p class="mut">'+escapeHtml(text)+'</p>'`.  
Poziva: `escapeHtml` L5460 → F0523.  
Pozivaju: index.html:L5476 (F0559); index.html:L5557 (F0578); index.html:L5558 (F0578); index.html:L5606 (F0595); index.html:L5614 (F0597); index.html:L5629 (F0599); index.html:L5631 (F0599); index.html:L5658 (F0604); index.html:L5672 (F0604); index.html:L5675 (F0604); index.html:L5682 (F0604); index.html:L5685 (F0604); index.html:L5709 (F0613); index.html:L5715 (F0613); index.html:L5735 (F0621); index.html:L5736 (F0621); index.html:L5753 (F0624); index.html:L5765 (F0625); index.html:L5824 (F0627); index.html:L5853 (F0633); index.html:L5863 (F0645); index.html:L5865 (F0645); index.html:L5939 (F0668); index.html:L5950 (F0668); index.html:L5966 (F0668); index.html:L5967 (F0668); index.html:L5990 (F0680); index.html:L6007 (F0686); index.html:L6013 (F0688); index.html:L6022 (F0689); index.html:L6024 (F0689); index.html:L6039 (F0691); index.html:L6048 (F0691); index.html:L6050 (F0691); index.html:L6060 (F0697); index.html:L6085 (F0706); index.html:L6096 (F0708); index.html:L6099 (F0708); index.html:L6107 (F0709); index.html:L6110 (F0709); index.html:L6120 (F0711); index.html:L6121 (F0711); index.html:L6132 (F0715); index.html:L6134 (F0715); index.html:L6137 (F0715); index.html:L6139 (F0715); index.html:L6142 (F0715); index.html:L6147 (F0715); index.html:L6148 (F0715); index.html:L6154 (F0715); index.html:L6193 (F0718); index.html:L6210 (F0718); index.html:L6213 (F0718); index.html:L6311 (F0745); index.html:L6314 (F0747); index.html:L6319 (F0747); index.html:L6332 (F0749); index.html:L6333 (F0749); index.html:L6344 (F0749); index.html:L6345 (F0749); index.html:L6347 (F0749); index.html:L6350 (F0749); index.html:L6353 (F0749); index.html:L6354 (F0749); index.html:L6363 (F0749); index.html:L6365 (F0757); index.html:L6367 (F0749); index.html:L6371 (F0749); index.html:L6372 (F0749); index.html:L6373 (F0749); index.html:L6428 (F0762); index.html:L6430 (F0762); index.html:L6431 (F0762); index.html:L6448 (F0764); index.html:L6463 (F0766); index.html:L6464 (F0766); index.html:L6465 (F0766); index.html:L6496 (F0768); index.html:L6497 (F0768); index.html:L6498 (F0768); index.html:L6507 (F0775).

**F0544 · pnl** — `index.html:L5461–5461` · ArrowFunction · parent F0522.  
Ulaz: `inner, css=''`.  
Trag tela: `'<section class="pnl '+css+'">'+inner+'</section>'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L5476 (F0559); index.html:L5613 (F0597); index.html:L5627 (F0599); index.html:L5634 (F0599); index.html:L5657 (F0604); index.html:L5669 (F0604); index.html:L5677 (F0604); index.html:L5683 (F0604); index.html:L5709 (F0613); index.html:L5711 (F0613); index.html:L5720 (F0618); index.html:L5729 (F0621); index.html:L5740 (F0622); index.html:L5748 (F0624); index.html:L5764 (F0625); index.html:L5862 (F0645); index.html:L5864 (F0645); index.html:L5869 (F0645); index.html:L5876 (F0645); index.html:L5895 (F0655); index.html:L5909 (F0655); index.html:L5937 (F0668); index.html:L5964 (F0668); index.html:L5965 (F0668); index.html:L5967 (F0668); index.html:L5990 (F0680); index.html:L6005 (F0686); index.html:L6011 (F0688); index.html:L6019 (F0689); index.html:L6022 (F0689); index.html:L6023 (F0689); index.html:L6028 (F0689); index.html:L6039 (F0691); index.html:L6049 (F0691); index.html:L6060 (F0697); index.html:L6064 (F0697); index.html:L6067 (F0697); index.html:L6070 (F0697); index.html:L6080 (F0706); index.html:L6089 (F0708); index.html:L6095 (F0708); index.html:L6096 (F0708); index.html:L6098 (F0708); index.html:L6106 (F0709); index.html:L6108 (F0709); index.html:L6109 (F0709); index.html:L6118 (F0711); index.html:L6124 (F0713); index.html:L6133 (F0715); index.html:L6136 (F0715); index.html:L6139 (F0715); index.html:L6141 (F0715); index.html:L6146 (F0715); index.html:L6154 (F0715); index.html:L6160 (F0716); index.html:L6180 (F0718); index.html:L6188 (F0718); index.html:L6209 (F0718); index.html:L6215 (F0718); index.html:L6218 (F0718); index.html:L6297 (F0735); index.html:L6309 (F0745); index.html:L6330 (F0749); index.html:L6333 (F0749); index.html:L6336 (F0749); index.html:L6337 (F0749); index.html:L6357 (F0749); index.html:L6369 (F0749); index.html:L6373 (F0749); index.html:L6377 (F0759).

**F0545 · prow** — `index.html:L5462–5462` · ArrowFunction · parent F0522.  
Ulaz: `title, right=''`.  
Trag tela: `'<div class="prow"><h3>'+title+'</h3>'+(right?'<span class="mut">'+right+'</span>':'')+'</div>'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L5476 (F0559); index.html:L5613 (F0597); index.html:L5627 (F0599); index.html:L5634 (F0599); index.html:L5657 (F0604); index.html:L5669 (F0604); index.html:L5677 (F0604); index.html:L5683 (F0604); index.html:L5709 (F0613); index.html:L5711 (F0613); index.html:L5720 (F0618); index.html:L5740 (F0622); index.html:L5764 (F0625); index.html:L5862 (F0645); index.html:L5869 (F0645); index.html:L5964 (F0668); index.html:L5965 (F0668); index.html:L6005 (F0686); index.html:L6011 (F0688); index.html:L6028 (F0689); index.html:L6049 (F0691); index.html:L6064 (F0697); index.html:L6067 (F0697); index.html:L6070 (F0697); index.html:L6080 (F0706); index.html:L6095 (F0708); index.html:L6096 (F0708); index.html:L6098 (F0708); index.html:L6106 (F0709); index.html:L6109 (F0709); index.html:L6118 (F0711); index.html:L6133 (F0715); index.html:L6136 (F0715); index.html:L6141 (F0715); index.html:L6146 (F0715); index.html:L6188 (F0718); index.html:L6218 (F0718); index.html:L6297 (F0735); index.html:L6309 (F0745); index.html:L6330 (F0749); index.html:L6333 (F0749); index.html:L6336 (F0749); index.html:L6337 (F0749); index.html:L6357 (F0749); index.html:L6369 (F0749); index.html:L6373 (F0749).

**F0546 · bar** — `index.html:L5463–5463` · ArrowFunction · parent F0522.  
Ulaz: `value, max, css=''`.  
Trag tela: `'<div class="bar '+css+'"><i style="width:'+Math.max(0,Math.min(100,max>0?value/max*100:0)).toFixed(1)+'%"></i></div>'`.  
Poziva: `Math.max(0,Math.min(100,max>0?value/max*100:0)).toFixed` L5463 → —; `Math.max` L5463 → —; `Math.min` L5463 → —.  
Pozivaju: index.html:L5627 (F0599); index.html:L5670 (F0604); index.html:L5862 (F0645); index.html:L5959 (F0672); index.html:L6093 (F0708); index.html:L6107 (F0709); index.html:L6118 (F0711).

**F0547 · card** — `index.html:L5464–5465` · ArrowFunction · parent F0522.  
Ulaz: `title, meta, actions='', media='', css=''`.  
Trag tela: `'<article class="crd '+css+'">'+media+'<div class="crd-copy"><h4>'+escapeHtml(title)+'</h4>'+ (meta?'<p>'+escapeHtml(meta)+'</p>':'')+action`.  
Poziva: `escapeHtml` L5464 → F0523; `escapeHtml` L5465 → F0523.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0548 · countdown** — `index.html:L5466–5466` · ArrowFunction · parent F0522.  
Ulaz: `when, ready='Spremno'`.  
Trag tela: `'<span data-until="'+Number(when)+'" data-ready="'+escapeHtml(ready)+'">…</span>'`.  
Poziva: `Number` L5466 → —; `escapeHtml` L5466 → F0523.  
Pozivaju: index.html:L5702 (F0612); index.html:L5703 (F0612); index.html:L5766 (F0625); index.html:L5790 (F0629); index.html:L6012 (F0688); index.html:L6065 (F0700); index.html:L6197 (F0723); index.html:L6220 (F0718).

**F0549 · incubationProgress** — `index.html:L5467–5467` · ArrowFunction · parent F0522.  
Ulaz: `start, end, now`.  
Trag tela: `now>=end?1:Math.max(0,Math.min(1,(now-start)/Math.max(1,end-start)))`.  
Poziva: `Math.max` L5467 → —; `Math.min` L5467 → —; `Math.max` L5467 → —.  
Pozivaju: index.html:L5696 (F0612); index.html:L6442 (F0763).

**F0550 · options** — `index.html:L5468–5469` · ArrowFunction · parent F0522.  
Ulaz: `list, selectedId, label=n=>snailName(n)+' · '+power(n), empty=''`.  
Trag tela: `(empty?'<option value="">'+escapeHtml(empty)+'</option>':'')+ list.map(n=>'<option value="'+escapeHtml(n.id)+'" '+(n.id===selectedId?'select`.  
Poziva: `escapeHtml` L5468 → F0523; `list.map(n=>'<option value="'+escapeHtml(n.id)+'" '+(n.id===selectedId?'selected':'')+'>'+escapeHtml(label(n))+'</option>').join` L5469 → —; `list.map` L5469 → —.  
Pozivaju: index.html:L5902 (F0655); index.html:L5946 (F0669); index.html:L5993 (F0680); index.html:L5995 (F0680); index.html:L6041 (F0691); index.html:L6071 (F0704).

**F0551 · anonimna** — `index.html:L5468–5468` · ArrowFunction · parent F0550.  
Ulaz: `n`.  
Trag tela: `snailName(n)+' · '+power(n)`.  
Poziva: `snailName` L5468 → ~F0107; `power` L5468 → F0536.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0552 · callback list.map** — `index.html:L5469–5469` · ArrowFunction · parent F0550.  
Ulaz: `n`.  
Trag tela: `'<option value="'+escapeHtml(n.id)+'" '+(n.id===selectedId?'selected':'')+'>'+escapeHtml(label(n))+'</option>'`.  
Poziva: `escapeHtml` L5469 → F0523; `escapeHtml` L5469 → F0523; `label` L5469 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0553 · homeIndex** — `index.html:L5470–5470` · ArrowFunction · parent F0522.  
Ulaz: `s, id`.  
Trag tela: `s.homes.findIndex(h=>h.id===id)`.  
Poziva: `s.homes.findIndex` L5470 → —.  
Pozivaju: index.html:L5514 (F0565); index.html:L5549 (F0573).

**F0554 · callback s.homes.findIndex** — `index.html:L5470–5470` · ArrowFunction · parent F0553.  
Ulaz: `h`.  
Trag tela: `h.id===id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0555 · occupancy** — `index.html:L5471–5471` · ArrowFunction · parent F0522.  
Ulaz: `s, home`.  
Trag tela: `s.snails.filter(n=>n.home===home.id).length`.  
Poziva: `s.snails.filter` L5471 → —.  
Pozivaju: index.html:L5578 (F0580); index.html:L5665 (F0604); index.html:L5741 (F0623).

**F0556 · callback s.snails.filter** — `index.html:L5471–5471` · ArrowFunction · parent F0555.  
Ulaz: `n`.  
Trag tela: `n.home===home.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0557 · totalSeats** — `index.html:L5472–5472` · ArrowFunction · parent F0522.  
Ulaz: `s`.  
Trag tela: `s.homes.reduce((sum,h)=>sum+capacity(h.level),0)`.  
Poziva: `s.homes.reduce` L5472 → —.  
Pozivaju: index.html:L5620 (F0599); index.html:L5673 (F0604).

**F0558 · callback s.homes.reduce** — `index.html:L5472–5472` · ArrowFunction · parent F0557.  
Ulaz: `sum, h`.  
Trag tela: `sum+capacity(h.level)`.  
Poziva: `capacity` L5472 → ~F0077.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0559 · builtState** — `index.html:L5473–5479` · FunctionDeclaration · parent F0522.  
Ulaz: `s, id, go, subtitle=''`.  
Trag tela: `{ if(s.built.includes(id))return null; const [name,level,cost]=buildings[id]; return header(name)+pnl(prow(escapeHtml(subtitle||name))+info(`.  
Poziva: `s.built.includes` L5474 → —; `header` L5476 → F0539; `pnl` L5476 → F0544; `prow` L5476 → F0545; `escapeHtml` L5476 → F0523; `info` L5476 → F0543; `format` L5476 → F0526; `btn` L5477 → F0537; `cur` L5477 → F0538; `short` L5477 → F0527; `btn` L5478 → F0537.  
Pozivaju: index.html:L5888 (F0655); index.html:L5932 (F0668); index.html:L5986 (F0680); index.html:L6017 (F0689); index.html:L6033 (F0691); index.html:L6055 (F0697).

**F0560 · sec1** — `index.html:L5485–5485` · ArrowFunction · parent F0522.  
Ulaz: `v`.  
Trag tela: `dec(v,1)+' s'`.  
Poziva: `dec` L5485 → F0528.  
Pozivaju: index.html:L5489 (F0561); index.html:L5490 (F0561); index.html:L5490 (F0561); index.html:L5491 (F0561); index.html:L5491 (F0561).

**F0561 · trailNumbers** — `index.html:L5486–5498` · FunctionDeclaration · parent F0522.  
Ulaz: `n`.  
Trag tela: `{ const inf=1+.04*(n.infusion??0); const str=Math.min(2.5,Math.max(.8,trailPowerByClass[n.cls]*(1+Math.min(.3,(n.beauty??0)/1000))*inf)); co`.  
Poziva: `Math.min` L5488 → —; `Math.max` L5488 → —; `Math.min` L5488 → —; `sec1` L5489 → F0560; `sec1` L5490 → F0560; `sec1` L5490 → F0560; `sec1` L5491 → F0560; `sec1` L5491 → F0560; `dec` L5493 → F0528; `Math.max` L5494 → —; `Math.round` L5494 → —; `Math.max` L5495 → —; `Math.round` L5495 → —; `Math.max` L5495 → —; `Math.round` L5495 → —.  
Pozivaju: index.html:L5500 (F0562).

**F0562 · trailBox** — `index.html:L5499–5508` · FunctionDeclaration · parent F0522.  
Ulaz: `n, s, css='', withWeak=false, mode='both', fullLabels=false`.  
Trag tela: `{ const [name,color]=trailOf(n), [race,battle]=trailNumbers(n); const tr=modules.i18n.translate; // single existing language source, never t`.  
Poziva: `trailOf` L5500 → F0535; `trailNumbers` L5500 → F0561; `escapeHtml` L5502 → F0523; `tr` L5502 → —; `tr` L5502 → —; `tr` L5502 → —; `escapeHtml` L5503 → F0523; `tr` L5503 → —; `tr` L5503 → —; `tr` L5507 → —; `tr` L5507 → —; `tr` L5507 → —.  
Pozivaju: index.html:L5527 (F0565); index.html:L5557 (F0578); index.html:L5915 (F0661); index.html:L5923 (F0662); index.html:L5984 (F0679).

**F0563 · statCells** — `index.html:L5509–5512` · FunctionDeclaration · parent F0522.  
Ulaz: `n, keys=['hp','atk','speed','weight','beauty']`.  
Trag tela: `{ return '<div class="sn-stats">'+keys.map(key=>'<span data-stat="'+key+'" class="'+(n.flaw===key?'weak':n.talent===key?'talent':'')+'"><sma`.  
Poziva: `keys.map(key=>'<span data-stat="'+key+'" class="'+(n.flaw===key?'weak':n.talent===key?'talent':'')+'"><small>'+ (key==='prod'?'Sliz/s':attri` L5510 → —; `keys.map` L5510 → —.  
Pozivaju: index.html:L5526 (F0565); index.html:L5564 (F0573); index.html:L5915 (F0661); index.html:L5923 (F0662); index.html:L5984 (F0679).

**F0564 · callback keys.map** — `index.html:L5510–5511` · ArrowFunction · parent F0563.  
Ulaz: `key`.  
Trag tela: `'<span data-stat="'+key+'" class="'+(n.flaw===key?'weak':n.talent===key?'talent':'')+'"><small>'+ (key==='prod'?'Sliz/s':attributes[key])+'<`.  
Poziva: `escapeHtml` L5511 → F0523; `dec` L5511 → F0528.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0565 · snailRow** — `index.html:L5513–5528` · FunctionDeclaration · parent F0522.  
Ulaz: `n, s, withHome=true`.  
Trag tela: `{ const i=homeIndex(s,n.home); const place=n.busy?'Na ekspediciji':i>=0?'Stanište '+(i+1):'Bez staništa'; const feed=upgradeInfo(n,s,'snail-`.  
Poziva: `homeIndex` L5514 → F0553; `upgradeInfo` L5516 → ~F0037; `escapeHtml` L5517 → F0523; `available` L5518 → ~F0095; `escapeHtml` L5518 → F0523; `escapeHtml` L5519 → F0523; `cur` L5519 → F0538; `short` L5519 → F0527; `escapeHtml` L5520 → F0523; `escapeHtml` L5521 → F0523; `snailName` L5521 → ~F0107; `snailPic` L5521 → F0541; `escapeHtml` L5522 → F0523; `escapeHtml` L5522 → F0523; `snailName` L5522 → ~F0107; `power` L5524 → F0536; `statCells` L5526 → F0563; `trailBox` L5527 → F0562.  
Pozivaju: index.html:L5606 (F0596); index.html:L5684 (F0611).

**F0566 · upgrades** — `index.html:L5530–5537` · FunctionDeclaration · parent F0522.  
Ulaz: `n, s`.  
Trag tela: `{ return '<h3 class="uph">Nadogradnje</h3><div class="upgrid">'+Object.entries(upgradeLabels).filter(([key])=>key!=='fix-flaw'||n.flaw) .map`.  
Poziva: `Object.entries(upgradeLabels).filter(([key])=>key!=='fix-flaw'||n.flaw) .map(([key,label])=>{ const {cost,currency,blocked}=upgradeInfo(n,s,` L5531 → —; `Object.entries(upgradeLabels).filter(([key])=>key!=='fix-flaw'||n.flaw) .map` L5531 → —; `Object.entries(upgradeLabels).filter` L5531 → —; `Object.entries` L5531 → —.  
Pozivaju: index.html:L5556 (F0577).

**F0567 · callback Object.entries(upgradeLabels).filter** — `index.html:L5531–5531` · ArrowFunction · parent F0566.  
Ulaz: `[key]`.  
Trag tela: `key!=='fix-flaw'||n.flaw`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0568 · callback Object.entries(upgradeLabels).filter(([key])=>key!=='fix-flaw'||n.flaw) .map** — `index.html:L5532–5536` · ArrowFunction · parent F0566.  
Ulaz: `[key,label]`.  
Trag tela: `{ const {cost,currency,blocked}=upgradeInfo(n,s,key); return '<div class="uptile"><b>'+label+'</b>'+(blocked?'<small>'+escapeHtml(blocked)+'`.  
Poziva: `upgradeInfo` L5533 → ~F0037; `escapeHtml` L5534 → F0523; `btn` L5535 → F0537; `cur` L5535 → F0538; `short` L5535 → F0527; `available` L5535 → ~F0095.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0569 · iconBtn** — `index.html:L5539–5540` · ArrowFunction · parent F0522.  
Ulaz: `tab, label, active, extra=''`.  
Trag tela: `'<button type="button" class="btn ibtn" data-action="snail-tab" data-value="'+tab+ '" aria-label="'+label+'" aria-pressed="'+active+'" title`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L5565 (F0573); index.html:L5566 (F0573); index.html:L5566 (F0573).

**F0570 · snailElement** — `index.html:L5541–5541` · FunctionDeclaration · parent F0522.  
Ulaz: `n`.  
Trag tela: `{return species[n.species].elements.map(key=>elements[key]??key).join(' / ');}`.  
Poziva: `species[n.species].elements.map(key=>elements[key]??key).join` L5541 → —; `species[n.species].elements.map` L5541 → —.  
Pozivaju: index.html:L5543 (F0572); index.html:L5570 (F0573); index.html:L5913 (F0661); index.html:L5921 (F0662); index.html:L6042 (F0691).

**F0571 · callback species[n.species].elements.map** — `index.html:L5541–5541` · ArrowFunction · parent F0570.  
Ulaz: `key`.  
Trag tela: `elements[key]??key`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0572 · snailShareText** — `index.html:L5542–5546` · FunctionDeclaration · parent F0522.  
Ulaz: `n`.  
Trag tela: `{ return ['🐌 Snail City · '+snailName(n).trim().replace(/\s+/g,' '),clsNames[n.cls]+' · '+snailElement(n), 'NP '+(n.sl??1)+' · HP '+n.hp+' `.  
Poziva: `['🐌 Snail City · '+snailName(n).trim().replace(/\s+/g,' '),clsNames[n.cls]+' · '+snailElement(n), 'NP '+(n.sl??1)+' · HP '+n.hp+' · Snaga '` L5543 → —; `snailName(n).trim().replace` L5543 → —; `snailName(n).trim` L5543 → —; `snailName` L5543 → ~F0107; `snailElement` L5543 → F0570; `trailOf` L5545 → F0535.  
Pozivaju: ~index.html:L7987 (F0943).

**F0573 · snailPopup** — `index.html:L5548–5573` · FunctionDeclaration · parent F0522.  
Ulaz: `n, s, view`.  
Trag tela: `{ const tab=view.snailTab??'info', usable=available(s,n), i=homeIndex(s,n.home); const slots=s.homes.map((h,k)=>'<option value="'+escapeHtml`.  
Poziva: `available` L5549 → ~F0095; `homeIndex` L5549 → F0553; `s.homes.map((h,k)=>'<option value="'+escapeHtml(h.id)+'" '+(h.id===n.home?'selected':'')+'>Stanište '+(k+1)+'</option>').join` L5550 → —; `s.homes.map` L5550 → —; `escapeHtml` L5561 → F0523; `snailName` L5561 → ~F0107; `snailPic` L5563 → F0541; `escapeHtml` L5563 → F0523; `snailName` L5563 → ~F0107; `statCells` L5564 → F0563; `iconBtn` L5565 → F0569; `iconBtn` L5566 → F0569; `iconBtn` L5566 → F0569; `escapeHtml` L5567 → F0523; `escapeHtml` L5569 → F0523; `escapeHtml` L5570 → F0523; `snailElement` L5570 → F0570; `power` L5570 → F0536; `escapeHtml` L5571 → F0523; `content[tab]` L5572 → —.  
Pozivaju: index.html:L5637 (F0599); index.html:L5686 (F0604); index.html:L5871 (F0645).

**F0574 · callback s.homes.map** — `index.html:L5550–5550` · ArrowFunction · parent F0573.  
Ulaz: `h, k`.  
Trag tela: `'<option value="'+escapeHtml(h.id)+'" '+(h.id===n.home?'selected':'')+'>Stanište '+(k+1)+'</option>'`.  
Poziva: `escapeHtml` L5550 → F0523.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0575 · name** — `index.html:L5552–5553` · ArrowFunction · parent F0573.  
Ulaz: `—`.  
Trag tela: `'<label class="field">Ime puža<input id="rename-input" maxlength="28" value="'+escapeHtml(n.name)+'" placeholder="'+ escapeHtml(snailName(n)`.  
Poziva: `escapeHtml` L5552 → F0523; `escapeHtml` L5553 → F0523; `snailName` L5553 → ~F0107; `btn` L5553 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0576 · home** — `index.html:L5554–5555` · ArrowFunction · parent F0573.  
Ulaz: `—`.  
Trag tela: `'<label class="field">Stanište<select id="home-select"><option value="">Drvo sa satom</option>'+slots+'</select></label>'+ btn('assign','Pre`.  
Poziva: `btn` L5555 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0577 · up** — `index.html:L5556–5556` · ArrowFunction · parent F0573.  
Ulaz: `—`.  
Trag tela: `upgrades(n,s)`.  
Poziva: `upgrades` L5556 → F0566.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0578 · info** — `index.html:L5557–5559` · ArrowFunction · parent F0573.  
Ulaz: `—`.  
Trag tela: `trailBox(n,s,'big',true)+(n.busy?info('Na ekspediciji'):'')+ (n.showWins?info(n.showWins+' prvih mesta na izložbama'):'')+ '<div class="acts`.  
Poziva: `trailBox` L5557 → F0562; `info` L5557 → F0543; `info` L5558 → F0543; `btn` L5559 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0579 · habitatTiles** — `index.html:L5576–5580` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now, action='habitat-open'`.  
Trag tela: `{ return '<div class="hsgrid">'+s.homes.map((h,k)=>'<button type="button" class="hst" data-action="'+action+'" data-value="'+escapeHtml(h.id`.  
Poziva: `s.homes.map((h,k)=>'<button type="button" class="hst" data-action="'+action+'" data-value="'+escapeHtml(h.id)+'">'+ image('h_st'+Math.min(4,` L5577 → —; `s.homes.map` L5577 → —.  
Pozivaju: index.html:L5631 (F0599).

**F0580 · callback s.homes.map** — `index.html:L5577–5579` · ArrowFunction · parent F0579.  
Ulaz: `h, k`.  
Trag tela: `'<button type="button" class="hst" data-action="'+action+'" data-value="'+escapeHtml(h.id)+'">'+ image('h_st'+Math.min(4,h.level)+'.webp')+'`.  
Poziva: `escapeHtml` L5577 → F0523; `image` L5578 → F0540; `Math.min` L5578 → —; `occupancy` L5578 → F0555; `capacity` L5578 → ~F0077; `dec` L5579 → F0528; `rate` L5579 → ~F0139.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0581 · nextExpansion** — `index.html:L5581–5591` · FunctionDeclaration · parent F0522.  
Ulaz: `s`.  
Trag tela: `{ const parts=[]; const up=s.homes.map((h,k)=>[h,k,upgradePrice(h)]).find(([,,p])=>p); if(up){ const [h,k,p]=up; parts.push('Stanište '+(k+1`.  
Poziva: `s.homes.map((h,k)=>[h,k,upgradePrice(h)]).find` L5583 → —; `s.homes.map` L5583 → —; `parts.push` L5586 → —; `capacity` L5586 → ~F0077; `capacity` L5586 → ~F0077; `habitatPrice` L5588 → ~F0124; `parts.push` L5589 → —; `parts.join` L5590 → —.  
Pozivaju: index.html:L5631 (F0599).

**F0582 · callback s.homes.map** — `index.html:L5583–5583` · ArrowFunction · parent F0581.  
Ulaz: `h, k`.  
Trag tela: `[h,k,upgradePrice(h)]`.  
Poziva: `upgradePrice` L5583 → ~F0125.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0583 · callback s.homes.map((h,k)=>[h,k,upgradePrice(h)]).find** — `index.html:L5583–5583` · ArrowFunction · parent F0581.  
Ulaz: `[,,p]`.  
Trag tela: `p`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0584 · name** — `index.html:L5592–5592` · ArrowFunction · parent F0522.  
Ulaz: `a, b`.  
Trag tela: `snailName(a).localeCompare(snailName(b),'sr-Latn')`.  
Poziva: `snailName(a).localeCompare` L5592 → —; `snailName` L5592 → ~F0107; `snailName` L5592 → ~F0107.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0585 · power** — `index.html:L5592–5592` · ArrowFunction · parent F0522.  
Ulaz: `a, b`.  
Trag tela: `power(b)-power(a)`.  
Poziva: `power` L5592 → F0536; `power` L5592 → F0536.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0586 · prod** — `index.html:L5593–5593` · ArrowFunction · parent F0522.  
Ulaz: `a, b`.  
Trag tela: `b.prod-a.prod`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0587 · hp** — `index.html:L5593–5593` · ArrowFunction · parent F0522.  
Ulaz: `a, b`.  
Trag tela: `b.hp-a.hp`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0588 · atk** — `index.html:L5593–5593` · ArrowFunction · parent F0522.  
Ulaz: `a, b`.  
Trag tela: `b.atk-a.atk`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0589 · speed** — `index.html:L5593–5593` · ArrowFunction · parent F0522.  
Ulaz: `a, b`.  
Trag tela: `b.speed-a.speed`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0590 · beauty** — `index.html:L5593–5593` · ArrowFunction · parent F0522.  
Ulaz: `a, b`.  
Trag tela: `b.beauty-a.beauty`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0591 · weight** — `index.html:L5593–5593` · ArrowFunction · parent F0522.  
Ulaz: `a, b`.  
Trag tela: `a.weight-b.weight`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0592 · sortedSnails** — `index.html:L5596–5599` · FunctionDeclaration · parent F0522.  
Ulaz: `list, key, dir=sortDirection`.  
Trag tela: `{ const f=sorters[key], out=f?list.slice().sort(f):list.slice(); return dir==='asc'?out.reverse():out; }`.  
Poziva: `list.slice().sort` L5597 → —; `list.slice` L5597 → —; `list.slice` L5597 → —; `out.reverse` L5598 → —.  
Pozivaju: index.html:L5624 (F0599); index.html:L5666 (F0604).

**F0593 · sortBar** — `index.html:L5600–5602` · ArrowFunction · parent F0522.  
Ulaz: `view`.  
Trag tela: `'<div class="tsort"><label class="sr-only" for="tree-sort">Poređaj po</label><select id="tree-sort">'+Object.entries(sortNames).map(([key,la`.  
Poziva: `Object.entries(sortNames).map(([key,label])=> '<option value="'+key+'" '+((view.snailSort??'prod')===key?'selected':'')+'>'+label+'</option>` L5600 → —; `Object.entries(sortNames).map` L5600 → —; `Object.entries` L5600 → —; `btn` L5602 → F0537.  
Pozivaju: index.html:L5635 (F0599); index.html:L5683 (F0604).

**F0594 · callback Object.entries(sortNames).map** — `index.html:L5600–5601` · ArrowFunction · parent F0593.  
Ulaz: `[key,label]`.  
Trag tela: `'<option value="'+key+'" '+((view.snailSort??'prod')===key?'selected':'')+'>'+label+'</option>'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0595 · snailList** — `index.html:L5604–5608` · FunctionDeclaration · parent F0522.  
Ulaz: `list, s, view, withHome=true`.  
Trag tela: `{ const shown=(view.collectionPage+1)*PAGE; return '<div class="sn-list">'+(list.slice(0,shown).map(n=>snailRow(n,s,withHome)).join('')||inf`.  
Poziva: `list.slice(0,shown).map(n=>snailRow(n,s,withHome)).join` L5606 → —; `list.slice(0,shown).map` L5606 → —; `list.slice` L5606 → —; `info` L5606 → F0543; `btn` L5607 → F0537.  
Pozivaju: index.html:L5636 (F0599); index.html:L5871 (F0645).

**F0596 · callback list.slice(0,shown).map** — `index.html:L5606–5606` · ArrowFunction · parent F0595.  
Ulaz: `n`.  
Trag tela: `snailRow(n,s,withHome)`.  
Poziva: `snailRow` L5606 → F0565.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0597 · masteryPanel** — `index.html:L5610–5618` · FunctionDeclaration · parent F0522.  
Ulaz: `s`.  
Trag tela: `{ const rank=s.mastery??0, open=masteryOpen(s); if(!open&&!rank)return ''; return pnl(prow('Majstorstvo staništa','+'+2*rank+'% proizvodnje'`.  
Poziva: `masteryOpen` L5611 → ~F0083; `pnl` L5613 → F0544; `prow` L5613 → F0545; `info` L5614 → F0543; `[0,1,2].map(i=>'<div class="ctile"><b>'+['I','II','III'][i]+'</b><small>+'+2*(i+1)+'%</small>'+ (i<rank?'<small class="ok">Stečeno</small>':` L5615 → —; `[0,1,2].map` L5615 → —.  
Pozivaju: index.html:L5633 (F0599).

**F0598 · callback [0,1,2].map** — `index.html:L5615–5617` · ArrowFunction · parent F0597.  
Ulaz: `i`.  
Trag tela: `'<div class="ctile"><b>'+['I','II','III'][i]+'</b><small>+'+2*(i+1)+'%</small>'+ (i<rank?'<small class="ok">Stečeno</small>':i===rank?btn('m`.  
Poziva: `btn` L5616 → F0537; `cur` L5616 → F0538; `short` L5616 → F0527.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0599 · tree** — `index.html:L5619–5638` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view, now`.  
Trag tela: `{ const occupied=s.snails.filter(n=>n.home!==null).length, total=totalSeats(s), free=Math.max(0,total-occupied); const homeless=s.snails.fil`.  
Poziva: `s.snails.filter` L5620 → —; `totalSeats` L5620 → F0557; `Math.max` L5620 → —; `s.snails.filter` L5621 → —; `rate` L5622 → ~F0139; `sortedSnails` L5624 → F0592; `s.snails.find` L5625 → —; `header` L5626 → F0539; `pnl` L5627 → F0544; `prow` L5627 → F0545; `bar` L5627 → F0546; `info` L5629 → F0543; `dec` L5630 → F0528; `short` L5630 → F0527; `habitatTiles` L5631 → F0579; `info` L5631 → F0543; `nextExpansion` L5631 → F0581; `Math.round` L5632 → —; `tourists` L5632 → ~F0085; `masteryPanel` L5633 → F0597; `pnl` L5634 → F0544; `prow` L5634 → F0545; `format` L5634 → F0526; `s.snails.reduce` L5634 → —; `sortBar` L5635 → F0593; `snailList` L5636 → F0595; `snailPopup` L5637 → F0573.  
Pozivaju: index.html:L6405 (F0762).

**F0600 · callback s.snails.filter** — `index.html:L5620–5620` · ArrowFunction · parent F0599.  
Ulaz: `n`.  
Trag tela: `n.home!==null`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0601 · callback s.snails.filter** — `index.html:L5621–5621` · ArrowFunction · parent F0599.  
Ulaz: `n`.  
Trag tela: `n.home===null&&!n.busy`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0602 · callback s.snails.find** — `index.html:L5625–5625` · ArrowFunction · parent F0599.  
Ulaz: `n`.  
Trag tela: `n.id===view.inspect`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0603 · callback s.snails.reduce** — `index.html:L5634–5634` · ArrowFunction · parent F0599.  
Ulaz: `a, n`.  
Trag tela: `a+power(n)`.  
Poziva: `power` L5634 → F0536.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0604 · habitat** — `index.html:L5641–5687` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view, now`.  
Trag tela: `{ const pages=s.homes.length+(habitatPrice(s.homes.length)?1:0); let page=s.homes.findIndex(h=>h.id===view.habitat); if(view.habitat==='new'`.  
Poziva: `habitatPrice` L5642 → ~F0124; `s.homes.findIndex` L5643 → —; `habitatPrice` L5644 → ~F0124; `btn` L5646 → F0537; `btn` L5648 → F0537; `s.snails.find` L5649 → —; `habitatPrice` L5651 → ~F0124; `Math.max` L5653 → —; `format` L5655 → F0526; `format` L5655 → F0526; `header` L5657 → F0539; `pnl` L5657 → F0544; `prow` L5657 → F0545; `info` L5658 → F0543; `format` L5658 → F0526; `escapeHtml` L5659 → F0523; `btn` L5660 → F0537; `cur` L5660 → F0538; `short` L5660 → F0527; `cur` L5661 → F0538; `short` L5661 → F0527; `occupancy` L5665 → F0555; `capacity` L5665 → ~F0077; `rate` L5665 → ~F0139; `upgradePrice` L5665 → ~F0125; `sortedSnails` L5666 → F0592; `s.snails.filter` L5666 → —; `header` L5668 → F0539; `pnl` L5669 → F0544; `prow` L5669 → F0545; `image` L5670 → F0540; `bar` L5670 → F0546; `dec` L5671 → F0528; `short` L5671 → F0527; `info` L5672 → F0543; `Math.round` L5672 → —; `dec` L5672 → F0528; `rate` L5672 → ~F0139; `s.snails.filter` L5673 → —; `totalSeats` L5673 → F0557; `btn` L5674 → F0537; `cur` L5674 → F0538; `short` L5674 → F0527; `cur` L5674 → F0538; `info` L5675 → F0543; `capacity` L5675 → ~F0077; `Math.round` L5675 → —; `pnl` L5677 → F0544; `prow` L5677 → F0545; `AUTO_HOME_STATS.map(key=>'<option value="'+key+'" '+(key===(s.autoStat??'prod')?'selected':'')+'>'+ ({prod:'Proizvodnja (sliz/s)',power:'Uku` L5678 → —; `AUTO_HOME_STATS.map` L5678 → —; `btn` L5680 → F0537; `btn` L5681 → F0537; `info` L5682 → F0543; `pnl` L5683 → F0544; `prow` L5683 → F0545; `format` L5683 → F0526; `residents.reduce` L5683 → —; `sortBar` L5683 → F0593; `residents.map(n=>snailRow(n,s,false)).join` L5684 → —; `residents.map` L5684 → —; `info` L5685 → F0543; `snailPopup` L5686 → F0573.  
Pozivaju: index.html:L6407 (F0762).

**F0605 · callback s.homes.findIndex** — `index.html:L5643–5643` · ArrowFunction · parent F0604.  
Ulaz: `h`.  
Trag tela: `h.id===view.habitat`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0606 · callback s.snails.find** — `index.html:L5649–5649` · ArrowFunction · parent F0604.  
Ulaz: `n`.  
Trag tela: `n.id===view.inspect`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0607 · callback s.snails.filter** — `index.html:L5666–5666` · ArrowFunction · parent F0604.  
Ulaz: `n`.  
Trag tela: `n.home===h.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0608 · callback s.snails.filter** — `index.html:L5673–5673` · ArrowFunction · parent F0604.  
Ulaz: `n`.  
Trag tela: `n.home!==null`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0609 · callback AUTO_HOME_STATS.map** — `index.html:L5678–5679` · ArrowFunction · parent F0604.  
Ulaz: `key`.  
Trag tela: `'<option value="'+key+'" '+(key===(s.autoStat??'prod')?'selected':'')+'>'+ ({prod:'Proizvodnja (sliz/s)',power:'Ukupna jačina',cls:'Klasa (r`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0610 · callback residents.reduce** — `index.html:L5683–5683` · ArrowFunction · parent F0604.  
Ulaz: `a, n`.  
Trag tela: `a+power(n)`.  
Poziva: `power` L5683 → F0536.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0611 · callback residents.map** — `index.html:L5684–5684` · ArrowFunction · parent F0604.  
Ulaz: `n`.  
Trag tela: `snailRow(n,s,false)`.  
Poziva: `snailRow` L5684 → F0565.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0612 · eggCard** — `index.html:L5690–5707` · FunctionDeclaration · parent F0522.  
Ulaz: `e, s, now`.  
Trag tela: `{ const ready=e.readyAt<=now, care=canCare(e,now)&&now>=e.careAt; const xp=hatchExperience(e,s.level); const picture=image('e_'+eggAssets[e.`.  
Poziva: `canCare` L5691 → ~F0049; `hatchExperience` L5692 → ~F0123; `image` L5693 → F0540; `escapeHtml` L5694 → F0523; `incubationProgress` L5696 → F0549; `eggLabel` L5699 → F0534; `countdown` L5702 → F0548; `countdown` L5703 → F0548; `btn` L5704 → F0537; `btn` L5705 → F0537; `cur` L5705 → F0538; `btn` L5705 → F0537; `btn` L5706 → F0537.  
Pozivaju: index.html:L5721 (F0620); index.html:L6019 (F0689); index.html:L6024 (F0689).

**F0613 · dailyPanel** — `index.html:L5708–5716` · FunctionDeclaration · parent F0522.  
Ulaz: `s`.  
Trag tela: `{ if(s.level<3)return pnl(prow('Dnevni zadaci')+info('Dnevni zadaci se otvaraju na 3. nivou.')); const done=s.daily.keys.filter(k=>{const t=`.  
Poziva: `pnl` L5709 → F0544; `prow` L5709 → F0545; `info` L5709 → F0543; `s.daily.keys.filter` L5710 → —; `pnl` L5711 → F0544; `prow` L5711 → F0545; `s.daily.keys.map(k=>{ const task=dailyDefs.find(v=>v[0]===k), have=Math.min(s.daily.counts[k]||0,task[3]), claimed=s.daily.claimed.includes(` L5711 → —; `s.daily.keys.map` L5711 → —; `info` L5715 → F0543.  
Pozivaju: index.html:L5723 (F0618).

**F0614 · callback s.daily.keys.filter** — `index.html:L5710–5710` · ArrowFunction · parent F0613.  
Ulaz: `k`.  
Trag tela: `{const t=dailyDefs.find(v=>v[0]===k);return (s.daily.counts[k]||0)>=t[3];}`.  
Poziva: `dailyDefs.find` L5710 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0615 · callback dailyDefs.find** — `index.html:L5710–5710` · ArrowFunction · parent F0614.  
Ulaz: `v`.  
Trag tela: `v[0]===k`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0616 · callback s.daily.keys.map** — `index.html:L5711–5715` · ArrowFunction · parent F0613.  
Ulaz: `k`.  
Trag tela: `{ const task=dailyDefs.find(v=>v[0]===k), have=Math.min(s.daily.counts[k]||0,task[3]), claimed=s.daily.claimed.includes(k), ok=have>=task[3]`.  
Poziva: `dailyDefs.find` L5712 → —; `Math.min` L5712 → —; `s.daily.claimed.includes` L5712 → —; `escapeHtml` L5713 → F0523; `btn` L5714 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0617 · callback dailyDefs.find** — `index.html:L5712–5712` · ArrowFunction · parent F0616.  
Ulaz: `v`.  
Trag tela: `v[0]===k`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0618 · incubator** — `index.html:L5717–5724` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ const list=s.eggs.filter(e=>e.kind!==8), free=eggCapacity(s)-incubatorUsed(s); return header('Inkubator','',btn('open',image('b_timebreake`.  
Poziva: `s.eggs.filter` L5718 → —; `eggCapacity` L5718 → ~F0088; `incubatorUsed` L5718 → ~F0089; `header` L5719 → F0539; `btn` L5719 → F0537; `image` L5719 → F0540; `pnl` L5720 → F0544; `prow` L5720 → F0545; `incubatorUsed` L5720 → ~F0089; `eggCapacity` L5720 → ~F0088; `craterUsed` L5720 → ~F0091; `list.map(e=>eggCard(e,s,now)).join` L5721 → —; `list.map` L5721 → —; `btn` L5722 → F0537; `dailyPanel` L5723 → F0613; `craterUsed` L5723 → ~F0091; `btn` L5723 → F0537.  
Pozivaju: index.html:L6403 (F0762).

**F0619 · callback s.eggs.filter** — `index.html:L5718–5718` · ArrowFunction · parent F0618.  
Ulaz: `e`.  
Trag tela: `e.kind!==8`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0620 · callback list.map** — `index.html:L5721–5721` · ArrowFunction · parent F0618.  
Ulaz: `e`.  
Trag tela: `eggCard(e,s,now)`.  
Poziva: `eggCard` L5721 → F0612.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0621 · reservoirPanel** — `index.html:L5727–5737` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ const amount=reserveAt(s,now), limit=reservoirCapacity(s), pct=Math.round(amount/limit*100), production=rate(s,now); return pnl('<div clas`.  
Poziva: `reserveAt` L5728 → ~F0142; `reservoirCapacity` L5728 → ~F0081; `Math.round` L5728 → —; `rate` L5728 → ~F0139; `pnl` L5729 → F0544; `short` L5729 → F0527; `Math.min` L5730 → —; `format` L5731 → F0526; `short` L5731 → F0527; `btn` L5733 → F0537; `dec` L5734 → F0528; `short` L5734 → F0527; `info` L5735 → F0543; `reservoirHours` L5735 → ~F0080; `info` L5736 → F0543; `Math.max` L5736 → —; `Math.floor` L5736 → —.  
Pozivaju: index.html:L5739 (F0622).

**F0622 · reservoir** — `index.html:L5738–5743` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ return header('Rezervoar sliza')+reservoirPanel(s,now)+ pnl(prow('Odakle dolazi sliz')+s.homes.map((h,k)=>'<div class="srcrow"><div><b>Sta`.  
Poziva: `header` L5739 → F0539; `reservoirPanel` L5739 → F0621; `pnl` L5740 → F0544; `prow` L5740 → F0545; `s.homes.map((h,k)=>'<div class="srcrow"><div><b>Stanište '+(k+1)+' · nivo '+h.level+'</b>'+ '<span class="mut">'+occupancy(s,h)+' / '+capaci` L5740 → —; `s.homes.map` L5740 → —.  
Pozivaju: index.html:L6420 (F0762).

**F0623 · callback s.homes.map** — `index.html:L5740–5742` · ArrowFunction · parent F0622.  
Ulaz: `h, k`.  
Trag tela: `'<div class="srcrow"><div><b>Stanište '+(k+1)+' · nivo '+h.level+'</b>'+ '<span class="mut">'+occupancy(s,h)+' / '+capacity(h.level)+' pužev`.  
Poziva: `occupancy` L5741 → F0555; `capacity` L5741 → ~F0077; `dec` L5741 → F0528; `rate` L5741 → ~F0139; `Math.round` L5742 → —; `btn` L5742 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0624 · timebreaker** — `index.html:L5746–5755` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ const cost=timeBreakCost(rate(s,now)); return header('Razbijač vremena')+pnl('<div class="tbtop">'+image('b_timebreaker.webp','',false)+ '`.  
Poziva: `timeBreakCost` L5747 → ~F0042; `rate` L5747 → ~F0139; `header` L5748 → F0539; `pnl` L5748 → F0544; `image` L5748 → F0540; `image` L5750 → F0540; `image` L5750 → F0540; `image` L5750 → F0540; `btn` L5751 → F0537; `cur` L5751 → F0538; `short` L5751 → F0527; `btn` L5752 → F0537; `cur` L5752 → F0538; `short` L5752 → F0527; `info` L5753 → F0543; `btn` L5754 → F0537.  
Pozivaju: index.html:L6426 (F0762).

**F0625 · weatherControls** — `index.html:L5760–5770` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ if(s.level<11)return ''; const choices=summonChoices(weatherFor(s,now).hour); const cooling=(s.summonAt??0)>now; return pnl(prow('Prizivan`.  
Poziva: `summonChoices` L5762 → ~F0045; `weatherFor` L5762 → ~F0134; `pnl` L5764 → F0544; `prow` L5764 → F0545; `info` L5765 → F0543; `countdown` L5766 → F0548; `choices.map(id=> '<option value="'+id+'">'+(weatherIcons[id]??'')+' '+escapeHtml(weatherNames[id]??id)+'</option>').join` L5767 → —; `choices.map` L5767 → —; `btn` L5769 → F0537; `cur` L5769 → F0538.  
Pozivaju: index.html:L5793 (F0627); index.html:L6101 (F0708).

**F0626 · callback choices.map** — `index.html:L5767–5768` · ArrowFunction · parent F0625.  
Ulaz: `id`.  
Trag tela: `'<option value="'+id+'">'+(weatherIcons[id]??'')+' '+escapeHtml(weatherNames[id]??id)+'</option>'`.  
Poziva: `escapeHtml` L5768 → F0523.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0627 · shop** — `index.html:L5771–5829` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view, now`.  
Trag tela: `{ const tabs='<nav class="shoptabs" aria-label="Odeljci prodavnice">'+shopTabs.map(([key,name,art])=> '<button type="button" class="stab'+(v`.  
Poziva: `shopTabs.map(([key,name,art])=> '<button type="button" class="stab'+(view.shopTab===key?' on':'')+'" data-action="shop-tab" data-value="'+ke` L5772 → —; `shopTabs.map` L5772 → —; `getSeason` L5780 → ~F0030; `rate` L5780 → ~F0139; `Object.entries(exchanges).map(([key,[,price,days]])=>{ const name=key==='tokens'?'Vremenski žetoni':key==='stone'?'Kosmički kamen':key.start` L5781 → —; `Object.entries(exchanges).map` L5781 → —; `Object.entries` L5781 → —; `image` L5792 → F0540; `btn` L5793 → F0537; `cur` L5793 → F0538; `weatherControls` L5793 → F0625; `Object.entries(buildings).map(([id,[name,lvl,price]])=>{ const done=s.built.includes(id); return '<div class="ctile bld">'+image((buildingAr` L5795 → —; `Object.entries(buildings).map` L5795 → —; `Object.entries` L5795 → —; `image` L5799 → F0540; `btn` L5799 → F0537; `WHEAT_FIELDS.map((level,index)=>{ const built=s.wheatBuilt?.includes(index)??false; const unlocked=s.level>=level; const label='Žitno polje ` L5802 → —; `WHEAT_FIELDS.map` L5802 → —; `btn` L5815 → F0537; `modules.i18n.translate` L5819 → ~F0814; `modules.i18n.translate` L5819 → ~F0814; `eggCosts.map((price,i)=>{ const lock=s.level<eggLevels[i], xp=hatchExperience({kind:i},s.level), full=incubatorUsed(s)>=eggCapacity(s); retu` L5819 → —; `eggCosts.map` L5819 → —; `incubatorUsed` L5824 → ~F0089; `eggCapacity` L5824 → ~F0088; `info` L5824 → F0543; `header` L5826 → F0539; `btn` L5826 → F0537; `image` L5826 → F0540; `s.built.includes` L5827 → —; `btn` L5827 → F0537; `image` L5827 → F0540.  
Pozivaju: index.html:L6404 (F0762).

**F0628 · callback shopTabs.map** — `index.html:L5772–5774` · ArrowFunction · parent F0627.  
Ulaz: `[key,name,art]`.  
Trag tela: `'<button type="button" class="stab'+(view.shopTab===key?' on':'')+'" data-action="shop-tab" data-value="'+key+'" aria-pressed="'+(view.shopT`.  
Poziva: `image` L5774 → F0540.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0629 · callback Object.entries(exchanges).map** — `index.html:L5781–5792` · ArrowFunction · parent F0627.  
Ulaz: `[key,[,price,days]]`.  
Trag tela: `{ const name=key==='tokens'?'Vremenski žetoni':key==='stone'?'Kosmički kamen':key.startsWith('dust')?'Zvezdana prašina':'Sliz'; const amount`.  
Poziva: `key.startsWith` L5782 → —; `packAmount` L5783 → ~F0035; `key.startsWith` L5786 → —; `key.startsWith` L5787 → —; `key.startsWith` L5788 → —; `image` L5789 → F0540; `short` L5789 → F0527; `countdown` L5790 → F0548; `btn` L5791 → F0537; `cur` L5791 → F0538.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0630 · callback Object.entries(buildings).map** — `index.html:L5795–5799` · ArrowFunction · parent F0627.  
Ulaz: `[id,[name,lvl,price]]`.  
Trag tela: `{ const done=s.built.includes(id); return '<div class="ctile bld">'+image((buildingArt[id]??'b_shop')+'.webp')+'<b>'+escapeHtml(name)+'</b>'`.  
Poziva: `s.built.includes` L5796 → —; `image` L5797 → F0540; `escapeHtml` L5797 → F0523; `btn` L5798 → F0537; `btn` L5798 → F0537; `cur` L5798 → F0538; `short` L5798 → F0527.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0631 · callback WHEAT_FIELDS.map** — `index.html:L5802–5813` · ArrowFunction · parent F0627.  
Ulaz: `level, index`.  
Trag tela: `{ const built=s.wheatBuilt?.includes(index)??false; const unlocked=s.level>=level; const label='Žitno polje '+(index+1); const state=built?'`.  
Poziva: `s.wheatBuilt?.includes` L5803 → —; `image` L5808 → F0540; `btn` L5810 → F0537; `String` L5810 → —; `btn` L5811 → F0537; `cur` L5811 → F0538; `short` L5811 → F0527.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0632 · callback eggCosts.map** — `index.html:L5819–5824` · ArrowFunction · parent F0627.  
Ulaz: `price, i`.  
Trag tela: `{ const lock=s.level<eggLevels[i], xp=hatchExperience({kind:i},s.level), full=incubatorUsed(s)>=eggCapacity(s); return '<div class="egt ec'+`.  
Poziva: `hatchExperience` L5820 → ~F0123; `incubatorUsed` L5820 → ~F0089; `eggCapacity` L5820 → ~F0088; `modules.i18n.translate` L5821 → ~F0814; `modules.i18n.translate` L5821 → ~F0814; `image` L5822 → F0540; `spanRange` L5822 → F0531; `btn` L5823 → F0537; `cur` L5823 → F0538; `short` L5823 → F0527; `cur` L5823 → F0538; `short` L5823 → F0527; `eggLabel` L5823 → F0534; `format` L5823 → F0526.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0633 · catalogGrid** — `index.html:L5833–5854` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view`.  
Trag tela: `{ const f=view.colFilter??{}; const owned=new Map(); for(const n of s.snails){const o=owned.get(n.species)??{count:0,working:false};o.count+`.  
Poziva: `Map` L5835 → —; `owned.get` L5836 → —; `owned.set` L5836 → —; `species.filter` L5837 → —; `list.slice().sort` L5840 → —; `list.slice` L5840 → —; `list.slice().sort` L5841 → —; `list.slice` L5841 → —; `[...new Set(list.map(n=>n.cls))].sort((a,b)=>a-b).map` L5842 → —; `[...new Set(list.map(n=>n.cls))].sort` L5842 → —; `Set` L5842 → —; `list.map` L5842 → —; `groups.map(([c,items])=>(c===null?'':'<h4 class="grp"><i class="cls" data-k="'+c+'">'+clsNames[c]+'</i> '+ items.filter(n=>s.seen.includes(n` L5851 → —; `groups.map` L5851 → —; `info` L5853 → F0543.  
Pozivaju: index.html:L5881 (F0645).

**F0634 · callback species.filter** — `index.html:L5837–5838` · ArrowFunction · parent F0633.  
Ulaz: `n`.  
Trag tela: `(f.cls===undefined||f.cls===''||n.cls===Number(f.cls))&&(!f.role||view.roles[n.id]===f.role)&& (!f.found||(f.found==='yes'?s.seen.includes(n`.  
Poziva: `Number` L5837 → —; `s.seen.includes` L5838 → —; `s.seen.includes` L5838 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0635 · callback list.slice().sort** — `index.html:L5840–5840` · ArrowFunction · parent F0633.  
Ulaz: `a, b`.  
Trag tela: `a.sr.localeCompare(b.sr,'sr-Latn')`.  
Poziva: `a.sr.localeCompare` L5840 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0636 · callback list.slice().sort** — `index.html:L5841–5841` · ArrowFunction · parent F0633.  
Ulaz: `a, b`.  
Trag tela: `a.level-b.level||a.cls-b.cls`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0637 · callback list.map** — `index.html:L5842–5842` · ArrowFunction · parent F0633.  
Ulaz: `n`.  
Trag tela: `n.cls`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0638 · callback [...new Set(list.map(n=>n.cls))].sort** — `index.html:L5842–5842` · ArrowFunction · parent F0633.  
Ulaz: `a, b`.  
Trag tela: `a-b`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0639 · callback [...new Set(list.map(n=>n.cls))].sort((a,b)=>a-b).map** — `index.html:L5842–5842` · ArrowFunction · parent F0633.  
Ulaz: `c`.  
Trag tela: `[c,list.filter(n=>n.cls===c)]`.  
Poziva: `list.filter` L5842 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0640 · callback list.filter** — `index.html:L5842–5842` · ArrowFunction · parent F0639.  
Ulaz: `n`.  
Trag tela: `n.cls===c`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0641 · tile** — `index.html:L5843–5850` · ArrowFunction · parent F0633.  
Ulaz: `n`.  
Trag tela: `{ const found=view.colAll||s.seen.includes(n.id), own=owned.get(n.id), t=trails[catalog.trails[n.id]]; return '<div class="mrk'+(found?'':' `.  
Poziva: `s.seen.includes` L5844 → —; `owned.get` L5844 → —; `snailPic` L5846 → F0541; `escapeHtml` L5846 → F0523; `escapeHtml` L5847 → F0523; `escapeHtml` L5848 → F0523; `btn` L5849 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0642 · callback groups.map** — `index.html:L5851–5853` · ArrowFunction · parent F0633.  
Ulaz: `[c,items]`.  
Trag tela: `(c===null?'':'<h4 class="grp"><i class="cls" data-k="'+c+'">'+clsNames[c]+'</i> '+ items.filter(n=>s.seen.includes(n.id)).length+' / '+speci`.  
Poziva: `items.filter` L5852 → —; `species.filter` L5852 → —; `items.map(tile).join` L5853 → —; `items.map` L5853 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0643 · callback items.filter** — `index.html:L5852–5852` · ArrowFunction · parent F0642.  
Ulaz: `n`.  
Trag tela: `s.seen.includes(n.id)`.  
Poziva: `s.seen.includes` L5852 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0644 · callback species.filter** — `index.html:L5852–5852` · ArrowFunction · parent F0642.  
Ulaz: `n`.  
Trag tela: `n.cls===c`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0645 · collection** — `index.html:L5855–5882` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view`.  
Trag tela: `{ const mode=view.collection; const tabs='<div class="ctabs">'+[['catalog','Katalog'],['mine','Moji puževi'],['museum','Muzej']].map(([k,l])`.  
Poziva: `[['catalog','Katalog'],['mine','Moji puževi'],['museum','Muzej']].map(([k,l])=> btn('collection-mode',l,k,true,'ctab'+(mode===k?' on':''))).` L5857 → —; `[['catalog','Katalog'],['mine','Moji puževi'],['museum','Muzej']].map` L5857 → —; `s.snails.find` L5859 → —; `museumTiers.find` L5861 → —; `header` L5862 → F0539; `pnl` L5862 → F0544; `prow` L5862 → F0545; `bar` L5862 → F0546; `Math.min` L5862 → —; `info` L5863 → F0543; `pnl` L5864 → F0544; `(s.museum??[]).slice().reverse().map(n=>'<div class="mrk" data-k="'+(species[n.species]?.cls??0)+'">'+snailPic(n)+'<b>'+escapeHtml(n.name)+'` L5864 → —; `(s.museum??[]).slice().reverse().map` L5864 → —; `(s.museum??[]).slice().reverse` L5864 → —; `(s.museum??[]).slice` L5864 → —; `info` L5865 → F0543; `s.snails.filter` L5868 → —; `header` L5869 → F0539; `pnl` L5869 → F0544; `prow` L5869 → F0545; `escapeHtml` L5870 → F0523; `snailList` L5871 → F0595; `snailPopup` L5871 → F0573; `header` L5876 → F0539; `pnl` L5876 → F0544; `sel` L5877 → F0651; `clsNames.map` L5877 → —; `sel` L5878 → F0651; `roleKeys.map` L5878 → —; `sel` L5879 → F0651; `sel` L5880 → F0651; `catalogGrid` L5881 → F0633.  
Pozivaju: index.html:L6406 (F0762).

**F0646 · callback [['catalog','Katalog'],['mine','Moji puževi'],['museum','Muzej']].map** — `index.html:L5857–5858` · ArrowFunction · parent F0645.  
Ulaz: `[k,l]`.  
Trag tela: `btn('collection-mode',l,k,true,'ctab'+(mode===k?' on':''))`.  
Poziva: `btn` L5858 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0647 · callback s.snails.find** — `index.html:L5859–5859` · ArrowFunction · parent F0645.  
Ulaz: `n`.  
Trag tela: `n.id===view.inspect`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0648 · callback museumTiers.find** — `index.html:L5861–5861` · ArrowFunction · parent F0645.  
Ulaz: `[target]`.  
Trag tela: `target>points`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0649 · callback (s.museum??[]).slice().reverse().map** — `index.html:L5864–5864` · ArrowFunction · parent F0645.  
Ulaz: `n`.  
Trag tela: `'<div class="mrk" data-k="'+(species[n.species]?.cls??0)+'">'+snailPic(n)+'<b>'+escapeHtml(n.name)+'</b><em>Sačuvana uspomena</em></div>'`.  
Poziva: `snailPic` L5864 → F0541; `escapeHtml` L5864 → F0523.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0650 · callback s.snails.filter** — `index.html:L5868–5868` · ArrowFunction · parent F0645.  
Ulaz: `n`.  
Trag tela: `snailName(n).toLowerCase().includes(view.search.toLowerCase())`.  
Poziva: `snailName(n).toLowerCase().includes` L5868 → —; `snailName(n).toLowerCase` L5868 → —; `snailName` L5868 → ~F0107; `view.search.toLowerCase` L5868 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0651 · sel** — `index.html:L5874–5875` · ArrowFunction · parent F0645.  
Ulaz: `id, label, opts, value`.  
Trag tela: `'<label class="sr-only" for="'+id+'">'+label+'</label><select id="'+id+'" class="colf">'+ opts.map(([v,t])=>'<option value="'+v+'" '+(String`.  
Poziva: `opts.map(([v,t])=>'<option value="'+v+'" '+(String(value??'')===v?'selected':'')+'>'+t+'</option>').join` L5875 → —; `opts.map` L5875 → —.  
Pozivaju: index.html:L5877 (F0645); index.html:L5878 (F0645); index.html:L5879 (F0645); index.html:L5880 (F0645).

**F0652 · callback opts.map** — `index.html:L5875–5875` · ArrowFunction · parent F0651.  
Ulaz: `[v,t]`.  
Trag tela: `'<option value="'+v+'" '+(String(value??'')===v?'selected':'')+'>'+t+'</option>'`.  
Poziva: `String` L5875 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0653 · callback clsNames.map** — `index.html:L5877–5877` · ArrowFunction · parent F0645.  
Ulaz: `n, i`.  
Trag tela: `[String(i),n]`.  
Poziva: `String` L5877 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0654 · callback roleKeys.map** — `index.html:L5878–5878` · ArrowFunction · parent F0645.  
Ulaz: `k`.  
Trag tela: `[k,roleNames[k]]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0655 · races** — `index.html:L5887–5910` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view`.  
Trag tela: `{ const locked=builtState(s,'races','island-menu','Četiri trake'); if(locked)return locked; const stock=s.snails.filter(n=>available(s,n)).s`.  
Poziva: `builtState` L5888 → F0559; `s.snails.filter(n=>available(s,n)).sort` L5890 → —; `s.snails.filter` L5890 → —; `dimensionOf` L5890 → ~F0073; `stock.find` L5892 → —; `header` L5894 → F0539; `pnl` L5895 → F0544; `imagePath` L5895 → ~F0277; `btn` L5897 → F0537; `btn` L5897 → F0537; `Object.entries(tracks).map(([id,track])=> '<button type="button" class="trk'+(view.track===id?' on':'')+'" data-action="track" data-value="'` L5898 → —; `Object.entries(tracks).map` L5898 → —; `Object.entries` L5898 → —; `options` L5902 → F0550; `btn` L5903 → F0537; `btn` L5904 → F0537; `btn` L5905 → F0537; `escapeHtml` L5908 → F0523; `pnl` L5909 → F0544; `runnerCard` L5909 → F0661.  
Pozivaju: index.html:L6416 (F0762).

**F0656 · callback s.snails.filter** — `index.html:L5890–5890` · ArrowFunction · parent F0655.  
Ulaz: `n`.  
Trag tela: `available(s,n)`.  
Poziva: `available` L5890 → ~F0095.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0657 · callback s.snails.filter(n=>available(s,n)).sort** — `index.html:L5890–5890` · ArrowFunction · parent F0655.  
Ulaz: `a, b`.  
Trag tela: `power(b)-power(a)`.  
Poziva: `power` L5890 → F0536; `power` L5890 → F0536.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0658 · callback stock.find** — `index.html:L5892–5892` · ArrowFunction · parent F0655.  
Ulaz: `n`.  
Trag tela: `n.id===view.racer`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0659 · callback Object.entries(tracks).map** — `index.html:L5898–5901` · ArrowFunction · parent F0655.  
Ulaz: `[id,track]`.  
Trag tela: `'<button type="button" class="trk'+(view.track===id?' on':'')+'" data-action="track" data-value="'+id+'" aria-pressed="'+(view.track===id)+'`.  
Poziva: `imagePath` L5900 → ~F0277; `escapeHtml` L5900 → F0523; `dec` L5901 → F0528; `records[id].seconds.toFixed` L5901 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0660 · callback options** — `index.html:L5902–5902` · ArrowFunction · parent F0655.  
Ulaz: `n`.  
Trag tela: `snailName(n)+' · '+modules.i18n.translate('Brzina')+' '+n.speed+' · '+modules.i18n.translate('Težina')+' '+n.weight`.  
Poziva: `snailName` L5902 → ~F0107; `modules.i18n.translate` L5902 → ~F0814; `modules.i18n.translate` L5902 → ~F0814.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0661 · runnerCard** — `index.html:L5911–5916` · FunctionDeclaration · parent F0522.  
Ulaz: `n, s`.  
Trag tela: `{ return '<div class="runner-card" data-k="'+n.cls+'">'+snailPic(n,false)+'<div class="runner-ident"><h3>'+escapeHtml(snailName(n))+'</h3>'+`.  
Poziva: `snailPic` L5912 → F0541; `escapeHtml` L5912 → F0523; `snailName` L5912 → ~F0107; `escapeHtml` L5913 → F0523; `snailElement` L5913 → F0570; `power` L5914 → F0536; `statCells` L5915 → F0563; `trailBox` L5915 → F0562.  
Pozivaju: index.html:L5909 (F0655).

**F0662 · fighterCard** — `index.html:L5919–5924` · FunctionDeclaration · parent F0522.  
Ulaz: `n, s`.  
Trag tela: `{ return '<div class="fcard" data-k="'+n.cls+'"><div class="fhead">'+snailPic(n)+'<div><strong class="sc-fighter-name">'+escapeHtml(snailNam`.  
Poziva: `snailPic` L5920 → F0541; `escapeHtml` L5920 → F0523; `snailName` L5920 → ~F0107; `escapeHtml` L5921 → F0523; `snailElement` L5921 → F0570; `power` L5922 → F0536; `statCells` L5923 → F0563; `trailBox` L5923 → F0562.  
Pozivaju: index.html:L5946 (F0669).

**F0663 · arenaDefaults** — `index.html:L5925–5930` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view`.  
Trag tela: `{ const stock=s.snails.filter(n=>available(s,n)).sort((a,b)=>power(b)-power(a)); const team=(view.arenaTeam??[]).filter(id=>stock.some(n=>n.`.  
Poziva: `s.snails.filter(n=>available(s,n)).sort` L5926 → —; `s.snails.filter` L5926 → —; `(view.arenaTeam??[]).filter` L5927 → —; `team.includes` L5928 → —; `team.push` L5928 → —.  
Pozivaju: index.html:L5936 (F0668); ~index.html:L7924 (F0943).

**F0664 · callback s.snails.filter** — `index.html:L5926–5926` · ArrowFunction · parent F0663.  
Ulaz: `n`.  
Trag tela: `available(s,n)`.  
Poziva: `available` L5926 → ~F0095.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0665 · callback s.snails.filter(n=>available(s,n)).sort** — `index.html:L5926–5926` · ArrowFunction · parent F0663.  
Ulaz: `a, b`.  
Trag tela: `power(b)-power(a)`.  
Poziva: `power` L5926 → F0536; `power` L5926 → F0536.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0666 · callback (view.arenaTeam??[]).filter** — `index.html:L5927–5927` · ArrowFunction · parent F0663.  
Ulaz: `id`.  
Trag tela: `stock.some(n=>n.id===id)`.  
Poziva: `stock.some` L5927 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0667 · callback stock.some** — `index.html:L5927–5927` · ArrowFunction · parent F0666.  
Ulaz: `n`.  
Trag tela: `n.id===id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0668 · arena** — `index.html:L5931–5971` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view`.  
Trag tela: `{ const locked=builtState(s,'arena','island-menu','Borba 4 na 4'); if(locked)return locked; const duel=s.arena; if(!duel){ const {stock,team`.  
Poziva: `builtState` L5932 → F0559; `arenaDefaults` L5936 → F0663; `header` L5937 → F0539; `pnl` L5937 → F0544; `info` L5939 → F0543; `Math.min` L5942 → —; `[0,1,2,3].map(i=>{ const n=stock.find(v=>v.id===team[i]); return '<div class="slot"><label class="sc-pick-label" for="arena-slot-'+i+'">Bora` L5943 → —; `[0,1,2,3].map` L5943 → —; `btn` L5948 → F0537; `btn` L5949 → F0537; `btn` L5949 → F0537; `info` L5950 → F0543; `btn` L5961 → F0537; `btn` L5962 → F0537; `header` L5963 → F0539; `pnl` L5964 → F0544; `prow` L5964 → F0545; `duel.team.map(n=>fighter(n,false)).join` L5964 → —; `duel.team.map` L5964 → —; `pnl` L5965 → F0544; `prow` L5965 → F0545; `duel.foes.map(n=>fighter(n,true)).join` L5965 → —; `duel.foes.map` L5965 → —; `info` L5966 → F0543; `pnl` L5967 → F0544; `info` L5967 → F0543; `format` L5967 → F0526; `format` L5967 → F0526; `btn` L5969 → F0537; `btn` L5969 → F0537; `duel.team.slice(duel.round%duel.team.length).concat(duel.team.slice(0,duel.round%duel.team.length)).find` L5969 → —; `duel.team.slice(duel.round%duel.team.length).concat` L5969 → —; `duel.team.slice` L5969 → —; `duel.team.slice` L5969 → —; `btn` L5969 → F0537; `btn` L5970 → F0537; `btn` L5970 → F0537.  
Pozivaju: index.html:L6419 (F0762).

**F0669 · callback [0,1,2,3].map** — `index.html:L5943–5947` · ArrowFunction · parent F0668.  
Ulaz: `i`.  
Trag tela: `{ const n=stock.find(v=>v.id===team[i]); return '<div class="slot"><label class="sc-pick-label" for="arena-slot-'+i+'">Borac '+(i+1)+' · sna`.  
Poziva: `stock.find` L5944 → —; `options` L5946 → F0550; `fighterCard` L5946 → F0662.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0670 · callback stock.find** — `index.html:L5944–5944` · ArrowFunction · parent F0669.  
Ulaz: `v`.  
Trag tela: `v.id===team[i]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0671 · callback options** — `index.html:L5946–5946` · ArrowFunction · parent F0669.  
Ulaz: `v`.  
Trag tela: `snailName(v)+' · '+modules.i18n.translate('Snaga')+' '+v.atk+' · HP '+v.hp`.  
Poziva: `snailName` L5946 → ~F0107; `modules.i18n.translate` L5946 → ~F0814.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0672 · fighter** — `index.html:L5952–5960` · ArrowFunction · parent F0668.  
Ulaz: `n, enemy`.  
Trag tela: `{ const last=duel.last, hitHere=n.id===last?.target&&last.dealt, actor=n.id===last?.actor; const animation=hitHere?'hit':actor&&last.action=`.  
Poziva: `Number.isInteger` L5957 → —; `snailPic` L5957 → F0541; `image` L5957 → F0540; `escapeHtml` L5958 → F0523; `bar` L5959 → F0546; `btn` L5959 → F0537.  
Pozivaju: index.html:L5964 (F0673); index.html:L5965 (F0674).

**F0673 · callback duel.team.map** — `index.html:L5964–5964` · ArrowFunction · parent F0668.  
Ulaz: `n`.  
Trag tela: `fighter(n,false)`.  
Poziva: `fighter` L5964 → F0672.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0674 · callback duel.foes.map** — `index.html:L5965–5965` · ArrowFunction · parent F0668.  
Ulaz: `n`.  
Trag tela: `fighter(n,true)`.  
Poziva: `fighter` L5965 → F0672.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0675 · callback duel.team.slice(duel.round%duel.team.length).concat(duel.team.slice(0,duel.round%duel.team.length)).find** — `index.html:L5969–5969` · ArrowFunction · parent F0668.  
Ulaz: `n`.  
Trag tela: `n.hp>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0676 · breedingPreview** — `index.html:L5974–5980` · FunctionDeclaration · parent F0522.  
Ulaz: `s, a, b`.  
Trag tela: `{ const plan=breedPlan(s,s.snails.find(n=>n.id===a),s.snails.find(n=>n.id===b)); if(!plan)return {message:'Izaberi dva različita dostupna pu`.  
Poziva: `breedPlan` L5975 → ~F0167; `s.snails.find` L5975 → —; `s.snails.find` L5975 → —; `eggLabel` L5978 → F0534.  
Pozivaju: ~index.html:L7083 (F0869).

**F0677 · callback s.snails.find** — `index.html:L5975–5975` · ArrowFunction · parent F0676.  
Ulaz: `n`.  
Trag tela: `n.id===a`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0678 · callback s.snails.find** — `index.html:L5975–5975` · ArrowFunction · parent F0676.  
Ulaz: `n`.  
Trag tela: `n.id===b`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0679 · parentCard** — `index.html:L5981–5984` · ArrowFunction · parent F0522.  
Ulaz: `n, s`.  
Trag tela: `'<div class="pcard sc84-parent-card" data-k="'+n.cls+'">'+ '<div class="sc84-parent-ident">'+snailPic(n)+'<div class="sc84-parent-name"><b>'`.  
Poziva: `snailPic` L5982 → F0541; `escapeHtml` L5982 → F0523; `snailName` L5982 → ~F0107; `modules.i18n.translate` L5983 → ~F0814; `power` L5983 → F0536; `statCells` L5984 → F0563; `trailBox` L5984 → F0562.  
Pozivaju: index.html:L5994 (F0680); index.html:L5996 (F0680).

**F0680 · breeding** — `index.html:L5985–5998` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view`.  
Trag tela: `{ const locked=builtState(s,'breeding','island-menu','Uzgoj'); if(locked)return locked; const stock=s.snails.filter(n=>available(s,n)).sort(`.  
Poziva: `builtState` L5986 → F0559; `s.snails.filter(n=>available(s,n)).sort` L5988 → —; `s.snails.filter` L5988 → —; `stock.find` L5989 → —; `stock.find` L5989 → —; `header` L5990 → F0539; `pnl` L5990 → F0544; `info` L5990 → F0543; `incubatorUsed` L5992 → ~F0089; `eggCapacity` L5992 → ~F0088; `options` L5993 → F0550; `parentCard` L5994 → F0679; `options` L5995 → F0550; `stock.filter` L5995 → —; `parentCard` L5996 → F0679.  
Pozivaju: index.html:L6422 (F0762).

**F0681 · callback s.snails.filter** — `index.html:L5988–5988` · ArrowFunction · parent F0680.  
Ulaz: `n`.  
Trag tela: `available(s,n)`.  
Poziva: `available` L5988 → ~F0095.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0682 · callback s.snails.filter(n=>available(s,n)).sort** — `index.html:L5988–5988` · ArrowFunction · parent F0680.  
Ulaz: `a, b`.  
Trag tela: `power(b)-power(a)`.  
Poziva: `power` L5988 → F0536; `power` L5988 → F0536.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0683 · callback stock.find** — `index.html:L5989–5989` · ArrowFunction · parent F0680.  
Ulaz: `n`.  
Trag tela: `n.id===view.parents?.[0]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0684 · callback stock.find** — `index.html:L5989–5989` · ArrowFunction · parent F0680.  
Ulaz: `n`.  
Trag tela: `n.id===view.parents?.[1]&&n.id!==pa?.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0685 · callback stock.filter** — `index.html:L5995–5995` · ArrowFunction · parent F0680.  
Ulaz: `n`.  
Trag tela: `n.id!==pa?.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0686 · weeklyPanel** — `index.html:L6001–6008` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ if(s.level<11)return ''; const season=getSeason(s,now), done=season.missions??[]; const names={race:'Pobedi u trci',arena:'Pobedi u areni'`.  
Poziva: `getSeason` L6003 → ~F0030; `pnl` L6005 → F0544; `prow` L6005 → F0545; `weeklyTasks(s.level).map(key=>'<li class="'+(done.includes(key)?'ok':'')+'"><span>'+ (done.includes(key)?'✓':'○')+' '+names[key]+'</span></l` L6005 → —; `weeklyTasks(s.level).map` L6005 → —; `weeklyTasks` L6005 → ~F0031; `info` L6007 → F0543.  
Pozivaju: index.html:L6027 (F0689).

**F0687 · callback weeklyTasks(s.level).map** — `index.html:L6005–6006` · ArrowFunction · parent F0686.  
Ulaz: `key`.  
Trag tela: `'<li class="'+(done.includes(key)?'ok':'')+'"><span>'+ (done.includes(key)?'✓':'○')+' '+names[key]+'</span></li>'`.  
Poziva: `done.includes` L6005 → —; `done.includes` L6006 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0688 · meteorPanel** — `index.html:L6009–6015` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ const rain=s.rain&&s.rain.until>now?s.rain:null; return pnl(prow(rain?'Meteorski pljusak':'Meteorsko polje',rain?rain.caught+' / '+RAIN_LI`.  
Poziva: `pnl` L6011 → F0544; `prow` L6011 → F0545; `countdown` L6012 → F0548; `info` L6013 → F0543; `btn` L6014 → F0537; `Boolean` L6014 → —; `nextMeteor` L6014 → ~F0053.  
Pozivaju: index.html:L6027 (F0689); index.html:L6242 (F0726).

**F0689 · crater** — `index.html:L6016–6029` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ const locked=builtState(s,'crater','island-menu','Cosmic Fall'); const egg=s.eggs.find(v=>v.kind===8); if(locked)return egg?header('Kosmič`.  
Poziva: `builtState` L6017 → F0559; `s.eggs.find` L6018 → —; `header` L6019 → F0539; `pnl` L6019 → F0544; `eggCard` L6019 → F0612; `btn` L6019 → F0537; `craterPrice` L6020 → ~F0043; `cosmicTradeCost` L6021 → ~F0032; `rate` L6021 → ~F0139; `header` L6022 → F0539; `pnl` L6022 → F0544; `info` L6022 → F0543; `pnl` L6023 → F0544; `image` L6023 → F0540; `eggCard` L6024 → F0612; `info` L6024 → F0543; `btn` L6025 → F0537; `cur` L6025 → F0538; `Boolean` L6025 → —; `btn` L6026 → F0537; `cur` L6026 → F0538; `weeklyPanel` L6027 → F0686; `meteorPanel` L6027 → F0688; `pnl` L6028 → F0544; `prow` L6028 → F0545; `btn` L6028 → F0537; `cur` L6028 → F0538; `short` L6028 → F0527; `cur` L6028 → F0538; `getSeason` L6028 → ~F0030.  
Pozivaju: index.html:L6423 (F0762).

**F0690 · callback s.eggs.find** — `index.html:L6018–6018` · ArrowFunction · parent F0689.  
Ulaz: `v`.  
Trag tela: `v.kind===8`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0691 · pageants** — `index.html:L6032–6051` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view`.  
Trag tela: `{ const locked=builtState(s,'pageant','island-menu','Prestiž'); if(locked)return locked; const stock=s.snails.filter(n=>available(s,n)).sort`.  
Poziva: `builtState` L6033 → F0559; `s.snails.filter(n=>available(s,n)).sort` L6035 → —; `s.snails.filter` L6035 → —; `stock.find` L6036 → —; `header` L6039 → F0539; `pnl` L6039 → F0544; `info` L6039 → F0543; `options` L6041 → F0550; `snailPic` L6042 → F0541; `escapeHtml` L6042 → F0523; `snailElement` L6042 → F0570; `power` L6043 → F0536; `cell` L6043 → F0695; `cell` L6043 → F0695; `cell` L6044 → F0695; `cell` L6044 → F0695; `trailOf` L6044 → F0535; `cell` L6044 → F0695; `btn` L6047 → F0537; `Boolean` L6047 → —; `info` L6048 → F0543; `pnl` L6049 → F0544; `prow` L6049 → F0545; `info` L6050 → F0543.  
Pozivaju: index.html:L6424 (F0762).

**F0692 · callback s.snails.filter** — `index.html:L6035–6035` · ArrowFunction · parent F0691.  
Ulaz: `n`.  
Trag tela: `available(s,n)`.  
Poziva: `available` L6035 → ~F0095.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0693 · callback s.snails.filter(n=>available(s,n)).sort** — `index.html:L6035–6035` · ArrowFunction · parent F0691.  
Ulaz: `a, b`.  
Trag tela: `b.beauty-a.beauty`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0694 · callback stock.find** — `index.html:L6036–6036` · ArrowFunction · parent F0691.  
Ulaz: `n`.  
Trag tela: `n.id===view.showSnail`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0695 · cell** — `index.html:L6038–6038` · ArrowFunction · parent F0691.  
Ulaz: `k, v`.  
Trag tela: `'<span><small>'+k+'</small><b>'+escapeHtml(v)+'</b></span>'`.  
Poziva: `escapeHtml` L6038 → F0523.  
Pozivaju: index.html:L6043 (F0691); index.html:L6043 (F0691); index.html:L6044 (F0691); index.html:L6044 (F0691); index.html:L6044 (F0691).

**F0696 · callback options** — `index.html:L6041–6041` · ArrowFunction · parent F0691.  
Ulaz: `n`.  
Trag tela: `snailName(n)+' · Lepota '+n.beauty`.  
Poziva: `snailName` L6041 → ~F0107.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0697 · expeditionsScreen** — `index.html:L6054–6074` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view, now`.  
Trag tela: `{ const locked=builtState(s,'expeditions','island-menu','Svemirska luka'); if(locked)return locked; const stock=s.snails.filter(n=>available`.  
Poziva: `builtState` L6055 → F0559; `s.snails.filter(n=>available(s,n)).sort` L6057 → —; `s.snails.filter` L6057 → —; `Number.isInteger` L6058 → —; `header` L6060 → F0539; `pnl` L6060 → F0544; `info` L6060 → F0543; `dec` L6061 → F0528; `expeditionFactor` L6061 → ~F0068; `pnl` L6064 → F0544; `prow` L6064 → F0545; `s.expeditions.map(e=>'<div class="srcrow"><div><b>'+escapeHtml(expeditions[e.destination][0])+'</b>'+ '<span class="mut">'+escapeHtml(expedi` L6064 → —; `s.expeditions.map` L6064 → —; `pnl` L6067 → F0544; `prow` L6067 → F0545; `expeditions.map(([name,lvl,h,bonus,dia,stone],i)=> '<button type="button" class="dest'+(dest===i?' on':'')+'" data-action="expedition-dest" ` L6067 → —; `expeditions.map` L6067 → —; `pnl` L6070 → F0544; `prow` L6070 → F0545; `[0,1,2].map(i=>'<label class="sr-only" for="expedition-slot-'+i+'">Puž '+(i+1)+'</label><select id="expedition-slot-'+i+'" name="expedition-` L6070 → —; `[0,1,2].map` L6070 → —; `btn` L6072 → F0537; `btn` L6072 → F0537; `btn` L6073 → F0537.  
Pozivaju: index.html:L6425 (F0762).

**F0698 · callback s.snails.filter** — `index.html:L6057–6057` · ArrowFunction · parent F0697.  
Ulaz: `n`.  
Trag tela: `available(s,n)`.  
Poziva: `available` L6057 → ~F0095.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0699 · callback s.snails.filter(n=>available(s,n)).sort** — `index.html:L6057–6057` · ArrowFunction · parent F0697.  
Ulaz: `a, b`.  
Trag tela: `b.prod-a.prod`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0700 · callback s.expeditions.map** — `index.html:L6064–6066` · ArrowFunction · parent F0697.  
Ulaz: `e`.  
Trag tela: `'<div class="srcrow"><div><b>'+escapeHtml(expeditions[e.destination][0])+'</b>'+ '<span class="mut">'+escapeHtml(expeditionTeam(e).map(id=>{`.  
Poziva: `escapeHtml` L6064 → F0523; `escapeHtml` L6065 → F0523; `expeditionTeam(e).map(id=>{const n=s.snails.find(v=>v.id===id);return n?snailName(n):'?';}).join` L6065 → —; `expeditionTeam(e).map` L6065 → —; `expeditionTeam` L6065 → ~F0076; `countdown` L6065 → F0548; `btn` L6066 → F0537; `btn` L6066 → F0537; `cur` L6066 → F0538.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0701 · callback expeditionTeam(e).map** — `index.html:L6065–6065` · ArrowFunction · parent F0700.  
Ulaz: `id`.  
Trag tela: `{const n=s.snails.find(v=>v.id===id);return n?snailName(n):'?';}`.  
Poziva: `s.snails.find` L6065 → —; `snailName` L6065 → ~F0107.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0702 · callback s.snails.find** — `index.html:L6065–6065` · ArrowFunction · parent F0701.  
Ulaz: `v`.  
Trag tela: `v.id===id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0703 · callback expeditions.map** — `index.html:L6067–6069` · ArrowFunction · parent F0697.  
Ulaz: `[name,lvl,h,bonus,dia,stone], i`.  
Trag tela: `'<button type="button" class="dest'+(dest===i?' on':'')+'" data-action="expedition-dest" data-value="'+i+'" aria-pressed="'+(dest===i)+'" '+`.  
Poziva: `escapeHtml` L6068 → F0523; `dec` L6069 → F0528; `Math.round` L6069 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0704 · callback [0,1,2].map** — `index.html:L6070–6071` · ArrowFunction · parent F0697.  
Ulaz: `i`.  
Trag tela: `'<label class="sr-only" for="expedition-slot-'+i+'">Puž '+(i+1)+'</label><select id="expedition-slot-'+i+'" name="expedition-slot" class="pi`.  
Poziva: `options` L6071 → F0550.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0705 · callback options** — `index.html:L6071–6071` · ArrowFunction · parent F0704.  
Ulaz: `n`.  
Trag tela: `snailName(n)+' · '+dec(n.prod)+' sliza/s'`.  
Poziva: `snailName` L6071 → ~F0107; `dec` L6071 → F0528.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0706 · feedbackPanel** — `index.html:L6078–6086` · FunctionDeclaration · parent F0522.  
Ulaz: `view`.  
Trag tela: `{ const kind=view?.feedbackKind??'bug'; return pnl(prow('Piši nam','<span class="subtle">preko imejla</span>')+'<div class="fbk">'+[['bug','`.  
Poziva: `pnl` L6080 → F0544; `prow` L6080 → F0545; `[['bug','🐞 Greška'],['idea','💡 Ideja'],['other','✉️ Drugo']].map(([k,l])=> btn('feedback-kind',l,k,true,'fbt'+(kind===k?' on':''))).join` L6080 → —; `[['bug','🐞 Greška'],['idea','💡 Ideja'],['other','✉️ Drugo']].map` L6080 → —; `btn` L6084 → F0537; `info` L6085 → F0543.  
Pozivaju: index.html:L6097 (F0708).

**F0707 · callback [['bug','🐞 Greška'],['idea','💡 Ideja'],['other','✉️ Drugo']].map** — `index.html:L6080–6081` · ArrowFunction · parent F0706.  
Ulaz: `[k,l]`.  
Trag tela: `btn('feedback-kind',l,k,true,'fbt'+(kind===k?' on':''))`.  
Poziva: `btn` L6081 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0708 · progress** — `index.html:L6087–6102` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now, view`.  
Trag tela: `{ const weather=weatherFor(s,now); return header('Napredak')+pnl('<div class="prof">'+(s.avatar!=null?snailPic({species:s.avatar},false):ima`.  
Poziva: `weatherFor` L6088 → ~F0134; `header` L6089 → F0539; `pnl` L6089 → F0544; `snailPic` L6089 → F0541; `image` L6089 → F0540; `escapeHtml` L6090 → F0523; `bar` L6093 → F0546; `xpNeeded` L6093 → ~F0079; `format` L6093 → F0526; `format` L6093 → F0526; `xpNeeded` L6093 → ~F0079; `format` L6093 → F0526; `btn` L6094 → F0537; `btn` L6094 → F0537; `btn` L6094 → F0537; `btn` L6094 → F0537; `pnl` L6095 → F0544; `prow` L6095 → F0545; `btn` L6095 → F0537; `pnl` L6096 → F0544; `prow` L6096 → F0545; `info` L6096 → F0543; `btn` L6096 → F0537; `feedbackPanel` L6097 → F0706; `pnl` L6098 → F0544; `prow` L6098 → F0545; `info` L6099 → F0543; `btn` L6100 → F0537; `incubatorUsed` L6100 → ~F0089; `eggCapacity` L6100 → ~F0088; `weatherControls` L6101 → F0625; `btn` L6101 → F0537.  
Pozivaju: index.html:L6408 (F0762).

**F0709 · trophyRoom** — `index.html:L6103–6112` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ const season=getSeason(s,now), division=divisionOf(s.trophies), next=divisions[division+1]; const claim=previousReward(season.previous); r`.  
Poziva: `getSeason` L6104 → ~F0030; `divisionOf` L6104 → ~F0026; `previousReward` L6105 → ~F0029; `header` L6106 → F0539; `pnl` L6106 → F0544; `prow` L6106 → F0545; `format` L6106 → F0526; `bar` L6107 → F0546; `info` L6107 → F0543; `format` L6107 → F0526; `pnl` L6108 → F0544; `divisions.map(([name,min],index)=>'<li class="'+(index===division?'ok':'')+'"><span>'+(index===division?'▶ ':'')+name+'</span><span class="m` L6108 → —; `divisions.map` L6108 → —; `pnl` L6109 → F0544; `prow` L6109 → F0545; `info` L6110 → F0543; `btn` L6111 → F0537; `cur` L6111 → F0538; `btn` L6111 → F0537.  
Pozivaju: index.html:L6417 (F0762).

**F0710 · callback divisions.map** — `index.html:L6108–6108` · ArrowFunction · parent F0709.  
Ulaz: `[name,min], index`.  
Trag tela: `'<li class="'+(index===division?'ok':'')+'"><span>'+(index===division?'▶ ':'')+name+'</span><span class="mut">'+format(min)+'+</span></li>'`.  
Poziva: `format` L6108 → F0526.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0711 · loginPanel** — `index.html:L6113–6122` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ const login=getLogin(getSeason(s,now),rate(s,now)); const {day,reward}=login; const parts=[reward.sliz&&format(reward.sliz)+' sliza',rewar`.  
Poziva: `getLogin` L6114 → ~F0058; `getSeason` L6114 → ~F0030; `rate` L6114 → ~F0139; `[reward.sliz&&format(reward.sliz)+' sliza',reward.diamonds&&reward.diamonds+' dijamanata', reward.tokens&&reward.tokens+' žetona',reward.dus` L6116 → —; `format` L6116 → F0526; `header` L6118 → F0539; `pnl` L6118 → F0544; `prow` L6118 → F0545; `bar` L6118 → F0546; `loginMilestones.map(n=>'<div class="'+(day>=n?'ok':'')+'"><b>'+(modules.i18n?.current()==='en'?'Day '+n:n+'.')+'</b> '+(modules.i18n?.curren` L6119 → —; `loginMilestones.map` L6119 → —; `info` L6120 → F0543; `info` L6121 → F0543; `parts.join` L6121 → —; `btn` L6121 → F0537; `btn` L6121 → F0537.  
Pozivaju: index.html:L6410 (F0762).

**F0712 · callback loginMilestones.map** — `index.html:L6119–6119` · ArrowFunction · parent F0711.  
Ulaz: `n`.  
Trag tela: `'<div class="'+(day>=n?'ok':'')+'"><b>'+(modules.i18n?.current()==='en'?'Day '+n:n+'.')+'</b> '+(modules.i18n?.current()==='en'?'· ':'dan · `.  
Poziva: `modules.i18n?.current` L6119 → —; `modules.i18n?.current` L6119 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0713 · profilePanel** — `index.html:L6123–6129` · FunctionDeclaration · parent F0522.  
Ulaz: `s`.  
Trag tela: `{ return header('Profil čuvara')+pnl('<div class="prof">'+(s.avatar!=null?snailPic({species:s.avatar},false):image('c_medal.webp','',false))`.  
Poziva: `header` L6124 → F0539; `pnl` L6124 → F0544; `snailPic` L6124 → F0541; `image` L6124 → F0540; `escapeHtml` L6125 → F0523; `format` L6125 → F0526; `s.seen.map(id=>'<option value="'+id+'" '+(s.avatar===id?'selected':'')+'>'+escapeHtml(species[id].sr)+'</option>').join` L6127 → —; `s.seen.map` L6127 → —; `btn` L6128 → F0537; `btn` L6128 → F0537; `btn` L6128 → F0537.  
Pozivaju: index.html:L6411 (F0762).

**F0714 · callback s.seen.map** — `index.html:L6127–6127` · ArrowFunction · parent F0713.  
Ulaz: `id`.  
Trag tela: `'<option value="'+id+'" '+(s.avatar===id?'selected':'')+'>'+escapeHtml(species[id].sr)+'</option>'`.  
Poziva: `escapeHtml` L6127 → F0523.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0715 · cloudPanel** — `index.html:L6130–6157` · FunctionDeclaration · parent F0522.  
Ulaz: `view`.  
Trag tela: `{ const state=view.cloud,connected=Boolean(state.account),account=state.account; const top=header('Cloud kopija · Supabase')+(state.message?`.  
Poziva: `Boolean` L6131 → —; `header` L6132 → F0539; `info` L6132 → F0543; `escapeHtml` L6132 → F0523; `pnl` L6133 → F0544; `prow` L6133 → F0545; `info` L6134 → F0543; `btn` L6135 → F0537; `pnl` L6136 → F0544; `prow` L6136 → F0545; `info` L6137 → F0543; `btn` L6138 → F0537; `pnl` L6139 → F0544; `info` L6139 → F0543; `btn` L6140 → F0537; `pnl` L6141 → F0544; `prow` L6141 → F0545; `info` L6142 → F0543; `btn` L6143 → F0537; `btn` L6144 → F0537; `new Date(account.updatedAt).toLocaleString` L6145 → —; `Date` L6145 → —; `pnl` L6146 → F0544; `prow` L6146 → F0545; `info` L6147 → F0543; `escapeHtml` L6147 → F0523; `info` L6148 → F0543; `btn` L6149 → F0537; `btn` L6150 → F0537; `btn` L6151 → F0537; `btn` L6152 → F0537; `btn` L6153 → F0537; `pnl` L6154 → F0544; `info` L6154 → F0543; `btn` L6155 → F0537; `btn` L6156 → F0537.  
Pozivaju: index.html:L6412 (F0762).

**F0716 · dimensionPanel** — `index.html:L6158–6163` · FunctionDeclaration · parent F0522.  
Ulaz: `s`.  
Trag tela: `{ const active=dimensionOf(s.level); return header('Dimenzije')+pnl('<ul class="dtl">'+dimensions.map(item=>'<li class="'+(active===item?'ok`.  
Poziva: `dimensionOf` L6159 → ~F0073; `header` L6160 → F0539; `pnl` L6160 → F0544; `dimensions.map(item=>'<li class="'+(active===item?'ok':'')+'"><span><b>'+escapeHtml(item.name)+'</b> · nivo '+item.level+ '<br><small class=` L6160 → —; `dimensions.map` L6160 → —; `btn` L6162 → F0537.  
Pozivaju: index.html:L6409 (F0762).

**F0717 · callback dimensions.map** — `index.html:L6160–6161` · ArrowFunction · parent F0716.  
Ulaz: `item`.  
Trag tela: `'<li class="'+(active===item?'ok':'')+'"><span><b>'+escapeHtml(item.name)+'</b> · nivo '+item.level+ '<br><small class="mut">'+escapeHtml(it`.  
Poziva: `escapeHtml` L6160 → F0523; `escapeHtml` L6161 → F0523.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0718 · wheatPanel** — `index.html:L6164–6223` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now, field`.  
Trag tela: `{ const yieldPer=wheatYield(s); const states=WHEAT_FIELDS.map((level,index)=>{ const available=s.level>=level; const built=available&&s.whea`.  
Poziva: `wheatYield` L6165 → ~F0063; `WHEAT_FIELDS.map` L6166 → —; `states.filter` L6172 → —; `states.filter` L6173 → —; `header` L6175 → F0539; `btn` L6177 → F0537; `states.map(v=>btn('wheat-field',String(v.index+1),String(v.index),true,field===v.index?'primary':'')).join` L6178 → —; `states.map` L6178 → —; `pnl` L6180 → F0544; `Math.round` L6181 → —; `format` L6181 → F0526; `format` L6182 → F0526; `cur` L6184 → F0538; `format` L6184 → F0526; `format` L6185 → F0526; `btn` L6187 → F0537; `format` L6187 → F0526; `pnl` L6188 → F0544; `prow` L6188 → F0545; `btn` L6191 → F0537; `format` L6191 → F0526; `info` L6193 → F0543; `states.map(v=>{ const status=!v.available?'Zaključano · nivo '+v.level:!v.built?'Čeka izgradnju':v.stage==='ripe'?'Spremno':v.stage==='green` L6194 → —; `states.map` L6194 → —; `states.filter(v=>v.available&&!v.built).map(v=> btn('island-edit','Izgradi žitno polje '+(v.index+1)+' · probno 0 sliza','new-wheat:'+v.inde` L6206 → —; `states.filter(v=>v.available&&!v.built).map` L6206 → —; `states.filter` L6206 → —; `Number.isInteger` L6208 → —; `pnl` L6209 → F0544; `info` L6210 → F0543; `info` L6213 → F0543; `pnl` L6215 → F0544; `btn` L6216 → F0537; `pnl` L6218 → F0544; `prow` L6218 → F0545; `countdown` L6220 → F0548; `btn` L6221 → F0537; `format` L6221 → F0526.  
Pozivaju: index.html:L6421 (F0762).

**F0719 · callback WHEAT_FIELDS.map** — `index.html:L6166–6171` · ArrowFunction · parent F0718.  
Ulaz: `level, index`.  
Trag tela: `{ const available=s.level>=level; const built=available&&s.wheatBuilt?.includes(index)&&Boolean(s.islandPositions?.[index?'wheat:'+index:'wh`.  
Poziva: `s.wheatBuilt?.includes` L6168 → —; `Boolean` L6168 → —; `wheatStage` L6169 → ~F0067; `wheatDeadline` L6170 → ~F0066.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0720 · callback states.filter** — `index.html:L6172–6172` · ArrowFunction · parent F0718.  
Ulaz: `v`.  
Trag tela: `v.stage==='ripe'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0721 · callback states.filter** — `index.html:L6173–6173` · ArrowFunction · parent F0718.  
Ulaz: `v`.  
Trag tela: `v.unlocked`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0722 · callback states.map** — `index.html:L6178–6178` · ArrowFunction · parent F0718.  
Ulaz: `v`.  
Trag tela: `btn('wheat-field',String(v.index+1),String(v.index),true,field===v.index?'primary':'')`.  
Poziva: `btn` L6178 → F0537; `String` L6178 → —; `String` L6178 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0723 · callback states.map** — `index.html:L6194–6205` · ArrowFunction · parent F0718.  
Ulaz: `v`.  
Trag tela: `{ const status=!v.available?'Zaključano · nivo '+v.level:!v.built?'Čeka izgradnju':v.stage==='ripe'?'Spremno':v.stage==='green'?'Raste':'Pos`.  
Poziva: `countdown` L6197 → F0548.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0724 · callback states.filter** — `index.html:L6206–6206` · ArrowFunction · parent F0718.  
Ulaz: `v`.  
Trag tela: `v.available&&!v.built`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0725 · callback states.filter(v=>v.available&&!v.built).map** — `index.html:L6206–6207` · ArrowFunction · parent F0718.  
Ulaz: `v`.  
Trag tela: `btn('island-edit','Izgradi žitno polje '+(v.index+1)+' · probno 0 sliza','new-wheat:'+v.index,true,'primary')`.  
Poziva: `btn` L6207 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0726 · more** — `index.html:L6225–6243` · FunctionDeclaration · parent F0522.  
Ulaz: `s, now`.  
Trag tela: `{ // v147 Shop > Build card presentation, current v0.8.x actions and reducer unchanged. const art=Object.fromEntries(islandBuildings.map(([i`.  
Poziva: `Object.fromEntries` L6227 → —; `islandBuildings.map` L6227 → —; `islandBuildings.map(([id,label])=>{ const lock=buildings[id]&&!s.built.includes(id); return card(id,label,art[id]??'b_shop',lock?'Od nivoa '` L6232 → —; `islandBuildings.map` L6232 → —; `card` L6236 → F0728; `card` L6237 → F0728; `card` L6238 → F0728; `header` L6239 → F0539; `btn` L6242 → F0537; `meteorPanel` L6242 → F0688.  
Pozivaju: index.html:L6415 (F0762).

**F0727 · callback islandBuildings.map** — `index.html:L6227–6227` · ArrowFunction · parent F0726.  
Ulaz: `[id]`.  
Trag tela: `[id,{reservoir:'b_barrel',incubator:'b_incubator',tree:'b_tree',shop:'b_shop',timebreaker:'b_timebreaker',...buildingArt}[id]]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0728 · card** — `index.html:L6228–6231` · ArrowFunction · parent F0726.  
Ulaz: `id, label, asset, sub, action='open'`.  
Trag tela: `'<button type="button" class="sc147-bcard" data-action="'+action+'" data-value="'+escapeHtml(id)+'">'+ (asset?image(asset+'.webp'):'<span cl`.  
Poziva: `escapeHtml` L6229 → F0523; `image` L6230 → F0540; `escapeHtml` L6231 → F0523; `escapeHtml` L6231 → F0523.  
Pozivaju: index.html:L6234 (F0729); index.html:L6236 (F0726); index.html:L6237 (F0726); index.html:L6238 (F0726).

**F0729 · callback islandBuildings.map** — `index.html:L6232–6235` · ArrowFunction · parent F0726.  
Ulaz: `[id,label]`.  
Trag tela: `{ const lock=buildings[id]&&!s.built.includes(id); return card(id,label,art[id]??'b_shop',lock?'Od nivoa '+buildings[id][1]:'Otvori'); }`.  
Poziva: `s.built.includes` L6233 → —; `card` L6234 → F0728.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0730 · settings** — `index.html:L6245–6273` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view`.  
Trag tela: `{ const cloud=view.cloud, online=cloud.account?'Supabase kopija':cloud.status==='offline'?'Van mreže':'Lokalno'; const sec=(title,inner)=>'<`.  
Poziva: `popHead` L6248 → F0542; `modules.i18n?.translate` L6248 → —; `sec` L6249 → F0731; `btn` L6249 → F0537; `Math.round` L6250 → —; `sec` L6252 → F0731; `escapeHtml` L6252 → F0523; `btn` L6253 → F0537; `sec` L6255 → F0731; `btn` L6256 → F0537; `sec` L6257 → F0731; `btn('lang','🇷🇸 Srpski','sr',true,view.lang==='sr'?'primary':'').replace` L6257 → —; `btn` L6257 → F0537; `btn('lang','🇬🇧 English','en',true,view.lang==='en'?'primary':'').replace` L6257 → —; `btn` L6257 → F0537; `sec` L6259 → F0731; `btn` L6259 → F0537; `btn` L6260 → F0537; `sec` L6261 → F0731; `btn` L6261 → F0537; `sec` L6263 → F0731; `btn` L6263 → F0537; `btn` L6264 → F0537; `sec` L6265 → F0731; `btn` L6265 → F0537; `btn` L6265 → F0537; `btn` L6266 → F0537; `sec` L6267 → F0731; `btn` L6267 → F0537; `btn` L6267 → F0537; `btn` L6268 → F0537; `btn` L6269 → F0537; `btn` L6269 → F0537; `btn` L6270 → F0537; `btn` L6270 → F0537; `btn` L6271 → F0537; `btn` L6271 → F0537; `btn` L6272 → F0537.  
Pozivaju: index.html:L6413 (F0762).

**F0731 · sec** — `index.html:L6247–6247` · ArrowFunction · parent F0730.  
Ulaz: `title, inner`.  
Trag tela: `'<section class="sec"><h4>'+title+'</h4>'+inner+'</section>'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L6249 (F0730); index.html:L6252 (F0730); index.html:L6255 (F0730); index.html:L6257 (F0730); index.html:L6259 (F0730); index.html:L6261 (F0730); index.html:L6263 (F0730); index.html:L6265 (F0730); index.html:L6267 (F0730).

**F0732 · anBars** — `index.html:L6288–6291` · FunctionDeclaration · parent F0522.  
Ulaz: `rows, key, names`.  
Trag tela: `{ const max=Math.max(1,...rows.map(r=>r[key])); return rows.map(r=>'<div class="anr"><span class="ana">'+escapeHtml(names[r.a]??r.a)+'</span`.  
Poziva: `Math.max` L6289 → —; `rows.map` L6289 → —; `rows.map(r=>'<div class="anr"><span class="ana">'+escapeHtml(names[r.a]??r.a)+'</span><i style="width:'+Math.round(r[key]/max*100)+'%"></i><` L6290 → —; `rows.map` L6290 → —.  
Pozivaju: index.html:L6298 (F0735); index.html:L6299 (F0735); index.html:L6336 (F0749).

**F0733 · callback rows.map** — `index.html:L6289–6289` · ArrowFunction · parent F0732.  
Ulaz: `r`.  
Trag tela: `r[key]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0734 · callback rows.map** — `index.html:L6290–6290` · ArrowFunction · parent F0732.  
Ulaz: `r`.  
Trag tela: `'<div class="anr"><span class="ana">'+escapeHtml(names[r.a]??r.a)+'</span><i style="width:'+Math.round(r[key]/max*100)+'%"></i><b>'+short(r[`.  
Poziva: `escapeHtml` L6290 → F0523; `Math.round` L6290 → —; `short` L6290 → F0527.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0735 · anCurrency** — `index.html:L6292–6300` · FunctionDeclaration · parent F0522.  
Ulaz: `an, k`.  
Trag tela: `{ const rows=Object.entries(an.acts).map(([a,r])=>({a,inn:r[k+'+']??0,out:r[k+'-']??0})).filter(r=>r.inn||r.out); if(!rows.length)return '';`.  
Poziva: `Object.entries(an.acts).map(([a,r])=>({a,inn:r[k+'+']??0,out:r[k+'-']??0})).filter` L6293 → —; `Object.entries(an.acts).map` L6293 → —; `Object.entries` L6293 → —; `rows.filter(r=>r.inn).sort` L6295 → —; `rows.filter` L6295 → —; `rows.filter(r=>r.out).sort` L6295 → —; `rows.filter` L6295 → —; `fin.reduce` L6296 → —; `fout.reduce` L6296 → —; `pnl` L6297 → F0544; `prow` L6297 → F0545; `cur` L6297 → F0538; `short` L6297 → F0527; `short` L6297 → F0527; `short` L6297 → F0527; `Math.abs` L6297 → —; `anBars` L6298 → F0732; `anBars` L6299 → F0732.  
Pozivaju: index.html:L6335 (F0755).

**F0736 · callback Object.entries(an.acts).map** — `index.html:L6293–6293` · ArrowFunction · parent F0735.  
Ulaz: `[a,r]`.  
Trag tela: `({a,inn:r[k+'+']??0,out:r[k+'-']??0})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0737 · callback Object.entries(an.acts).map(([a,r])=>({a,inn:r[k+'+']??0,out:r[k+'-']??0})).filter** — `index.html:L6293–6293` · ArrowFunction · parent F0735.  
Ulaz: `r`.  
Trag tela: `r.inn||r.out`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0738 · callback rows.filter** — `index.html:L6295–6295` · ArrowFunction · parent F0735.  
Ulaz: `r`.  
Trag tela: `r.inn`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0739 · callback rows.filter(r=>r.inn).sort** — `index.html:L6295–6295` · ArrowFunction · parent F0735.  
Ulaz: `x, y`.  
Trag tela: `y.inn-x.inn`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0740 · callback rows.filter** — `index.html:L6295–6295` · ArrowFunction · parent F0735.  
Ulaz: `r`.  
Trag tela: `r.out`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0741 · callback rows.filter(r=>r.out).sort** — `index.html:L6295–6295` · ArrowFunction · parent F0735.  
Ulaz: `x, y`.  
Trag tela: `y.out-x.out`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0742 · callback fin.reduce** — `index.html:L6296–6296` · ArrowFunction · parent F0735.  
Ulaz: `a, r`.  
Trag tela: `a+r.inn`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0743 · callback fout.reduce** — `index.html:L6296–6296` · ArrowFunction · parent F0735.  
Ulaz: `a, r`.  
Trag tela: `a+r.out`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0744 · graphCanvas** — `index.html:L6301–6303` · FunctionDeclaration · parent F0522.  
Ulaz: `points, label, kind`.  
Trag tela: `{ return '<canvas role="img" aria-label="'+escapeHtml(label)+'" width="640" height="160" style="width:100%;height:80px" data-plot="'+kind+'"`.  
Poziva: `escapeHtml` L6302 → F0523; `escapeHtml` L6302 → F0523.  
Pozivaju: index.html:L6310 (F0745); index.html:L6318 (F0747).

**F0745 · anSpark** — `index.html:L6304–6312` · FunctionDeclaration · parent F0522.  
Ulaz: `an`.  
Trag tela: `{ const lv=an.lv; if(lv.length<2)return ''; const W=320,H=64,hx=Math.max(.01,lv[lv.length-1][0]),ly=Math.max(1,lv[lv.length-1][1]); const pt`.  
Poziva: `Math.max` L6307 → —; `Math.max` L6307 → —; `lv.map(p=>(p[0]/hx*W).toFixed(1)+','+(H-p[1]/ly*H).toFixed(1)).join` L6308 → —; `lv.map` L6308 → —; `pnl` L6309 → F0544; `prow` L6309 → F0545; `dec` L6309 → F0528; `graphCanvas` L6310 → F0744; `info` L6311 → F0543.  
Pozivaju: index.html:L6335 (F0749).

**F0746 · callback lv.map** — `index.html:L6308–6308` · ArrowFunction · parent F0745.  
Ulaz: `p`.  
Trag tela: `(p[0]/hx*W).toFixed(1)+','+(H-p[1]/ly*H).toFixed(1)`.  
Poziva: `(p[0]/hx*W).toFixed` L6308 → —; `(H-p[1]/ly*H).toFixed` L6308 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0747 · anRaceFrameGraph** — `index.html:L6313–6320` · FunctionDeclaration · parent F0522.  
Ulaz: `values`.  
Trag tela: `{ if(!values?.length)return info('Nema uzoraka trke. Grafikon se puni tokom stvarne trke.'); const W=320,H=64,cap=250; const pts=values.map(`.  
Poziva: `info` L6314 → F0543; `values.map((ms,i)=>(i/Math.max(1,values.length-1)*W).toFixed(1)+','+ (H-Math.min(cap,ms)/cap*H).toFixed(1)).join` L6316 → —; `values.map` L6316 → —; `graphCanvas` L6318 → F0744; `info` L6319 → F0543.  
Pozivaju: index.html:L6362 (F0749).

**F0748 · callback values.map** — `index.html:L6316–6317` · ArrowFunction · parent F0747.  
Ulaz: `ms, i`.  
Trag tela: `(i/Math.max(1,values.length-1)*W).toFixed(1)+','+ (H-Math.min(cap,ms)/cap*H).toFixed(1)`.  
Poziva: `(i/Math.max(1,values.length-1)*W).toFixed` L6316 → —; `Math.max` L6316 → —; `(H-Math.min(cap,ms)/cap*H).toFixed` L6317 → —; `Math.min` L6317 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0749 · analytics** — `index.html:L6321–6375` · FunctionDeclaration · parent F0522.  
Ulaz: `s, view`.  
Trag tela: `{ const an=view.analytics??{sess:0,secs:0,acts:{},scr:{},lv:[]}; const acts=Object.values(an.acts).reduce((a,r)=>a+r.n,0); const scr=Object.`.  
Poziva: `Object.values(an.acts).reduce` L6323 → —; `Object.values` L6323 → —; `Object.entries(an.scr).sort((a,b)=>b[1]-a[1]).slice` L6324 → —; `Object.entries(an.scr).sort` L6324 → —; `Object.entries` L6324 → —; `report.races?.findLast` L6326 → —; `header` L6330 → F0539; `pnl` L6330 → F0544; `prow` L6330 → F0545; `cell` L6330 → F0754; `cell` L6330 → F0754; `dec` L6330 → F0528; `cell` L6331 → F0754; `cell` L6331 → F0754; `info` L6332 → F0543; `pnl` L6333 → F0544; `prow` L6333 → F0545; `info` L6333 → F0543; `btn` L6334 → F0537; `anSpark` L6335 → F0745; `Object.keys(curNames).map(k=>anCurrency(an,k)).join` L6335 → —; `Object.keys(curNames).map` L6335 → —; `Object.keys` L6335 → —; `pnl` L6336 → F0544; `prow` L6336 → F0545; `anBars` L6336 → F0732; `scr.map` L6336 → —; `pnl` L6337 → F0544; `prow` L6337 → F0545; `cell` L6337 → F0754; `cell` L6338 → F0754; `cell` L6338 → F0754; `cell` L6338 → F0754; `cell` L6339 → F0754; `cell` L6339 → F0754; `cell` L6340 → F0754; `cell` L6340 → F0754; `cell` L6341 → F0754; `cell` L6342 → F0754; `cell` L6343 → F0754; `info` L6344 → F0543; `shown` L6344 → F0753; `info` L6345 → F0543; `shown` L6345 → F0753; `shown` L6346 → F0753; `shown` L6346 → F0753; `info` L6347 → F0543; `shown` L6349 → F0753; `info` L6350 → F0543; `shown` L6351 → F0753; `shown` L6352 → F0753; `info` L6353 → F0543; `info` L6354 → F0543; `shown` L6355 → F0753; `shown` L6355 → F0753; `shown` L6356 → F0753; `pnl` L6357 → F0544; `prow` L6357 → F0545; `cell` L6358 → F0754; `cell` L6359 → F0754; `cell` L6360 → F0754; `cell` L6361 → F0754; `anRaceFrameGraph` L6362 → F0747; `info` L6363 → F0543; `escapeHtml` L6363 → F0523; `report.assets.missing.join` L6363 → —; `report.stalls.slice(-8).reverse().map(e=>info(escapeHtml(e.source)+' · '+ e.duration+' ms · '+escapeHtml(e.at))).join` L6365 → —; `report.stalls.slice(-8).reverse().map` L6365 → —; `report.stalls.slice(-8).reverse` L6365 → —; `report.stalls.slice` L6365 → —; `info` L6367 → F0543; `pnl` L6369 → F0544; `prow` L6369 → F0545; `returns.slice(-8).reverse().map(entry=>'<div class="srcrow"><div><b>'+escapeHtml(tracks[entry.track]?.name??entry.track)+'</b><span class="m` L6369 → —; `returns.slice(-8).reverse().map` L6369 → —; `returns.slice(-8).reverse` L6369 → —; `returns.slice` L6369 → —; `info` L6371 → F0543; `info` L6372 → F0543; `pnl` L6373 → F0544; `prow` L6373 → F0545; `info` L6373 → F0543; `btn` L6374 → F0537; `btn` L6374 → F0537; `btn` L6374 → F0537; `btn` L6374 → F0537.  
Pozivaju: index.html:L6418 (F0762).

**F0750 · callback Object.values(an.acts).reduce** — `index.html:L6323–6323` · ArrowFunction · parent F0749.  
Ulaz: `a, r`.  
Trag tela: `a+r.n`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0751 · callback Object.entries(an.scr).sort** — `index.html:L6324–6324` · ArrowFunction · parent F0749.  
Ulaz: `a, b`.  
Trag tela: `b[1]-a[1]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0752 · callback report.races?.findLast** — `index.html:L6326–6326` · ArrowFunction · parent F0749.  
Ulaz: `entry`.  
Trag tela: `entry.sampledN>0`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0753 · shown** — `index.html:L6328–6328` · ArrowFunction · parent F0749.  
Ulaz: `value`.  
Trag tela: `value??'—'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L6329 (F0754); index.html:L6344 (F0749); index.html:L6345 (F0749); index.html:L6346 (F0749); index.html:L6346 (F0749); index.html:L6349 (F0749); index.html:L6351 (F0749); index.html:L6352 (F0749); index.html:L6355 (F0749); index.html:L6355 (F0749); index.html:L6356 (F0749); index.html:L6370 (F0758); index.html:L6370 (F0758).

**F0754 · cell** — `index.html:L6329–6329` · ArrowFunction · parent F0749.  
Ulaz: `v, l`.  
Trag tela: `'<div><strong>'+shown(v)+'</strong><span>'+l+'</span></div>'`.  
Poziva: `shown` L6329 → F0753.  
Pozivaju: index.html:L6330 (F0749); index.html:L6330 (F0749); index.html:L6331 (F0749); index.html:L6331 (F0749); index.html:L6337 (F0749); index.html:L6338 (F0749); index.html:L6338 (F0749); index.html:L6338 (F0749); index.html:L6339 (F0749); index.html:L6339 (F0749); index.html:L6340 (F0749); index.html:L6340 (F0749); index.html:L6341 (F0749); index.html:L6342 (F0749); index.html:L6343 (F0749); index.html:L6358 (F0749); index.html:L6359 (F0749); index.html:L6360 (F0749); index.html:L6361 (F0749).

**F0755 · callback Object.keys(curNames).map** — `index.html:L6335–6335` · ArrowFunction · parent F0749.  
Ulaz: `k`.  
Trag tela: `anCurrency(an,k)`.  
Poziva: `anCurrency` L6335 → F0735.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0756 · callback scr.map** — `index.html:L6336–6336` · ArrowFunction · parent F0749.  
Ulaz: `[a,n]`.  
Trag tela: `({a,inn:n})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0757 · callback report.stalls.slice(-8).reverse().map** — `index.html:L6365–6366` · ArrowFunction · parent F0749.  
Ulaz: `e`.  
Trag tela: `info(escapeHtml(e.source)+' · '+ e.duration+' ms · '+escapeHtml(e.at))`.  
Poziva: `info` L6365 → F0543; `escapeHtml` L6365 → F0523; `escapeHtml` L6366 → F0523.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0758 · callback returns.slice(-8).reverse().map** — `index.html:L6369–6370` · ArrowFunction · parent F0749.  
Ulaz: `entry`.  
Trag tela: `'<div class="srcrow"><div><b>'+escapeHtml(tracks[entry.track]?.name??entry.track)+'</b><span class="mut">'+ shown(entry.maxGapMs)+' ms najdu`.  
Poziva: `escapeHtml` L6369 → F0523; `shown` L6370 → F0753; `shown` L6370 → F0753.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0759 · help** — `index.html:L6376–6381` · FunctionDeclaration · parent F0522.  
Ulaz: `—`.  
Trag tela: `{ return header('Kako se igra')+pnl('<ul class="dtl">'+ '<li><span><b>1. Izlezi puža.</b> Otvori Inkubator; spremno jaje daje puža i XP.</sp`.  
Poziva: `header` L6377 → F0539; `pnl` L6377 → F0544; `btn` L6378 → F0537; `btn` L6379 → F0537.  
Pozivaju: index.html:L6414 (F0762).

**F0760 · wrap** — `index.html:L6384–6392` · ArrowFunction · parent F0522.  
Ulaz: `html, key`.  
Trag tela: `{ // Presentation-only scope; no duplicate menu/state or action dispatch. const shell='<div class="scr-body screen-'+escapeHtml(key)+'">'; c`.  
Poziva: `escapeHtml` L6386 → F0523; `html.indexOf` L6387 → —; `html.startsWith` L6390 → —; `html.indexOf` L6390 → —; `html.slice` L6391 → —; `html.slice` L6391 → —.  
Pozivaju: index.html:L6399 (F0761).

**F0761 · renderPanel** — `index.html:L6393–6400` · FunctionDeclaration · parent F0522.  
Ulaz: `key, s, view, now, moveKey`.  
Trag tela: `{ let html=screen(key,s,view,now); if(moveKey){ const move='<button type="button" class="btn building-move" data-action="island-edit" data-v`.  
Poziva: `screen` L6394 → F0762; `escapeHtml` L6396 → F0523; `html.replace` L6397 → —; `wrap` L6399 → F0760.  
Pozivaju: ~index.html:L7068 (F0864).

**F0762 · screen** — `index.html:L6401–6433` · FunctionDeclaration · parent F0522.  
Ulaz: `key, s, view, now`.  
Trag tela: `{ switch(key){ case 'incubator':return incubator(s,now); case 'shop':return shop(s,view,now); case 'tree':return tree(s,view,now); case 'col`.  
Poziva: `incubator` L6403 → F0618; `shop` L6404 → F0627; `tree` L6405 → F0599; `collection` L6406 → F0645; `habitat` L6407 → F0604; `progress` L6408 → F0708; `dimensionPanel` L6409 → F0716; `loginPanel` L6410 → F0711; `profilePanel` L6411 → F0713; `cloudPanel` L6412 → F0715; `settings` L6413 → F0730; `help` L6414 → F0759; `more` L6415 → F0726; `races` L6416 → F0655; `trophyRoom` L6417 → F0709; `analytics` L6418 → F0749; `arena` L6419 → F0668; `reservoir` L6420 → F0622; `wheatPanel` L6421 → F0718; `breeding` L6422 → F0680; `crater` L6423 → F0689; `pageants` L6424 → F0691; `expeditionsScreen` L6425 → F0697; `timebreaker` L6426 → F0624; `header` L6427 → F0539; `info` L6428 → F0543; `header` L6429 → F0539; `info` L6430 → F0543; `header` L6431 → F0539; `info` L6431 → F0543.  
Pozivaju: index.html:L6394 (F0761).

**F0763 · updateClockNodes** — `index.html:L6434–6445` · FunctionDeclaration · parent F0522.  
Ulaz: `root, now`.  
Trag tela: `{ for(const n of root.querySelectorAll('[data-until]')){ const until=Number(n.dataset.until); const value=now>=until?n.dataset.ready:timer(u`.  
Poziva: `root.querySelectorAll` L6435 → —; `Number` L6436 → —; `timer` L6437 → F0529; `root.querySelectorAll` L6440 → —; `Number` L6441 → —; `Number` L6441 → —; `incubationProgress` L6442 → F0549.  
Pozivaju: ~index.html:L7101 (F0871).

**F0764 · modal** — `index.html:L6447–6449` · FunctionDeclaration · parent F0522.  
Ulaz: `title, message, actions`.  
Trag tela: `{ return popHead(title)+info(message)+'<div class="acts">'+actions+'</div>'; }`.  
Poziva: `popHead` L6448 → F0542; `info` L6448 → F0543.  
Pozivaju: index.html:L6503 (F0774); index.html:L6517 (F0777); index.html:L6522 (F0778); index.html:L6524 (F0779); index.html:L6526 (F0780).

**F0765 · hatchPanel** — `index.html:L6450–6456` · FunctionDeclaration · parent F0522.  
Ulaz: `{name,species:speciesId,kind}, levelUp=false`.  
Trag tela: `{ return popHead('Izlegao se puž',eggLabel(kind))+'<div class="hatch-reveal hatch-stage egg-'+kind+'"><div class="hatch-portrait">'+snailPic`.  
Poziva: `popHead` L6451 → F0542; `eggLabel` L6451 → F0534; `snailPic` L6451 → F0541; `escapeHtml` L6452 → F0523; `image` L6452 → F0540; `btn` L6454 → F0537; `btn` L6455 → F0537.  
Pozivaju: ~index.html:L8146 (F0943).

**F0766 · resultPanel** — `index.html:L6457–6469` · FunctionDeclaration · parent F0522.  
Ulaz: `value, race, pending=false`.  
Trag tela: `{ const name=tracks[race.key].name; return popHead(pending?'Upis rezultata…':race.finish.place===1?'Pobeda!':'Cilj',name)+ '<div class="race`.  
Poziva: `popHead` L6459 → F0542; `race.finish.seconds.toFixed` L6461 → —; `info` L6463 → F0543; `info` L6464 → F0543; `info` L6465 → F0543; `btn` L6466 → F0537; `btn` L6467 → F0537; `btn` L6467 → F0537; `btn` L6468 → F0537.  
Pozivaju: ~index.html:L7291 (F0885); ~index.html:L7296 (F0885).

**F0767 · quickSlot** — `index.html:L6471–6480` · FunctionDeclaration · parent F0522.  
Ulaz: `p, i, snail, badge=''`.  
Trag tela: `{ const isMe=i===0, sp=species[p.species]; const colour=isMe?trailOf(snail)[1]:sp.color; const name=isMe?snailName(snail):sp.sr; const pic=i`.  
Poziva: `trailOf` L6473 → F0535; `snailName` L6474 → ~F0107; `snailPic` L6475 → F0541; `snailPic` L6475 → F0541; `p.finished.toFixed` L6476 → —; `escapeHtml` L6478 → F0523.  
Pozivaju: index.html:L6491 (F0772); index.html:L6492 (F0773).

**F0768 · quickResultPanel** — `index.html:L6481–6502` · FunctionDeclaration · parent F0522.  
Ulaz: `value, race, snail, trace=[]`.  
Trag tela: `{ const name=tracks[race.key].name, place=race.finish.place; const order=race.players.map((p,i)=>({p,i})).sort((a,b)=>{ const x=a.p,y=b.p; i`.  
Poziva: `race.players.map((p,i)=>({p,i})).sort` L6483 → —; `race.players.map` L6483 → —; `order.map((o,k)=>quickSlot(o.p,o.i,snail,badge(k))).join` L6491 → —; `order.map` L6491 → —; `race.players.map((p,i)=>quickSlot(p,i,snail)).join` L6492 → —; `race.players.map` L6492 → —; `popHead` L6493 → F0542; `race.finish.seconds.toFixed` L6494 → —; `info` L6496 → F0543; `info` L6497 → F0543; `info` L6498 → F0543; `btn` L6501 → F0537; `btn` L6501 → F0537; `btn` L6501 → F0537.  
Pozivaju: ~index.html:L6970 (F0847).

**F0769 · callback race.players.map** — `index.html:L6483–6483` · ArrowFunction · parent F0768.  
Ulaz: `p, i`.  
Trag tela: `({p,i})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0770 · callback race.players.map((p,i)=>({p,i})).sort** — `index.html:L6483–6489` · ArrowFunction · parent F0768.  
Ulaz: `a, b`.  
Trag tela: `{ const x=a.p,y=b.p; if(x.finished===null&&y.finished===null)return y.dist-x.dist; if(x.finished===null)return 1; if(y.finished===null)retur`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0771 · badge** — `index.html:L6490–6490` · ArrowFunction · parent F0768.  
Ulaz: `k`.  
Trag tela: `order[k].i===0&&k<3?'<b class="qmedal m'+(k+1)+'">'+['Zlato','Srebro','Bronza'][k]+'</b>':'<b class="qplace">'+(k+1)+'</b>'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L6491 (F0772).

**F0772 · callback order.map** — `index.html:L6491–6491` · ArrowFunction · parent F0768.  
Ulaz: `o, k`.  
Trag tela: `quickSlot(o.p,o.i,snail,badge(k))`.  
Poziva: `quickSlot` L6491 → F0767; `badge` L6491 → F0771.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0773 · callback race.players.map** — `index.html:L6492–6492` · ArrowFunction · parent F0768.  
Ulaz: `p, i`.  
Trag tela: `quickSlot(p,i,snail)`.  
Poziva: `quickSlot` L6492 → F0767.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0774 · discardResultPanel** — `index.html:L6503–6504` · ArrowFunction · parent F0522.  
Ulaz: `—`.  
Trag tela: `modal('Izlaz bez čuvanja','Vreme i nagrada ove trke biće izgubljeni.', btn('return-map','Potvrdi izlaz','',true,'danger')+btn('retry-reward'`.  
Poziva: `modal` L6503 → F0764; `btn` L6504 → F0537; `btn` L6504 → F0537.  
Pozivaju: ~index.html:L7949 (F0943).

**F0775 · pausePanel** — `index.html:L6505–6514` · FunctionDeclaration · parent F0522.  
Ulaz: `lost=false, o={}`.  
Trag tela: `{ return popHead(lost?'Obnavljanje grafike':'Pauza','Trka')+ info(lost?'Trka je pauzirana dok se obnavljaju grafički resursi.':'Nastavi kad `.  
Poziva: `popHead` L6506 → F0542; `info` L6507 → F0543; `btn` L6508 → F0537; `btn` L6509 → F0537; `btn` L6510 → F0537; `escapeHtml` L6510 → F0523; `modules.race.RACE_SPEED_OPTIONS.map(v=>btn('race-speed','×'+v+(v===modules.race.RACE_NORMAL_SPEED?' · normalno':''),v,true,o.speed===v?'prim` L6511 → —; `modules.race.RACE_SPEED_OPTIONS.map` L6511 → —; `btn` L6513 → F0537; `btn` L6513 → F0537.  
Pozivaju: ~index.html:L7326 (F0889); ~index.html:L8004 (F0943); ~index.html:L8011 (F0943); ~index.html:L8014 (F0943); ~index.html:L8298 (F0978).

**F0776 · callback modules.race.RACE_SPEED_OPTIONS.map** — `index.html:L6511–6511` · ArrowFunction · parent F0775.  
Ulaz: `v`.  
Trag tela: `btn('race-speed','×'+v+(v===modules.race.RACE_NORMAL_SPEED?' · normalno':''),v,true,o.speed===v?'primary':'')`.  
Poziva: `btn` L6511 → F0537.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0777 · importPanel** — `index.html:L6515–6521` · FunctionDeclaration · parent F0522.  
Ulaz: `parsed`.  
Trag tela: `{ const s=parsed.save; return modal('Pregled sejva','Nivo '+s.level+' · '+s.snails.length+' puževa · '+s.eggs.length+' jaja · '+format(s.sli`.  
Poziva: `modal` L6517 → F0764; `format` L6517 → F0526; `btn` L6520 → F0537; `btn` L6520 → F0537.  
Pozivaju: ~index.html:L7204 (F0878).

**F0778 · releasePanel** — `index.html:L6522–6523` · ArrowFunction · parent F0522.  
Ulaz: `n`.  
Trag tela: `modal('Pusti puža',snailName(n)+' odlazi iz kolekcije. U Muzeju ostaje uspomena.', btn('release','Potvrdi',n.id,true,'danger')+btn('release-`.  
Poziva: `modal` L6522 → F0764; `snailName` L6522 → ~F0107; `btn` L6523 → F0537; `btn` L6523 → F0537.  
Pozivaju: ~index.html:L7998 (F0943).

**F0779 · resetPanel** — `index.html:L6524–6525` · ArrowFunction · parent F0522.  
Ulaz: `—`.  
Trag tela: `modal('Započni novu igru','Novi sejv postaje aktivan. Pre upisa možeš izvesti trenutni napredak.', btn('export','Izvezi sejv')+btn('reset','`.  
Poziva: `modal` L6524 → F0764; `btn` L6525 → F0537; `btn` L6525 → F0537; `btn` L6525 → F0537.  
Pozivaju: ~index.html:L8076 (F0943).

**F0780 · erasePanel** — `index.html:L6526–6528` · ArrowFunction · parent F0522.  
Ulaz: `—`.  
Trag tela: `modal('Obriši lokalne podatke', 'Brišu se lokalni napredak i rezervni snimci ove igre. Izvezeni fajlovi i udaljeni profil ostaju na svom mes`.  
Poziva: `modal` L6526 → F0764; `btn` L6528 → F0537; `btn` L6528 → F0537; `btn` L6528 → F0537.  
Pozivaju: ~index.html:L8074 (F0943).

### metrics — merenje

**F0781 · anonimna** — `index.html:L6532–6610` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const { VERSION }=modules.domain; const rounded = (n,d=1) => Math.round(n*10**d)/10**d; function summarize(values) { if(!values.length)ret`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0782 · rounded** — `index.html:L6534–6534` · ArrowFunction · parent F0781.  
Ulaz: `n, d=1`.  
Trag tela: `Math.round(n*10**d)/10**d`.  
Poziva: `Math.round` L6534 → —.  
Pozivaju: index.html:L6538 (F0785); index.html:L6552 (F0787); index.html:L6581 (F0791); index.html:L6582 (F0791); index.html:L6583 (F0791); index.html:L6593 (F0794); index.html:L6598 (F0795); index.html:L6603 (F0795); index.html:L6604 (F0795).

**F0783 · summarize** — `index.html:L6535–6540` · FunctionDeclaration · parent F0781.  
Ulaz: `values`.  
Trag tela: `{ if(!values.length)return {n:0}; const sorted=values.slice().sort((a,b)=>a-b); const pick=p=>rounded(sorted[Math.ceil(p*sorted.length)-1]);`.  
Poziva: `values.slice().sort` L6537 → —; `values.slice` L6537 → —; `pick` L6539 → F0785; `pick` L6539 → F0785; `pick` L6539 → F0785; `pick` L6539 → F0785.  
Pozivaju: index.html:L6581 (F0791); index.html:L6581 (F0791); index.html:L6582 (F0791); index.html:L6582 (F0791); index.html:L6603 (F0795).

**F0784 · callback values.slice().sort** — `index.html:L6537–6537` · ArrowFunction · parent F0783.  
Ulaz: `a, b`.  
Trag tela: `a-b`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0785 · pick** — `index.html:L6538–6538` · ArrowFunction · parent F0783.  
Ulaz: `p`.  
Trag tela: `rounded(sorted[Math.ceil(p*sorted.length)-1])`.  
Poziva: `rounded` L6538 → F0782; `Math.ceil` L6538 → —.  
Pozivaju: index.html:L6539 (F0783); index.html:L6539 (F0783); index.html:L6539 (F0783); index.html:L6539 (F0783).

**F0786 · createMetrics** — `index.html:L6541–6607` · FunctionDeclaration · parent F0781.  
Ulaz: `—`.  
Trag tela: `{ const races=[],returns=[]; const loading={}; const islandCpu=new Float32Array(120);let islandN=0,islandWorst=0; let session=null,longTasks`.  
Poziva: `Float32Array` L6544 → —; `Float32Array` L6548 → —; `PerformanceObserver` L6557 → —; `observer.observe` L6563 → —.  
Pozivaju: ~index.html:L6786 (F0818).

**F0787 · addStall** — `index.html:L6551–6554` · ArrowFunction · parent F0786.  
Ulaz: `source, duration`.  
Trag tela: `{ stalls.push({source,duration:rounded(duration),at:new Date().toISOString()}); if(stalls.length>12)stalls.shift(); }`.  
Poziva: `stalls.push` L6552 → —; `rounded` L6552 → F0782; `new Date().toISOString` L6552 → —; `Date` L6552 → —; `stalls.shift` L6553 → —.  
Pozivaju: index.html:L6560 (F0788); index.html:L6572 (F0790).

**F0788 · anonimna** — `index.html:L6557–6562` · ArrowFunction · parent F0786.  
Ulaz: `list`.  
Trag tela: `{ for(const e of list.getEntries()){ longTasks++;longMax=Math.max(longMax,e.duration); if(e.duration>=250)addStall('longtask',e.duration); }`.  
Poziva: `list.getEntries` L6558 → —; `Math.max` L6559 → —; `addStall` L6560 → F0787.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0789 · start** — `index.html:L6565–6567` · FunctionDeclaration · parent F0786.  
Ulaz: `track, mode, backend, size, raceType, camera`.  
Trag tela: `{ session={track,mode,backend,size,raceType,camera,frames:[],cpu:[],calls:[],upload:[],ms:0,total:0,over50:0,worst:0}; }`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0790 · frame** — `index.html:L6568–6576` · FunctionDeclaration · parent F0786.  
Ulaz: `gap, cpu, calls, upload`.  
Trag tela: `{ if(!session||!(gap>0))return; session.total+=1;session.ms+=gap;session.worst=Math.max(gap,session.worst); if(gap>50)session.over50++; if(g`.  
Poziva: `Math.max` L6570 → —; `addStall` L6572 → F0787; `session.frames.push` L6575 → —; `session.cpu.push` L6575 → —; `session.calls.push` L6575 → —; `session.upload.push` L6575 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0791 · end** — `index.html:L6577–6586` · FunctionDeclaration · parent F0786.  
Ulaz: `status`.  
Trag tela: `{ if(!session)return; const {track,mode,backend,size,raceType,camera,frames,cpu,calls,upload,ms,total,over50,worst}=session; races.push({tra`.  
Poziva: `races.push` L6580 → —; `rounded` L6581 → F0782; `summarize` L6581 → F0783; `summarize` L6581 → F0783; `summarize` L6582 → F0783; `summarize` L6582 → F0783; `rounded` L6582 → F0782; `rounded` L6583 → F0782; `races.shift` L6584 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0792 · islandDraw** — `index.html:L6587–6591` · FunctionDeclaration · parent F0786.  
Ulaz: `cpu`.  
Trag tela: `{ if(!(Number.isFinite(cpu)&&cpu>=0))return; islandCpu[islandN++%islandCpu.length]=cpu; islandWorst=Math.max(islandWorst,cpu); }`.  
Poziva: `Number.isFinite` L6588 → —; `Math.max` L6590 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0793 · mapReturn** — `index.html:L6592–6592` · FunctionDeclaration · parent F0786.  
Ulaz: `samples`.  
Trag tela: `{returns.push(samples);if(returns.length>24)returns.shift();}`.  
Poziva: `returns.push` L6592 → —; `returns.shift` L6592 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0794 · markLoading** — `index.html:L6593–6593` · FunctionDeclaration · parent F0786.  
Ulaz: `name, ms`.  
Trag tela: `{if(Number.isFinite(ms))loading[name]=rounded(Math.max(0,ms));}`.  
Poziva: `Number.isFinite` L6593 → —; `rounded` L6593 → F0782; `Math.max` L6593 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0795 · report** — `index.html:L6594–6605` · FunctionDeclaration · parent F0786.  
Ulaz: `renderer`.  
Trag tela: `{ // Reverse the circular ring into chronological order only when requested. const count=Math.min(raceHistoryCount,raceHistory.length); cons`.  
Poziva: `Math.min` L6596 → —; `Array` L6597 → —; `rounded` L6598 → F0782; `stalls.slice` L6600 → —; `races.slice` L6602 → —; `returns.slice` L6602 → —; `summarize` L6603 → F0783; `Array.from` L6603 → —; `islandCpu.slice` L6603 → —; `Math.min` L6603 → —; `rounded` L6603 → F0782; `rounded` L6604 → F0782.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### cloud — sinhronizacija

**F0796 · anonimna** — `index.html:L6611–6700` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ // Single opt-in cloud backup adapter for the existing local save format. // Publishable frontend key only; Row Level Security enforces us`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0797 · originOk** — `index.html:L6617–6618` · ArrowFunction · parent F0796.  
Ulaz: `—`.  
Trag tela: `!globalThis.Capacitor?.isNativePlatform?.()&& (location.protocol==='https:'||location.protocol==='http:'&&['localhost','127.0.0.1','[::1]'].`.  
Poziva: `globalThis.Capacitor?.isNativePlatform` L6617 → —; `['localhost','127.0.0.1','[::1]'].includes` L6618 → —.  
Pozivaju: index.html:L6625 (F0800).

**F0798 · library** — `index.html:L6619–6623` · FunctionDeclaration · parent F0796.  
Ulaz: `—`.  
Trag tela: `{ if(!libraryPromise)libraryPromise=import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.119.2/+esm') .catch(error=>{libraryPromise=`.  
Poziva: `import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.119.2/+esm') .catch` L6620 → —; `import` L6620 → —.  
Pozivaju: index.html:L6627 (F0800).

**F0799 · callback import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.119.2/+esm') .catch** — `index.html:L6621–6621` · ArrowFunction · parent F0798.  
Ulaz: `error`.  
Trag tela: `{libraryPromise=null;throw error;}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0800 · getClient** — `index.html:L6624–6632` · FunctionDeclaration · parent F0796.  
Ulaz: `—`.  
Trag tela: `{ if(!originOk())throw Error('Cloud radi na HTTPS sajtu ili localhost-u, ne iz lokalnog fajla.'); if(!client){ const {createClient}=await li`.  
Poziva: `originOk` L6625 → F0797; `Error` L6625 → —; `library` L6627 → F0798; `createClient` L6628 → —.  
Pozivaju: index.html:L6634 (F0801); index.html:L6685 (F0805).

**F0801 · identity** — `index.html:L6633–6647` · FunctionDeclaration · parent F0796.  
Ulaz: `create=false`.  
Trag tela: `{ const sdk=await getClient(); const {data:sessionResult,error:sessionError}=await sdk.auth.getSession(); if(sessionError)throw sessionError`.  
Poziva: `getClient` L6634 → F0800; `sdk.auth.getSession` L6635 → —; `sdk.auth.signInAnonymously` L6639 → —; `sdk.auth.getUser` L6643 → —; `Error` L6645 → —.  
Pozivaju: index.html:L6649 (F0802); index.html:L6659 (F0803); index.html:L6675 (F0804); index.html:L6690 (F0806).

**F0802 · status** — `index.html:L6648–6657` · FunctionDeclaration · parent F0796.  
Ulaz: `create=false`.  
Trag tela: `{ const {sdk,user}=await identity(create); if(!user)return {account:null}; const {data,error}=await sdk.from('sc_player_saves') .select('rev`.  
Poziva: `identity` L6649 → F0801; `sdk.from('sc_player_saves') .select('revision,schema_version,updated_at').eq('user_id',user.id).maybeSingle` L6651 → —; `sdk.from('sc_player_saves') .select('revision,schema_version,updated_at').eq` L6651 → —; `sdk.from('sc_player_saves') .select` L6651 → —; `sdk.from` L6651 → —; `Number` L6654 → —; `Error` L6655 → —; `Number` L6656 → —; `Boolean` L6656 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0803 · upload** — `index.html:L6658–6673` · FunctionDeclaration · parent F0796.  
Ulaz: `save, expected, exists=false`.  
Trag tela: `{ const {sdk,user}=await identity(); if(!user)throw Error('Prvo poveži cloud profil.'); if(!Number.isSafeInteger(expected)||expected<0)throw`.  
Poziva: `identity` L6659 → F0801; `Error` L6660 → —; `Number.isSafeInteger` L6661 → —; `Error` L6661 → —; `new Date().toISOString` L6662 → —; `Date` L6662 → —; `sdk.from('sc_player_saves').insert({user_id:user.id,...record}).select('revision,updated_at').maybeSingle` L6665 → —; `sdk.from('sc_player_saves').insert({user_id:user.id,...record}).select` L6665 → —; `sdk.from('sc_player_saves').insert` L6665 → —; `sdk.from` L6665 → —; `sdk.from('sc_player_saves').update(record) .eq('user_id',user.id).eq('revision',expected).select('revision,updated_at').maybeSingle` L6667 → —; `sdk.from('sc_player_saves').update(record) .eq('user_id',user.id).eq('revision',expected).select` L6667 → —; `sdk.from('sc_player_saves').update(record) .eq('user_id',user.id).eq` L6667 → —; `sdk.from('sc_player_saves').update(record) .eq` L6667 → —; `sdk.from('sc_player_saves').update` L6667 → —; `sdk.from` L6667 → —; `Error` L6670 → —; `Number` L6672 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0804 · deleteCopy** — `index.html:L6674–6683` · FunctionDeclaration · parent F0796.  
Ulaz: `expected`.  
Trag tela: `{ const {sdk,user}=await identity(); if(!user)throw Error('Cloud sesija nije aktivna.'); if(!Number.isSafeInteger(expected)||expected<0)thro`.  
Poziva: `identity` L6675 → F0801; `Error` L6676 → —; `Number.isSafeInteger` L6677 → —; `Error` L6677 → —; `sdk.from('sc_player_saves').delete() .eq('user_id',user.id).eq('revision',expected).select('revision').maybeSingle` L6678 → —; `sdk.from('sc_player_saves').delete() .eq('user_id',user.id).eq('revision',expected).select` L6678 → —; `sdk.from('sc_player_saves').delete() .eq('user_id',user.id).eq` L6678 → —; `sdk.from('sc_player_saves').delete() .eq` L6678 → —; `sdk.from('sc_player_saves').delete` L6678 → —; `sdk.from` L6678 → —; `Error` L6681 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0805 · signOut** — `index.html:L6684–6688` · FunctionDeclaration · parent F0796.  
Ulaz: `—`.  
Trag tela: `{ const sdk=await getClient(); const {error}=await sdk.auth.signOut(); if(error)throw error; }`.  
Poziva: `getClient` L6685 → F0800; `sdk.auth.signOut` L6686 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0806 · download** — `index.html:L6689–6698` · FunctionDeclaration · parent F0796.  
Ulaz: `—`.  
Trag tela: `{ const {sdk,user}=await identity(); if(!user)throw Error('Cloud sesija nije aktivna.'); const {data,error}=await sdk.from('sc_player_saves'`.  
Poziva: `identity` L6690 → F0801; `Error` L6691 → —; `sdk.from('sc_player_saves') .select('save_data,revision,schema_version,updated_at').eq('user_id',user.id).maybeSingle` L6692 → —; `sdk.from('sc_player_saves') .select('save_data,revision,schema_version,updated_at').eq` L6692 → —; `sdk.from('sc_player_saves') .select` L6692 → —; `sdk.from` L6692 → —; `Error` L6695 → —; `Number` L6696 → —; `Error` L6696 → —; `Number` L6697 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### i18n — prevodi

**F0807 · anonimna** — `index.html:L6702–6770` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const EN_DICTIONARY=Object.freeze({"Privremena sesija: prethodni HTTPS sejv nije učitan. Napredak se ovde NE čuva. Otvori igru preko HTTPS`.  
Poziva: `Object.freeze` L6703 → —; `WeakMap` L6704 → —; `WeakMap` L6705 → —; `Map` L6706 → —; `Map` L6708 → —; `Object.entries(EN_DICTIONARY).filter(([key])=>/\{[0-9]+\}/.test(key)).map(([key,val])=>{ const escaped=key.replace(/[.*+?^${}()|[\]\\]/g,'\\` L6710 → —; `Object.entries(EN_DICTIONARY).filter(([key])=>/\{[0-9]+\}/.test(key)).map(([key,val])=>{ const escaped=key.replace(/[.*+?^${}()|[\]\\]/g,'\\` L6710 → —; `Object.entries(EN_DICTIONARY).filter(([key])=>/\{[0-9]+\}/.test(key)).map` L6710 → —; `Object.entries(EN_DICTIONARY).filter` L6710 → —; `Object.entries` L6710 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0808 · callback Object.entries(EN_DICTIONARY).filter** — `index.html:L6710–6710` · ArrowFunction · parent F0807.  
Ulaz: `[key]`.  
Trag tela: `/\{[0-9]+\}/.test(key)`.  
Poziva: `/\{[0-9]+\}/.test` L6710 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0809 · callback Object.entries(EN_DICTIONARY).filter(([key])=>/\{[0-9]+\}/.test(key)).map** — `index.html:L6710–6713` · ArrowFunction · parent F0807.  
Ulaz: `[key,val]`.  
Trag tela: `{ const escaped=key.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/\\\{(\d+)\\\}/g,'(.+?)'); return {expr:new RegExp('^'+escaped+'$','u'),tr`.  
Poziva: `key.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace` L6711 → —; `key.replace` L6711 → —; `RegExp` L6712 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0810 · callback Object.entries(EN_DICTIONARY).filter(([key])=>/\{[0-9]+\}/.test(key)).map(([key,val])=>{ const escaped=key.replace(/[.*+?^${}()|[\]\\]/g,'\\** — `index.html:L6713–6713` · ArrowFunction · parent F0807.  
Ulaz: `o`.  
Trag tela: `o.expr`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0811 · callback Object.entries(EN_DICTIONARY).filter(([key])=>/\{[0-9]+\}/.test(key)).map(([key,val])=>{ const escaped=key.replace(/[.*+?^${}()|[\]\\]/g,'\\** — `index.html:L6713–6713` · ArrowFunction · parent F0807.  
Ulaz: `a, b`.  
Trag tela: `b.expr.source.length-a.expr.source.length`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0812 · current** — `index.html:L6714–6714` · FunctionDeclaration · parent F0807.  
Ulaz: `—`.  
Trag tela: `{return lang;}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0813 · setLanguage** — `index.html:L6715–6719` · FunctionDeclaration · parent F0807.  
Ulaz: `value`.  
Trag tela: `{ if(value!=='sr'&&value!=='en')return false; lang=value;document.documentElement.lang=value==='sr'?'sr-Latn':'en'; document.title='Snail Ci`.  
Poziva: `modules.domain.VERSION.split` L6718 → —; `memo.clear` L6718 → —.  
Pozivaju: ~index.html:L6793 (F0818); ~index.html:L7930 (F0943).

**F0814 · translate** — `index.html:L6720–6738` · FunctionDeclaration · parent F0807.  
Ulaz: `value`.  
Trag tela: `{ if(lang==='sr'||typeof value!=='string'||!value)return value; if(memo.has(value))return memo.get(value); const begin=value.match(/^\s*/u)?`.  
Poziva: `memo.has` L6722 → —; `memo.get` L6722 → —; `value.match` L6723 → —; `value.match` L6724 → —; `value.slice` L6725 → —; `/[\p{L}]/u.test` L6726 → —; `Object.prototype.hasOwnProperty.call` L6727 → —; `x.expr.exec` L6729 → —; `x.translation.replace` L6729 → —; `memo.clear` L6736 → —; `memo.set` L6737 → —.  
Pozivaju: index.html:L6742 (F0816); index.html:L6755 (F0817); index.html:L6764 (F0817); ~index.html:L5819 (F0627); ~index.html:L5819 (F0627); ~index.html:L5821 (F0632); ~index.html:L5821 (F0632); ~index.html:L5902 (F0660); ~index.html:L5902 (F0660); ~index.html:L5946 (F0671); ~index.html:L5983 (F0679).

**F0815 · callback x.translation.replace** — `index.html:L6729–6729` · ArrowFunction · parent F0814.  
Ulaz: `_, i`.  
Trag tela: `m[Number(i)+1]??''`.  
Poziva: `Number` L6729 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0816 · rememberText** — `index.html:L6739–6744` · FunctionDeclaration · parent F0807.  
Ulaz: `node, source`.  
Trag tela: `{ if(!node)return; sources.set(node,String(source)); const dst=translate(String(source)); if(node.textContent!==dst)node.textContent=dst; }`.  
Poziva: `sources.set` L6741 → —; `String` L6741 → —; `translate` L6742 → F0814; `String` L6742 → —.  
Pozivaju: ~index.html:L6827 (F0826).

**F0817 · apply** — `index.html:L6745–6768` · FunctionDeclaration · parent F0807.  
Ulaz: `root`.  
Trag tela: `{ if(!root)return; // Localized only at explicit view updates. No DOM observer on game frame loop. const walker=document.createTreeWalker(ro`.  
Poziva: `document.createTreeWalker` L6748 → —; `walker.nextNode` L6749 → —; `parent.closest` L6751 → —; `sources.get` L6752 → —; `source?.trim` L6753 → —; `sources.set` L6754 → —; `translate` L6755 → F0814; `root.querySelectorAll` L6758 → —; `attributes.get` L6760 → —; `el.hasAttribute` L6762 → —; `Object.prototype.hasOwnProperty.call` L6763 → —; `el.getAttribute` L6763 → —; `translate` L6764 → F0814; `el.getAttribute` L6764 → —; `el.setAttribute` L6764 → —; `attributes.set` L6766 → —.  
Pozivaju: ~index.html:L7019 (F0857); ~index.html:L7932 (F0943); ~index.html:L8344 (F0975).

### app — orkestracija, unos, lifecycle

**F0818 · anonimna** — `index.html:L6771–8364` · ArrowFunction · parent F0023.  
Ulaz: `—`.  
Trag tela: `{ const { VERSION, WHEAT_LEVEL, WHEAT_FIELDS, wheatStage, ACTIVE_MS, newGame, eggAssets, applyCommand, available, uuid, reserveAt, reservoir`.  
Poziva: `$` L6785 → F0819; `$` L6785 → F0819; `$` L6785 → F0819; `$` L6785 → F0819; `createMetrics` L6786 → ~F0786; `globalThis.matchMedia` L6787 → —; `(()=>{ try{return JSON.parse(localStorage.getItem('snail-city-rebuild.preferences')??'null')??{};}catch{return {};} })` L6788 → —; `(navigator.languages?.length?navigator.languages:[navigator.language||'sr']).some` L6792 → —; `modules.i18n.setLanguage` L6793 → ~F0813; `Set` L6803 → —; `Map` L6817 → —; `(()=>{ let a=null; try{a=JSON.parse(localStorage.getItem(AN_KEY)??'null');}catch{} if(!a||typeof a!=='object')a={}; return {sess:a.sess??0,s` L6845 → —; `boot` L8361 → F0975.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0819 · $** — `index.html:L6784–6784` · ArrowFunction · parent F0818.  
Ulaz: `id`.  
Trag tela: `document.getElementById(id)`.  
Poziva: `document.getElementById` L6784 → —.  
Pozivaju: index.html:L6785 (F0818); index.html:L6785 (F0818); index.html:L6785 (F0818); index.html:L6785 (F0818); index.html:L6828 (F0827); index.html:L6832 (F0830); index.html:L6888 (F0837); index.html:L6889 (F0837); index.html:L6890 (F0837); index.html:L6892 (F0837); index.html:L6892 (F0837); index.html:L6893 (F0837); index.html:L6894 (F0837); index.html:L6908 (F0837); index.html:L6911 (F0837); index.html:L6911 (F0837); index.html:L6911 (F0837); index.html:L6912 (F0837); index.html:L6917 (F0839); index.html:L6929 (F0844); index.html:L6929 (F0844); index.html:L6936 (F0845); index.html:L6936 (F0845); index.html:L6936 (F0845); index.html:L6944 (F0846); index.html:L6996 (F0852); index.html:L7069 (F0864); index.html:L7070 (F0864); index.html:L7071 (F0864); index.html:L7072 (F0864); index.html:L7072 (F0864); index.html:L7084 (F0869); index.html:L7085 (F0869); index.html:L7102 (F0871); index.html:L7102 (F0871); index.html:L7121 (F0871); index.html:L7122 (F0871); index.html:L7122 (F0871); index.html:L7126 (F0871); index.html:L7128 (F0871); index.html:L7128 (F0871); index.html:L7137 (F0871); index.html:L7138 (F0871); index.html:L7141 (F0871); index.html:L7143 (F0871); index.html:L7148 (F0871); index.html:L7149 (F0871); index.html:L7151 (F0871); index.html:L7163 (F0871); index.html:L7180 (F0876); index.html:L7229 (F0882); index.html:L7229 (F0882); index.html:L7230 (F0882); index.html:L7231 (F0882); index.html:L7232 (F0882); index.html:L7232 (F0882); index.html:L7234 (F0882); index.html:L7237 (F0882); index.html:L7237 (F0882); index.html:L7238 (F0882); index.html:L7239 (F0882); index.html:L7245 (F0882); index.html:L7246 (F0882); index.html:L7247 (F0882); index.html:L7278 (F0883); index.html:L7278 (F0883); index.html:L7278 (F0883); index.html:L7278 (F0883); index.html:L7319 (F0887); index.html:L7337 (F0892); index.html:L7365 (F0894); index.html:L7648 (F0909); index.html:L7649 (F0909); index.html:L7649 (F0909); index.html:L7650 (F0909); index.html:L7651 (F0909); index.html:L7655 (F0910); index.html:L7655 (F0910); index.html:L7659 (F0910); index.html:L7663 (F0910); index.html:L7670 (F0911); index.html:L7733 (F0922); index.html:L7733 (F0922); index.html:L7835 (F0939); index.html:L7842 (F0940); index.html:L7846 (F0940); index.html:L7871 (F0941); index.html:L7876 (F0941); index.html:L8010 (F0943); index.html:L8014 (F0943); index.html:L8024 (F0943); index.html:L8025 (F0943); index.html:L8066 (F0943); index.html:L8148 (F0943); index.html:L8180 (F0965); index.html:L8212 (F0967); index.html:L8215 (F0960); index.html:L8276 (F0975); index.html:L8351 (F0975); index.html:L8358 (F0975); index.html:L8358 (F0975).

**F0820 · anonimna** — `index.html:L6788–6790` · ArrowFunction · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ try{return JSON.parse(localStorage.getItem('snail-city-rebuild.preferences')??'null')??{};}catch{return {};} }`.  
Poziva: `JSON.parse` L6789 → —; `localStorage.getItem` L6789 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0821 · callback (navigator.languages?.length?navigator.languages:[navigator.language||'sr']).some** — `index.html:L6792–6792` · ArrowFunction · parent F0818.  
Ulaz: `v`.  
Trag tela: `/^(sr|hr|bs|sh|cnr|me)(-|$)/i.test(v)`.  
Poziva: `/^(sr|hr|bs|sh|cnr|me)(-|$)/i.test` L6792 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0822 · watchTransient** — `index.html:L6804–6810` · FunctionDeclaration · parent F0818.  
Ulaz: `animation`.  
Trag tela: `{ transientFx.add(animation); const done=()=>transientFx.delete(animation); animation.addEventListener('finish',done,{once:true}); animation`.  
Poziva: `transientFx.add` L6805 → —; `animation.addEventListener` L6807 → —; `animation.addEventListener` L6808 → —.  
Pozivaju: index.html:L7679 (F0911); index.html:L7688 (F0913); index.html:L8127 (F0954); index.html:L8133 (F0957).

**F0823 · done** — `index.html:L6806–6806` · ArrowFunction · parent F0822.  
Ulaz: `—`.  
Trag tela: `transientFx.delete(animation)`.  
Poziva: `transientFx.delete` L6806 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0824 · clearTransientFx** — `index.html:L6811–6815` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ for(const animation of transientFx)animation.cancel(); transientFx.clear(); for(const node of document.querySelectorAll('img.fly,.lvup'))n`.  
Poziva: `animation.cancel` L6812 → —; `transientFx.clear` L6813 → —; `document.querySelectorAll` L6814 → —; `node.remove` L6814 → —.  
Pozivaju: index.html:L7044 (F0859); index.html:L7062 (F0864); index.html:L8239 (F0971).

**F0825 · testing** — `index.html:L6820–6820` · ArrowFunction · parent F0818.  
Ulaz: `—`.  
Trag tela: `regularTestSnapshot!==null`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L6829 (F0828); index.html:L7126 (F0871); index.html:L7173 (F0876); index.html:L7176 (F0876); index.html:L7191 (F0877); index.html:L7558 (F0908); index.html:L7713 (F0916); index.html:L7738 (F0922); index.html:L7739 (F0922); index.html:L7752 (F0923); index.html:L7762 (F0924); index.html:L7769 (F0924); index.html:L7777 (F0924); index.html:L7897 (F0943); index.html:L8068 (F0943); index.html:L8074 (F0943); index.html:L8076 (F0943).

**F0826 · set** — `index.html:L6827–6827` · ArrowFunction · parent F0818.  
Ulaz: `element, value`.  
Trag tela: `{if(element)modules.i18n.rememberText(element,String(value));}`.  
Poziva: `modules.i18n.rememberText` L6827 → ~F0816; `String` L6827 → —.  
Pozivaju: index.html:L6838 (F0830); index.html:L6888 (F0837); index.html:L6889 (F0837); index.html:L6893 (F0837); index.html:L6894 (F0837); index.html:L6911 (F0837); index.html:L6911 (F0837); index.html:L6911 (F0837); index.html:L7084 (F0869); index.html:L7088 (F0869); index.html:L7105 (F0871); index.html:L7110 (F0871); index.html:L7122 (F0871); index.html:L7122 (F0871); index.html:L7123 (F0871); index.html:L7126 (F0871); index.html:L7130 (F0871); index.html:L7135 (F0871); index.html:L7137 (F0871); index.html:L7141 (F0871); index.html:L7148 (F0871); index.html:L7163 (F0871); index.html:L7229 (F0882); index.html:L7229 (F0882); index.html:L7230 (F0882); index.html:L7231 (F0882); index.html:L7238 (F0882); index.html:L7243 (F0882); index.html:L7245 (F0882); index.html:L7251 (F0882); index.html:L7278 (F0883); index.html:L7278 (F0883); index.html:L7278 (F0883); index.html:L7278 (F0883); index.html:L7337 (F0892); index.html:L7365 (F0894); index.html:L7649 (F0909); index.html:L7649 (F0909); index.html:L7659 (F0910); index.html:L7663 (F0910); index.html:L7736 (F0922); index.html:L8010 (F0943); index.html:L8014 (F0943); index.html:L8358 (F0975).

**F0827 · selected** — `index.html:L6828–6828` · ArrowFunction · parent F0818.  
Ulaz: `key`.  
Trag tela: `$(key)?.value??''`.  
Poziva: `$` L6828 → F0819.  
Pozivaju: index.html:L6954 (F0847); index.html:L7082 (F0869); index.html:L7082 (F0869); index.html:L7254 (F0883); index.html:L7909 (F0943); index.html:L7910 (F0943); index.html:L8092 (F0943); index.html:L8095 (F0943); index.html:L8096 (F0943); index.html:L8098 (F0943); index.html:L8098 (F0943); index.html:L8099 (F0943); index.html:L8100 (F0943); index.html:L8101 (F0943); index.html:L8103 (F0943); index.html:L8103 (F0943); index.html:L8107 (F0943); index.html:L8107 (F0943); index.html:L8191 (F0964); index.html:L8191 (F0964).

**F0828 · nowBound** — `index.html:L6829–6829` · ArrowFunction · parent F0818.  
Ulaz: `—`.  
Trag tela: `Math.max(Date.now()+(testing()?testClockShift:0),s?.lastAt??0)`.  
Poziva: `Math.max` L6829 → —; `Date.now` L6829 → —; `testing` L6829 → F0825.  
Pozivaju: index.html:L7009 (F0855); index.html:L7064 (F0864); index.html:L7096 (F0871); index.html:L7390 (F0894); index.html:L7726 (F0916); index.html:L7747 (F0923); index.html:L7796 (F0924); index.html:L7864 (F0941); index.html:L8241 (F0971); index.html:L8259 (F0973).

**F0829 · baseTime** — `index.html:L6830–6830` · ArrowFunction · parent F0818.  
Ulaz: `—`.  
Trag tela: `performance.now()`.  
Poziva: `performance.now` L6830 → —.  
Pozivaju: index.html:L7258 (F0883); index.html:L7264 (F0883); index.html:L7267 (F0883); index.html:L7280 (F0883); index.html:L7305 (F0887); index.html:L7325 (F0889); index.html:L7352 (F0894); index.html:L7354 (F0894); index.html:L7356 (F0894); index.html:L7383 (F0894); index.html:L7389 (F0894); index.html:L7391 (F0894); index.html:L7392 (F0894); index.html:L7394 (F0894); index.html:L8275 (F0975); index.html:L8278 (F0975); index.html:L8309 (F0975); index.html:L8312 (F0980); index.html:L8315 (F0981).

**F0830 · toast** — `index.html:L6831–6840` · FunctionDeclaration · parent F0818.  
Ulaz: `text`.  
Trag tela: `{ let target=$('toast'); if(panel.open){ target=panel.querySelector('.dialog-toast')??document.createElement('p'); target.className='dialog-`.  
Poziva: `$` L6832 → F0819; `panel.querySelector` L6834 → —; `document.createElement` L6834 → —; `target.setAttribute` L6835 → —; `panel.prepend` L6836 → —; `set` L6838 → F0826; `clearTimeout` L6839 → —; `setTimeout` L6839 → —.  
Pozivaju: index.html:L6955 (F0847); index.html:L6966 (F0847); index.html:L7186 (F0876); index.html:L7191 (F0877); index.html:L7200 (F0877); index.html:L7205 (F0878); index.html:L7257 (F0883); index.html:L7282 (F0883); index.html:L7547 (F0907); index.html:L7757 (F0923); index.html:L7766 (F0924); index.html:L7775 (F0924); index.html:L7777 (F0924); index.html:L7791 (F0924); index.html:L7818 (F0924); index.html:L7892 (F0943); index.html:L7897 (F0943); index.html:L7933 (F0943); index.html:L8026 (F0943); index.html:L8027 (F0943); index.html:L8044 (F0943); index.html:L8046 (F0943); index.html:L8047 (F0943); index.html:L8052 (F0943); index.html:L8053 (F0943); index.html:L8061 (F0943); index.html:L8062 (F0943); index.html:L8063 (F0943); index.html:L8068 (F0943); index.html:L8072 (F0943); index.html:L8074 (F0943); index.html:L8075 (F0943); index.html:L8076 (F0943); index.html:L8077 (F0943); index.html:L8120 (F0943); index.html:L8149 (F0943); index.html:L8150 (F0943); index.html:L8153 (F0943); index.html:L8154 (F0943); index.html:L8155 (F0943); index.html:L8156 (F0943); index.html:L8157 (F0943); index.html:L8158 (F0943); index.html:L8159 (F0943); index.html:L8160 (F0943); index.html:L8161 (F0943); index.html:L8162 (F0943); index.html:L8163 (F0943); index.html:L8219 (F0968); index.html:L8220 (F0968); index.html:L8290 (F0976); index.html:L8293 (F0977); index.html:L8305 (F0979); index.html:L8324 (F0975); index.html:L8340 (F0975); index.html:L8341 (F0975).

**F0831 · callback setTimeout** — `index.html:L6839–6839` · ArrowFunction · parent F0830.  
Ulaz: `—`.  
Trag tela: `{target.hidden=true;}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0832 · settingsWrite** — `index.html:L6841–6841` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{try{localStorage.setItem('snail-city-rebuild.preferences',JSON.stringify({quality:view.quality,music:view.music,theme:view.theme,lang:view.`.  
Poziva: `localStorage.setItem` L6841 → —; `JSON.stringify` L6841 → —.  
Pozivaju: index.html:L7931 (F0943); index.html:L7935 (F0943); index.html:L8003 (F0943); index.html:L8203 (F0966).

**F0833 · anonimna** — `index.html:L6845–6850` · ArrowFunction · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ let a=null; try{a=JSON.parse(localStorage.getItem(AN_KEY)??'null');}catch{} if(!a||typeof a!=='object')a={}; return {sess:a.sess??0,secs:a`.  
Poziva: `JSON.parse` L6847 → —; `localStorage.getItem` L6847 → —; `Array.isArray` L6849 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0834 · analyticsSave** — `index.html:L6853–6857` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!analyticsDirty)return; analyticsDirty=false; try{localStorage.setItem(AN_KEY,JSON.stringify(analytics));}catch{} }`.  
Poziva: `localStorage.setItem` L6856 → —; `JSON.stringify` L6856 → —.  
Pozivaju: index.html:L8044 (F0943); index.html:L8246 (F0971); index.html:L8256 (F0973); index.html:L8338 (F0975).

**F0835 · analyticsLog** — `index.html:L6858–6868` · FunctionDeclaration · parent F0818.  
Ulaz: `type, before, after`.  
Trag tela: `{ const row=analytics.acts[type]??={n:0}; row.n++; for(const key of CUR_KEYS){ const d=(after[key]??0)-(before[key]??0); if(d>0)row[key+'+']`.  
Poziva: `analytics.lv.push` L6865 → —; `(analytics.secs/3600).toFixed` L6865 → —; `analytics.lv.splice` L6866 → —.  
Pozivaju: index.html:L7176 (F0876).

**F0836 · measureReport** — `index.html:L6869–6884` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ const report=metrics.report({...renderer.estimate(),nodes:document.getElementsByTagName?.('*').length??null, jsHeapMB:performance.memory?+`.  
Poziva: `metrics.report` L6870 → —; `renderer.estimate` L6870 → —; `document.getElementsByTagName` L6870 → —; `(performance.memory.usedJSHeapSize/1048576).toFixed` L6871 → —; `sceneManager?.stats` L6872 → —; `modules.renderer.imageHealth` L6873 → ~F0269; `String` L6876 → —; `gl.getParameter` L6876 → —; `String` L6877 → —; `gl.getParameter` L6877 → —; `gl.getParameter` L6877 → —; `gl.isContextLost` L6878 → —; `Boolean` L6882 → —.  
Pozivaju: index.html:L7065 (F0864); index.html:L8051 (F0943).

**F0837 · updateStatus** — `index.html:L6885–6914` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!s)return; if(view.devOpen)renderDev(); set($('level'),s.level); for(const resource of CUR_KEYS)set($(resource),format(s[resource]??0))`.  
Poziva: `renderDev` L6887 → F0922; `set` L6888 → F0826; `$` L6888 → F0819; `set` L6889 → F0826; `$` L6889 → F0819; `format` L6889 → ~F0526; `$` L6890 → F0819; `xpNeeded` L6892 → ~F0079; `$` L6892 → F0819; `$` L6892 → F0819; `Math.min` L6892 → —; `set` L6893 → F0826; `$` L6893 → F0819; `format` L6893 → ~F0526; `format` L6893 → ~F0526; `set` L6894 → F0826; `$` L6894 → F0819; `activityBadge` L6895 → F0839; `Boolean` L6897 → —; `s.eggs.some` L6900 → —; `s.built.includes` L6904 → —; `$` L6908 → F0819; `set` L6911 → F0826; `$` L6911 → F0819; `set` L6911 → F0826; `$` L6911 → F0819; `set` L6911 → F0826; `$` L6911 → F0819; `$` L6912 → F0819.  
Pozivaju: index.html:L7177 (F0876); index.html:L7199 (F0877); index.html:L7754 (F0923); index.html:L7766 (F0924); index.html:L7775 (F0924); index.html:L7791 (F0924); index.html:L7799 (F0924); index.html:L7933 (F0943); index.html:L8303 (F0979); index.html:L8344 (F0975).

**F0838 · callback s.eggs.some** — `index.html:L6900–6900` · ArrowFunction · parent F0837.  
Ulaz: `egg`.  
Trag tela: `egg.kind!==8`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0839 · activityBadge** — `index.html:L6916–6919` · FunctionDeclaration · parent F0818.  
Ulaz: `now=Date.now()`.  
Trag tela: `{ const badge=$('activity'); if(badge?.classList)badge.classList[Boolean(s)&&!race&&view.touchAt+ACTIVE_MS>now?'add':'remove']('on'); }`.  
Poziva: `Date.now` L6916 → —; `$` L6917 → F0819; `badge.classList[Boolean(s)&&!race&&view.touchAt+ACTIVE_MS>now?'add':'remove']` L6918 → —; `Boolean` L6918 → —.  
Pozivaju: index.html:L6895 (F0837); index.html:L7099 (F0871); index.html:L8224 (F0969).

**F0840 · traceRow** — `index.html:L6923–6923` · ArrowFunction · parent F0818.  
Ulaz: `run`.  
Trag tela: `run.players.map(p=>Math.min(run.course.goal,p.dist))`.  
Poziva: `run.players.map` L6923 → —.  
Pozivaju: index.html:L6964 (F0847); index.html:L6967 (F0847).

**F0841 · callback run.players.map** — `index.html:L6923–6923` · ArrowFunction · parent F0840.  
Ulaz: `p`.  
Trag tela: `Math.min(run.course.goal,p.dist)`.  
Poziva: `Math.min` L6923 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0842 · playQuickBars** — `index.html:L6924–6951` · FunctionDeclaration · parent F0818.  
Ulaz: `run, trace`.  
Trag tela: `{ const goal=run.course.goal, started=performance.now(), span=3500; const paint=idx=>{ const row=trace[Math.min(idx,trace.length-1)]; row.fo`.  
Poziva: `performance.now` L6925 → —; `paint` L6942 → F0843; `finish` L6942 → F0845; `requestAnimationFrame` L6950 → —.  
Pozivaju: index.html:L6971 (F0847).

**F0843 · paint** — `index.html:L6926–6933` · ArrowFunction · parent F0842.  
Ulaz: `idx`.  
Trag tela: `{ const row=trace[Math.min(idx,trace.length-1)]; row.forEach((d,i)=>{ const bar=$('qr-bar-'+i), pct=$('qr-pct-'+i); if(bar)bar.style.width=(`.  
Poziva: `Math.min` L6927 → —; `row.forEach` L6928 → —.  
Pozivaju: index.html:L6940 (F0845); index.html:L6942 (F0842); index.html:L6946 (F0846).

**F0844 · callback row.forEach** — `index.html:L6928–6932` · ArrowFunction · parent F0843.  
Ulaz: `d, i`.  
Trag tela: `{ const bar=$('qr-bar-'+i), pct=$('qr-pct-'+i); if(bar)bar.style.width=(d/goal*100).toFixed(1)+'%'; if(pct)pct.textContent=Math.floor(d/goal`.  
Poziva: `$` L6929 → F0819; `$` L6929 → F0819; `(d/goal*100).toFixed` L6930 → —; `Math.floor` L6931 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0845 · finish** — `index.html:L6935–6941` · ArrowFunction · parent F0842.  
Ulaz: `—`.  
Trag tela: `{ const list=$('qr-bars'), final=$('qr-final'), status=$('qr-status'); if(!list||!final)return; list.innerHTML=final.innerHTML; if(status)st`.  
Poziva: `$` L6936 → F0819; `$` L6936 → F0819; `$` L6936 → F0819; `paint` L6940 → F0843.  
Pozivaju: index.html:L6942 (F0842); index.html:L6948 (F0846).

**F0846 · tick** — `index.html:L6943–6949` · ArrowFunction · parent F0842.  
Ulaz: `now`.  
Trag tela: `{ if(!$('qr-bars'))return; const t=Math.min(1,(now-started)/span); paint(Math.round(t*(trace.length-1))); if(t<1)requestAnimationFrame(tick)`.  
Poziva: `$` L6944 → F0819; `Math.min` L6945 → —; `paint` L6946 → F0843; `Math.round` L6946 → —; `requestAnimationFrame` L6947 → —; `finish` L6948 → F0845.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0847 · quickRace** — `index.html:L6952–6976` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(race||savePending||view.loading||view.quickBusy||!s.built.includes('races'))return; const snailId=selected('race-snail')||view.racer, s`.  
Poziva: `s.built.includes` L6953 → —; `selected` L6954 → F0827; `s.snails.find` L6954 → —; `available` L6955 → ~F0095; `toast` L6955 → F0830; `globalThis.crypto?.getRandomValues` L6958 → —; `Uint32Array` L6958 → —; `Math.floor` L6958 → —; `Math.random` L6958 → —; `createRace` L6959 → ~F0240; `uuid` L6959 → ~F0110; `boostCommand` L6962 → ~F0244; `advanceRace` L6963 → ~F0257; `trace.push` L6964 → —; `traceRow` L6964 → F0840; `toast` L6966 → F0830; `trace.push` L6967 → —; `traceRow` L6967 → F0840; `commit` L6968 → F0876; `showSheet` L6970 → F0857; `quickResultPanel` L6970 → ~F0768; `playQuickBars` L6971 → F0842; `setTimeout` L6974 → —.  
Pozivaju: index.html:L7918 (F0943); index.html:L7920 (F0943).

**F0848 · callback s.snails.find** — `index.html:L6954–6954` · ArrowFunction · parent F0847.  
Ulaz: `n`.  
Trag tela: `n.id===snailId`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0849 · callback setTimeout** — `index.html:L6974–6974` · ArrowFunction · parent F0847.  
Ulaz: `—`.  
Trag tela: `celebrate(level)`.  
Poziva: `celebrate` L6974 → F0914.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0850 · arenaLoop** — `index.html:L6978–6991` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ clearTimeout(arenaTimer);arenaTimer=0; if(!view.arenaAuto||!s?.arena||s.arena.done||view.viewKey!=='arena')return; arenaTimer=setTimeout(a`.  
Poziva: `clearTimeout` L6979 → —; `setTimeout` L6981 → —.  
Pozivaju: index.html:L6989 (F0851); index.html:L7100 (F0871); index.html:L7927 (F0943); index.html:L7928 (F0943).

**F0851 · callback setTimeout** — `index.html:L6981–6990` · ArrowFunction · parent F0850.  
Ulaz: `—`.  
Trag tela: `{ arenaTimer=0; if(!view.arenaAuto||!s?.arena||s.arena.done||view.viewKey!=='arena')return; if(!savePending){ const r=await commit('arena-tu`.  
Poziva: `commit` L6985 → F0876; `updatePanel` L6987 → F0870; `arenaLoop` L6989 → F0850.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0852 · meteorFall** — `index.html:L6995–7004` · FunctionDeclaration · parent F0818.  
Ulaz: `rain`.  
Trag tela: `{ const fx=$('meteor-fx');if(!fx?.style)return; const right=Math.random()<.5; fx.classList[right?'add':'remove']('fromright'); fx.style.left`.  
Poziva: `$` L6996 → F0819; `Math.random` L6997 → —; `fx.classList[right?'add':'remove']` L6998 → —; `Math.random` L6999 → —; `Math.random` L6999 → —; `Math.random` L7000 → —; `clearTimeout` L7003 → —; `setTimeout` L7003 → —.  
Pozivaju: index.html:L7146 (F0871).

**F0853 · callback setTimeout** — `index.html:L7003–7003` · ArrowFunction · parent F0852.  
Ulaz: `—`.  
Trag tela: `{fx.hidden=true;}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0854 · applyTheme** — `index.html:L7005–7005` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{document.body.classList[view.theme==='warm'?'add':'remove']('warm');}`.  
Poziva: `document.body.classList[view.theme==='warm'?'add':'remove']` L7005 → —.  
Pozivaju: index.html:L7935 (F0943); index.html:L8344 (F0975).

**F0855 · markMap** — `index.html:L7007–7014` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(s){ const now=nowBound(); paintedWheatStage=WHEAT_FIELDS.map((_,i)=>wheatStage(s,now,i)).join(','); objects=mapObjects(s,now); } dirty=`.  
Poziva: `nowBound` L7009 → F0828; `WHEAT_FIELDS.map((_,i)=>wheatStage(s,now,i)).join` L7010 → —; `WHEAT_FIELDS.map` L7010 → —; `mapObjects` L7011 → ~F0339; `schedule` L7013 → F0893.  
Pozivaju: index.html:L7098 (F0871); index.html:L7177 (F0876); index.html:L7199 (F0877); index.html:L7754 (F0923); index.html:L7766 (F0924); index.html:L7775 (F0924); index.html:L7791 (F0924); index.html:L7799 (F0924); index.html:L7955 (F0943); index.html:L8250 (F0971); index.html:L8299 (F0978); index.html:L8344 (F0975).

**F0856 · callback WHEAT_FIELDS.map** — `index.html:L7010–7010` · ArrowFunction · parent F0855.  
Ulaz: `_, i`.  
Trag tela: `wheatStage(s,now,i)`.  
Poziva: `wheatStage` L7010 → ~F0067.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0857 · showSheet** — `index.html:L7017–7042` · FunctionDeclaration · parent F0818.  
Ulaz: `html, layout='popup'`.  
Trag tela: `{ panel.dataset.layout=layout; sheet.innerHTML=html;modules.i18n.apply(sheet); for(const graph of sheet.querySelectorAll('canvas[data-plot]'`.  
Poziva: `modules.i18n.apply` L7019 → ~F0817; `sheet.querySelectorAll` L7020 → —; `graph.getContext` L7021 → —; `ctx.scale` L7023 → —; `ctx.setLineDash` L7026 → —; `ctx.beginPath` L7027 → —; `ctx.moveTo` L7027 → —; `ctx.lineTo` L7027 → —; `ctx.stroke` L7027 → —; `ctx.setLineDash` L7027 → —; `ctx.beginPath` L7030 → —; `graph.dataset.points.split(' ').forEach` L7031 → —; `graph.dataset.points.split` L7031 → —; `ctx.stroke` L7035 → —; `panel.show` L7038 → —; `document.body.classList.add` L7041 → —.  
Pozivaju: index.html:L6970 (F0847); index.html:L7068 (F0864); index.html:L7204 (F0878); index.html:L7291 (F0885); index.html:L7296 (F0885); index.html:L7326 (F0889); index.html:L7949 (F0943); index.html:L7998 (F0943); index.html:L8004 (F0943); index.html:L8011 (F0943); index.html:L8014 (F0943); index.html:L8074 (F0943); index.html:L8076 (F0943); index.html:L8146 (F0943); index.html:L8298 (F0978).

**F0858 · callback graph.dataset.points.split(' ').forEach** — `index.html:L7031–7034` · ArrowFunction · parent F0857.  
Ulaz: `point, index`.  
Trag tela: `{ const [x,y]=point.split(',').map(Number); if(index===0)ctx.moveTo(x,y);else ctx.lineTo(x,y); }`.  
Poziva: `point.split(',').map` L7032 → —; `point.split` L7032 → —; `ctx.moveTo` L7033 → —; `ctx.lineTo` L7033 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0859 · dismiss** — `index.html:L7043–7048` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ clearTransientFx(); if(panel.open)panel.close(); document.body.classList.remove('screen-open'); view.viewKey=null;pendingImport=null; }`.  
Poziva: `clearTransientFx` L7044 → F0824; `panel.close` L7045 → —; `document.body.classList.remove` L7046 → —.  
Pozivaju: index.html:L7274 (F0883); index.html:L7312 (F0887); index.html:L7331 (F0891); index.html:L7774 (F0924); index.html:L7790 (F0924); index.html:L7866 (F0941); index.html:L7907 (F0943); index.html:L7908 (F0943); index.html:L7919 (F0943); index.html:L8075 (F0943); index.html:L8077 (F0943); index.html:L8149 (F0943).

**F0860 · signatures** — `index.html:L7049–7052` · FunctionDeclaration · parent F0818.  
Ulaz: `time`.  
Trag tela: `{ return [s.eggs.map(e=>[time>=e.readyAt,time>=e.careAt,time>e.careEnd,Boolean(e.halfHeld)].join('')).join(), s.expeditions.map(e=>time>=e.u`.  
Poziva: `[s.eggs.map(e=>[time>=e.readyAt,time>=e.careAt,time>e.careEnd,Boolean(e.halfHeld)].join('')).join(), s.expeditions.map(e=>time>=e.until).joi` L7050 → —; `s.eggs.map(e=>[time>=e.readyAt,time>=e.careAt,time>e.careEnd,Boolean(e.halfHeld)].join('')).join` L7050 → —; `s.eggs.map` L7050 → —; `s.expeditions.map(e=>time>=e.until).join` L7051 → —; `s.expeditions.map` L7051 → —; `WHEAT_FIELDS.map((_,i)=>wheatStage(s,time,i)).join` L7051 → —; `WHEAT_FIELDS.map` L7051 → —; `nextMeteor` L7051 → ~F0053; `Math.floor` L7051 → —.  
Pozivaju: index.html:L7078 (F0864); index.html:L8269 (F0973).

**F0861 · callback s.eggs.map** — `index.html:L7050–7050` · ArrowFunction · parent F0860.  
Ulaz: `e`.  
Trag tela: `[time>=e.readyAt,time>=e.careAt,time>e.careEnd,Boolean(e.halfHeld)].join('')`.  
Poziva: `[time>=e.readyAt,time>=e.careAt,time>e.careEnd,Boolean(e.halfHeld)].join` L7050 → —; `Boolean` L7050 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0862 · callback s.expeditions.map** — `index.html:L7051–7051` · ArrowFunction · parent F0860.  
Ulaz: `e`.  
Trag tela: `time>=e.until`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0863 · callback WHEAT_FIELDS.map** — `index.html:L7051–7051` · ArrowFunction · parent F0860.  
Ulaz: `_, i`.  
Trag tela: `wheatStage(s,time,i)`.  
Poziva: `wheatStage` L7051 → ~F0067.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0864 · openScreen** — `index.html:L7053–7080` · FunctionDeclaration · parent F0818.  
Ulaz: `key, {keepScroll=false}={}`.  
Trag tela: `{ if(race)return; const top=keepScroll?sheet.scrollTop:0; if(key==='market'){view.shopTab='market';key='shop';} if(view.viewKey!==key){ view`.  
Poziva: `clearTransientFx` L7062 → F0824; `nowBound` L7064 → F0828; `measureReport` L7065 → F0836; `objects.some` L7067 → —; `showSheet` L7068 → F0857; `renderPanel` L7068 → ~F0761; `Array.from($('race-snail')?.options??[]).some` L7069 → —; `Array.from` L7069 → —; `$` L7069 → F0819; `$` L7070 → F0819; `$` L7071 → F0819; `$` L7072 → F0819; `$` L7072 → F0819; `Array.from(a.options).some` L7073 → —; `Array.from` L7073 → —; `Array.from(b.options).some` L7074 → —; `Array.from` L7074 → —; `refreshBreeding` L7075 → F0869; `signatures` L7078 → F0860; `tickClocks` L7079 → F0871.  
Pozivaju: index.html:L7092 (F0870); index.html:L7460 (F0897); index.html:L7813 (F0924); index.html:L7904 (F0943); index.html:L7915 (F0943); index.html:L7920 (F0943); index.html:L7963 (F0943); index.html:L8000 (F0943); index.html:L8072 (F0943); index.html:L8117 (F0943); index.html:L8150 (F0943).

**F0865 · callback objects.some** — `index.html:L7067–7067` · ArrowFunction · parent F0864.  
Ulaz: `o`.  
Trag tela: `o.key===objectKey&&o.screen===key&&movable(o,s)`.  
Poziva: `movable` L7067 → ~F0348.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0866 · callback Array.from($('race-snail')?.options??[]).some** — `index.html:L7069–7069` · ArrowFunction · parent F0864.  
Ulaz: `o`.  
Trag tela: `o.value===view.racer`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0867 · callback Array.from(a.options).some** — `index.html:L7073–7073` · ArrowFunction · parent F0864.  
Ulaz: `o`.  
Trag tela: `o.value===view.parents[0]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0868 · callback Array.from(b.options).some** — `index.html:L7074–7074` · ArrowFunction · parent F0864.  
Ulaz: `o`.  
Trag tela: `o.value===view.parents[1]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0869 · refreshBreeding** — `index.html:L7081–7090` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ view.parents=[selected('parent-a'),selected('parent-b')]; const preview=breedingPreview(s,...view.parents); set($('breed-preview'),preview`.  
Poziva: `selected` L7082 → F0827; `selected` L7082 → F0827; `breedingPreview` L7083 → ~F0676; `set` L7084 → F0826; `$` L7084 → F0819; `$` L7085 → F0819; `set` L7088 → F0826; `format` L7088 → ~F0526.  
Pozivaju: index.html:L7075 (F0864).

**F0870 · updatePanel** — `index.html:L7091–7093` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(view.viewKey)openScreen(view.viewKey,{keepScroll:true}); }`.  
Poziva: `openScreen` L7092 → F0864.  
Pozivaju: index.html:L6987 (F0851); index.html:L7261 (F0883); index.html:L7284 (F0883); index.html:L7547 (F0907); index.html:L7549 (F0906); index.html:L7644 (F0908); index.html:L7758 (F0923); index.html:L7813 (F0924); index.html:L7909 (F0943); index.html:L7910 (F0943); index.html:L7911 (F0943); index.html:L7925 (F0943); index.html:L7927 (F0943); index.html:L7928 (F0943); index.html:L7933 (F0943); index.html:L7935 (F0943); index.html:L7951 (F0943); index.html:L7957 (F0943); index.html:L7963 (F0943); index.html:L7967 (F0943); index.html:L7969 (F0943); index.html:L7976 (F0943); index.html:L7978 (F0943); index.html:L7981 (F0943); index.html:L8000 (F0943); index.html:L8001 (F0943); index.html:L8002 (F0943); index.html:L8003 (F0943); index.html:L8036 (F0943); index.html:L8044 (F0943); index.html:L8079 (F0943); index.html:L8082 (F0943); index.html:L8151 (F0943); index.html:L8180 (F0965); index.html:L8191 (F0964); index.html:L8211 (F0967); index.html:L8267 (F0973); index.html:L8269 (F0973).

**F0871 · tickClocks** — `index.html:L7094–7166` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!s)return; const now=nowBound(); if(!race)modules.scenes.scUpdateReservoirFx(s,now); if(!race&&paintedWheatStage!==WHEAT_FIELDS.map((_,`.  
Poziva: `nowBound` L7096 → F0828; `modules.scenes.scUpdateReservoirFx` L7097 → ~F0394; `WHEAT_FIELDS.map((_,i)=>wheatStage(s,now,i)).join` L7098 → —; `WHEAT_FIELDS.map` L7098 → —; `markMap` L7098 → F0855; `activityBadge` L7099 → F0839; `arenaLoop` L7100 → F0850; `updateClockNodes` L7101 → ~F0763; `$` L7102 → F0819; `$` L7102 → F0819; `reserveAt` L7103 → ~F0142; `set` L7105 → F0826; `panel.querySelector` L7105 → —; `format` L7105 → ~F0526; `Math.round` L7107 → —; `Math.max` L7107 → —; `panel.querySelector` L7108 → —; `Math.min` L7109 → —; `set` L7110 → F0826; `panel.querySelector` L7110 → —; `s.eggs.find` L7113 → —; `s.expeditions.find` L7114 → —; `timer` L7115 → ~F0529; `reservoirCapacity` L7117 → ~F0081; `format` L7117 → ~F0526; `$` L7121 → F0819; `set` L7122 → F0826; `$` L7122 → F0819; `set` L7122 → F0826; `$` L7122 → F0819; `set` L7123 → F0826; `set` L7126 → F0826; `$` L7126 → F0819; `testing` L7126 → F0825; `islandWeather` L7127 → ~F0533; `$` L7128 → F0819; `$` L7128 → F0819; `schedule` L7129 → F0893; `set` L7130 → F0826; `set` L7135 → F0826; `timer` L7135 → ~F0529; `set` L7137 → F0826; `$` L7137 → F0819; `weatherFor` L7137 → ~F0134; `$` L7138 → F0819; `set` L7141 → F0826; `$` L7141 → F0819; `$` L7143 → F0819; `nextMeteor` L7145 → ~F0053; `meteorFall` L7146 → F0852; `set` L7148 → F0826; `$` L7148 → F0819; `$` L7149 → F0819; `$` L7151 → F0819; `s.eggs.find` L7153 → —; `String` L7154 → —; `ready.querySelector` L7157 → —; `imagePath` L7158 → ~F0277; `set` L7163 → F0826; `$` L7163 → F0819.  
Pozivaju: index.html:L7079 (F0864); index.html:L7758 (F0923); index.html:L8146 (F0943); index.html:L8152 (F0943); index.html:L8162 (F0943); index.html:L8270 (F0973).

**F0872 · callback WHEAT_FIELDS.map** — `index.html:L7098–7098` · ArrowFunction · parent F0871.  
Ulaz: `_, i`.  
Trag tela: `wheatStage(s,now,i)`.  
Poziva: `wheatStage` L7098 → ~F0067.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0873 · callback s.eggs.find** — `index.html:L7113–7113` · ArrowFunction · parent F0871.  
Ulaz: `e`.  
Trag tela: `e.readyAt>now&&canCare(e,now)&&now>=e.careAt`.  
Poziva: `canCare` L7113 → ~F0049.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0874 · callback s.expeditions.find** — `index.html:L7114–7114` · ArrowFunction · parent F0871.  
Ulaz: `e`.  
Trag tela: `e.until<=now`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0875 · callback s.eggs.find** — `index.html:L7153–7153` · ArrowFunction · parent F0871.  
Ulaz: `e`.  
Trag tela: `e.readyAt<=now`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0876 · commit** — `index.html:L7167–7189` · FunctionDeclaration · parent F0818.  
Ulaz: `type, fields={}`.  
Trag tela: `{ if(!s||savePending)return {ok:false}; savePending=true; try{ const {state,value}=applyCommand(s,{id:uuid(),type,...fields,...(view.touchAt`.  
Poziva: `applyCommand` L7171 → ~F0185; `uuid` L7171 → ~F0110; `Date.now` L7171 → —; `testing` L7173 → F0825; `repo.commit` L7173 → —; `testing` L7176 → F0825; `analyticsLog` L7176 → F0835; `updateStatus` L7177 → F0837; `markMap` L7177 → F0855; `$(key)?.animate` L7180 → —; `$` L7180 → F0819; `celebrate` L7183 → F0914; `toast` L7186 → F0830.  
Pozivaju: index.html:L6968 (F0847); index.html:L6985 (F0851); index.html:L7292 (F0885); index.html:L7890 (F0943); index.html:L8115 (F0943); index.html:L8186 (F0964); index.html:L8266 (F0973).

**F0877 · replaceSave** — `index.html:L7190–7202` · FunctionDeclaration · parent F0818.  
Ulaz: `next, erase=false`.  
Trag tela: `{ if(testing()){toast('Uvoz, reset i brisanje nisu dostupni u testnoj kopiji.');return false;} if(savePending)return false; savePending=true`.  
Poziva: `testing` L7191 → F0825; `toast` L7191 → F0830; `Math.max` L7195 → —; `validateSave` L7196 → ~F0425; `repo.commit` L7197 → —; `updateStatus` L7199 → F0837; `markMap` L7199 → F0855; `toast` L7200 → F0830.  
Pozivaju: index.html:L8072 (F0943); index.html:L8075 (F0943); index.html:L8077 (F0943).

**F0878 · showImport** — `index.html:L7203–7206` · FunctionDeclaration · parent F0818.  
Ulaz: `text`.  
Trag tela: `{ try{pendingImport=parseSave(text);view.viewKey=null;showSheet(importPanel(pendingImport));} catch(e){toast(e.message);} }`.  
Poziva: `parseSave` L7204 → ~F0482; `showSheet` L7204 → F0857; `importPanel` L7204 → ~F0777; `toast` L7205 → F0830.  
Pozivaju: index.html:L7580 (F0908); index.html:L7634 (F0908); index.html:L8069 (F0943); index.html:L8220 (F0968).

**F0879 · selectRatio** — `index.html:L7207–7207` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{return Math.min(devicePixelRatio||1,view.quality==='high'?1.5:1);}`.  
Poziva: `Math.min` L7207 → —.  
Pozivaju: index.html:L7212 (F0880).

**F0880 · resize** — `index.html:L7208–7218` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ const {width,height}=stage.getBoundingClientRect(); if(!(width>0&&height>0))return; const before=renderer.width+'x'+renderer.height+'|'+re`.  
Poziva: `stage.getBoundingClientRect` L7209 → —; `renderer.resize` L7212 → —; `selectRatio` L7212 → F0879; `metrics.end` L7214 → —; `startMetricSegment` L7215 → F0881; `schedule` L7217 → F0893.  
Pozivaju: index.html:L8003 (F0943); index.html:L8344 (F0975).

**F0881 · startMetricSegment** — `index.html:L7219–7223` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!race)return; metrics.start(race.key,view.quality,renderer.backend,[renderer.canvas.width,renderer.canvas.height],race.mode,race.camera`.  
Poziva: `metrics.start` L7221 → —.  
Pozivaju: index.html:L7215 (F0880); index.html:L7281 (F0883); index.html:L7336 (F0892); index.html:L8298 (F0978).

**F0882 · updateRaceHud** — `index.html:L7224–7253` · FunctionDeclaration · parent F0818.  
Ulaz: `now, force=false`.  
Trag tela: `{ if(!race||!force&&now-lastHud<95)return; lastHud=now; const place=rankOf(race), goal=race.course.goal; const distance=race.finish?goal:rac`.  
Poziva: `rankOf` L7227 → ~F0258; `set` L7229 → F0826; `$` L7229 → F0819; `set` L7229 → F0826; `$` L7229 → F0819; `Math.floor` L7229 → —; `set` L7230 → F0826; `$` L7230 → F0819; `Math.floor` L7230 → —; `set` L7231 → F0826; `$` L7231 → F0819; `race.finish.seconds.toFixed` L7231 → —; `race.elapsed.toFixed` L7231 → —; `$` L7232 → F0819; `$` L7232 → F0819; `$` L7234 → F0819; `Math.min` L7235 → —; `$` L7237 → F0819; `$` L7237 → F0819; `Boolean` L7237 → —; `set` L7238 → F0826; `$` L7238 → F0819; `Math.floor` L7238 → —; `$` L7239 → F0819; `Boolean` L7241 → —; `set` L7243 → F0826; `bump.classList[race.notice.cracked?'add':'remove']` L7243 → —; `set` L7245 → F0826; `$` L7245 → F0819; `Math.ceil` L7245 → —; `$` L7246 → F0819; `$` L7247 → F0819; `set` L7251 → F0826.  
Pozivaju: index.html:L7280 (F0883); index.html:L7299 (F0886); index.html:L7325 (F0889); index.html:L7370 (F0894).

**F0883 · startRace** — `index.html:L7254–7286` · FunctionDeclaration · parent F0818.  
Ulaz: `snailId=selected('race-snail')`.  
Trag tela: `{ if(race||savePending||view.loading||!s.built.includes('races')||renderer.lost)return; const snail=s.snails.find(n=>n.id===snailId); if(!av`.  
Poziva: `selected` L7254 → F0827; `s.built.includes` L7255 → —; `s.snails.find` L7256 → —; `available` L7257 → ~F0095; `toast` L7257 → F0830; `baseTime` L7258 → F0829; `updatePanel` L7261 → F0870; `baseTime` L7264 → F0829; `renderer.preload` L7265 → —; `trackAtlas` L7265 → ~F0072; `metrics.markLoading` L7267 → —; `baseTime` L7267 → F0829; `globalThis.crypto?.getRandomValues` L7268 → —; `Uint32Array` L7268 → —; `Math.floor` L7268 → —; `Math.random` L7268 → —; `metrics.mapReturn` L7269 → —; `Math.max` L7269 → —; `createRace` L7272 → ~F0240; `uuid` L7272 → ~F0110; `sceneManager.activate` L7273 → —; `trackAtlas` L7273 → ~F0072; `dismiss` L7274 → F0859; `document.body.classList.add` L7277 → —; `set` L7278 → F0826; `$` L7278 → F0819; `set` L7278 → F0826; `$` L7278 → F0819; `set` L7278 → F0826; `$` L7278 → F0819; `set` L7278 → F0826; `$` L7278 → F0819; `updateRaceHud` L7280 → F0882; `baseTime` L7280 → F0829; `startMetricSegment` L7281 → F0881; `schedule` L7281 → F0893; `toast` L7282 → F0830; `updatePanel` L7284 → F0870.  
Pozivaju: index.html:L7917 (F0943); index.html:L7939 (F0943).

**F0884 · callback s.snails.find** — `index.html:L7256–7256` · ArrowFunction · parent F0883.  
Ulaz: `n`.  
Trag tela: `n.id===snailId`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0885 · saveReward** — `index.html:L7287–7297` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!race?.finish||rewardPending||reward)return; const currentRace=race; rewardPending=true; showSheet(resultPanel(null,currentRace,true));`.  
Poziva: `showSheet` L7291 → F0857; `resultPanel` L7291 → ~F0766; `commit` L7292 → F0876; `showSheet` L7296 → F0857; `resultPanel` L7296 → ~F0766.  
Pozivaju: index.html:L7301 (F0886); index.html:L7948 (F0943).

**F0886 · finishRace** — `index.html:L7298–7302` · FunctionDeclaration · parent F0818.  
Ulaz: `now`.  
Trag tela: `{ updateRaceHud(now,true); metrics.end('finished'); saveReward(); }`.  
Poziva: `updateRaceHud` L7299 → F0882; `metrics.end` L7300 → —; `saveReward` L7301 → F0885.  
Pozivaju: index.html:L7371 (F0894).

**F0887 · returnMap** — `index.html:L7303–7321` · FunctionDeclaration · parent F0818.  
Ulaz: `inputAt=null`.  
Trag tela: `{ if(!race||rewardPending)return; const at=baseTime(); const old=race, before=renderer.canvas; if(!old.finish)metrics.end('abandoned'); // R`.  
Poziva: `baseTime` L7305 → F0829; `metrics.end` L7307 → —; `sceneManager.activate` L7310 → —; `dismiss` L7312 → F0859; `document.body.classList.remove` L7312 → —; `(at-inputAt).toFixed` L7314 → —; `schedule` L7318 → F0893; `$('nav-map').focus` L7319 → —; `$` L7319 → F0819; `setTimeout` L7320 → —.  
Pozivaju: index.html:L7939 (F0943); index.html:L7947 (F0943).

**F0888 · callback setTimeout** — `index.html:L7320–7320` · ArrowFunction · parent F0887.  
Ulaz: `—`.  
Trag tela: `celebrate(level)`.  
Poziva: `celebrate` L7320 → F0914.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0889 · pauseRace** — `index.html:L7322–7327` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!race||race.finish)return; race.paused=true;race.pendingTime=0;previousTime=0;lastPaint=0; updateRaceHud(baseTime(),true); showSheet(pa`.  
Poziva: `updateRaceHud` L7325 → F0882; `baseTime` L7325 → F0829; `showSheet` L7326 → F0857; `pausePanel` L7326 → ~F0775; `pauseOptions` L7326 → F0890.  
Pozivaju: index.html:L7945 (F0943); index.html:L8232 (F0970); index.html:L8244 (F0971); index.html:L8283 (F0976).

**F0890 · pauseOptions** — `index.html:L7328–7328` · ArrowFunction · parent F0818.  
Ulaz: `—`.  
Trag tela: `({quality:view.quality,speed:view.raceSpeed,camera:race?cameraLabels[race.cameraMode]:''})`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L7326 (F0889); index.html:L8004 (F0943); index.html:L8011 (F0943); index.html:L8014 (F0943); index.html:L8298 (F0978).

**F0891 · resumeRace** — `index.html:L7329–7332` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!race||race.finish||renderer.lost)return; dismiss();race.paused=false;previousTime=0;dueDraw=0;lastPaint=0;schedule(); }`.  
Poziva: `dismiss` L7331 → F0859; `schedule` L7331 → F0893.  
Pozivaju: index.html:L7946 (F0943); index.html:L8175 (F0963); index.html:L8232 (F0970).

**F0892 · toggleCamera** — `index.html:L7333–7339` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!race||race.finish)return; race.cameraMode=cycleCamera(race.cameraMode); metrics.end('camera');startMetricSegment(); set($('race-camera`.  
Poziva: `cycleCamera` L7335 → ~F0238; `metrics.end` L7336 → —; `startMetricSegment` L7336 → F0881; `set` L7337 → F0826; `$` L7337 → F0819; `schedule` L7338 → F0893.  
Pozivaju: index.html:L7944 (F0943); index.html:L8235 (F0970).

**F0893 · schedule** — `index.html:L7340–7340` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{if(!raf&&!document.hidden)raf=requestAnimationFrame(loop);}`.  
Poziva: `requestAnimationFrame` L7340 → —.  
Pozivaju: index.html:L7013 (F0855); index.html:L7129 (F0871); index.html:L7217 (F0880); index.html:L7281 (F0883); index.html:L7318 (F0887); index.html:L7331 (F0891); index.html:L7338 (F0892); index.html:L7372 (F0894); index.html:L7400 (F0894); index.html:L7404 (F0895); index.html:L7420 (F0896); index.html:L7519 (F0901); index.html:L7836 (F0939); index.html:L7853 (F0940); index.html:L8298 (F0978).

**F0894 · loop** — `index.html:L7341–7409` · FunctionDeclaration · parent F0818.  
Ulaz: `now`.  
Trag tela: `{ raf=0; if(!s||!renderer||renderer.lost||document.hidden)return; if(race&&!race.paused&&!race.finish){ const gap=previousTime?now-previousT`.  
Poziva: `advanceRace` L7348 → ~F0257; `Math.min` L7348 → —; `Math.max` L7348 → —; `baseTime` L7352 → F0829; `paintRace` L7353 → ~F0404; `baseTime` L7354 → F0829; `metrics.markLoading` L7356 → —; `baseTime` L7356 → F0829; `metrics.frame` L7360 → —; `set` L7365 → F0826; `$` L7365 → F0819; `Math.round` L7365 → —; `updateRaceHud` L7370 → F0882; `finishRace` L7371 → F0886; `schedule` L7372 → F0893; `Boolean` L7374 → —; `document.body.classList.contains` L7374 → —; `document.body.classList.contains` L7375 → —; `document.body.classList.contains` L7375 → —; `(baseTime()-returnTrace.at).toFixed` L7383 → —; `baseTime` L7383 → F0829; `returnTrace.gaps.push` L7384 → —; `(now-returnPrevious).toFixed` L7384 → —; `baseTime` L7389 → F0829; `paintMap` L7390 → ~F0395; `nowBound` L7390 → F0828; `sceneManager.paintedMap` L7391 → —; `metrics.islandDraw` L7391 → —; `baseTime` L7391 → F0829; `metrics.markLoading` L7392 → —; `baseTime` L7392 → F0829; `globalThis.SC_STARTUP_TRACE?.mark` L7392 → —; `(baseTime()-begin).toFixed` L7394 → —; `baseTime` L7394 → F0829; `metrics.mapReturn` L7397 → —; `Math.max` L7397 → —; `schedule` L7400 → F0893; `setTimeout` L7404 → —; `paintRace` L7407 → ~F0404.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0895 · callback setTimeout** — `index.html:L7404–7404` · ArrowFunction · parent F0894.  
Ulaz: `—`.  
Trag tela: `{waterWakeTimer=0;schedule();}`.  
Poziva: `schedule` L7404 → F0893.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0896 · zoomAt** — `index.html:L7410–7421` · FunctionDeclaration · parent F0818.  
Ulaz: `value, point`.  
Trag tela: `{ const before=mapView(renderer.width,renderer.height,mapCamera); const x=(point.x-before.x)/before.sizeX,y=(point.y-before.y)/before.sizeY;`.  
Poziva: `mapView` L7411 → ~F0331; `Math.max` L7413 → —; `Math.min` L7413 → —; `mapView` L7414 → ~F0331; `Math.max` L7418 → —; `Math.min` L7418 → —; `Math.max` L7419 → —; `Math.min` L7419 → —; `schedule` L7420 → F0893.  
Pozivaju: index.html:L7509 (F0901); index.html:L7536 (F0905); index.html:L7954 (F0943).

**F0897 · mapTap** — `index.html:L7422–7463` · FunctionDeclaration · parent F0818.  
Ulaz: `point`.  
Trag tela: `{ const current=mapView(renderer.width,renderer.height,mapCamera); if(islandEditor){ // The touch/mouse point targets the *centre of the phy`.  
Poziva: `mapView` L7423 → ~F0331; `modules.scenes.supportFootprint` L7429 → ~F0347; `Math.round` L7430 → —; `Math.round` L7431 → —; `refreshEditor` L7434 → F0940; `modules.scenes.scBuildVisualInstances` L7442 → ~F0383; `modules.scenes.supportFootprint` L7448 → ~F0347; `modules.scenes.scMapArtRect` L7452 → ~F0386; `openScreen` L7460 → F0864.  
Pozivaju: index.html:L7531 (F0903).

**F0898 · attachInput** — `index.html:L7464–7538` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ const c=renderer.canvas; let bounds=null,canvasWidth=0,canvasHeight=0; const coords=(x,y,refresh=false)=>{ if(refresh||!bounds||canvasWidt`.  
Poziva: `c.addEventListener` L7475 → —; `c.addEventListener` L7487 → —; `c.addEventListener` L7523 → —; `c.addEventListener` L7533 → —; `c.addEventListener` L7534 → —.  
Pozivaju: index.html:L8303 (F0979); index.html:L8344 (F0975).

**F0899 · coords** — `index.html:L7467–7474` · ArrowFunction · parent F0898.  
Ulaz: `x, y, refresh=false`.  
Trag tela: `{ if(refresh||!bounds||canvasWidth!==renderer.width||canvasHeight!==renderer.height){ bounds=c.getBoundingClientRect(); canvasWidth=renderer`.  
Poziva: `c.getBoundingClientRect` L7469 → —; `Math.max` L7472 → —; `Math.max` L7473 → —.  
Pozivaju: index.html:L7477 (F0900); index.html:L7492 (F0901); index.html:L7505 (F0901); index.html:L7524 (F0903); index.html:L7536 (F0905).

**F0900 · callback c.addEventListener** — `index.html:L7475–7486` · ArrowFunction · parent F0898.  
Ulaz: `e`.  
Trag tela: `{ if(e.button!==0)return; const p=coords(e.clientX,e.clientY,true); c.setPointerCapture(e.pointerId); if(race){raceTouch={id:e.pointerId,x:p`.  
Poziva: `coords` L7477 → F0899; `c.setPointerCapture` L7478 → —; `pointers.set` L7481 → —; `pointers.values` L7483 → —; `Math.hypot` L7484 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0901 · callback c.addEventListener** — `index.html:L7487–7522` · ArrowFunction · parent F0898.  
Ulaz: `e`.  
Trag tela: `{ if(!race&&islandEditor&&e.pointerType==='mouse'&&!pointers.has(e.pointerId)){ // Hover is a ghost preview ONLY before the player clicks th`.  
Poziva: `pointers.has` L7488 → —; `coords` L7492 → F0899; `mapView` L7493 → ~F0331; `modules.scenes.supportFootprint` L7496 → ~F0347; `Math.round` L7497 → —; `Math.round` L7498 → —; `next.some` L7499 → —; `refreshEditor` L7500 → F0940; `pointers.has` L7504 → —; `coords` L7505 → F0899; `pointers.get` L7505 → —; `pointers.set` L7506 → —; `pointers.values` L7508 → —; `Math.hypot` L7508 → —; `zoomAt` L7509 → F0896; `Math.hypot` L7513 → —; `Math.min` L7516 → —; `Math.max` L7517 → —; `Math.min` L7517 → —; `Math.max` L7518 → —; `Math.min` L7518 → —; `schedule` L7519 → F0893.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0902 · callback next.some** — `index.html:L7499–7499` · ArrowFunction · parent F0901.  
Ulaz: `v, i`.  
Trag tela: `v!==islandEditor.target[i]`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0903 · callback c.addEventListener** — `index.html:L7523–7532` · ArrowFunction · parent F0898.  
Ulaz: `e`.  
Trag tela: `{ const p=coords(e.clientX,e.clientY); if(race){ if(raceTouch?.id===e.pointerId&&Math.abs(p.x-raceTouch.x)>27)laneCommand(race,p.x>raceTouch`.  
Poziva: `coords` L7524 → F0899; `Math.abs` L7526 → —; `laneCommand` L7526 → ~F0243; `pointers.has` L7529 → —; `pointers.delete` L7530 → —; `mapTap` L7531 → F0897.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0904 · callback c.addEventListener** — `index.html:L7533–7533` · ArrowFunction · parent F0898.  
Ulaz: `e`.  
Trag tela: `{pointers.delete(e.pointerId);raceTouch=null;}`.  
Poziva: `pointers.delete` L7533 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0905 · callback c.addEventListener** — `index.html:L7534–7537` · ArrowFunction · parent F0898.  
Ulaz: `e`.  
Trag tela: `{ if(race)return; e.preventDefault();zoomAt(mapCamera.zoom*(e.deltaY<0?1.09:.92),coords(e.clientX,e.clientY,true)); }`.  
Poziva: `e.preventDefault` L7536 → —; `zoomAt` L7536 → F0896; `coords` L7536 → F0899.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0906 · soundToggle** — `index.html:L7539–7550` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!audio){ audio=new Audio(imagePath('ambient.mp3')); audio.loop=true;audio.volume=.26*view.music; } if(view.sound){view.sound=false;audi`.  
Poziva: `Audio` L7541 → —; `imagePath` L7541 → ~F0277; `audio.pause` L7544 → —; `audio.play().catch` L7547 → —; `audio.play` L7547 → —; `updatePanel` L7549 → F0870.  
Pozivaju: index.html:L8037 (F0943).

**F0907 · callback audio.play().catch** — `index.html:L7547–7547` · ArrowFunction · parent F0906.  
Ulaz: `—`.  
Trag tela: `{view.sound=false;updatePanel();toast('Zvuk trenutno nije dostupan.');}`.  
Poziva: `updatePanel` L7547 → F0870; `toast` L7547 → F0830.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0908 · cloudAction** — `index.html:L7551–7646` · FunctionDeclaration · parent F0818.  
Ulaz: `action, value=''`.  
Trag tela: `{ const cloud=privateProfile; if(cloud.busy)return; cloud.busy=true;cloud.message=''; try{ switch(action){ case 'cloud-legacy-import':{ if(t`.  
Poziva: `testing` L7558 → F0825; `Error` L7558 → —; `Error` L7560 → —; `URL` L7561 → —; `origin.hostname.endsWith` L7562 → —; `Error` L7563 → —; `cloudBackup.library` L7564 → —; `createClient` L7565 → —; `legacy.auth.getSession` L7566 → —; `Error` L7568 → —; `legacy.auth.getUser` L7569 → —; `Error` L7572 → —; `legacy.from('game_saves').select('data,rev,updated_at').eq('user_id',user.id).maybeSingle` L7573 → —; `legacy.from('game_saves').select('data,rev,updated_at').eq` L7573 → —; `legacy.from('game_saves').select` L7573 → —; `legacy.from` L7573 → —; `Error` L7575 → —; `JSON.stringify` L7576 → —; `parseSave` L7577 → ~F0482; `Error` L7578 → —; `showImport` L7580 → F0878; `cloudBackup.originOk` L7583 → —; `cloudBackup.status` L7584 → —; `cloudBackup.originOk` L7591 → —; `cloudBackup.status` L7592 → —; `Error` L7600 → —; `Error` L7601 → —; `validateSave` L7603 → ~F0425; `JSON.stringify` L7604 → —; `Error` L7605 → —; `cloudBackup.upload` L7606 → —; `cloudBackup.signOut` L7611 → —; `Error` L7619 → —; `cloudBackup.deleteCopy` L7620 → —; `Error` L7627 → —; `cloudBackup.download` L7628 → —; `JSON.stringify` L7630 → —; `parseSave` L7631 → ~F0482; `showImport` L7634 → F0878; `cloudBackup.originOk` L7640 → —; `updatePanel` L7644 → F0870.  
Pozivaju: index.html:L7897 (F0943); index.html:L7905 (F0943).

**F0909 · openShare** — `index.html:L7647–7653` · FunctionDeclaration · parent F0818.  
Ulaz: `title, text`.  
Trag tela: `{ const dialog=$('share-panel'); set($('share-title'),title);set($('share-status'),''); $('share-text').value=text; $('share-native').hidden`.  
Poziva: `$` L7648 → F0819; `set` L7649 → F0826; `$` L7649 → F0819; `set` L7649 → F0826; `$` L7649 → F0819; `$` L7650 → F0819; `$` L7651 → F0819; `dialog.showModal` L7652 → —.  
Pozivaju: index.html:L7987 (F0943); index.html:L7993 (F0943); index.html:L8041 (F0943).

**F0910 · submitShare** — `index.html:L7654–7665` · FunctionDeclaration · parent F0818.  
Ulaz: `native`.  
Trag tela: `{ const dialog=$('share-panel'),field=$('share-text'),text=field.value; if(!dialog.open)return; try{ if(native){await navigator.share({title`.  
Poziva: `$` L7655 → F0819; `$` L7655 → F0819; `navigator.share` L7658 → —; `dialog.close` L7658 → —; `navigator.clipboard.writeText` L7659 → —; `set` L7659 → F0826; `$` L7659 → F0819; `field.focus` L7662 → —; `field.select` L7662 → —; `set` L7663 → F0826; `$` L7663 → F0819.  
Pozivaju: index.html:L7995 (F0943); index.html:L7996 (F0943).

**F0911 · flyReward** — `index.html:L7668–7692` · FunctionDeclaration · parent F0818.  
Ulaz: `key`.  
Trag tela: `{ if(race||reduceMotion||typeof document.createElement!=='function')return; const chip=$(key)?.parentElement; const target=chip?.getBounding`.  
Poziva: `$` L7670 → F0819; `chip?.getBoundingClientRect` L7671 → —; `document.createElement` L7676 → —; `imagePath` L7676 → ~F0277; `document.body.append` L7677 → —; `watchTransient` L7679 → F0822; `img.animate` L7679 → —.  
Pozivaju: index.html:L8121 (F0943).

**F0912 · animation.oncancel** — `index.html:L7683–7683` · ArrowFunction · parent F0911.  
Ulaz: `—`.  
Trag tela: `img.remove()`.  
Poziva: `img.remove` L7683 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0913 · animation.onfinish** — `index.html:L7684–7690` · ArrowFunction · parent F0911.  
Ulaz: `—`.  
Trag tela: `{ img.remove(); // v147 chipPulse: one acknowledgement, not six independent pulses. if(i===5&&chip?.isConnected&&!reduceMotion) watchTransie`.  
Poziva: `img.remove` L7685 → —; `watchTransient` L7688 → F0822; `chip.animate` L7688 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0914 · celebrate** — `index.html:L7695–7708` · FunctionDeclaration · parent F0818.  
Ulaz: `level`.  
Trag tela: `{ if(race||view.quickBusy){pendingCelebration=level;return;} if(typeof document.createElement!=='function'||!document.body?.append||!stage?.`.  
Poziva: `document.createElement` L7698 → —; `box.setAttribute` L7698 → —; `Math.round` L7702 → —; `Math.cos` L7702 → —; `Math.round` L7702 → —; `Math.sin` L7702 → —; `stage.append` L7706 → —; `setTimeout` L7707 → —.  
Pozivaju: index.html:L6974 (F0849); index.html:L7183 (F0876); index.html:L7320 (F0888); index.html:L7755 (F0923).

**F0915 · callback setTimeout** — `index.html:L7707–7707` · ArrowFunction · parent F0914.  
Ulaz: `—`.  
Trag tela: `box.remove()`.  
Poziva: `box.remove` L7707 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0916 · devMarkup** — `index.html:L7710–7731` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ const b=(action,label,value='',on=false,disabled=false,title='')=>'<button type="button" class="btn sm'+(on?' on':'')+'" data-action="'+ac`.  
Poziva: `testing` L7713 → F0825; `b` L7715 → F0917; `b` L7716 → F0917; `b` L7716 → F0917; `b` L7717 → F0917; `[1,45,60,1000,10000].map(v=>b('dev-speed','x'+v,v,view.eggSpeed===v)).join` L7718 → —; `[1,45,60,1000,10000].map` L7718 → —; `[3,7,11,22,33,44,66,99].map(l=>b('dev-level',l,l,false,l<=s.level)).join` L7719 → —; `[3,7,11,22,33,44,66,99].map` L7719 → —; `b` L7720 → F0917; `b` L7720 → F0917; `b` L7721 → F0917; `Object.keys(modules.catalog.catalog.weather).filter(k=>k!=='calm'&&k!=='starfall') .map(k=>b('dev-weather',k,k,false,s.level<11)).join` L7722 → —; `Object.keys(modules.catalog.catalog.weather).filter(k=>k!=='calm'&&k!=='starfall') .map` L7722 → —; `Object.keys(modules.catalog.catalog.weather).filter` L7722 → —; `Object.keys` L7722 → —; `b` L7724 → F0917; `b` L7725 → F0917; `b` L7725 → F0917; `b` L7726 → F0917; `Boolean` L7726 → —; `nowBound` L7726 → F0828; `b` L7727 → F0917; `b` L7728 → F0917; `b` L7729 → F0917; `b` L7729 → F0917.  
Pozivaju: index.html:L7740 (F0922).

**F0917 · b** — `index.html:L7711–7712` · ArrowFunction · parent F0916.  
Ulaz: `action, label, value='', on=false, disabled=false, title=''`.  
Trag tela: `'<button type="button" class="btn sm'+(on?' on':'')+'" data-action="'+action+'" data-value="'+value+'"'+ (title?' title="'+title+'"':'')+(di`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L7715 (F0916); index.html:L7716 (F0916); index.html:L7716 (F0916); index.html:L7717 (F0916); index.html:L7718 (F0918); index.html:L7719 (F0919); index.html:L7720 (F0916); index.html:L7720 (F0916); index.html:L7721 (F0916); index.html:L7723 (F0921); index.html:L7724 (F0916); index.html:L7725 (F0916); index.html:L7725 (F0916); index.html:L7726 (F0916); index.html:L7727 (F0916); index.html:L7728 (F0916); index.html:L7729 (F0916); index.html:L7729 (F0916).

**F0918 · callback [1,45,60,1000,10000].map** — `index.html:L7718–7718` · ArrowFunction · parent F0916.  
Ulaz: `v`.  
Trag tela: `b('dev-speed','x'+v,v,view.eggSpeed===v)`.  
Poziva: `b` L7718 → F0917.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0919 · callback [3,7,11,22,33,44,66,99].map** — `index.html:L7719–7719` · ArrowFunction · parent F0916.  
Ulaz: `l`.  
Trag tela: `b('dev-level',l,l,false,l<=s.level)`.  
Poziva: `b` L7719 → F0917.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0920 · callback Object.keys(modules.catalog.catalog.weather).filter** — `index.html:L7722–7722` · ArrowFunction · parent F0916.  
Ulaz: `k`.  
Trag tela: `k!=='calm'&&k!=='starfall'`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0921 · callback Object.keys(modules.catalog.catalog.weather).filter(k=>k!=='calm'&&k!=='starfall') .map** — `index.html:L7723–7723` · ArrowFunction · parent F0916.  
Ulaz: `k`.  
Trag tela: `b('dev-weather',k,k,false,s.level<11)`.  
Poziva: `b` L7723 → F0917.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0922 · renderDev** — `index.html:L7732–7741` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ const box=$('dev-panel'),toggle=$('dev-toggle'); if(!box||!toggle)return; box.hidden=!view.devOpen; set(toggle,view.devOpen?'−':'+'); togg`.  
Poziva: `$` L7733 → F0819; `$` L7733 → F0819; `set` L7736 → F0826; `toggle.setAttribute` L7737 → —; `String` L7737 → —; `toggle.setAttribute` L7738 → —; `testing` L7738 → F0825; `String` L7739 → —; `testing` L7739 → F0825; `devMarkup` L7740 → F0916.  
Pozivaju: index.html:L6887 (F0837); index.html:L7758 (F0923); index.html:L7766 (F0924); index.html:L7775 (F0924); index.html:L7788 (F0924); index.html:L7791 (F0924); index.html:L7793 (F0924); index.html:L7799 (F0924); index.html:L7813 (F0924); index.html:L8003 (F0943); index.html:L8344 (F0975).

**F0923 · devApply** — `index.html:L7742–7759` · FunctionDeclaration · parent F0818.  
Ulaz: `change`.  
Trag tela: `{ if(!s||race||savePending)return false; savePending=true; try{ const next=structuredClone(s); change(next,nowBound()); // Prepare the grid `.  
Poziva: `structuredClone` L7746 → —; `change` L7747 → —; `nowBound` L7747 → F0828; `modules.scenes.prepareIsland` L7749 → ~F0370; `validateSave` L7751 → ~F0425; `testing` L7752 → F0825; `repo.commit` L7752 → —; `updateStatus` L7754 → F0837; `markMap` L7754 → F0855; `celebrate` L7755 → F0914; `toast` L7757 → F0830; `renderDev` L7758 → F0922; `updatePanel` L7758 → F0870; `tickClocks` L7758 → F0871.  
Pozivaju: index.html:L7804 (F0924); index.html:L7806 (F0924); index.html:L7807 (F0924); index.html:L7808 (F0924); index.html:L7809 (F0924); index.html:L7810 (F0924); index.html:L7817 (F0924); index.html:L7820 (F0924).

**F0924 · devAction** — `index.html:L7760–7822` · FunctionDeclaration · parent F0818.  
Ulaz: `action, value`.  
Trag tela: `{ if(action==='dev-start'){ if(race||savePending||testing())return; regularTestSnapshot=structuredClone(s); s=structuredClone(regularTestSna`.  
Poziva: `testing` L7762 → F0825; `structuredClone` L7763 → —; `structuredClone` L7764 → —; `updateStatus` L7766 → F0837; `markMap` L7766 → F0855; `renderDev` L7766 → F0922; `toast` L7766 → F0830; `testing` L7769 → F0825; `repo?.load` L7772 → —; `validateSave` L7772 → ~F0425; `dismiss` L7774 → F0859; `stage.querySelectorAll('.lvup').forEach` L7774 → —; `stage.querySelectorAll` L7774 → —; `updateStatus` L7775 → F0837; `markMap` L7775 → F0855; `renderDev` L7775 → F0922; `toast` L7775 → F0830; `testing` L7777 → F0825; `toast` L7777 → F0830; `renderDev` L7788 → F0922; `newGame` L7790 → ~F0126; `modules.scenes.prepareIsland` L7790 → ~F0370; `dismiss` L7790 → F0859; `updateStatus` L7791 → F0837; `markMap` L7791 → F0855; `renderDev` L7791 → F0922; `toast` L7791 → F0830; `Number` L7793 → —; `renderDev` L7793 → F0922; `nowBound` L7796 → F0828; `[3600,21600,25200,43200].find` L7797 → —; `Math.ceil` L7798 → —; `updateStatus` L7799 → F0837; `markMap` L7799 → F0855; `renderDev` L7799 → F0922; `String` L7802 → —; `Object.hasOwn` L7803 → —; `devApply` L7804 → F0923; `devApply` L7806 → F0923; `devApply` L7807 → F0923; `devApply` L7808 → F0923; `devApply` L7809 → F0923; `devApply` L7810 → F0923; `renderDev` L7813 → F0922; `updatePanel` L7813 → F0870; `openScreen` L7813 → F0864; `Number` L7815 → —; `devApply` L7817 → F0923; `toast` L7818 → F0830; `devApply` L7820 → F0923.  
Pozivaju: index.html:L7898 (F0943); index.html:L8258 (F0973).

**F0925 · callback stage.querySelectorAll('.lvup').forEach** — `index.html:L7774–7774` · ArrowFunction · parent F0924.  
Ulaz: `el`.  
Trag tela: `el.remove()`.  
Poziva: `el.remove` L7774 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0926 · shift** — `index.html:L7778–7786` · ArrowFunction · parent F0924.  
Ulaz: `next, ms`.  
Trag tela: `{ for(const e of next.eggs){ if(e.readyAt<=next.lastAt)continue; e.readyAt-=ms;e.startedAt-=ms; if(e.careAt!==null)e.careAt-=ms; if(e.careEn`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: index.html:L7820 (F0935).

**F0927 · callback [3600,21600,25200,43200].find** — `index.html:L7797–7797` · ArrowFunction · parent F0924.  
Ulaz: `v`.  
Trag tela: `v>seconds`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0928 · callback devApply** — `index.html:L7804–7804` · ArrowFunction · parent F0924.  
Ulaz: `n, now`.  
Trag tela: `{n.weather={id,until:now+300000};n.weatherAt=now+600000;}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0929 · callback devApply** — `index.html:L7806–7806` · ArrowFunction · parent F0924.  
Ulaz: `n`.  
Trag tela: `{n.level=Math.max(n.level,Number(value));n.xp=0;}`.  
Poziva: `Math.max` L7806 → —; `Number` L7806 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0930 · callback devApply** — `index.html:L7807–7807` · ArrowFunction · parent F0924.  
Ulaz: `n`.  
Trag tela: `{n.level=Math.min(99,n.level+1);n.xp=0;}`.  
Poziva: `Math.min` L7807 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0931 · callback devApply** — `index.html:L7808–7808` · ArrowFunction · parent F0924.  
Ulaz: `n, now`.  
Trag tela: `{n.reserve=Math.floor(reservoirCapacity(n)*Number(value));n.lastAt=now;}`.  
Poziva: `Math.floor` L7808 → —; `reservoirCapacity` L7808 → ~F0081; `Number` L7808 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0932 · callback devApply** — `index.html:L7809–7809` · ArrowFunction · parent F0924.  
Ulaz: `n, now`.  
Trag tela: `{n.rain={until:now+180000,readyAt:now,caught:0};}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0933 · callback devApply** — `index.html:L7810–7812` · ArrowFunction · parent F0924.  
Ulaz: `n, now`.  
Trag tela: `{ n.sliz+=Math.max(1000000,Math.round(rate(n,now)*360000));n.diamonds+=2000;n.dust+=500;n.tokens+=100;n.stones+=5;n.fragments+=50; }`.  
Poziva: `Math.max` L7811 → —; `Math.round` L7811 → —; `rate` L7811 → ~F0139.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0934 · callback devApply** — `index.html:L7817–7817` · ArrowFunction · parent F0924.  
Ulaz: `n, now`.  
Trag tela: `{n.eggs.push({id:uuid(),kind:type.cls,startedAt:now,readyAt:now,careAt:null,careEnd:null,cared:false,parents:null,recipe:id});}`.  
Poziva: `n.eggs.push` L7817 → —; `uuid` L7817 → ~F0110.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0935 · callback devApply** — `index.html:L7820–7820` · ArrowFunction · parent F0924.  
Ulaz: `n`.  
Trag tela: `shift(n,(view.eggSpeed-1)*1000)`.  
Poziva: `shift` L7820 → F0926.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0936 · picks** — `index.html:L7824–7828` · FunctionDeclaration · parent F0818.  
Ulaz: `name`.  
Trag tela: `{ const seen=[]; for(const field of panel.querySelectorAll('[name='+name+']'))if(field.value&&!seen.includes(field.value))seen.push(field.va`.  
Poziva: `panel.querySelectorAll` L7826 → —; `seen.includes` L7826 → —; `seen.push` L7826 → —.  
Pozivaju: index.html:L8105 (F0943); index.html:L8109 (F0943).

**F0937 · keepPicks** — `index.html:L7829–7832` · FunctionDeclaration · parent F0818.  
Ulaz: `name, key`.  
Trag tela: `{ const fields=[...panel.querySelectorAll('[name='+name+']')]; if(fields.length)view[key]=fields.map(field=>field.value||null); }`.  
Poziva: `panel.querySelectorAll` L7830 → —; `fields.map` L7831 → —.  
Pozivaju: index.html:L7969 (F0943); index.html:L8193 (F0964); index.html:L8194 (F0964).

**F0938 · callback fields.map** — `index.html:L7831–7831` · ArrowFunction · parent F0937.  
Ulaz: `field`.  
Trag tela: `field.value||null`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0939 · closeEditor** — `index.html:L7834–7837` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ islandEditor=null;$('island-editor').hidden=true; document.body.classList.remove('editing-island');dirty=true;schedule(); }`.  
Poziva: `$` L7835 → F0819; `document.body.classList.remove` L7836 → —; `schedule` L7836 → F0893.  
Pozivaju: index.html:L7885 (F0943); index.html:L7892 (F0943); index.html:L8166 (F0961).

**F0940 · refreshEditor** — `index.html:L7838–7854` · FunctionDeclaration · parent F0818.  
Ulaz: `redraw=true`.  
Trag tela: `{ if(!islandEditor)return; const {key,target,fits}=islandEditor; const valid=Boolean(target&&fits?.(...target)); $('island-confirm').disable`.  
Poziva: `Boolean` L7841 → —; `fits` L7841 → —; `$` L7842 → F0819; `Boolean` L7844 → —; `$` L7846 → F0819; `schedule` L7853 → F0893.  
Pozivaju: index.html:L7434 (F0897); index.html:L7500 (F0901); index.html:L7878 (F0941); index.html:L8260 (F0973).

**F0941 · openEditor** — `index.html:L7855–7879` · FunctionDeclaration · parent F0818.  
Ulaz: `key`.  
Trag tela: `{ if(!s||race||typeof key!=='string'||!key)return; const selected=objects.find(o=>o.key===key&&movable(o,s)); const newHome=key==='new-home'`.  
Poziva: `objects.find` L7857 → —; `/^new-wheat:[0-4]$/.test` L7859 → —; `key.startsWith` L7860 → —; `key.slice` L7860 → —; `Boolean` L7861 → —; `s.built.includes` L7861 → —; `placementRules` L7864 → ~F0377; `nowBound` L7864 → F0828; `dismiss` L7866 → F0859; `$` L7871 → F0819; `Uint8Array` L7872 → —; `fits` L7873 → —; `$` L7876 → F0819; `document.body.classList.add` L7877 → —; `refreshEditor` L7878 → F0940.  
Pozivaju: index.html:L7881 (F0943); index.html:L7883 (F0943).

**F0942 · callback objects.find** — `index.html:L7857–7857` · ArrowFunction · parent F0941.  
Ulaz: `o`.  
Trag tela: `o.key===key&&movable(o,s)`.  
Poziva: `movable` L7857 → ~F0348.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0943 · controls** — `index.html:L7880–8164` · FunctionDeclaration · parent F0818.  
Ulaz: `action, value, inputAt=null`.  
Trag tela: `{ if(action==='island-edit'){openEditor(value);return;} // Existing build buttons reuse the same grid, preview and confirmation as moving. i`.  
Poziva: `openEditor` L7881 → F0941; `openEditor` L7883 → F0941; `closeEditor` L7885 → F0939; `islandEditor.fits` L7886 → —; `[1,2,3,4].find` L7888 → —; `key.startsWith` L7889 → —; `key.slice` L7889 → —; `commit` L7890 → F0876; `key.startsWith` L7890 → —; `key.startsWith` L7891 → —; `Number` L7891 → —; `key.split` L7891 → —; `closeEditor` L7892 → F0939; `toast` L7892 → F0830; `action.startsWith` L7897 → —; `testing` L7897 → F0825; `toast` L7897 → F0830; `cloudAction` L7897 → F0908; `action.startsWith` L7898 → —; `devAction` L7898 → F0924; `openScreen` L7904 → F0864; `cloudAction` L7905 → F0908; `dismiss` L7907 → F0859; `dismiss` L7908 → F0859; `selected` L7909 → F0827; `updatePanel` L7909 → F0870; `selected` L7910 → F0827; `updatePanel` L7910 → F0870; `updatePanel` L7911 → F0870; `Number` L7913 → —; `Number.isInteger` L7914 → —; `openScreen` L7915 → F0864; `startRace` L7917 → F0883; `quickRace` L7918 → F0847; `dismiss` L7919 → F0859; `openScreen` L7920 → F0864; `quickRace` L7920 → F0847; `arenaDefaults(s,view).stock.slice(0,4).map` L7924 → —; `arenaDefaults(s,view).stock.slice` L7924 → —; `arenaDefaults` L7924 → ~F0663; `updatePanel` L7925 → F0870; `updatePanel` L7927 → F0870; `arenaLoop` L7927 → F0850; `updatePanel` L7928 → F0870; `arenaLoop` L7928 → F0850; `modules.i18n.setLanguage` L7930 → ~F0813; `settingsWrite` L7931 → F0832; `modules.i18n.apply` L7932 → ~F0817; `document.querySelector` L7932 → —; `updatePanel` L7933 → F0870; `updateStatus` L7933 → F0837; `toast` L7933 → F0830; `applyTheme` L7935 → F0854; `settingsWrite` L7935 → F0832; `updatePanel` L7935 → F0870; `returnMap` L7939 → F0887; `startRace` L7939 → F0883; `laneCommand` L7941 → ~F0243; `laneCommand` L7942 → ~F0243; `boostCommand` L7943 → ~F0244; `toggleCamera` L7944 → F0892; `pauseRace` L7945 → F0889; `resumeRace` L7946 → F0891; `returnMap` L7947 → F0887; `saveReward` L7948 → F0885; `showSheet` L7949 → F0857; `discardResultPanel` L7949 → ~F0774; `Number` L7951 → —; `updatePanel` L7951 → F0870; `panel.querySelector('[data-action="plot"][aria-pressed="true"]')?.focus` L7952 → —; `panel.querySelector` L7952 → —; `zoomAt` L7954 → F0896; `Object.assign` L7955 → —; `markMap` L7955 → F0855; `updatePanel` L7957 → F0870; `panel.querySelector('.snx')?.focus` L7958 → —; `panel.querySelector` L7958 → —; `panel.querySelector('.sn-pic')?.focus` L7959 → —; `panel.querySelector` L7959 → —; `updatePanel` L7963 → F0870; `openScreen` L7963 → F0864; `Number` L7966 → —; `updatePanel` L7967 → F0870; `Number` L7969 → —; `keepPicks` L7969 → F0937; `updatePanel` L7969 → F0870; `s.snails.filter(n=>available(s,n)) .sort((a,b)=>modules.domain.snailPower(b)-modules.domain.snailPower(a)||b.prod-a.prod||a.id.localeCompare` L7973 → —; `s.snails.filter(n=>available(s,n)) .sort((a,b)=>modules.domain.snailPower(b)-modules.domain.snailPower(a)||b.prod-a.prod||a.id.localeCompare` L7973 → —; `s.snails.filter(n=>available(s,n)) .sort` L7973 → —; `s.snails.filter` L7973 → —; `updatePanel` L7976 → F0870; `updatePanel` L7978 → F0870; `['name','home','up'].includes` L7980 → —; `updatePanel` L7981 → F0870; `panel.querySelector('[data-action="snail-tab"][aria-pressed=true]')?.focus` L7982 → —; `panel.querySelector` L7982 → —; `s.snails.find` L7986 → —; `openShare` L7987 → F0909; `snailShareText` L7987 → ~F0572; `globalThis.Capacitor?.isNativePlatform` L7992 → —; `URL` L7992 → —; `openShare` L7993 → F0909; `[text,url].filter(Boolean).join` L7993 → —; `[text,url].filter` L7993 → —; `submitShare` L7995 → F0910; `submitShare` L7996 → F0910; `s.snails.find` L7998 → —; `showSheet` L7998 → F0857; `releasePanel` L7998 → ~F0778; `openScreen` L8000 → F0864; `updatePanel` L8000 → F0870; `Number` L8001 → —; `updatePanel` L8001 → F0870; `updatePanel` L8002 → F0870; `settingsWrite` L8003 → F0832; `resize` L8003 → F0880; `updatePanel` L8003 → F0870; `renderDev` L8003 → F0922; `showSheet` L8004 → F0857; `pausePanel` L8004 → ~F0775; `pauseOptions` L8004 → F0890; `Number` L8006 → —; `RACE_SPEED_OPTIONS.includes` L8007 → —; `RACE_SPEED_OPTIONS.indexOf` L8008 → —; `set` L8010 → F0826; `$` L8010 → F0819; `showSheet` L8011 → F0857; `pausePanel` L8011 → ~F0775; `pauseOptions` L8011 → F0890; `cycleCamera` L8014 → ~F0238; `set` L8014 → F0826; `$` L8014 → F0819; `showSheet` L8014 → F0857; `pausePanel` L8014 → ~F0775; `pauseOptions` L8014 → F0890; `panel.querySelectorAll('[data-action="feedback-kind"]').forEach` L8018 → —; `panel.querySelectorAll` L8018 → —; `($('feedback-text')?.value??'').trim().slice` L8024 → —; `($('feedback-text')?.value??'').trim` L8024 → —; `$` L8024 → F0819; `$` L8025 → F0819; `toast` L8026 → F0830; `mail.checkValidity` L8027 → —; `toast` L8027 → F0830; `mail.value.trim` L8029 → —; `encodeURIComponent` L8031 → —; `encodeURIComponent` L8032 → —; `updatePanel` L8036 → F0870; `soundToggle` L8037 → F0906; `JSON.stringify` L8039 → —; `(analytics.secs/3600).toFixed` L8039 → —; `Object.fromEntries` L8040 → —; `CUR_KEYS.map` L8040 → —; `openShare` L8041 → F0909; `Object.assign` L8044 → —; `analyticsSave` L8044 → F0834; `updatePanel` L8044 → F0870; `toast` L8044 → F0830; `download` L8046 → ~F0483; `globalThis.SC_STARTUP_TRACE?.export` L8046 → —; `toast` L8046 → F0830; `toast` L8047 → F0830; `download` L8051 → ~F0483; `measureReport` L8051 → F0836; `toast` L8052 → F0830; `toast` L8053 → F0830; `repo?.read` L8058 → —; `download` L8061 → ~F0483; `validateSave` L8061 → ~F0425; `toast` L8061 → F0830; `toast` L8062 → F0830; `toast` L8063 → F0830; `$('import-file').click` L8066 → —; `$` L8066 → F0819; `testing` L8068 → F0825; `toast` L8068 → F0830; `oldLocalSave` L8069 → ~F0521; `showImport` L8069 → F0878; `replaceSave` L8072 → F0877; `openScreen` L8072 → F0864; `toast` L8072 → F0830; `testing` L8074 → F0825; `toast` L8074 → F0830; `showSheet` L8074 → F0857; `erasePanel` L8074 → ~F0780; `replaceSave` L8075 → F0877; `newGame` L8075 → ~F0126; `dismiss` L8075 → F0859; `toast` L8075 → F0830; `testing` L8076 → F0825; `toast` L8076 → F0830; `showSheet` L8076 → F0857; `resetPanel` L8076 → ~F0779; `replaceSave` L8077 → F0877; `newGame` L8077 → ~F0126; `dismiss` L8077 → F0859; `toast` L8077 → F0830; `updatePanel` L8079 → F0870; `Number` L8081 → —; `updatePanel` L8082 → F0870; `Number` L8089 → —; `Number` L8091 → —; `selected` L8092 → F0827; `selected` L8095 → F0827; `selected` L8096 → F0827; `selected` L8098 → F0827; `Number` L8098 → —; `selected` L8098 → F0827; `selected` L8099 → F0827; `Boolean` L8100 → —; `selected` L8100 → F0827; `selected` L8101 → F0827; `selected` L8103 → F0827; `selected` L8103 → F0827; `picks` L8105 → F0936; `selected` L8107 → F0827; `selected` L8107 → F0827; `picks` L8109 → F0936; `clearTimeout` L8113 → —; `commit` L8115 → F0876; `openScreen` L8117 → F0864; `toast` L8120 → F0830; `['collect','expedition-claim','meteor','claim-daily','claim-login','exchange'].includes` L8121 → —; `flyReward` L8121 → F0911; `queueMicrotask` L8124 → —; `showSheet` L8146 → F0857; `hatchPanel` L8146 → ~F0765; `tickClocks` L8146 → F0871; `$` L8148 → F0819; `dismiss` L8149 → F0859; `toast` L8149 → F0830; `openScreen` L8150 → F0864; `toast` L8150 → F0830; `updatePanel` L8151 → F0870; `tickClocks` L8152 → F0871; `toast` L8153 → F0830; `format` L8153 → ~F0526; `toast` L8154 → F0830; `format` L8154 → ~F0526; `toast` L8155 → F0830; `format` L8155 → ~F0526; `toast` L8156 → F0830; `toast` L8157 → F0830; `toast` L8158 → F0830; `toast` L8159 → F0830; `toast` L8160 → F0830; `toast` L8161 → F0830; `format` L8161 → ~F0526; `tickClocks` L8162 → F0871; `toast` L8162 → F0830; `['arena-hit','arena-guard','arena-auto-finish'].includes` L8163 → —; `toast` L8163 → F0830.  
Pozivaju: index.html:L8171 (F0962); index.html:L8176 (F0963); index.html:L8177 (F0963); index.html:L8228 (F0970); index.html:L8228 (F0970).

**F0944 · callback [1,2,3,4].find** — `index.html:L7888–7888` · ArrowFunction · parent F0943.  
Ulaz: `i`.  
Trag tela: `!s.homes.some(h=>h.slot===i)`.  
Poziva: `s.homes.some` L7888 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0945 · callback s.homes.some** — `index.html:L7888–7888` · ArrowFunction · parent F0944.  
Ulaz: `h`.  
Trag tela: `h.slot===i`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0946 · callback arenaDefaults(s,view).stock.slice(0,4).map** — `index.html:L7924–7924` · ArrowFunction · parent F0943.  
Ulaz: `n`.  
Trag tela: `n.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0947 · callback s.snails.filter** — `index.html:L7973–7973` · ArrowFunction · parent F0943.  
Ulaz: `n`.  
Trag tela: `available(s,n)`.  
Poziva: `available` L7973 → ~F0095.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0948 · callback s.snails.filter(n=>available(s,n)) .sort** — `index.html:L7974–7974` · ArrowFunction · parent F0943.  
Ulaz: `a, b`.  
Trag tela: `modules.domain.snailPower(b)-modules.domain.snailPower(a)||b.prod-a.prod||a.id.localeCompare(b.id)`.  
Poziva: `modules.domain.snailPower` L7974 → ~F0069; `modules.domain.snailPower` L7974 → ~F0069; `a.id.localeCompare` L7974 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0949 · callback s.snails.filter(n=>available(s,n)) .sort((a,b)=>modules.domain.snailPower(b)-modules.domain.snailPower(a)||b.prod-a.prod||a.id.localeCompare** — `index.html:L7975–7975` · ArrowFunction · parent F0943.  
Ulaz: `n`.  
Trag tela: `n.id`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0950 · callback s.snails.find** — `index.html:L7986–7986` · ArrowFunction · parent F0943.  
Ulaz: `n`.  
Trag tela: `n.id===value&&n.id===view.inspect`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0951 · callback s.snails.find** — `index.html:L7998–7998` · ArrowFunction · parent F0943.  
Ulaz: `n`.  
Trag tela: `n.id===value`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0952 · callback panel.querySelectorAll('[data-action="feedback-kind"]').forEach** — `index.html:L8018–8021` · ArrowFunction · parent F0943.  
Ulaz: `b`.  
Trag tela: `{ const active=b.dataset.value===value;b.classList.toggle('on',active); b.setAttribute('aria-pressed',String(active)); }`.  
Poziva: `b.classList.toggle` L8019 → —; `b.setAttribute` L8020 → —; `String` L8020 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0953 · callback CUR_KEYS.map** — `index.html:L8040–8040` · ArrowFunction · parent F0943.  
Ulaz: `k`.  
Trag tela: `[k,Math.floor(s[k]??0)]`.  
Poziva: `Math.floor` L8040 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0954 · callback queueMicrotask** — `index.html:L8124–8141` · ArrowFunction · parent F0943.  
Ulaz: `—`.  
Trag tela: `{ const el=panel.querySelector('.tbswap'); if(el){ const a=watchTransient(el.animate([{transform:'scale(.94)',opacity:.7},{transform:'scale(`.  
Poziva: `panel.querySelector` L8125 → —; `watchTransient` L8127 → F0822; `el.animate` L8127 → —; `a.finished.catch(()=>{}).finally` L8128 → —; `a.finished.catch` L8128 → —; `el.querySelectorAll` L8130 → —; `halves.forEach` L8131 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0955 · callback a.finished.catch** — `index.html:L8128–8128` · ArrowFunction · parent F0954.  
Ulaz: `—`.  
Trag tela: `{}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0956 · callback a.finished.catch(()=>{}).finally** — `index.html:L8128–8128` · ArrowFunction · parent F0954.  
Ulaz: `—`.  
Trag tela: `a.cancel()`.  
Poziva: `a.cancel` L8128 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0957 · callback halves.forEach** — `index.html:L8131–8139` · ArrowFunction · parent F0954.  
Ulaz: `half, i`.  
Trag tela: `{ const side=i===0?-1:1; const h=watchTransient(half.animate([ {transform:'translateX(0) rotate(0)',opacity:.75}, {transform:'translateX('+(`.  
Poziva: `watchTransient` L8133 → F0822; `half.animate` L8133 → —; `h.finished.catch(()=>{}).finally` L8138 → —; `h.finished.catch` L8138 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0958 · callback h.finished.catch** — `index.html:L8138–8138` · ArrowFunction · parent F0957.  
Ulaz: `—`.  
Trag tela: `{}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0959 · callback h.finished.catch(()=>{}).finally** — `index.html:L8138–8138` · ArrowFunction · parent F0957.  
Ulaz: `—`.  
Trag tela: `h.cancel()`.  
Poziva: `h.cancel` L8138 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0960 · attachUI** — `index.html:L8165–8254` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ document.addEventListener('keydown',e=>{if(e.key==='Escape'&&islandEditor)closeEditor();}); document.addEventListener('click',e=>{ const b`.  
Poziva: `document.addEventListener` L8166 → —; `document.addEventListener` L8168 → —; `panel.addEventListener` L8173 → —; `panel.addEventListener` L8179 → —; `panel.addEventListener` L8201 → —; `$('import-file').addEventListener` L8215 → —; `$` L8215 → F0819; `document.addEventListener` L8224 → —; `document.addEventListener` L8225 → —; `document.addEventListener` L8238 → —.  
Pozivaju: index.html:L8344 (F0975).

**F0961 · callback document.addEventListener** — `index.html:L8166–8166` · ArrowFunction · parent F0960.  
Ulaz: `e`.  
Trag tela: `{if(e.key==='Escape'&&islandEditor)closeEditor();}`.  
Poziva: `closeEditor` L8166 → F0939.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0962 · callback document.addEventListener** — `index.html:L8168–8172` · ArrowFunction · parent F0960.  
Ulaz: `e`.  
Trag tela: `{ const button=e.target.closest('button[data-action]'); if(!button||button.disabled||bootError)return; controls(button.dataset.action,button`.  
Poziva: `e.target.closest` L8169 → —; `controls` L8171 → F0943.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0963 · callback panel.addEventListener** — `index.html:L8173–8178` · ArrowFunction · parent F0960.  
Ulaz: `e`.  
Trag tela: `{ e.preventDefault(); if(race&&!race.finish)resumeRace(); else if(!race&&view.inspect)controls('inspect',''); else if(!race)controls('close-`.  
Poziva: `e.preventDefault` L8174 → —; `resumeRace` L8175 → F0891; `controls` L8176 → F0943; `controls` L8177 → F0943.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0964 · callback panel.addEventListener** — `index.html:L8179–8200` · ArrowFunction · parent F0960.  
Ulaz: `e`.  
Trag tela: `{ const id=e.target.id, again=()=>{updatePanel();$(id)?.focus({preventScroll:true});}; if(id==='home-sort'){ // v147 compatibility: choosing`.  
Poziva: `modules.domain.AUTO_HOME_STATS.includes` L8185 → —; `commit` L8186 → F0876; `Boolean` L8186 → —; `again` L8187 → F0965; `again` L8190 → F0965; `selected` L8191 → F0827; `selected` L8191 → F0827; `updatePanel` L8191 → F0870; `again` L8192 → F0965; `keepPicks` L8193 → F0937; `again` L8193 → F0965; `keepPicks` L8194 → F0937; `again` L8195 → F0965; `id.startsWith` L8197 → —; `id.slice` L8198 → —; `again` L8198 → F0965.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0965 · again** — `index.html:L8180–8180` · ArrowFunction · parent F0964.  
Ulaz: `—`.  
Trag tela: `{updatePanel();$(id)?.focus({preventScroll:true});}`.  
Poziva: `updatePanel` L8180 → F0870; `$(id)?.focus` L8180 → —; `$` L8180 → F0819.  
Pozivaju: index.html:L8187 (F0964); index.html:L8190 (F0964); index.html:L8192 (F0964); index.html:L8193 (F0964); index.html:L8195 (F0964); index.html:L8198 (F0964).

**F0966 · callback panel.addEventListener** — `index.html:L8201–8214` · ArrowFunction · parent F0960.  
Ulaz: `e`.  
Trag tela: `{ if(e.target.id==='music-volume'){ view.music=Math.max(0,Math.min(1,Number(e.target.value)/100));settingsWrite();if(audio)audio.volume=.26*`.  
Poziva: `Math.max` L8203 → —; `Math.min` L8203 → —; `Number` L8203 → —; `settingsWrite` L8203 → F0832; `clearTimeout` L8208 → —; `setTimeout` L8209 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0967 · callback setTimeout** — `index.html:L8209–8213` · ArrowFunction · parent F0966.  
Ulaz: `—`.  
Trag tela: `{ if(view.viewKey!=='collection'&&view.viewKey!=='tree')return; updatePanel(); $('collection-search')?.focus({preventScroll:true}); }`.  
Poziva: `updatePanel` L8211 → F0870; `$('collection-search')?.focus` L8212 → —; `$` L8212 → F0819.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0968 · callback $('import-file').addEventListener** — `index.html:L8215–8221` · ArrowFunction · parent F0960.  
Ulaz: `e`.  
Trag tela: `{ const file=e.target.files?.[0]; e.target.value=''; if(!file)return; if(file.size>2e6){toast('Sejv je prevelik.');return;} try{showImport(a`.  
Poziva: `toast` L8219 → F0830; `showImport` L8220 → F0878; `file.text` L8220 → —; `toast` L8220 → F0830.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0969 · callback document.addEventListener** — `index.html:L8224–8224` · ArrowFunction · parent F0960.  
Ulaz: `—`.  
Trag tela: `{view.touchAt=Date.now();activityBadge(view.touchAt);}`.  
Poziva: `Date.now` L8224 → —; `activityBadge` L8224 → F0839.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0970 · callback document.addEventListener** — `index.html:L8225–8237` · ArrowFunction · parent F0960.  
Ulaz: `e`.  
Trag tela: `{ if(!race&&panel.open&&e.key==='Escape'){ e.preventDefault(); if(view.inspect)controls('inspect','');else controls('close-panel'); return; `.  
Poziva: `e.preventDefault` L8227 → —; `controls` L8228 → F0943; `controls` L8228 → F0943; `e.target.matches` L8231 → —; `resumeRace` L8232 → F0891; `pauseRace` L8232 → F0889; `e.preventDefault` L8232 → —; `e.preventDefault` L8234 → —; `laneCommand` L8234 → ~F0243; `e.key.toLowerCase` L8235 → —; `toggleCamera` L8235 → F0892; `e.target.matches` L8236 → —; `e.preventDefault` L8236 → —; `boostCommand` L8236 → ~F0244.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0971 · callback document.addEventListener** — `index.html:L8238–8253` · ArrowFunction · parent F0960.  
Ulaz: `—`.  
Trag tela: `{ if(document.hidden)clearTransientFx(); // Reuse the existing lifecycle hook: hide decorative FX in background tabs. if(s)modules.scenes.sc`.  
Poziva: `clearTransientFx` L8239 → F0824; `modules.scenes.scUpdateReservoirFx` L8241 → ~F0394; `nowBound` L8241 → F0828; `cancelAnimationFrame` L8243 → —; `pauseRace` L8244 → F0889; `audio?.pause` L8245 → —; `analyticsSave` L8246 → F0834; `metrics.mapReturn` L8247 → —; `Math.max` L8247 → —; `markMap` L8250 → F0855; `audio?.play().catch` L8250 → —; `audio?.play` L8250 → —; `settleClock` L8251 → F0973.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0972 · callback audio?.play().catch** — `index.html:L8250–8250` · ArrowFunction · parent F0971.  
Ulaz: `—`.  
Trag tela: `{}`.  
Poziva: nema eksplicitnih call/new u ovom telu.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0973 · settleClock** — `index.html:L8255–8271` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ if(!document.hidden){analytics.secs++;if(analytics.secs%15===0){analyticsDirty=true;analyticsSave();}} if(document.hidden||race||!s)return`.  
Poziva: `analyticsSave` L8256 → F0834; `devAction` L8258 → F0924; `nowBound` L8259 → F0828; `islandEditor?.key.startsWith` L8260 → —; `refreshEditor` L8260 → F0940; `s.eggs.some` L8263 → —; `commit` L8266 → F0876; `['progress','shop','crater','incubator','island-menu'].includes` L8267 → —; `updatePanel` L8267 → F0870; `signatures` L8269 → F0860; `['incubator','island-menu','expeditions','trophies','progress','pageant','crater','shop','login','wheat'].includes` L8269 → —; `updatePanel` L8269 → F0870; `tickClocks` L8270 → F0871.  
Pozivaju: index.html:L8251 (F0971); index.html:L8350 (F0975).

**F0974 · callback s.eggs.some** — `index.html:L8263–8263` · ArrowFunction · parent F0973.  
Ulaz: `egg`.  
Trag tela: `egg.halfHeld&&!canCare(egg,now)`.  
Poziva: `canCare` L8263 → ~F0049.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0975 · boot** — `index.html:L8272–8360` · FunctionDeclaration · parent F0818.  
Ulaz: `—`.  
Trag tela: `{ const scT=globalThis.SC_STARTUP_TRACE,scBootStart=scT?.begin();scT?.mark('boot.enter'); try{ const init=baseTime(); renderer=new Renderer(`.  
Poziva: `scT?.begin` L8273 → —; `scT?.mark` L8273 → —; `baseTime` L8275 → F0829; `Renderer` L8276 → —; `$` L8276 → F0819; `SceneManager` L8277 → —; `metrics.markLoading` L8278 → —; `baseTime` L8278 → F0829; `scT?.end` L8307 → —; `scT?.mark` L8308 → —; `baseTime` L8309 → F0829; `repository().then` L8310 → —; `repository` L8310 → ~F0518; `renderer.preload('island').then` L8315 → —; `renderer.preload` L8315 → —; `renderer.preloadIllustratedMap` L8316 → —; `scT?.mark` L8317 → —; `Promise.all` L8318 → —; `scT?.mark` L8319 → —; `toast` L8324 → F0830; `Boolean` L8326 → —; `oldLocalSave` L8326 → ~F0521; `scT?.begin` L8327 → —; `validateSave` L8328 → ~F0425; `newGame` L8328 → ~F0126; `scT?.end` L8329 → —; `scT?.begin` L8333 → —; `modules.scenes.prepareIsland` L8334 → ~F0370; `scT?.end` L8335 → —; `Boolean` L8336 → —; `scT?.begin` L8337 → —; `analytics.lv.push` L8338 → —; `(analytics.secs/3600).toFixed` L8338 → —; `analyticsSave` L8338 → F0834; `scT?.end` L8339 → —; `toast` L8340 → F0830; `toast` L8341 → F0830; `scT?.begin` L8342 → —; `sceneManager.activate` L8343 → —; `applyTheme` L8344 → F0854; `resize` L8344 → F0880; `markMap` L8344 → F0855; `attachInput` L8344 → F0898; `attachUI` L8344 → F0960; `updateStatus` L8344 → F0837; `renderDev` L8344 → F0922; `modules.i18n.apply` L8344 → ~F0817; `document.querySelector` L8344 → —; `scT?.end` L8345 → —; `new ResizeObserver(resize).observe` L8348 → —; `ResizeObserver` L8348 → —; `window.addEventListener` L8349 → —; `setInterval` L8350 → —; `settleClock` L8350 → F0973; `$` L8351 → F0819; `document.body.classList.remove` L8351 → —; `scT?.mark` L8352 → —; `scT?.end` L8353 → —; `$` L8358 → F0819; `set` L8358 → F0826; `$` L8358 → F0819.  
Pozivaju: index.html:L8361 (F0818).

**F0976 · renderer.onLoss** — `index.html:L8279–8295` · ArrowFunction · parent F0975.  
Ulaz: `—`.  
Trag tela: `{ clearTimeout(restoreTimer); if(race&&!race.finish){ metrics.end('context-lost'); pauseRace(); } else{ if(returnTrace){ metrics.mapReturn({`.  
Poziva: `clearTimeout` L8280 → —; `metrics.end` L8282 → —; `pauseRace` L8283 → F0889; `metrics.mapReturn` L8287 → —; `Math.max` L8287 → —; `toast` L8290 → F0830; `setTimeout` L8292 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0977 · callback setTimeout** — `index.html:L8292–8294` · ArrowFunction · parent F0976.  
Ulaz: `—`.  
Trag tela: `{ if(renderer.lost&&!renderer.useCanvasFallback())toast('Grafika je nedostupna. Osveži igru za ponovni pokušaj.'); }`.  
Poziva: `renderer.useCanvasFallback` L8293 → —; `toast` L8293 → F0830.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0978 · renderer.onRestore** — `index.html:L8296–8300` · ArrowFunction · parent F0975.  
Ulaz: `—`.  
Trag tela: `{ clearTimeout(restoreTimer); if(race?.paused&&!race.finish){startMetricSegment();showSheet(pausePanel(false,pauseOptions()));dirty=true;sch`.  
Poziva: `clearTimeout` L8297 → —; `startMetricSegment` L8298 → F0881; `showSheet` L8298 → F0857; `pausePanel` L8298 → ~F0775; `pauseOptions` L8298 → F0890; `schedule` L8298 → F0893; `markMap` L8299 → F0855.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0979 · renderer.onFallback** — `index.html:L8301–8306` · ArrowFunction · parent F0975.  
Ulaz: `—`.  
Trag tela: `{ pointers.clear();raceTouch=null; attachInput();updateStatus(); renderer.onRestore(); toast('Prikaz je prešao na Canvas 2D.'); }`.  
Poziva: `pointers.clear` L8302 → —; `attachInput` L8303 → F0898; `updateStatus` L8303 → F0837; `renderer.onRestore` L8304 → —; `toast` L8305 → F0830.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0980 · callback repository().then** — `index.html:L8310–8314` · ArrowFunction · parent F0975.  
Ulaz: `store`.  
Trag tela: `{ const loaded=await store?.load(); metrics.markLoading('saveReadMs',baseTime()-startup); return {store,...loaded}; }`.  
Poziva: `store?.load` L8311 → —; `metrics.markLoading` L8312 → —; `baseTime` L8312 → F0829.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0981 · callback renderer.preload('island').then** — `index.html:L8315–8315` · ArrowFunction · parent F0975.  
Ulaz: `—`.  
Trag tela: `metrics.markLoading('islandAtlasMs',baseTime()-startup)`.  
Poziva: `metrics.markLoading` L8315 → —; `baseTime` L8315 → F0829.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

### SW — offline shell i HTTP presretanje

**F0982 · callback CORE_PATHS.map** — `sw.js:L16–19` · ArrowFunction · parent —.  
Ulaz: `path`.  
Trag tela: `{ const url = new URL(path,SCOPE); return [url.href, url]; }`.  
Poziva: `URL` L17 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0983 · isWithinScope** — `sw.js:L22–22` · FunctionDeclaration · parent —.  
Ulaz: `url`.  
Trag tela: `{return url.origin===SCOPE.origin && url.pathname.startsWith(SCOPE.pathname);}`.  
Poziva: `url.pathname.startsWith` L22 → —.  
Pozivaju: sw.js:L64 (F0993).

**F0984 · isCore** — `sw.js:L23–23` · FunctionDeclaration · parent —.  
Ulaz: `url`.  
Trag tela: `{return CORE.has(url.href);}`.  
Poziva: `CORE.has` L23 → —.  
Pozivaju: sw.js:L76 (F0993); sw.js:L84 (F0993).

**F0985 · isEntryNavigation** — `sw.js:L24–26` · FunctionDeclaration · parent —.  
Ulaz: `url`.  
Trag tela: `{ return url.pathname===SCOPE.pathname || url.pathname===new URL('./index.html',SCOPE).pathname; }`.  
Poziva: `URL` L25 → —.  
Pozivaju: sw.js:L67 (F0993).

**F0986 · callback self.addEventListener** — `sw.js:L27–51` · ArrowFunction · parent —.  
Ulaz: `event`.  
Trag tela: `{ event.waitUntil((async()=>{ const cache=await caches.open(CACHE_NAME); let total=0; try{ for (const [href] of CORE){ const response=await `.  
Poziva: `event.waitUntil` L28 → —; `(async()=>{ const cache=await caches.open(CACHE_NAME); let total=0; try{ for (const [href] of CORE){ const response=await fetch(new Request(` L28 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0987 · anonimna** — `sw.js:L28–50` · ArrowFunction · parent F0986.  
Ulaz: `—`.  
Trag tela: `{ const cache=await caches.open(CACHE_NAME); let total=0; try{ for (const [href] of CORE){ const response=await fetch(new Request(href,{cach`.  
Poziva: `caches.open` L29 → —; `fetch` L33 → —; `Request` L33 → —; `Error` L34 → —; `response.clone().blob` L35 → —; `response.clone` L35 → —; `Error` L37 → —; `(response.headers.get('content-type')||'').toLowerCase` L38 → —; `response.headers.get` L38 → —; `href.endsWith` L39 → —; `type.includes` L39 → —; `Error` L39 → —; `href.endsWith` L40 → —; `/json|manifest/.test` L40 → —; `Error` L40 → —; `href.endsWith` L41 → —; `type.includes` L41 → —; `Error` L41 → —; `cache.put` L42 → —; `self.skipWaiting` L45 → —; `caches.delete` L47 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0988 · callback self.addEventListener** — `sw.js:L52–59` · ArrowFunction · parent —.  
Ulaz: `event`.  
Trag tela: `{ event.waitUntil((async()=>{ const names=await caches.keys(); await Promise.all(names.filter(name=>name!==CACHE_NAME && OWNED_PREFIXES.some`.  
Poziva: `event.waitUntil` L53 → —; `(async()=>{ const names=await caches.keys(); await Promise.all(names.filter(name=>name!==CACHE_NAME && OWNED_PREFIXES.some(prefix=>name.star` L53 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0989 · anonimna** — `sw.js:L53–58` · ArrowFunction · parent F0988.  
Ulaz: `—`.  
Trag tela: `{ const names=await caches.keys(); await Promise.all(names.filter(name=>name!==CACHE_NAME && OWNED_PREFIXES.some(prefix=>name.startsWith(pre`.  
Poziva: `caches.keys` L54 → —; `Promise.all` L55 → —; `names.filter(name=>name!==CACHE_NAME && OWNED_PREFIXES.some(prefix=>name.startsWith(prefix))) .map` L55 → —; `names.filter` L55 → —; `self.clients.claim` L57 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0990 · callback names.filter** — `sw.js:L55–55` · ArrowFunction · parent F0989.  
Ulaz: `name`.  
Trag tela: `name!==CACHE_NAME && OWNED_PREFIXES.some(prefix=>name.startsWith(prefix))`.  
Poziva: `OWNED_PREFIXES.some` L55 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0991 · callback OWNED_PREFIXES.some** — `sw.js:L55–55` · ArrowFunction · parent F0990.  
Ulaz: `prefix`.  
Trag tela: `name.startsWith(prefix)`.  
Poziva: `name.startsWith` L55 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0992 · callback names.filter(name=>name!==CACHE_NAME && OWNED_PREFIXES.some(prefix=>name.startsWith(prefix))) .map** — `sw.js:L56–56` · ArrowFunction · parent F0989.  
Ulaz: `name`.  
Trag tela: `caches.delete(name)`.  
Poziva: `caches.delete` L56 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0993 · callback self.addEventListener** — `sw.js:L60–89` · ArrowFunction · parent —.  
Ulaz: `event`.  
Trag tela: `{ const req=event.request; if(req.method!=='GET')return; const url=new URL(req.url); if(!isWithinScope(url))return; if(req.mode==='navigate'`.  
Poziva: `URL` L63 → —; `isWithinScope` L64 → F0983; `isEntryNavigation` L67 → F0985; `event.respondWith` L68 → —; `(async()=>{ try{ const live=await fetch(req); if(live.ok)return live; }catch(_){} const cached=await (await caches.open(CACHE_NAME)).match(E` L68 → —; `isCore` L76 → F0984; `event.respondWith` L77 → —; `(async()=>{ try{const live=await fetch(req);if(live.ok)return live;}catch(_){} return (await (await caches.open(CACHE_NAME)).match(url.href)` L77 → —; `isCore` L84 → F0984; `event.respondWith` L85 → —; `(async()=>{ const cached=await (await caches.open(CACHE_NAME)).match(url.href); return cached || fetch(req); })` L85 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0994 · anonimna** — `sw.js:L68–75` · ArrowFunction · parent F0993.  
Ulaz: `—`.  
Trag tela: `{ try{ const live=await fetch(req); if(live.ok)return live; }catch(_){} const cached=await (await caches.open(CACHE_NAME)).match(ENTRY); ret`.  
Poziva: `fetch` L70 → —; `(await caches.open(CACHE_NAME)).match` L73 → —; `caches.open` L73 → —; `Response.error` L74 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0995 · anonimna** — `sw.js:L77–80` · ArrowFunction · parent F0993.  
Ulaz: `—`.  
Trag tela: `{ try{const live=await fetch(req);if(live.ok)return live;}catch(_){} return (await (await caches.open(CACHE_NAME)).match(url.href)) || Respo`.  
Poziva: `fetch` L78 → —; `(await caches.open(CACHE_NAME)).match` L79 → —; `caches.open` L79 → —; `Response.error` L79 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

**F0996 · anonimna** — `sw.js:L85–88` · ArrowFunction · parent F0993.  
Ulaz: `—`.  
Trag tela: `{ const cached=await (await caches.open(CACHE_NAME)).match(url.href); return cached || fetch(req); }`.  
Poziva: `(await caches.open(CACHE_NAME)).match` L86 → —; `caches.open` L86 → —; `fetch` L87 → —.  
Pozivaju: nije utvrđen direktan poziv; proveriti registraciju/alias.

## 8. Pozivi izvan funkcijskih tela (dodatak B)

- `index.html:L9` `(function(){ 'use strict'; // Diagnostic only: bounded in-memory timings, never stores/uploads player data. const events=[],longTasks=[];con` → —
- `index.html:L69` `(function(){ 'use strict'; var diagnostic={version:'0.8.93',state:'unsupported',ready:false,controlled:false,error:null}; window.SC_PWA_STAT` → —
- `index.html:L1885` `(()=>{ // Content imported from the v174.103 catalog. const catalog = {"species":[{"id":0,"sr":"Plamenko","en":"Pyre-Snail","elements":["fir` → —
- `index.html:L1932` `globalThis.SC_STARTUP_TRACE?.mark` → —
- `index.html:L1935` `(()=>{ const modules={}; modules.catalog=(()=>{ if(!globalThis.SnailCatalog)throw new Error('catalog.js nije učitan'); const catalog = globa` → —
- `sw.js:L15` `URL` → —
- `sw.js:L16` `Map` → —
- `sw.js:L16` `CORE_PATHS.map` → —
- `sw.js:L20` `URL` → —
- `sw.js:L21` `Error` → —
- `sw.js:L27` `self.addEventListener` → —
- `sw.js:L52` `self.addEventListener` → —
- `sw.js:L60` `self.addEventListener` → —

## 9. Status i održavanje
| Stavka | Status |
|---|---|
| Identitet i CRC ZIP | URAĐENO |
| AST inventar deklaracija i eksplicitnih call/new | URAĐENO |
| Statičke veze i kandidat aliasi | URAĐENO u definisanom opsegu |
| Ručna semantika ključnih funkcija | URAĐENO za odeljak 6 |
| Ručni ugovor, read/write i runtime graf svake funkcije | DELIMIČNO |
| Kontradikcije i rizici | URAĐENO za navedene nalaze; nije iscrpan bug audit |
| Chromium, Netlify, fizički Android | NIJE URAĐENO — dokumentacioni zadatak |
| GitHub, igra, save izmene | NIJE URAĐENO — namerno |

Izvori: priloženi 0.8.93 ZIP, SC-ARCH-01 §4–11, SC-AGENT-01 SC-A01–05 i G0–G7, Snail-City-0.8.93-SOURCES. Eksterni standardi su već referencirani u SC-ARCH-01; ovaj audit ne tvrdi da ih je ponovo proverio. Predložena lokacija: docs/tehnika/standardi/SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md.
