# Snail City · P1 izolacija zastoja pri pokretanju

**23.11.2026. · Odluka po PL‑01 · Nijedna probna izmena nema dovoljno dokaza za spajanje.**

U dostavljenom snimku glavni zastoj je Chromeov puni `Layout` od **400,896 ms proteklog vremena i 70,061 ms CPU vremena niti**. Lokalni pokušaj u čistom Chromiumu nije ponovio taj ekstrem. Tri probne promene nisu pokazale dosledno ubrzanje prvog vidljivog kadra preko obe identične kontrole. Najjači kodni trag za dalje profilisanje je dekodiranje grafike na kritičnom putu pre prvog rendera.

## 1. Forenzika stvarnog snimka

Izvršni `index.html` je izvučen iz `metadata.resources[0].content` korisnikovog trace-a. Sadržaj se podudara bajt za bajt sa HTML-om preuzetim sa referentnog Netlify domena. Repozitorijum se koristi za projektna pravila i prethodni nalaz. Linije ispod pripadaju HTML-u iz trace-a.

- Trace SHA‑256 `bb73ddf95d671f43b3f0eafab9b09564f1ba2f5fbcacd07acfe4770ebd83da48`.
- HTML SHA‑256 `43b67c0fb601fd751082e0a71cb81b678aaf976d66458821a3c955f20be14daf`.
- Reprodukovan je build `0.8.90-p1-startup-probe`. Referentni trace sadrži 90.182 događaja. Glavna nit renderera ima PID 27204 i TID 11144. Vremena su relativna na `navigationStart` (ts 6771436523 µs).

| Od navigacije | Nivo | Utvrđeno |
|---:|---|---|
| 766,67 ms | Navigacija | Renderer beleži odgovor za dokument iz Service Workera. Razlog za ceo interval od početka navigacije do te oznake nije izolovan. |
| 980,93 ms | JS eval | `EvaluateScript` glavnog skripta traje 65,50 ms, uz 56,20 ms CPU vremena niti. |
| 1.022,10–1.306,10 ms | Boot i I/O | `boot:8252` pokreće sejv, atlas ostrva i ilustraciju. `Promise.all` nastavlja kad su sve tri grane gotove. Ilustracija i njene teksture poslednje ispunjavaju uslov u ovom snimku. |
| 1.307,75 ms | DOM geometrija | Posle `applyTheme:7002`, čitanje `stage.getBoundingClientRect()` u `resize:7189` vezano je za `UpdateLayoutTree` od oko 0,62 ms. |
| 1.315,79 ms | Canvas | `boot:8324 → resize:7192 → Renderer.resize:3901` invalidira raspored prilikom inicijalizacije drawing buffera. |
| 1.346,20 ms | UI | `boot:8331` sakriva overlay i skida klasu `booting`. CSS tom klasom skriva više UI grupa. U tom putu nema tajmera koji namerno zadržava logo posle spremnosti. |
| 1.356,20 ms | JS crtanje | `loop:7321 → paintMap:4611 → canvas.firstSubmittedFrame:7372`. Ceo prvi JS callback ima oko 5,72 ms. |
| 1.357,83 ms | DOM | Beleži se još jedan `InvalidateLayout` bez JS steka, **42,04 ms posle** događaja sa stekom za Canvas. |
| 1.358,32–1.759,22 ms | Chromium layout | `Layout` nad celim dokumentom, 86/86 objekata označeno za raspored. `RunTask` traje 412,928 ms, od toga Chrome beleži 81,212 ms CPU vremena niti. Udeo samog `Layout` događaja je oko 97% proteklog vremena tog zadatka. |
| 1.488,46 → 1.802,71 ms | Vidljiv kadar | Raniji sačuvani Chrome screenshot još pokazuje logo. Na narednom sačuvanom screenshotu vidi se ostrvo, oko **446,51 ms** posle JS submit markera. |

**Uzročnost.** Canvas upis ima potvrđen invalidacioni stek. Zajedno sa promenom teme, hidratacijom DOM-a, skidanjem overlaya i kasnijom invalidacijom on ostaje jedan od kandidata za okidač rasporeda. Trace daje oko **330,835 ms razlike** između proteklog i CPU vremena tog `Layout` događaja, bez dovoljne atribucije čekanja. U snimku ima i izvršavanja Chrome ekstenzija, ali njihov uticaj na konkretnih 401 ms nije utvrđen. Čitanje geometrije dešava se pre dugog `Layout` događaja, koji nastaje u obradi frame-a posle prvog JS crtanja.

### Grafika i sejv pre prvog kadra

| Grana | Funkcija | `texImage2D` interval | Ugnježdeni `Decode Image` wall / CPU |
|---|---|---:|---:|
| Atlas ostrva | `Renderer.preload → upload` | 75,70 ms | 61,52 / 59,49 ms |
| Ilustracija ostrva | `preloadIllustratedMap → uploadIllustratedMap` | 38,50 ms | 27,51 / 26,54 ms |
| Dnevno nebo | `preloadIllustratedMap → uploadSky → upload` | 17,10 ms | 6,68 / 6,44 ms |
| Noćno nebo | Isti lanac za noć | 10,30 ms | 7,55 / 7,29 ms |
| Odvojeni objekti | `preloadIllustratedMap → uploadDetachedAtlas` | 51,00 ms | 42,53 / 40,37 ms |

Pet dekodiranja ima oko **140,13 ms CPU vremena niti**. Dekodiranje je ugnježdeno unutar izmerenih JS poziva za upload, pa se ta vremena ne sabiraju sa intervalima `texImage2D`. Izmera tih poziva takođe ne meri završetak rada GPU-a. IndexedDB transakcija je trajala oko 151,6 ms proteklog vremena, uz oko 2,6 ms validacije trenutnog zapisa. Završila se pre grafičke grane, pa u ovom uzorku nije poslednja zadržala `Promise.all`.

## 2. Kontrolisani eksperimenti

Korišćen je Chromium 151.0.7922.34, bez ekstenzija, sa WebGL 1 preko SwiftShadera, 772 × 731 CSS px i DPR 1, preko lokalnih HTTP origin-a. Svaki start ima nov browser kontekst i novi sejv. Service Worker je isključen samo u vremenskim serijama, uz zasebnu proveru offline ponašanja. Redosled varijanti je rotiran po bloku, pa obrnut u svakom drugom ciklusu. Prva serija ima **20 × 5 CDP trace-ova**. Druga ima **20 × 5 Chromium screencast startova**, od kojih je na 99 zabeleženo ostrvo u prozoru snimanja.

| Varijanta | Tačna lokalna promena |
|---|---|
| **A · Original** | HTML iz trace-a. |
| **B · Izostavljanje identičnog upisa** | Samo u `Renderer.resize:3901` upisati svaku osu drawing buffera ako se njena izračunata vrednost razlikuje od atributa. Početne i dalje potrebne dimenzije se upisuju. |
| **R · Vraćanje** | Vraćen originalni kod bajt za bajt. Poseban lokalni origin i isti uslovi kao A. Kontrola pokazuje i varijaciju koju daje sam test. |
| **C · Raniji drawing buffer** | Jedan rani poziv `renderer.resize` odmah posle stvaranja `SceneManager`, pre preloada. Redovni `resize()` ostaje u boot hidrataciji i zadržava proveru nove geometrije. Kod ne briše nijednu osu. |
| **D · Uslovni dev UI** | Izostaviti samo eksplicitni početni `renderDev()` kada je dev panel zatvoren. Otvaranje panela zadržava svoju regularnu funkciju. Ovo je dijagnostička proba za deo DOM hidratacije. |

### Vremena p50 / p95 / maksimum u milisekundama

| Varijanta | Prvi JS submit (CDP) | Prvo zabeleženo ostrvo (screencast) | Layout uz prvi submit, wall | Layout uz prvi submit, CPU | Broj Layout-a p50 |
|---|---:|---:|---:|---:|---:|
| A | 640,50 / 1.143,45 / 1.210,25 | 702,59 / 898,26 / 898,26 | 26,71 / 40,17 / 61,56 | 8,56 / 11,15 / 15,14 | 3 |
| B | 658,61 / 912,87 / 998,62 | 691,54 / 863,89 / 912,39 | 28,11 / 47,51 / 48,20 | 8,41 / 13,84 / 16,00 | 3 |
| R | 680,51 / 803,05 / 950,19 | 689,70 / 906,35 / 965,91 | 26,29 / 33,25 / 36,97 | 8,86 / 10,04 / 11,06 | 3 |
| C | 664,71 / 715,94 / 848,60 | 693,79 / 887,13 / 1.039,69 | 26,55 / 30,93 / 31,59 | 8,71 / 10,61 / 11,47 | 4 |
| D | 660,38 / 896,89 / 987,29 | 684,39 / 789,74 / 1.166,84 | 27,11 / 33,46 / 51,64 | 8,46 / 12,13 / 14,98 | 3 |

Za p95 je uzet najbliži viši rang. `Layout uz prvi submit` je prvi takav događaj koji počinje u intervalu od 0 do 18 ms od JS markera na istoj niti. U mernoj seriji svi startovi zadovoljavaju taj kriterijum. Screencast kadar određen je poređenjem centralnog dela ostrva sa referentnim stvarnim kadrom. Za A nedostaje jedan kadar i statistika prikaza koristi 19 startova. To je vreme najranijeg uhvaćenog kadra sa ostrvom. CDP i screencast serije imaju nezavisne uzorke.

- **Kontrola A/R.** Dva identična HTML-a dala su razliku od oko 340 ms u p95 prvog JS submit-a u CDP seriji. Najveći lokalni `Layout` iznosi 61,56 ms. Lokalna merenja ne reprodukuju izvorni ekstrem i ne određuju njegov uzrok.
- **B odbačen za P1 startup.** Prvi upis u desktop probama i dalje menja obe ose. Medijana prvog submit-a je sporija od A, a medijana vidljivog kadra je malo sporija od R. Treba razlikovati potencijal uklanjanja viška upisa pri promeni jedne ose od ovog zastoja na boot-u.
- **C odbačen.** Dobit u p95 JS submit-a uz C prati dodatni `Layout` i dodatna invalidacija u tipičnom startu. Ostrvo se u uparenim blokovima pojavilo ranije od A u 10 od 19 validnih parova, dok je najsporiji vidljivi kadar C gori od obe kontrole.
- **D odbačen.** Uparen prvi vidljivi kadar je kasniji za 8,67 ms na medijani i sporiji od A u 11 od 19 uparenih prolaza. Početni `renderDev()` ima i zasebne obaveze za atribute kontrolnog dugmeta.
- **Long tasks.** U mernom prozoru bilo je 105/99/104/99/97 zadataka od najmanje 50 ms za A/B/R/C/D. Najduži zadaci bili su 229,16/164,45/142,96/155,75/164,25 ms. Ovi maksimumi ne služe za pripisivanje uzroka promeni, što pokazuje raspon A/R kontrole.

## 3. Izolacija dodira posle trke

Ranijih 283–300 ms u `v174` na `map · tap+render` ostaje broj iz drugog builda i uređaja. Dostavljeni startup trace sadrži jedan desktop klik sa 16,34 ms do narednog prikaza. Zato sam na P1 buildu odvojeno ponovio tok trka → napuštanje → mapa → tap na zgradu Prodavnice, posle 15 rAF poziva. Otvaranje Prodavnice je potvrđeno naslovom prikazanog panela. Korišćen je stvarni Chromium touchscreen input u emuliranom portretu 360 × 697, DPR uređaja 3 i kvalitet High. Svaki prolaz je nov browser kontekst.

| Prolaz | Prvo otvaranje Prodavnice | Do sledećeg prikaza | Obrada `pointerup` | Ostatak posle obrade do prikaza |
|---|---|---:|---:|---:|
| WebGL 1, početna proba | posle meadow | 752 ms | 31,6 ms | nije izvezeno |
| WebGL 1, sa trace-om | posle meadow | 880 ms | 31,3 ms | 834,5 ms |
| Canvas 2D, WebGL ugašen u lokalnom Chromiumu | posle meadow | 1.104 ms | 51,1 ms | 1.036,9 ms |
| WebGL 1 vraćen | posle meadow | 848 ms | 29,3 ms | 806,5 ms |
| WebGL 1, obrnut redosled trka | posle cosmos | 912 ms | 33,1 ms | 864,8 ms |
| WebGL 1, ista Prodavnica otvorena pre bilo koje trke | pre trke | 896 ms | 39,8 ms | 841,8 ms |

U poslednjem prolazu svi dodiri Prodavnice posle trka iznosili su **64–128 ms**, prvi posle meadow **88 ms**. Ranije zabeleženi hit nakon izlaska sa cave bio je 728 ms u jednom prolazu, uz 708 ms posle obrade događaja. Naredni WebGL prolazi na cave beleže 80–88 ms. Veza sa hladnim otvaranjem Prodavnice ponovljena je sa promenjenom stazom i bez trke, uz odvojene povremene zastoje na toplim otvaranjima. Canvas 2D zadržava browser kompoziciju i u ovoj probi takođe ima ekstrem.

### Šta se zadržava i gde

1. **Povratak na mapu.** `controls('return-map') → returnMap:7283 → sceneManager.activate → schedule → loop → paintMap`. U glavnoj WebGL seriji prvi rAF posle povratka je 8,3–13,9 ms, CPU crtanje mape 0,1–0,3 ms, a koristi se isti canvas i drawing buffer. Kasniji razmaci između kadrova povremeno su visoki i odvojeni su od CPU cene prvog crtanja. Ukupan broj otpuštanja teksture izvezen iz `SceneManager` je nula u ovim kratkim sekvencama. Njegov prvi tajmer za čišćenje počinje sa odlaganjem od 1.500 ms posle crtanja mape.
2. **Sinhrona obrada dodira.** `attachInput:7444 → pointerup:7503 → mapTap:7402 → openScreen:7033 → renderPanel:6390 → showSheet:7014`. Otvaranje pravi sadržaj panela, primenjuje i18n, prikazuje dijalog i postavlja `scrollTop`. U glavnoj hladnoj WebGL probi CDP beleži **31,27 ms** u `EventDispatch(pointerup)`, uključujući **15,41 ms `UpdateLayoutTree`** i **9,80 ms `Layout`**. Ti događaji se nalaze unutar istog vremena obrade.
3. **Posle obrade.** U toj probi renderer šalje rad, a interval posle obrade se poklapa sa `GPUTask` od **817,36 ms wall / 227,80 ms CPU niti** u drugom procesu. Pri Canvas 2D probi postoji `GPUTask` od **1.018,82 ms wall / 233,67 ms CPU niti**. Pri vraćenom WebGL-u taj događaj traje **793,39 ms wall / 238,14 ms CPU niti**. Pri otvaranju pre trke najduži pojedinačni `GPUTask` je 439,67 ms wall / 100,50 ms CPU niti. Poklapanje vremenski lokalizuje znatan deo čekanja. Oznake u snimku ne identifikuju pojedinačnu operaciju unutar tih zadataka.

`PerformanceEventTiming.duration` je zaokruženo trajanje do sledećeg prikaza. Ostatak u tabeli je `startTime + duration − processingEnd`, pa je približan. Chrome headless softverski GPU i skripta za test mogu uticati na apsolutne vrednosti. Rezultat izoluje slučaj u P1 i daje uzrok za dalji test prikaza panela. Isti brojevi i isti mehanizam za raniji Android zastoj ostaju nepotvrđeni.

## 4. Regresije u lokalnom Chromiumu

Svaka varijanta je zasebno otvorena online, sa jednim registrovanim SW scope-om i sedam stavki u precache-u. Kroz korisnički interfejs ispražnjen je rezervoar i potvrđeno je povećanje revizije sejva za 1. Zatvorena je kartica, kontekst je prebačen offline i otvorena je nova kartica. Za svih pet varijanti navigacioni odgovor stigao je iz Service Workera, ostrvo se iscrtalo i `saveId/revision/level` ostali su identični poslednjem upisanom testnom sejvu (revizija 1, nivo 1).

| Provera | Rezultat |
|---|---|
| Portret, uređaj emuliran sa DPR 3, kvalitet Eco | PASS · canvas 360 × 697 |
| Portret, kvalitet High (interni limit DPR 1,5) | PASS · canvas 540 × 1.046 |
| Promena samo širine u High, 360 → 410 CSS px | PASS · canvas 615 × 1.046. A i R upisuju i visinu 1.046 → 1.046. B upisuje samo širinu 540 → 615. |
| Landscape, 697 × 360 CSS px, High | PASS · canvas 1.046 × 540. Uspešno vraćen portret. |
| Prvi upisi u C | PASS kao provera eksperimenta · širina i visina upisuju se pre `boot.rendererReady` i pre završetka preloada. U A i R oba upisa su posle `boot.parallelTasksComplete`. |
| Otvaranje i napuštanje trke u offline testnoj kopiji | PASS · svih pet staza (meadow, forest, cave, meadow2, cosmos), u svih pet varijanti. Povratak koristi isti canvas. |
| WebGL događaji i JS greške | PASS · 0 spontanih gubitaka ili obnova konteksta i 0 neuhvaćenih page error-a u toj lokalnoj proveri. |
| Pristupačnost dev prekidača, stanje pri boot-u | FAIL za D · `aria-label` je „Testing tools“, dok A/B/R/C imaju „Otvori alate za testiranje“ u istom engleskom browser kontekstu. Promena je posledica preskočenog `renderDev()`. |
| Uređaj HONOR ABR‑L31, realan GPU i Android PWA | Otvoreno · lokalna emulacija koristi drugi GPU i drugi OS. |
| Produžen test stabilnosti 30/60 FPS, završetak trke i dodela nagrade | Nije obuhvaćeno ovom izolacijom. Test ulaska, prvog rendera i napuštanja trke ima uži opseg. |

PWA provera koristi worker preuzet sa istog P1 domena, sa cache imenom `snail-city-shell-0.8.90-p1-probe-r1`. SHA‑256 workera je `707cb33e39dbfb12e06812b9cc1c684396786ce737b0b13069c821c367979784`. Trke su otvarane iz RAM testne kopije na nivou 3 i kroz uobičajene kontrole, uključujući izbor mesta za gradnju Trkališta i normalan taster za izlaz.

## 5. Odluka i preostali dokaz

- **P1 startup · DOKAZAN događaj, otvoren uzrok ekstrema.** Nijedna od tri probe nema dovoljno dokaza za produkcioni patch. Guard B ostaje odvojiva hipoteza za resize samo jedne ose. Vrednost tog guarda za UX treba meriti u scenariju promene širine/visine.
- **Dodir Prodavnice · lokalno ponovljen.** Hladno otvaranje Prodavnice ima najveću cenu posle obrade `pointerup`. Za sledeću usku probu prvo profilisati hladni `showSheet` na fizičkom Android uređaju i uporediti direktan tap na zgradu, otvaranje iste Prodavnice kroz meni i tap u praznu mapu. Odvojeno meriti layout unutar handlera i čekanje na prezentaciju.
- **Kritični put grafike.** Prvi odvojeni kandidat iz ovog nalaza je pomeranje dekodiranja i uploada samo onog neba koje prvi kadar ne koristi. `paintMap` bira dnevno/noćno nebo prema stanju igre, pa kandidat mora očuvati prvi kadar, prelaz dana/noći i obnovu konteksta. Postojeći trace potvrđuje CPU rad obe grane. Nema izmerenog dobitka od tog kandidata.
- **Raspoređivanje CPU niti.** Za objašnjenje razlike wall/CPU u događaju od 401 ms treba ponoviti A/R na izvornom uređaju sa čistim profilom i istim viewport-om, a uz novi ekstrem prikupiti podatke o raspoređivanju niti i koegzistirajućem radu browsera/GPU-a. Trace koji ovde postoji ne daje takvu atribuciju.
- **DeepSeek.** Spoljni DeepSeek pregled nije izvršen. Analiza se oslanja na izvorni trace, izvršni HTML, CDP, stvarne Chromium kadrove i lokalne testove.
- **GitHub i Netlify.** Promene su izvršene samo na lokalnim kopijama za probe. Zaključak PL‑01 je bez izmene stabilne verzije.

### Izvori i prilozi

- [Projekat · AGENTS.md](https://github.com/tihidon/snail-city-test/blob/main/AGENTS.md)
- [Projekat · PL‑01](https://github.com/tihidon/snail-city-test/blob/main/docs/SC-PL-01-LAYOUT-INVALIDATION-REVIEW-STANDARD.md)
- [Projekat · prethodni forenzički zapis](https://github.com/tihidon/snail-city-test/blob/main/docs/SC-v0.8.90-P1-CHROME-TRACE-FUNCTION-ROOT-CAUSE.md)
- [Chrome DevTools · Performance Insights](https://developer.chrome.com/blog/devtools-insights-sidebar)
- [MDN · PerformanceEventTiming](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceEventTiming)
- [MDN · HTMLCanvasElement.width](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/width)
- `Snail-City-P1-mere-po-startu.csv` ima 200 redova merenja prikazanih serija.
- `Snail-City-P1-dokaz-kadrova.png` prikazuje dva kadra iz korisnikovog trace-a i po jedan kadar lokalnih varijanti A i C.
