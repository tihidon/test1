# SC-DEC-01 — lanac pouzdanog odlučivanja

Status: kandidat za CI i nezavisnu evaluaciju; vlasnik odobrio nadogradnju. Baseline 9d638c4730caf63c02e2c01397a1eea96f2197eb. Dodatak SC-REL-01, SC-QA-02, SC-AGENT-01, PL-01, PW-01; ne zamenjuje nijedan gate. Jedan decision record po zadatku; dva specijalistička skilla primenjuju postojeći D0–D8 proces.

## Predaja nalaza i odluka

Handoff pokazuje postojeći zapis zadatka sa odobrenim opsegom, tačnim commitom ili buildom, izvršiocima, relevantnim diffom, odlukama i dostupnim dokazima. Za bezbednosni ili etički nalaz koristi polja i pragove iz [SC-BEH-01](SC-BEH-01-PONASANJE-AGENATA.md). Zabeleži odvojene zaključke auditora i QA, neslaganje i ciljnu proveru. Status provere i odluka vlasnika o merge/deploy vode se odvojeno. D7 nezavisno proverava originalne dokaze.

## D0–D8
- D0 Engineering: zamrzni zahtev, scope, baseline SHA, candidate plan, nezavisni oracle i required gates pre izmena. Za dirty tree zabeleži diff/hash; ne tvrdi clean commit identity za lokalne izmene.
- D1 Engineering: pročitaj stvarno telo, pozivaoce i dinamičke ivice, state reads/writes, lifecycle, ugovor i odobrena pravila. Razlikuj OBSERVED, HYPOTHESIS, PROVEN. Dokumentacija ne dokazuje runtime.
- D2 QA: stvarna korisnička akcija, izolovan profil, identity HTML/SW, scenario, očekivano i stvarno stanje; sačuvaj raw evidence. Ako reprodukcija nije uspela, NO-CHANGE ili ZADRŽI ZA QA, ne izmišljaj fix.
- D3 Engineering+QA: najmanje jedna falsifikabilna hipoteza i alternativno objašnjenje; unapred definiši šta bi oborilo hipotezu. Za texture upload odvojiti cold boot, offline reload, warm interaction; broj poziva i resource identity nisu isto što i CPU sample.
- D4 QA: prvo opaženo odstupanje od očekivanog ponašanja u relevantnoj putanji. Zabeleži tačan owner/symbol/source anchor, input/output, caller, async order i nezavisnu negativnu kontrolu. Samo poređenje redosleda razlika između buildova, timeout ili hotspot je trag za istragu. Uzrok označi kao PROVEN tek kada postoje dokazi iz D4 i D6 i nezavisan pregled D7.
- D5 Engineering: minimalni patch u postojećem owneru, jedna hipoteza; sačuvaj user changes, assets, save, behavior i rollback. Bez paralelnog schedulera ili automatskog brisanja validnih petlji.
- D6 QA: isti test/oracle FAIL na baseline za očekivani razlog, PASS na kandidatu; relevantni pozitivni, negativni i lifecycle regression. PL-01 A/B/R sa odgovarajućim uslovima za performance; instrumentacija odvojena od merenja. Android fizički dokaz zasebno.
- D7 Reliability: nezavisno pregleda originalne logove, scope diff, oracle, hashes i obavezne gate-ove. Agent ne može sam sebe proglasiti nezavisnim reviewerom. Ako kontradikcija nije razrešena, blokiraj prihvatanje. Structural PASS nije potvrda istinitosti, behavioral eval ili release authorization.
- D8 odluka: PRIHVATI KANDIDAT samo kada sve required provere prolaze i nezavisni pregled potvrdi dokaz; ZADRŽI ZA QA za nedostatke; ROLLBACK za dokazanu regresiju kada je odobreno; NO-CHANGE kada nema dokaza za patch. Merge/deploy samo uz owner authorization. Odluke o docs/tooling ne zahtevaju lažne gameplay testove; scope se definiše unapred.

## Interna kvalifikacija D7 evaluatora (27.11.2026.)

Vlasnik je odobrio interni postupak. Kontrolor može biti član tima ili vlasnik, pod uslovom da nije autor testirane revizije evaluatora niti izvršilac čije rezultate ocenjuje. Uloga kontrolora i formalna odluka vlasnika evidentiraju se u postojećem zapisu zadatka.

1. Kontrolor priprema sveže slučajeve i očekivane statuse i razloge. Ključ i svi materijali koji otkrivaju očekivane ishode ostaju u lokalnom prostoru kontrolora van ChatGPT-a, Git-a, povezanih servisa i radnog prostora evaluatora. Pre predaje ulaza kontrolor beleži SHA-256 ključa i ugovora, vreme zaključavanja i identitet kontrolora. Evaluator dobija ugovor za učesnika i testne ulaze.
2. Evaluator radi u novoj sesiji postojećeg internog okruženja. Poseban sandbox, drugi nalog i globalno gašenje istorije, memorije, konektora, Git-a ili mreže nisu uslovi interne probe. Kontrolor u preflight-u evidentira identitet sesije, model, učitanu reviziju i alate relevantne za ugovor. Uz inertan ulaz i probnu predaju proverava oba smera prenosa. Status razdvajanja zasniva se na tome gde su stvarni materijali napravljeni, čuvani i deljeni. Ako su očekivani ishodi bili dostupni kroz bilo koji izvor koji evaluator koristi ili ako se njihovo razdvajanje ne može utvrditi, pogođeni slučajevi se zamenjuju svežim.
3. Kontrolor zaključava originalnu predaju i beleži SHA-256, vreme i redni broj pokušaja pre poređenja sa ključem. Proverava zaključani ključ, ocenjuje status i razlog po slučaju i povezuje nalaz sa originalnim ulazima i odgovorima. Vlasnik donosi odluku o D7 na osnovu te evidencije.
4. Prethodni E0.6 za eksterno okruženje ostaje istorijski BLOCKED za stvarnu sesiju. Lokalnih 12/12 važi za POSIX pilot. Interna provera predaje i razdvajanja ima svoju evidenciju u istom zapisu. Za reviziju `b559a871…` početni status je ZADRŽI ZA QA. D7 ostaje BLOCKED dok interni uslovi nemaju dokaze i slepa proba ne prođe.

## Predaja između dva agenta

Arhitektura i infrastruktura vodi D0/D1/D3/D5, a stres-test specijalista D2/D4/D6. Zajednički zapis sadrži identitet oba builda, zamrznutu proveru, očekivani razlog pada, kontrolni scenario, ishode svih pokušaja i izvorne dokaze. Agent Reliability određuje postupak pregleda D7/D8. Kada su oba agenta učestvovala, nezavisni pregled radi vlasnik ili drugi reviewer. Bez njega odluka ostaje **ZADRŽI ZA QA**.

## Pouzdanost
Ne koristiti procente samopouzdanja bez kalibracije. Dokaz je jači od broja glasova agenata. Nezavisnost znači odvojen pregled originalnih artefakata, ne samo tri uloge istog modela. Najviše tri neuspešne hipoteze bez novog dokaza; ne ponavljati isti patch. Nema automatskog retry za zelen rezultat. Čuvati neuspešne runove, razlikovati FAIL/BLOCKED/NOT RUN/N/A. Ne menjati oracle posle viđenog ishoda.

## Izvršna kontrola odluke
Postojeći tools/reliability/check_evidence.py ostaje vlasnik provere artefakata. Novi check_decision.py koristi taj checker i dodaje strukturnu proveru odluke za bug-fix. Contract i expected reason definiše reviewer pre rada; SHA-256 contract-a zabeležiti nezavisno. Format i primer u tools/reliability/decision-example.json (šablon, ne izvršeni dokaz). Pokretanje:
python tools/reliability/check_decision.py CONTRACT RECORD ARTIFACT_ROOT --contract-sha256 EXPECTED_HASH
Checker proverava dva različita commita, isti oracle hash, očekivani baseline failure reason, gate-ove, nepromenjen ugovor, artefakte i deklarisano stanje. Ne proverava autentičnost reviewera, sadržaj oracle-a ili istinitost logova. Rezultat STRUCTURAL_PASS nikada sam ne odobrava merge/deploy. Stvarni nezavisni pregled ostaje obavezan. Za druge vrste zadataka koristi postojeći check_evidence i D0–D8 u odgovarajućem scope-u.

## Runtime nalaz 25.11.2026
Dostavljeni report(1).json za cef09906eca4b79e6d735ba8182e9da2fd759104: online/cache/offline HTML hash 7e6213ecadcaa08e8d62a87628b37942c38b8a603fc78e97e3395d62605ded6c; scenario_steps_executed=0. Shell PASS, gameplay i save durability NOT RUN. Prethodni CPU profil ukazuje na upload/uploadDetachedAtlas/uploadMapTexture kao hipotezu za ciljano istraživanje, ne dokaz baga. Novi trace(2).zip nije mogao biti otvoren u izvršnom okruženju; trace analysis BLOCKED. Ne menjati renderer na osnovu toga.

## Zatvaranje posle integracije

D8 je odluka o kandidatu, ne dokaz konačnog merge-a. [SC-PMV-01](SC-PMV-01-POST-MERGE-VERIFICATION-STANDARD.md) dopunjava postojeći zapis nakon merge-a stvarnim SHA, CI i dokazima. D7 ostaje nezavisan; Coordinator ne odobrava sopstveni rad. Bez potrebnih dokaza MERGED—UNVERIFIED; nema samostalnog merge/deploy/rollback.
