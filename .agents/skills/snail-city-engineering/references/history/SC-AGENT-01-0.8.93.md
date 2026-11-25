# SNAIL CITY — OBAVEZNI STANDARD RADA AGENATA

**Oznaka:** SC-AGENT-01 | **Revizija dokumenta:** 1.0 | **Datum:** 24.11.2026.  
**Opseg:** Snail City 0.8.93 i naredni kandidati; AI agenti, developeri, revieweri i QA.  
**Namena:** normativni operativni dokument za Project Sources. Ne predstavlja novi runtime autoritet, zamenu za `AGENTS.md`, odobrenje za deploy ili potvrdu da je igra testirana.  
**Modalitet:** MORA = uslov prihvatanja; ZABRANJENO = blokada; PREPORUČENO = primeniti kada odgovara postojećoj arhitekturi. Oznake SC-A01…SC-A15 služe za pozivanje u izveštajima, ne za novi registar izvršnih pravila.

## 0. Obavezan rezultat svakog zadatka

Pre rada agent mora prikazati spisak konkretnih rezultata i merljivih kriterijuma prihvatanja. Po završetku za svaku stavku upisati **URAĐENO / DELIMIČNO / NIJE URAĐENO**, uz dokaz ili razlog blokade. Na primer, za trku: pozadina, staza, ograda, propovi, senke, start, cilj, rezultat, povratak na ostrvo. Nema deklaracije „gotovo“ dok svaka obavezna stavka nije implementirana i proverena u stvarnoj igri. Dokumentacioni zadatak ne zahteva izmišljene testove igre.

**Zlatno pravilo:** Prvo pronađi postojeće rešenje, razumi njegovu svrhu i zavisnosti, proširi ga najmanjom bezbednom izmenom, pa dokaži rezultat. Funkcionalnost, integritet napretka i kvalitet prikaza imaju prednost nad estetikom implementacije, novim bibliotekama i brzinom isporuke.

## 1. SC-A01 — Izvor, verzija i stvarni opseg

1. Pre izmene pročitaj root `AGENTS.md`, `docs/README.md`, relevantni standard i QA registar. Proveri pristup fajlovima; nedostajući ZIP, sliku, uređaj ili backend prijavi odmah.
2. Identifikuj repozitorijum, granu, commit, Git tree/blob SHA i po potrebi SHA-256 izvršnog ZIP/HTML/SW. Zabeleži URL, origin, backend, stvarnu oznaku verzije u runtime-u, status SW i deploy inventar. Ne pretpostavljaj da naziv foldera predstavlja izdanje.
3. `snail-city-test/main` je dokumentovana stabilna referenca 0.8.90 za PW-01; `test-2/main` ima SW označen 0.8.93. Sama oznaka SW nije dokaz identiteta celog HTML-a ili produkcije. v0.8.92 audit je izolovani istorijski P1 kandidat, ne audit 0.8.93. v174 je zamenjena aplikacija; njene brojke i komande nisu aktivna specifikacija.
4. U slučaju konflikta između pravila, dokumentacije i izvršnog koda: zabeleži konflikt, verzije i dokaz; ne prepravljaj igru prema arhivskom dokumentu niti proglašavaj bug standardom. P0 rizik izoluj. Za promenu pravila ili destruktivan zahvat potrebno je eksplicitno odobrenje vlasnika.
5. Ovaj dokument objedinjuje već usvojena projektna pravila i dopunjuje ih operativnim kriterijumima. Za specifičan podsistem važi njegov izvorni detaljni standard; nove dopune služe kao gate za naredni rad, ne kao dokaz postojeće implementacije.

## 2. SC-A02 — Jedan izvor istine (SSOT)

ZABRANJENI su paralelni renderer, koordinatni proračun, maska kolizije, lista brzina, tajmer, game loop, ekonomski registar, save adapter ili UI logika koja samostalno menja domensko stanje, kada odgovarajući autoritet već postoji.

Pre patch-a: pretraži deklaracije, export/import, sve čitaoce i pisce, dinamičke pozive, string reference i testove (`rg`, IDE, AST parser). Nacrtaj lanac vlasnik → potrošači → proračun → prikaz → potvrda → save. Promeni vlasnika i njegove potrošače, ne napravi konkurentski autoritet. Ako postojeće rešenje zaista ne zadovoljava zahtev, dokumentuj zašto, predloži migraciju i dokaz da stari autoritet neće ostati paralelno aktivan.

Poznati autoriteti iz projektnog SSOT dokumenta (njihovo prisustvo i potpis proveriti u ciljnom buildu):

| Oblast | Referentni vlasnik |
|---|---|
| Trajne prepreke i teren | `FIELD.rows` → `forbiddenCell()` |
| Stvarna osnova i sidro | `SC_STRUCTURE` → `supportFootprint()` |
| Validacija gradnje | `placementRules()` → `fitsTerrain()` / `canPlace()` |
| Položaji | `s.islandPositions` |
| Vizuelne instance | `mapRect()` → `scBuildVisualInstances()` |
| Brzine trke | `modules.race.RACE_SPEED_OPTIONS` |
| Fizika | `modules.physics.integrate()` / `step()` |
| Perspektiva trke | `modules.race.createProjection()` |
| Staza | `modules.scenes.paintRace()` |
| Nagrade i stanje | reducer / `applyCommand()` |
| Render petlja | `schedule()` / `loop()` — jedan rAF |
| Čuvanje | `modules.storage` / `modules.cloud` |

Lista `[10,20,30,40,50,60]` i `RACE_NORMAL_SPEED` iz SSOT standarda predstavljaju referencu za odgovarajuću verziju: UI i handler čitaju jednu vrednosnu listu; ne upisuj nove vrednosti bez provere trenutnog izvora. Test sme imati nezavisnu očekivanu vrednost. Izvedeni keš je dozvoljen samo ako je obnovljiv, invalidiran pri promeni vlasnika, nije editable i ne postaje save autoritet.

## 3. SC-A03 — Minimalna, izolovana izmena

Jedan problem — jedan kandidat — jedna uzročna hipoteza. Sačuvaj neizmenjeni baseline i rollback. Ne mešaj UI optimizaciju, atlas, save, SW, ekonomiju i fiziku u istom eksperimentu. Ne uvodi framework, drugi engine, novu biblioteku, prepisivanje ili migraciju arhitekture ako postojeće rešenje ispunjava potrebu. Proveri da li postojeći API/biblioteka već rešava problem. Bez nepotrebnog formatiranja celog fajla, preimenovanja ili promene verzije izvan dogovorenog opsega.

Razdvoji činjenicu, hipotezu, promenu i rezultat. Ograniči diff na relevantne fajlove. Novi dependency zahteva razlog, proveru kompatibilnosti, licence, veličine, offline dostupnosti i plan održavanja. Nema automatskog merge/deploy-a, promene stvarnih podataka ili brisanja udaljene istorije.

## 4. SC-A04 — Mapa, input, gradnja, kolizije

- Jedinstven tok: pointer/touch → canvas CSS koordinate → stvarni drawing buffer/viewport → inverzna projekcija kamere → world → grid. Uvaži DPR, zoom, pan, rotaciju, granice i scroll. CSS pikseli i buffer pikseli nisu isto. Ne primenjuj DPR dvaput.
- Isti kanonski proračun osnove, rotacije, snap-a, sidra i terena koristi se za preview, hit-test, potvrdu i upis. Kolizija se računa iz stvarne stajne površine, ne pravougaonika cele slike ili senke. Putevi, ivice, fontana, bazen, vodopad i druge zabranjene ćelije proveravaju se eksplicitno iz vlasnika terena.
- Prikaz dozvoljeno/zabranjeno mora odgovarati potvrdi. Pre commit-a ponovo validiraj trenutno stanje. Odbijena radnja ne menja valutu, inventar ni položaj; drag cancel vraća original, bez duplih event handlera.
- QA: validna ćelija, zauzeta ćelija, svaka vrsta trajne prepreke, delimični izlaz osnove, različita veličina građevine, pomeranje i otkaz, reload, minimum/maksimum zuma, 2 orijentacije, miš i touch. Proveri vizuelno sidro i hitbox u istom kadru.

## 5. SC-A05 — Trke, borbe, ekonomija i tajmeri

Koristi postojeće komande, definicije staza, statistike puževa i centralni reducer. Brzina, izdržljivost i šteta izvode se iz stvarnih atributa i odobrene formule, bez hardkodovanja nezavisnog UI rezultata. Ne menja se balans, cena, valuta, XP, verovatnoća, cooldown ili nagrada radi optimizacije. Svaka nova mehanika mora imati cilj, okidač, pravilo, merljivi rezultat, validne/nevalidne ulaze, vidljiv feedback i test; kontrolu, rezultat, pauzu i povratak zadržati prema aktivnoj specifikaciji.

Simulacija ne sme zavisiti od FPS-a. Koristi postojeći delta/fixed-step mehanizam i ograničenje koraka; proveri velike speed multiplikatore i resume posle background-a, bez preskakanja sudara ili duplih nagrada. Odvoji real-time tajmere jaja/uzgoja/resursa od vremena simulacije. Trajanje se izvodi iz sačuvanih vremenskih oznaka; validiraj negativne i nevažeće intervale, promenu sata i granice napretka prema postojećoj politici. Jedna potvrđena transakcija → jedna naplata/nagrada; neuspeh, dupli klik, ponovno otvaranje ili prekid ne smeju ponovo izvršiti komandu.

QA: postojeće staze, start/cilj, rezultat/pauza/izlaz, povratak na ostrvo, kolizije više puževa, 30/60 FPS režimi ako postoje, kupovina bez sredstava, dupli klik, jaje/inkubator, iste vrednosti posle reload-a i offline napredak. Ne izmišljaj brojeve iz v174 ili starog GDD-a.

## 6. SC-A06 — Renderer, WebGL i resursi

- Jedan postojeći rAF scheduler i renderer. Update simulacije, stanje i crtanje imaju odvojene odgovornosti; render ne pokreće transakcije, save ili poslovnu logiku. Ne dodaj drugi canvas/loop da sakrije grešku prvog.
- Recikliraj objekte/bafer-e i geometriju kada profilisanje opravdava; izbegavaj alokacije, dekodiranje i upload tekstura u hot path-u. Batch-uj kompatibilne draw pozive unutar postojećeg renderera. Izbegavaj sinhroni `readPixels`/`getError`/`getParameter` u svakom frejmu; dijagnostika u posebnom režimu.
- Poštuj realne GPU limite i budžet tekstura. Koristi stvarni format, dimenzije, alfa kanal, atlas i filter primeren postojećem stilu. Pri promeni scene očisti resurse čiji je životni ciklus završen; ne uništavaj zajedničke resurse koje druga scena koristi.
- Obradi `webglcontextlost` i `webglcontextrestored` prema postojećem rendereru; sačuvaj stanje igre, zaustavi nevažeće GL pozive, obnovi GPU resurse jednom, ne dodaj rAF duplikat. Kontrolisani loss/restore test se vodi odvojeno od spontanih gubitaka u normalnom QA.
- Pri skrivanju taba zaustavi ili smanji nevidljivi rad u postojećoj petlji, ali real-time ekonomija ostaje tačna. Proveri resize/orijentaciju i povratak na mapu. Canvas 2D/SwiftShader ne dokazuju performanse fizičkog Android GPU-a.

## 7. SC-A07 — PL-01: layout i CSS-01

`InvalidateLayout` je normalna interna oznaka Chromiuma. ZABRANJENO je uklanjati funkciju ili resize zato što se pojavljuje u trace-u. Ispitati `boot → resize → Renderer.resize → rAF → Layout` i ostale pisce geometrije, razlikovati wall (`dur`) od CPU (`tdur`). Canvas width/height postaviti kada je potrebno; proveru istih dimenzija uvesti samo kontrolisanim patch-em koji ne kvari inicijalizaciju, DPR, hit-test ili fullscreen. Grupisati geometry read pre write, izbegavati read/write cikluse. Chrome forced-reflow insight cilja odsustvo forced reflow-a dužeg od 30 ms; nije zahtev da prirodni Layout nikad ne postoji.

CSS-01: preko 4.096 znakova Base64 image URI u custom property koja se koristi kroz `var()` za ponavljane/kritične background, mask ili content elemente zahteva obavezan pregled i ne sme se uvoditi kao podrazumevano rešenje. Preferiraj deljeni postojeći raster URL obuhvaćen SW; za single-HTML arhitekturu direktan statički `url(...)` u zajedničkom pravilu može biti opravdan. Sačuvaj boje/dimenzije kao male CSS tokene. Ne uklanjaj Grid/Flex, kartice, slike, senke ili animacije radi boljeg benchmarka. Jedan CSS `<style>` u v0.8.92 je dokumentovani cilj konsolidacije; proveri stanje v0.8.93, čuvaj kaskadu, redosled, media i keyframes. Ne vraćaj SVG ukrase u ovaj build bez odobrenog razloga i merenja; SVG nije univerzalno loš format. Ne tvrdi da Base64/var() znači ponovno dekodiranje po elementu bez dokaza.

A/B/R: baseline A → izolovani kandidat B → povratak R, rotirati redosled; isti uređaj, sejv, browser, GPU, DPR, viewport, cache/SW, sadržaj i uslovi. Meriti 20–30 ponavljanja po varijanti prema PL-01; p50/p95/max, input → naredni prikaz, CPU i wall, first visible frame, raster i long tasks. Bez merljive održive koristi ili uz regresiju: NO-CHANGE/rollback.

## 8. SC-A08 — PW-01, offline i release integritet

Jedan SW po scope-u. Deterministički i verzionisani inventar stvarnih shell resursa, sa proverom putanja, case-sensitivity, HTTP statusa, MIME i budžeta. Instalacija ne sme aktivirati nepotpun keš. Ne keširaj Supabase/API, private profile, save zahteve ili arbitrarne rute. Očisti samo sopstvene stare cache namespace-e, nikada IndexedDB. Update i rollback moraju ostaviti dosledan shell i napredak; ne dodaj drugi SW. Ne menjaj strategiju aktivacije bez provere otvorenih tabova i offline update-a.

Na HTTPS staging-u proveri online → stvarno offline → promena napretka → zatvori/relaunch → reconnect; isti `saveId`, očekivana `revision`, inventar, nivo i grafika. Force Stop/cold start na fizičkom Androidu je poseban scenario od uklanjanja iz recents. Testiraj neuspelu instalaciju, upgrade/rollback i nedostajući asset. `navigator.onLine` nije dovoljan dokaz mrežne dostupnosti. ZIP CRC, manifest, worker, HTML i deploy inventar moraju odgovarati; svaki CORE_PATH i manifest icon mora imati tačan fajl ili dokumentovanu i testiranu deploy transformaciju.

**Posebno otvoreno P0 za test-2 (24.11.2026):** `public/sw.js` i `public/manifest.webmanifest` traže `./img/icon-192.png`, `./img/icon-512.png`, `./img/icon-maskable.png`, dok pregledano Git stablo ima `public/icon-192.png`, `public/icon-512.png`, `public/icon-maskable.png` i nema `public/img/`. Bez deploy transformacije to može oboriti precache/MIME proveru i instalaciju SW. Ovo je potvrđeno statičko neslaganje, a ne dokazan kvar produkcije. Prvo proveriti staging HTTP odgovore i stvarnu instalaciju, zatim najmanju korekciju postojećeg inventara ili rasporeda fajlova uz PW-01. Ne uvoditi drugi SW niti brisati podatke. Nije popravljeno ovim dokumentom.

## 9. SC-A09 — Lokalni save, migracije, cloud i bezbednost

- IndexedDB je trajni lokalni sloj za postojeći PWA; cloud je odvojena opciona odgovornost. Ne mešaj origin-e i ne kreiraj tiho drugi profil kada IDB nije dostupan. `content://`/RAM-only režim mora jasno upozoriti na privremenost i odbiti cloud-save. Ne predstavljaj neuspešan upis kao uspešan.
- Validacija šeme, identiteta, tipova, granica, revizije i potrebnih polja pre upisa. Backup/checkpoint i poslednji validni snapshot sačuvati. Nevažeći current → validan backup kroz postojeći recovery; svi nevažeći → fail-closed, objašnjenje i izvoz/oporavak, bez automatskog prepisivanja praznim profilom.
- Testiraj IDB getter/open exception, abort, quota, dva taba, stariji save, import/export, konflikt cloud/lokalno, istek sesije, reconnect. Stari profil ne migrirati bez backup-a i proverene migracije. Koristi zaseban staging origin i namenski testni nalog. Nikada `Clear storage` na stvarnom korisničkom profilu kao popravku.
- Cloud: autorizacija mora biti server-side (npr. Supabase RLS gde se koristi), ograničena na vlasnika podataka, validacija na serveru, bez service-role ključa u klijentu ili logu. Konflikt revizije razrešiti po postojećoj politici uz vidljivu potvrdu kada je potrebna. Ne šalji stvarni save na testni backend. Loguj samo neophodne tehničke podatke, bez tokena i ličnih podataka. Ne uvodi raw HTML iz neproverenih ulaza.

## 10. SC-A10 — UI, pristupačnost, grafika i animacije

Cilj za primenljive UI tokove: WCAG 2.2 AA, ne deklarisana sertifikacija. Native dugmad i semantičke kontrole gde su izvodljive; jasna imena, keyboard fokus, vidljiv fokus koji nije zaklonjen, zatvaranje modala i vraćanje fokusa. Interaktivni cilj najmanje 24×24 CSS px uz WCAG izuzetke; za touch preferirati 44×44. Kontrast običnog teksta 4.5:1, velikog 3:1, relevantnih UI granica 3:1; ne oslanjati se samo na boju. Drag alternativa bez prevlačenja gde primenljivo; ne blokirati korisnički zoom cele stranice. `prefers-reduced-motion` smanjuje neobavezne efekte, ne uklanja povratnu informaciju ili funkcionalnost.

Prilagoditi postojeći UI različitim viewport-ima, safe-area, DPR, portrait/landscape; bez preklapanja, odsecanja ili duplih kontrola. Sačuvati srpsku/englesku lokalizaciju, hitbox, slojeve, stil, čitljivost i postojeće kontrole zvuka. Ne ubacivati nove art resurse bez razloga, licence/porekla i provere da postojeći nisu dovoljni. UI ne sme prikrivati stvarnu grešku lažnim loading-om ili placeholder-om.

Za grafiku: pokreni stvarni build u Chromium-u; snimi pre/posle isti kadar, state, zoom, viewport i DPR. Pixel-diff za cilj očuvanja izgleda; očekivane razlike namerne izmene obeležiti i pregledati. Za animaciju snimi realne frejmove u redosledu sa zabeleženim intervalom, sastavi GIF/video i prikaži kao „Pogledaj kretanje“. Ne generiši mock sliku kao dokaz. Ako nije moguće pokrenuti igru, označi vizuelni QA BLOKIRANO. Nema zamenskih simulacija bez zahteva vlasnika.

## 11. SC-A11 — Merljivi standardi performansi

| Metrika | Kriterijum / primena |
|---|---|
| INP | ≤200 ms, LCP ≤2,5 s, CLS ≤0,1: dobri Core Web Vitals pragovi na 75. percentilu stvarnih poseta, odvojeno mobile/desktop; lab nije field potvrda |
| Render | 30 FPS ≈33,3 ms/frejm; 60 FPS ≈16,7 ms/frejm, prema postojećem režimu i ciljnom uređaju. Prijaviti p95 i max, trajanje, dropped frames; ne samo prosek |
| Long task | >50 ms evidentirati i istražiti na kritičnom putu; ne tvrditi da je apsolutno svaki takav zadatak bug |
| Forced reflow | Chrome cilj: nijedan forced reflow >30 ms; izmeriti, ne uklanjati normalni layout |
| Startup | Prvi stvarno vidljivi kadar ostrva od navigacije; odvojiti JS submit, LCP, save read, shader/atlas i compositor prikaz |
| Stabilnost | Nema novih uncaught exceptions, nedostajućih obaveznih resursa, spontanih context loss-a ili funkcionalnih regresija u relevantnom testu |

Ovo su eksterni pragovi i projektni kriterijumi, ne tvrdnje o ostvarenim performansama. Za igru posebno izmeriti ulaz do vizuelnog odgovora, trajanje trke, GPU/teksturnu memoriju i 10-minutni stabilni scenario na ciljnom uređaju gde je relevantan. Poređenje mora imati iste uslove; optimizacija je neprihvatljiva ako uklanja sadržaj, smanjuje funkcionalnost ili pogoršava drugi kritičan tok. Android HONOR/Brave/Chrome test fizičkog uređaja obavezan za odgovarajuće mobilne release gate-ove; desktop emulacija nije zamena.

## 12. SC-A12 — Tri nezavisne provere pre brisanja

1. Statička: sve deklaracije i reference, dinamički generisane klase, akcije, migracije, manifest, asset URL-ovi i testovi.
2. Runtime: relevantni ekrani, interakcije, stanja, rezolucije, reload i migracioni putevi, ne samo trenutno otvoren ekran.
3. Vizuelna i funkcionalna regresija: isti kadar i pixel-diff gde je primenljivo, relevantni testovi i očuvan save. Ako bilo koji dokaz nedostaje — NO-CHANGE. Ne briši po nazivu `v147` ili po jednom profiler događaju.

Projektni presedan: uklonjeno šest `.map-controls` deklaracija tek nakon statičkog pregleda, runtime provere 26 ekrana u dva viewport-a i nula promenjenih piksela u testiranom kadru. Taj rezultat ne odobrava brisanje drugih CSS/JS delova.

## 13. SC-A13 — GameMaker/GML 2024+ (samo za stvarni GML port)

Aktivni PWA nije GML projekat. Ne ubacuj GML kod u HTML/JS i ne izmišljaj GameMaker sobe u web patch-u. Ako je zadatak pravi port, prvo identifikuj postojeće objekte, sobe, skripte i engine verziju. Format isporuke: potrebni objekti/sobe, pa GML po Create, Step, Draw/Draw GUI, Clean Up i drugim stvarno potrebnim event-ima.

- Centralni `global.game_data` je jedini autoritet za podatke igrača. Puž struct: `id, name, element, level, xp, speed, armor, attack, stamina, habitat_id`. Lokalni objekat ne čuva jedinu kopiju napretka.
- Persistent `obj_game_manager` koordinira `GAME_STATE { CITY, BREEDING, RACE, BATTLE }`; city UI je neaktivan u RACE/BATTLE. Proveriti ulaz/izlaz i event lifecycle; nema drugog managera.
- Real-time `date_current_datetime()` / `date_second_span()` uz validaciju i sačuvane timestamp-e; `alarm[]` nije autoritet za offline progres. Statistike trke/borbe izvedene iz struct-a.
- JSON save preko `json_stringify()` / `buffer_save()`; load sa `try...catch`, validacijom, backup-om i odgovarajućim sandbox putanjama. Novi profil kreirati ako je potvrđeno da prethodni fajl ne postoji; korumpiran ili nedostupan nije isto što i nepostojeći. Očuvaj validnu prethodnu kopiju.
- `instance_exists()` pre pristupa drugoj instanci; proveriti resurse (`surface_exists` itd.); osloboditi owned `ds_*`, surface i buffer resurse u Clean Up ili ranije prema životnom ciklusu, bez double-free. U Step/update logika, u Draw samo prikaz. QA stvarnim GameMaker runner-om na odobrenom target-u.

## 14. SC-A14 — Obavezna QA matrica i release gate

| Gate | Dokaz za prolaz | Blokira |
|---|---|---|
| G0 Identitet | verzija, commit/sha, origin, baseline, rollback | početak patch-a ako ne postoji pouzdan baseline |
| G1 Statički | syntax/build/lint postojeće konfiguracije, diff, SSOT/reference, inventar | review ako postoji greška |
| G2 Funkcionalni | pozitivan/negativan tok, input, stanje, reload, pogođene zavisnosti | prihvatanje patch-a |
| G3 Vizuelni | stvarni Chromium screenshot pre/posle; GIF realnih frejmova za animacije | grafičku izmenu |
| G4 Podaci/PW-01 | staging save/backup, offline/upgrade/reconnect, revision, bez gubitka | release, naročito P0 |
| G5 Performanse | ponovljena A/B/R merenja, isto stanje i oprema, bez regresije | optimizacioni patch |
| G6 Fizički uređaj | Android touch/portrait/landscape, stvarni GPU i offline, relevantan E2E | mobilni release |
| G7 Review | dokaz po stavci, otvoreni rizici, rollback i odobrenje vlasnika | merge/deploy |

Testirati relevantne slučajeve iz centralnog QA registra (ne kopirati ga kao novi registar). P0: gubitak sejva, pogrešan profil, dvostruka transakcija, blokiran boot/offline, sigurnost. P1: osnovne interakcije, grafika, pristupačnost, cloud, mobilna stabilnost. P2: odobrena poboljšanja bez kritične regresije. PASS = stvarno izvršen relevantan test sa dokazom. FAIL = reprodukovana greška. BLOCKED = uslov nedostaje. NIJE TESTIRANO / SIMULIRANO / DELIMIČNO / ODLOŽENO nisu PASS. Stariji PASS nije novi PASS. Ako relevantni P0 ili P1 gate nije prošao, nema odobrenja za produkciju; izolovani kandidat može se predati sa tačnim statusom.

## 15. SC-A15 — Radni protokol i izveštaj (obavezan obrazac)

**PRE RADA**:  
Zadatak i granice: …  
Potrebni rezultati i kriterijumi: …  
Repo/grana/commit/hash/origin: …  
Nedostaje: …  
Postojeći vlasnik i čitaoci/pisci: …  
Način, alat, princip, rizik i rollback: …

**PRE TESTA**: minimalni diff i njegova svrha; postojeće funkcije i negativni slučajevi; dokazi pre izmene; kontrolisani testni profil; spisak gate-ova. Ne izmišljaj pristup, screenshot, terminal, browser, commit, metriku ili izlaz komande.

**POSLE RADA**:

| ID / rezultat | Status | Test i dokaz / blokada |
|---|---|---|
| … | URAĐENO / DELIMIČNO / NIJE URAĐENO | putanja, screenshot/log, očekivano vs. stvarno |

Za svaki test: datum/vreme/zona, ID, verzija/commit, uređaj/OS/browser, renderer/GPU, viewport/DPR, origin i režim mreže, testni saveId/revision, priprema i koraci, očekivano/stvarno, PASS/FAIL/BLOCKED, dokaz, eventualna prijava. Bez tajnih podataka. Zaključak: izmenjeni fajlovi, šta nije dirano, otvoreni rizici i odluka PRIHVATI KANDIDAT / ZADRŽI ZA QA / ROLLBACK / NO-CHANGE. Bez nepotrebnog prepričavanja. Tri projektna prolaza (pre rada, pre testa, pre release-a) nisu automatske izmene igre.

## 16. Provereni projektni izvori i poreklo

GitHub pristup potvrđen 24.11.2026; čitana dokumentacija, SW i manifest, pregledano Git stablo. Nije izvršena igra u ovoj sesiji. `public/index.html` v0.8.93 identifikovan u stablu (7.225.560 B), sadržaj nije pouzdano vraćen pri pokušaju čitanja velikog fajla; ne tvrdimo da su svi simboli ili CSS audit potvrđeni u 0.8.93.

- [AGENTS.md](https://github.com/tihidon/snail-city-test/blob/main/AGENTS.md) — PL-01, CSS-01, radni protokol (blob `d48d54ec3077140a7a272d829fafa340393ddc5f`).
- [SSOT](https://github.com/tihidon/snail-city-test/blob/main/docs/tehnika/standardi/PRAVILO-JEDAN-IZVOR-ISTINE.md) — vlasnici, tok i zabrana paralelnih autoriteta.
- [PL-01/CSS-01](https://github.com/tihidon/snail-city-test/blob/main/docs/tehnika/standardi/SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md) — merenje, prag, rollback (blob `836a95e50ef9faf44ba5c5f90c4f3648031e0d7a`).
- [SC-BRISANJE-3-PROVERE](https://github.com/tihidon/snail-city-test/blob/main/docs/tehnika/standardi/SC-BRISANJE-3-PROVERE.md) — presedan bezbednog brisanja.
- [PW-01 stabilna 0.8.90](https://github.com/tihidon/snail-city-test/blob/main/docs/tehnika/pwa-offline/SC-v0.8.90-STABLE-PW01-ANDROID.md) — granice dokaza i release gate.
- [Centralni QA registar](https://github.com/tihidon/snail-city-test/blob/main/docs/analize/qa/SC-OTVORENE-STAVKE-ZA-TESTIRANJE-v0.8.87.md) — save, cloud i testni protokol.
- [Sinteza 24.11.2026](https://github.com/tihidon/snail-city-test/blob/main/docs/SAZETAK-I-ODLUKE-2026-11-24.md) i [docs indeks](https://github.com/tihidon/snail-city-test/blob/main/docs/README.md) — status i istorijske razlike. Tree `4110a573c52dfae51cd834d5d50f6ad842d9b343`.
- [test-2 CSS P1 audit 0.8.92](https://github.com/tihidon/test-2/blob/main/SC-v0.8.92-P1-CSS-SINGLE-SOURCE-AUDIT.md) — izolovani kandidat, ne produkcioni PASS.
- [test-2 SW](https://github.com/tihidon/test-2/blob/main/public/sw.js), [manifest](https://github.com/tihidon/test-2/blob/main/public/manifest.webmanifest), [stablo](https://github.com/tihidon/test-2/tree/main/public) — tree `3192595507782fe6682d8561a31adddd2b400e8c`, SW blob `a9efddc8bca68ea15d8bf9255593487bde6f2645`, HTML blob `96805d08148be75189dd1c4a19d4f75f468620df`. Git tree SHA nije commit SHA.
- Projektna uputstva vlasnika: GML arhitektura, praktičnost, stvarni render, GIF i završni statusi. GML odeljak važi uslovno, nije tvrdnja o postojećem GML projektu.

## 17. Aktuelni eksterni tehnički izvori

Provereni web izvori 24.11.2026. Primenjivati prema postojećem browser/engine target-u; pre novog API-ja proveriti kompatibilnost, ne uvoditi promenu samo zato što je moderna.

- [Google Chrome Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance) — agent mora konsultovati relevantne smernice za konkretan zahvat.
- [MDN WebGL best practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices) — GPU resursi, sinhroni pozivi, batching, context i budžet.
- [Chrome forced reflow](https://developer.chrome.com/docs/performance/insights/forced-reflow) — read/write i prag 30 ms.
- [web.dev Core Web Vitals](https://web.dev/articles/vitals) — INP/LCP/CLS i 75. percentil.
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) — primenljiva pristupačnost AA.
- [MDN Service Worker](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers) — lifecycle i offline arhitektura.

**Obavezna primena:** agent mora navesti konkretan izvor i kriterijum koji je primenio. Tehnički savet, automatizovani lint, simulacija i tekstualni game-brief checker nisu dokaz funkcionalnosti. Ako alat nema pristup realnom okruženju, ne sme tvrditi da je implementacija verifikovana.
