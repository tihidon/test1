# SC-DEC-01 — lanac pouzdanog odlučivanja

Status: kandidat za CI i nezavisnu evaluaciju; vlasnik odobrio nadogradnju. Baseline 9d638c4730caf63c02e2c01397a1eea96f2197eb. Dodatak SC-REL-01, SC-QA-02, SC-AGENT-01, PL-01, PW-01; ne zamenjuje nijedan gate. Jedan decision record po zadatku; dva specijalistička skilla primenjuju postojeći D0–D8 proces.

## Predaja nalaza i odluka

Handoff pokazuje postojeći zapis zadatka sa odobrenim opsegom, tačnim commitom ili buildom, izvršiocima, relevantnim diffom, odlukama i dostupnim dokazima. Za bezbednosni ili etički nalaz koristi polja i pragove iz [SC-BEH-01](SC-BEH-01-PONASANJE-AGENATA.md). Zabeleži odvojene zaključke auditora i QA, neslaganje i ciljnu proveru. Status provere i odluka vlasnika o merge/deploy vode se odvojeno. D7 povezuje internu proveru sa originalnim dokazima.

## D0–D8
- D0 Engineering: zamrzni zahtev, scope, baseline SHA, candidate plan, nezavisni oracle i required gates pre izmena. Za dirty tree zabeleži diff/hash; ne tvrdi clean commit identity za lokalne izmene.
- D1 Engineering: pročitaj stvarno telo, pozivaoce i dinamičke ivice, state reads/writes, lifecycle, ugovor i odobrena pravila. Razlikuj OBSERVED, HYPOTHESIS, PROVEN. Dokumentacija ne dokazuje runtime.
- D2 QA: stvarna korisnička akcija, izolovan profil, identity HTML/SW, scenario, očekivano i stvarno stanje; sačuvaj raw evidence. Ako reprodukcija nije uspela, NO-CHANGE ili ZADRŽI ZA QA, ne izmišljaj fix.
- D3 Engineering+QA: najmanje jedna falsifikabilna hipoteza i alternativno objašnjenje; unapred definiši šta bi oborilo hipotezu. Za texture upload odvojiti cold boot, offline reload, warm interaction; broj poziva i resource identity nisu isto što i CPU sample.
- D4 QA: prvo opaženo odstupanje od očekivanog ponašanja u relevantnoj putanji. Zabeleži tačan owner/symbol/source anchor, input/output, caller, async order i nezavisnu negativnu kontrolu. Samo poređenje redosleda razlika između buildova, timeout ili hotspot je trag za istragu. Uzrok označi kao PROVEN tek kada postoje dokazi iz D4 i D6 i interna provera D7.
- D5 Engineering: minimalni patch u postojećem owneru, jedna hipoteza; sačuvaj user changes, assets, save, behavior i rollback. Bez paralelnog schedulera ili automatskog brisanja validnih petlji.
- D6 QA: isti test/oracle FAIL na baseline za očekivani razlog, PASS na kandidatu; relevantni pozitivni, negativni i lifecycle regression. PL-01 A/B/R sa odgovarajućim uslovima za performance; instrumentacija odvojena od merenja. Android fizički dokaz zasebno.
- D7 interna provera: proveri originalne logove, diff, zamrznuti ugovor, identitet i obavezne gate-ove. Izvršiva pravila obrađuju pouzdane dokaze, a relevantna interna uloga razrešava sporne nalaze prema prvom nerazjašnjenom koraku. Obavezno odobrenje nezavisnog agenta je ukinuto. Evidentiraj ko je prikupio i ko je proverio dokaze. Nerazrešena materijalna kontradikcija ili nedostajući obavezan dokaz ostavlja pogođenu tvrdnju otvorenom.
- D8 odluka: PRIHVATI KANDIDAT samo kada sve required provere prolaze i interna provera potvrdi dokaz; ZADRŽI ZA QA za nedostatke; ROLLBACK za dokazanu regresiju kada je odobreno; NO-CHANGE kada nema dokaza za patch. Merge/deploy samo uz owner authorization. Odluke o docs/tooling ne zahtevaju lažne gameplay testove; scope se definiše unapred.

## Interna kvalifikacija D7 evaluatora (27.11.2026.)

Vlasnik je odobrio interni postupak kao jedini aktivni put za kvalifikaciju D7 evaluatora. Uloga eksternog kontrolora i formalna slepa proba u eksternom okruženju su ukinute. Obavezan potpis ili odobrenje nezavisnog agenta je ukinuto. Istorijski E0.6 zapis čuva se radi sledljivosti. Kontrolor može biti član tima ili vlasnik, pod uslovom da nije autor testirane revizije evaluatora niti izvršilac čije rezultate ocenjuje. Uloga kontrolora i formalna odluka vlasnika evidentiraju se u postojećem zapisu zadatka.

1. Kontrolor priprema sveže slučajeve i očekivane statuse i razloge. Ključ i svi materijali koji otkrivaju očekivane ishode ostaju u lokalnom prostoru kontrolora van ChatGPT-a, Git-a, povezanih servisa i radnog prostora evaluatora. Pre predaje ulaza kontrolor beleži SHA-256 ključa i ugovora, vreme zaključavanja i identitet kontrolora. Evaluator dobija ugovor za učesnika i testne ulaze.
2. Evaluator radi u novoj sesiji postojećeg internog okruženja. Poseban sandbox, drugi nalog i globalno gašenje istorije, memorije, konektora, Git-a ili mreže nisu uslovi interne probe. Kontrolor u preflight-u evidentira identitet sesije, model, učitanu reviziju i alate relevantne za ugovor. Uz inertan ulaz i probnu predaju proverava oba smera prenosa. Status razdvajanja zasniva se na tome gde su stvarni materijali napravljeni, čuvani i deljeni. Ako su očekivani ishodi bili dostupni kroz bilo koji izvor koji evaluator koristi ili ako se njihovo razdvajanje ne može utvrditi, pogođeni slučajevi se zamenjuju svežim.
3. Kontrolor zaključava originalnu predaju i beleži SHA-256, vreme i redni broj pokušaja pre poređenja sa ključem. Proverava zaključani ključ, ocenjuje status i razlog po slučaju i povezuje nalaz sa originalnim ulazima i odgovorima. Vlasnik donosi odluku o D7 na osnovu te evidencije.
4. Prethodni E0.6 za eksterno okruženje ostaje istorijski BLOCKED za stvarnu sesiju. Lokalnih 12/12 važi za POSIX pilot. Interna provera predaje i razdvajanja ima svoju evidenciju u istom zapisu. Za reviziju `b559a871…` početni status je ZADRŽI ZA QA. D7 ostaje BLOCKED dok interni uslovi nemaju dokaze i slepa proba ne prođe.

## Predaja između dva agenta

Arhitektura i infrastruktura vodi D0/D1/D3/D5, a stres-test specijalista D2/D4/D6. Zajednički zapis sadrži identitet oba builda, zamrznutu proveru, očekivani razlog pada, kontrolni scenario, ishode svih pokušaja i izvorne dokaze. Reliability koordinira internu proveru D7 i predaje nalaz vlasniku za odluku D8. Tim usmerava sporne stavke prema stručnosti. Odsustvo posebnog nezavisnog agenta samo po sebi ne zadržava kandidata u QA.

## Pouzdanost
Ne koristiti procente samopouzdanja bez kalibracije. Dokaz je jači od broja glasova agenata. Ako više uloga analizira isti izvršilac, to zabeleži uz dokaze i navedi koje su provere stvarno izvršene. Najviše tri neuspešne hipoteze bez novog dokaza; ne ponavljati isti patch. Nema automatskog retry za zelen rezultat. Čuvati neuspešne runove, razlikovati FAIL/BLOCKED/NOT RUN/N/A. Ne menjati oracle posle viđenog ishoda.

## Izvršna kontrola odluke
Postojeći tools/reliability/check_evidence.py ostaje vlasnik provere artefakata. Novi check_decision.py koristi taj checker i dodaje strukturnu proveru odluke za bug-fix. Contract i expected reason definiše reviewer pre rada; SHA-256 contract-a zabeležiti nezavisno. Format i primer u tools/reliability/decision-example.json (šablon, ne izvršeni dokaz). Pokretanje:
python tools/reliability/check_decision.py CONTRACT RECORD ARTIFACT_ROOT --contract-sha256 EXPECTED_HASH
Checker proverava dva različita commita, isti oracle hash, očekivani baseline failure reason, gate-ove, nepromenjen ugovor, artefakte i deklarisano stanje. Ne proverava autentičnost reviewera, sadržaj oracle-a ili istinitost logova. Rezultat STRUCTURAL_PASS nikada sam ne odobrava merge/deploy. Za tvrdnje van strukturne provere primeni internu proveru originala i trijažu iz D7. Za druge vrste zadataka koristi postojeći check_evidence i D0–D8 u odgovarajućem scope-u.

## Automatska provera izvršnih dokaza

**Provera izvršnih dokaza** je naziv drugog koraka. Postojeći `check_evidence.py` i `check_decision.py` proveravaju strukturu i vezu dokaza sa ugovorom. Provera izvršnih dokaza računa ishod iz originalnih događaja i trajnog stanja. Ugovor unapred zaključava pravilo, izvore, identitet kandidata i pokušaja i očekivane uslove. Slobodan tekst iz dokaza ostaje podatak. Automatski izračunat ishod koristi se za ocenu evaluatorske predaje u slučajevima sa izvršivim pravilom. U slepoj probi interni kontrolor beleži verziju pravila i zaključava izračunate očekivane ishode pre predaje ulaza. Posle zaključavanja odgovora poredi status, kod razloga i lokator dokaza.

| Redosled | Provera i nalaz |
|---|---|
| 1. Identitet | Poveži build, run, attempt, profil, trku i operaciju. Pogrešna ili nejasna pripadnost obaveznog dokaza ide prvo Architecture & Infrastructure. |
| 2. Izvršavanje | Poveži završetak trke sa potvrdom transakcije. Ponovljena potvrda istog ID-ja sa istim sadržajem predstavlja jednu transakciju. Isti ID sa različitim sadržajem ili dve različite potvrđene transakcije za jednu operaciju idu Engineeringu kada je poreklo potvrđeno. |
| 3. Trajno stanje | U nezavisnom snimku posle ponovnog pokretanja proveri tačno jedan rezultat za trku i tačno jednu ugovorenu isplatu za operaciju. Dokazan duplikat ili pogrešan iznos daje automatski FAIL. Protivrečni izvori iste sačuvane revizije idu Engineeringu posle potvrde porekla. Ako tačno jedna transakcija, rezultat i isplata odgovaraju ugovoru, ishod je PASS. Pouzdano utvrđeni izostanak obaveznog rezultata ili isplate daje FAIL. Nedostupan snimak daje PREGLED jer odsustvo u stanju nije utvrđeno. |

Dokazan nedostupan preduslov daje BLOCKED. Dokazano preskočena provera sa dostupnim preduslovima daje NOT RUN. Nepotpun dokaz, nepokriveno pravilo ili dvosmislen kriterijum ide QA / Reliability. Neslaganje evaluatora sa automatskim nalazom ide QA / Reliability uz obe ocene. Ako spor dovodi u pitanje poreklo ili brojanje istih isplata na kojima bi se zasnivao FAIL, nalaz ide na PREGLED. Pouzdano dokazan FAIL evidentira se i kada postoji zaseban spor koji ne utiče na taj nalaz. Odluka o puštanju ostaje u D8.

U postojećem zapisu zadatka svaki nalaz sadrži verziju pravila, identitet kandidata i pokušaja, prvi sporni korak, očekivano i stvarno, status i kod razloga, lokatore originala i prvu odgovornu ulogu kada je potreban pregled. Architecture & Infrastructure prvo razrešava poreklo, Engineering ponašanje i transakcije, a QA / Reliability kriterijum i ocenu. Posle razrešenja ponovi proveru i zadrži prvobitni ishod.

### Poplava identičnih potvrda

Normalan retry i poplava događaja imaju odvojene nalaze. Milion identičnih potvrda je sintetički primer spama i opterećenja prijema. Jedna trajna isplata može zadovoljiti pravilo transakcije dok isti pokušaj dobija zaseban nalaz o poplavi. QA unapred zaključava prag i prozor po izvoru i operaciji prema izmerenoj uobičajenoj stopi ponavljanja.

Na prijemu u QA evidenciju objedini identične potvrde jedne operacije i pokušaja u brojač, uz prvi i poslednji lokator i vreme. U bazu nalaza ide jedan zbirni zapis o poplavi po pokušaju, pravilu i izvoru. Nepodudarne potvrde i dokazi o različitim trajnim isplatama zadržavaju zasebne lokatore. Kada ograničenje prijema onemogući potpunu proveru, evidentiraj obim izostavljenih događaja i pošalji pogođenu tvrdnju na pregled. Engineering prvi proverava izvor koji proizvodi višak, a Architecture & Infrastructure preuzima kada je problem u prijemu ili poreklu događaja. Obrada i ograničenja važe za QA putanju dokaza.

### Prioritet nalaza prema ponašanju

Prioritet određuje redosled obrade nalaza. Status provere ostaje zasebno polje, kao i otvorenost pregleda.

| Prioritet | Uslov | Postupak |
|---|---|---|
| P0 — Kritično | Dokazana dupla trajna isplata, gubitak sejva ili kontrolna proba koja potvrdi da checker takvoj grešci dodeljuje lažni PASS. | Zaustavi automatsko zatvaranje pogođenih nalaza. Engineering rešava kvar, Reliability proverava originale i ponovno izvršavanje. |
| P1 — Visoko | Poplava prekoračuje zaključani budžet prijema, ugrožava njegov kapacitet ili dovodi do gubitka obaveznih dokaza. | Ograniči QA prijem prema ugovoru. Architecture & Infrastructure prvo proverava prijem, Engineering proverava izvor. Pogođenu tvrdnju bez dovoljnog dokaza pošalji na pregled. |
| P2 — Srednje | Pomešani pokušaji, sukob potvrda ili nedostajući snimak čine nalaz neodlučivim. | Otvori jedan pregled i dodeli ga prema prvom spornom koraku. |
| P3 — Nisko | Ponavljanje prelazi prag za taj izvor i operaciju, a prijem ostaje u budžetu i obavezni dokazi su kompletni. | Evidentiraj zbirni nalaz i prati trend. |
| P4 — Očekivano | Retry ili ponovna potvrda je u izmerenom normalnom opsegu. | Obradi automatski bez timskog zadatka. |

Jedan pokušaj može imati više nalaza. Sačuvaj svaki uz sopstveni razlog i lokatore, a za redosled obrade pokušaja koristi njegov najviši otvoreni prioritet. Ista isplata može imati PASS za trajnost i zaseban P3 ili P1 za spam. P0 za duplu isplatu važi kada su poreklo i stvarni broj isplata dokazani. Ako isti spor to onemogućava, zadrži tvrdnju otvorenom za pregled. Slobodan tekst iz loga ne utiče na prioritet, status ili usmeravanje.

Prag retry-ja, vremenski prozor i budžet prijema zaključaj po izvoru i operaciji pre automatske klasifikacije. Ako nedostaje kalibracija, evidentiraj da P3/P4 nije utvrđen. Dokazana povreda budžeta ili gubitak obaveznog dokaza i dalje daje P1. Sirovi dokaz ostaje u izvornom QA artefaktu, a nalaz nosi brojač i lokatore. U SC-DEC-01 upiši primenjenu verziju pravila, izmereni uticaj, status, prioritet i prvu odgovornu ulogu kada je potreban pregled.

Za automatsko zatvaranje potreban je kompletan dokaz baš za tvrdnju koja se zatvara. Brojač potvrda, hash artefakta i oznaka PASS iz loga sami ne dokazuju trajnost. Ako izvor ne omogućava razlikovanje ponovljene potvrde od dve trajne isplate, otvori pregled umesto zaključka. Ponovljena obrada istog pokušaja i verzije pravila ažurira zbirni nalaz bez umnožavanja redova i čuva prethodne odluke u postojećoj evidenciji. Novi pokušaj zadržava zaseban identitet. Beleži da li je izmereni uticaj sintetički ili potiče iz originalnog QA izvršavanja.

Pilot koristi uredan retry, dodatni retry, dupli rezultat, duplu isplatu, duplu isplatu uz belešku koja traži PASS, potvrdu iz drugog pokušaja, protivrečan rezultat i nedostajući snimak. Dodatne kontrole pokrivaju ponovljenu potvrdu iste transakcije, isti ID sa različitim rezultatom, dve transakcije za istu operaciju i ponovljenu potvrdu uz stvarnu duplu isplatu. Kada se u testnoj kopiji namerno isključi provera isplate, kontrolni slučajevi duple isplate moraju otkriti kvar. Pogođeni automatski nalazi ostaju otvoreni do ponovnog izvršavanja sa ispravljenim pravilom.

Dokaz o pilotu obuhvata osam osnovnih sintetičkih slučajeva i četiri zasebne sintetičke kontrole transakcije. Provera izvršnih dokaza je definisana ovim nacrtom. Integracija u alat repozitorijuma i provera na originalnim zapisima igre tek slede.

## Runtime nalaz 25.11.2026
Dostavljeni report(1).json za cef09906eca4b79e6d735ba8182e9da2fd759104: online/cache/offline HTML hash 7e6213ecadcaa08e8d62a87628b37942c38b8a603fc78e97e3395d62605ded6c; scenario_steps_executed=0. Shell PASS, gameplay i save durability NOT RUN. Prethodni CPU profil ukazuje na upload/uploadDetachedAtlas/uploadMapTexture kao hipotezu za ciljano istraživanje, ne dokaz baga. Novi trace(2).zip nije mogao biti otvoren u izvršnom okruženju; trace analysis BLOCKED. Ne menjati renderer na osnovu toga.

## Zatvaranje posle integracije

D8 je odluka o kandidatu, ne dokaz konačnog merge-a. [SC-PMV-01](SC-PMV-01-POST-MERGE-VERIFICATION-STANDARD.md) dopunjava postojeći zapis nakon merge-a stvarnim SHA, CI i dokazima. D7 evidentira rezultat interne provere, a vlasnik donosi odluku D8. Bez potrebnih dokaza MERGED—UNVERIFIED; nema samostalnog merge/deploy/rollback.
