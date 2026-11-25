# Snail City · Zašto kasni prvo otvaranje prodavnice

23. novembar 2026. · Analiza po PL‑01 · Build iz snimka 0.8.90-p1-startup-probe. SHA-256 izvornog HTML-a je 43b67c0fb601fd751082e0a71cb81b678aaf976d66458821a3c955f20be14daf.

## Obuhvat i kontrole

Prvi dodir zgrade na mapi, početni sejv, kartica Jaja. Svaki red tabele obuhvata tri zasebna starta Chromium procesa. Redosled varijanti rotira se između ponavljanja. Isti lokalni HTML, 360 × 697, DPR 3, visok kvalitet, WebGL 1 preko SwiftShader-a. Servisni radnik i spoljna mreža blokirani, lokalni server isporučuje HTML. Posle dodira provereni su naslov i broj kartica. A i R pokreću identičan instrumentirani kod. R je kontrola sa vraćenim kodom u novom procesu.

Trajanje je Chromium Event Timing za pointerup do sledećeg prikaza, zaokruženo od strane pregledača. Click istog dodira se ne sabira. JS kolona meri sinhroni poziv shop(s,view,now). Obrada obuhvata ceo pointerup. Ostatak je procena od kraja obrade do sledećeg prikaza i obuhvata sav rad i čekanje u tom intervalu. Merenje ne razdvaja stil, raspored, raster, kompoziciju i čekanje na sledeći kadar.

| Serija | Izolovana promena | Tri dodira (ms) | Medijana (ms) | shop JS, med. (ms) | Obrada pointerup, med. (ms) | Posle obrade, med. (ms) |
|---|---|---|---:|---:|---:|---:|
| deep | Izvorna kontrola | 1112, 896, 920 | 920 | 2.5 | 45.1 | 865.2 |
| deep | Vraćena kontrola | 936, 976, 936 | 936 | 2.4 | 41.7 | 880.3 |
| deep | Skrivena mreža jaja, raspored zadržan | 824, 664, 592 | 664 | 3.1 | 47.9 | 567.8 |
| deep | Ugašene pozadinske slike kartica i potomaka | 608, 640, 712 | 640 | 2.4 | 36.3 | 581.5 |
| svg | Izvorna kontrola | 1032, 904, 960 | 960 | 2.3 | 44.0 | 905.5 |
| svg | botanical-corner | 912, 856, 824 | 856 | 3.7 | 34.5 | 798.2 |
| svg | wood-banner | 976, 912, 984 | 976 | 2.2 | 46.7 | 904.6 |
| svg | egg-pedestal | 872, 840, 864 | 864 | 2.8 | 44.7 | 805.4 |
| svg | xp-ribbon | 904, 984, 888 | 904 | 2.7 | 36.9 | 836.2 |
| svg | portrait-meadow | 960, 1144, 888 | 960 | 3.0 | 51.9 | 895.5 |
| svg | Vraćena kontrola | 904, 888, 824 | 888 | 2.3 | 38.6 | 812.5 |
| preserve | Izvorna kontrola | 920, 888, 824 | 888 | 2.6 | 42.0 | 820.1 |
| preserve | Četiri ukrasna SVG resursa zamenjena PNG-om 2× | 432, 416, 416 | 416 | 2.8 | 130.1 | 285.7 |
| preserve | Promenjena CSS klasa tela prodavnice | 368, 376, 368 | 368 | 3.5 | 34.6 | 318.8 |
| preserve | Vraćena kontrola | 888, 848, 880 | 880 | 2.6 | 47.1 | 823.2 |

## Nalazi i kontradikcije

1. **Obračun postoji.** U index.html:5768 funkcija shop bira granu po aktivnoj kartici. Na kartici Jaja za svaku od osam kartica računa hatchExperience, a izraz incubatorUsed(s) >= eggCapacity(s) izvršava još jednom posle petlje, ukupno devet puta. U proveri popunjenosti prolazi se kroz jaja. To je konkretno ponavljanje koje se može izvući ispred petlje. Ceo sinhroni shop na šest početnih kontrola traje 2,0–3,4 ms. Čak i potpuno uklanjanje tog rada objašnjava svega nekoliko milisekundi na ovom sejvu. Grana Market ima svoj rate(s,now) i getSeason(s,now). Ovaj dodir otvara Jaja i preskače tu granu.
2. **Vidljivost kartica menja ishod.** Posle skrivanja mreže svih osam kartica ostaje u DOM-u. Medijana je 664 ms. Samo gašenje pozadinskih slika na karticama daje 640 ms naspram 920 i 936 ms za kontrole. Rasponi se u ovoj seriji razdvajaju. Ipak ostaje preko pola sekunde čekanja. Efekti se preklapaju i njihove uštede se ne sabiraju.
3. **Jedna dekoracija i cela grupa daju različite probe.** Pojedinačno gašenje CSS promenljive deluje samo na potomke tela prodavnice. Zaglavlje je izvan tog tela (wrap, linija 6381). Zato test wood-banner ne isključuje odgovarajući baner u zaglavlju. Portrait-meadow služi kao kontrola opsega. Grupna proba ukida i gradijente tamo gde su zadati kao background-image. Njen rezultat sam po sebi ne izdvaja SVG dekoder.
4. **Promena formata i promena stila imaju različit obuhvat.** PNG proba rasterizuje četiri originalna ukrasa na 192 dpi i postavlja promenljive na ceo panel. Menja veličinu HTML-a i način dekodiranja. Proba styleScope menja samo ključ prosleđen funkciji wrap za prodavnicu, pa menja više CSS pravila i moguće geometriju kartica. Osam kartica i naslov potvrđuju otvaranje. Vizuelna jednakost, čitljivost i kupovina nisu proverene za te probne varijante.
5. **Dva zastoja imaju različit dokaz.** Layout od oko 401 ms u ranijem korisnikovom snimku pripada pokretanju igre. Ovde je reprodukovan kasniji dodir prodavnice. Zajednički uzrok zahteva trag istog dodira. Softverski WebGL i svež sejv ograničavaju prenos nalaza na HONOR sa Adreno 610, veći sejv i ostale kartice.
6. **Odluka po PL‑01.** Najjači ponovljiv efekat početne serije daje promena prikaza kartica. Izolovana proba skriva ili menja sadržaj i sama ne ispunjava uslove za izdanje. Sledeća potvrda uzroka traži vremensku korelaciju od pointerup preko umetanja panela do rasterizacije i prezentacije kadra na telefonu, sa identičnim sejvom i vraćenom kontrolom. Produkcijski kod, canvas dimenzije i pravila invalidacije nisu menjani.

## Provera zamene grafike uz zadržavanje sadržaja

- Izvorna kontrola — medijana 888 ms.
- Četiri ukrasna SVG resursa zamenjena PNG-om 2× — medijana 416 ms.
- Promenjena CSS klasa tela prodavnice — medijana 368 ms.
- Vraćena kontrola — medijana 880 ms.

Datoteke sva četiri PNG ukrasa sadrže vidljive piksele. Ukupno imaju 325.234 bajta pre base64 kodiranja. Pojedinačno gašenje postolja daje medijanu 864 ms, između početne kontrole od 960 ms i donjeg dela raspona vraćene kontrole (824–904 ms). Ni taj rezultat ni gašenje jednog drugog ukrasa ne identifikuju jednog krivca. Grupna zamena formata izdvaja četiri ukrasa kao kandidata za optimizaciju. Za odluku o isporuci treba proveriti izgled, hladno pokretanje i offline povratak.
