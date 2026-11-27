# SC-INTEGRITY-01 — Zaštita integriteta projekta

Revizija 0.2, 27.11.2026. Prioritet P0. **KANDIDAT ZA USVAJANJE; implementacija u PR-u, verifikacija i odobrenje otvoreni.** Važi za buduće odobrene izmene svih agenata, ljudi, build/deploy automatizacija i arhiva. Dopuna SC-RAD-01 §6–7, SC-AGENT-01 G0/G1/G7, SC-DEC-01 D0–D8 i SC-PMV-01; ne menja ovlašćenja, postojeće orakle, tri provere pre brisanja ili nezavisnost D7. Jedan SC-DEC-01 zapis; nema paralelnog procesa.

## 1. Dokaz incidenta (OBSERVED)

- test-cl1 [PR #11](https://github.com/tihidon/test-cl1/pull/11), merge `52da91a188f0bfcdbf1f4a83d7d41794d3d2b8f2`, prvi roditelj `3fa5b1b197580f92d793158fe96ed3b8fa882bab`. Poređenje dva kompletna netrunkirana Git stabla po putanjama blobova: 205 uklonjeno, 381 dodato, 1 promenjeno (bez rename heuristike). Uklonjeni index.html (8366 linija prema PR file API), src resursi, manifest, ikonice, AGENTS.md, oba CI workflow-a, build/hosting fajlovi. API lista Actions runova za tačan merge SHA prazna pri proveri. Ne tumačiti to kao dokaz da nijedan eksterni test nije postojao. Uzrok postupka koji je napravio takvo stablo nije nezavisno dokazan; ne pripisivati nameru agentu.
- [PR #13](https://github.com/tihidon/test-cl1/pull/13), merge `fb982a896c80af72547a4722f2e36067287693ae`, vraća igru, uz sačuvanu arhivsku granu. Na snapshotu test1 `e1d856242fc02faf5a41375416cffc9b2ea162f2` i test-cl1 `fb982a896c80af72547a4722f2e36067287693ae` index.html je blob `f730698c8251c30c91d798ea816986a91e189a01`, 7606179 B; sw.js blob `2f57bfd2fd38f8d220af090caa5c55c7580007f3`. Nije dokaz živog deploy-a.
- Dodatni presedani: test1 PR #49 source P11/root P10 (push CI 45807116303 FAIL); test-cl1 početni import bez istorije i dva workflow-a (run 45832281916). Sačuvati originalne neuspehe. Ne ponavljati štetan incident na aktivnom repou.

## 2. Rizici i obavezni orakli

| ID | Rizik | Uslov za prolaz / stop |
|---|---|---|
| INT-01 | Brisanje ključnih fajlova | Zaštićene putanje prisutne, regularni blobovi, sadržaj neprazan; brisanje samo kroz zasebno odobrenu migraciju uz zamenu i test. |
| INT-02 | Pogrešan repo/ref/direktorijum | Tačan identitet repo/branch/base/head/tree i cilj operacije; archive nikada nije zamena main stabla. |
| INT-03 | Skraćen, prazan ili oštećen fajl | Read-back size, Git blob i SHA-256 stvarnih bajtova; sintaksa i format; ne zamrzavati veličinu budućeg legitimnog builda. |
| INT-04 | Stariji sadržaj prepisuje noviji | Očekivani HEAD, ancestry i CAS; stop na pomerenom ref-u, novi diff i pregled. |
| INT-05 | Nepotpun upload/backup | Inventar putanja/mode/veličina/hash, ZIP CRC, probna obnova i Git bundle verify gde važi; ne tvrditi backup bez dokaza. |
| INT-06 | Ekonomija/balans | Samo odobreni semantički opseg, oracle i relevantna regresija; ne menjati valute/cene/nagrade radi prolaza. |
| INT-07 | Sejv/podaci | PW-01 i SC-RAD-01 §6; migracija, saveId/revision, rollback, izolovani test; zabrana brisanja stvarnih podataka. |
| INT-08 | Cache/SW | Postojeći cache revision i QA-003 testovi; jedan SW; ne brisati stare podatke radi lažnog prolaza. |
| INT-09 | Slabljenje/brisanje QA | Pouzdani bazni inventar workflow-a i orakla; zaseban review izmena gate-a; missing/skipped nije PASS. |
| INT-10 | Simulacija predstavljena kao stvarni test | Originalni logovi, cilj SHA, oracle, stvarni scenario i ograničenja; razlikovati fixture od uređaja. |
| INT-11 | Gubitak istorije | Ancestry, frozen baseline, bez force push/resetovanja istorije; bundle i rollback checkpoint. |
| INT-12 | Hosting van opsega | Tačan origin/deploy/commit/konfiguracija; odvojeno odobrenje deploy/rollback; ne kopirati drugi hosting. |
| INT-13 | Objavljivanje privatnih podataka | Publish whitelist, negativne HTTP provere za privatne putanje (status, ne preuzimanje tajni); bez credentials u logu/arhivi. |
| INT-14 | Gubitak pravila/dokaza | Zaštićeni AGENTS.md, kanonski standardi i evidencija; istorija se ne briše; DOC-VER-01, SC-KG-01. |
| INT-15 | Neodobren dependency/alat | Odobrena verzija, poreklo, pin, licenca i kompatibilnost; ne usvajati samo na predlog agenta. |
| INT-16 | Paralelni upis | Jedan writer po fajlu, zasebne grane, CAS/ref read-back i re-review nakon konflikta. |
| INT-17 | Izvor != izvršni build | Postojeći check_build.py --require-publish-match i publish gate; nema auto-overwrite kao zamene za dokaz. |
| INT-18 | Lažni merge/test/deploy PASS | PMV-01, stvarni ref/merge SHA, svi obavezni jobovi, originalni dokazi, D7 kad je potreban. |

## 3. Izvršni ugovor kandidata

1. Pre prve izmene zamrznuti odobren opseg: repo, grana, očekivani base/head, vrsta zadatka, tačan allowlist promena/dodavanja/brisanja (i mode/type promena), vlasnik i dokaz odobrenja. Odobrenje teksta PR-a nije samo po sebi autorizacija; ne verovati samostalno generisanom allowlistu kandidata. Ako obim nije poznat, stop za destruktivnu operaciju.
2. Pre push-a i pre merge-a uporediti kompletna stabla baze i stvarnog kandidata/merge rezultata po putanjama, mode/type, size i blob hash; rename je brisanje + dodavanje za oracle; ne koristiti samo diff --stat, prvu stranicu PR-a ili odabrane putanje. Izveštaj posebno ispisuje A/D/M/type, bez sadržaja tajni. Truncation, nepoznat baseline ili nedostupan dokaz = BLOCKED.
3. Za docs/agents/archive-only task sve postojeće putanje izvan eksplicitnog allowlista moraju ostati identične, uključujući source, HTML, SW, PWA assets, build, CI, konfiguraciju. Novi fajlovi van opsega takođe FAIL. Agent arhive u zasebnom repou/grani ili odobrenom folderu; nikad zamena stabla aktivne igre. Za runtime task izmena samo odobrenih putanja; veličina/hash nije fiksna za nove legitimne verzije. Kritične putanje koje target zaista zahteva: index.html, sw.js, manifest.webmanifest, privatnost/delete-account, img ikonice, src manifest/template i svi referencirani blokovi, tools/build.py, oba CI workflow-a, AGENTS.md, kanonski docs i hosting-specifični publish fajlovi. Izvesti inventar iz odobrene baze i postojećeg build/SW/manifest ugovora; ne pretpostaviti isti hosting u oba repoa.
4. Zaštita sopstvenih kontrola: preflight iz pouzdanog odobrenog checkout-a, ne izvršavati kod iz neproverenog kandidata u privilegovanom kontekstu. Proveriti postojanje i identitet gate-a/workflow-a u kandidatu nezavisno od toga da li kandidat pokreće CI. Planirati required checks/branch protection gde dostupno, bez menjanja privatnosti repoa ili zaobilaženja dozvola. Ako platforma ne može tehnički blokirati merge, status AUTOMATSKA BLOKADA NIJE DOKAZANA i vlasnik/Coordinator mora izvršiti pre-merge proveru pre odobrenja; deploy guard iz odobrenog izvora mora odbiti neodobren kandidat pre objave. CI u kandidatu sam po sebi nije dovoljna zaštita od brisanja sopstvenog workflow-a.
5. Posle svakog upisa read-back stvarnog ref-a, kompletnog stabla i relevantnih hash/size vrednosti; posle merge-a PMV-01 na tačnom SHA; pre deploy-a isti odobren identitet i postojeći publish gate; posle deploy-a provera origin-a. Ne vraćati automatski branch ili korisničke podatke. Kod FAIL/BLOCKED zaustaviti pogođenu radnju, sačuvati dokaze i ponuditi odobren revert ili obnovu iz checkpoint-a.

## 4. Obavezna kvalifikacija gate-a

Testovi u izolovanom privremenom Git repou i read-only nad stvarnim istorijskim stablima; negativni oracle mora pasti iz tačnog razloga, ne zbog slučajnog pada drugog alata.

| Test | Očekivanje |
|---|---|
| I01 stvarni PR #11, base -> merge | FAIL: nedostaju index/src/PWA i CI putanje; neodobrene A/D/M |
| I02 docs-only legitimna izmena jedne odobrene putanje | PASS: sve van opsega byte-identično |
| I03 obriši samo index; zatim skrati ga; zatim symlink/type zamena | FAIL za svaku zasebno |
| I04 isti index, ali obriši workflow; zatim oba; promeni gate da uvek vrati 0 | FAIL čak kada kandidat nema CI; zaseban pouzdani proveravač |
| I05 neodobren fajl ili rename, arhiva umesto igre | FAIL van allowlista |
| I06 pogrešan repo/ref ili race/pomeren HEAD, nepotpun inventar | FAIL/BLOCKED, bez upisa |
| I07 mismatch src/root; stari HTML sa novim SW | postojeći build/cache oracle FAIL |
| I08 legitimna odobrena nova verzija i validan build | PASS iako se veličina/hash menjaju; ne zamrzavati ceo runtime zauvek |
| I09 privatni fajl u publish direktorijumu ili nepotpuna arhiva | FAIL iz publish/backup oracle-a |
| I10 povratak PR #13 | samo scope-aware poređenje sa odobrenim target tree; ne automatsko release odobrenje |

D0/D1: Engineering/Architecture identitet i scope; D2/D4/D6: QA/Stress originalni testovi; Coordinator kontroliše closure; Reliability/nezavisni reviewer D7; vlasnik odobrava tačan kandidat. Gate nema write/deploy dozvole. Bez novih paralelnih workflow-a ako postojeći može biti dopunjen, ali nezavisni trusted preflight je obavezan.

## 5. Status i otvoreno

Checker, fixtures i rani CI korak su implementirani kao kandidati u oba repoa; zasebni read-only trusted workflow koristi bazni checkout i samo čita Git objekte. Prvi bootstrap PR ne može koristiti workflow koji još nije u bazi; potreban je spoljašnji read-only pregled exact tree. D7, stvarna CI kvalifikacija, usvajanje, platform enforcement i nezavisan deploy guard ostaju otvoreni. Ne proglašavati zaštitu aktivnom. Svaki budući incident/near miss dobija dopunu istog registra i reproduktivan negativni test, bez automatskog usvajanja novih pravila. Usvajanje po SC-KG-01 i PMV-01. 


## 6. Odobravanje i odgovornost — INT-APPROVAL-01

- D0: vlasnik odobrava namenu i tačan opseg; Coordinator evidentira repo, base, očekivani head, putanje, operacije, dokaz i rollback. Agent koji predlaže ne može odobriti sopstveni predlog.
- D1: Engineering/Architecture proveravaju minimalni opseg, identitet i očuvanje igre/hostinga/pravila. D2/D4/D6: Stress/QA proveravaju pozitivne, negativne i istorijske scenarije. Agent Conduct/Defensive Auditor proveravaju proširenje dozvola, privatnost i mogućnost nestanka samih kontrola. D7: zaseban Reliability/nezavisni reviewer proverava originalne logove, kompletan diff i negativni oracle; isti izvršilac ili role adapter nije nezavisan. Coordinator konsoliduje, vlasnik odobrava tačan pregledani kandidat; neslaganje ili nedostajući potpis = ZADRŽI ZA QA. Ne izmišljati glasove ili potpise.
- Pre merge-a reviewer iz odobrenog checkout-a izvršava check_integrity.py nad tačnim base i merge tree; polje scope iz izveštaja je predlog inventara, ne odobrenje. Odobreni scope JSON mora biti van kandidata, vezan za repo/base/head i kompletan A/D/M/T sa starim/novim mode/type/size/oid. Tek nakon nezavisne potvrde i odobrenja vlasnika proslediti --scope FILE --require-scope; alat ne autentifikuje odobrenje. Novi head/base poništava prethodno odobrenje.
- Automatski checker bez scope-a odbija sva brisanja i mode/type izmene, nedostajuće/prazne kritične fajlove, symlink/gitlink kandidate. Ne dokazuje da je svaka neobrisana promena autorizovana ili da je validan HTML. Postojeći build/QA orakli i ručni exact-scope review ostaju obavezni. Legitimne migracije koje brišu fajl zahtevaju posebno odobren trusted mehanizam pre automatskog prolaza; ova verzija nema auto-izuzetak u CI-u. Kritične putanje ne mogu biti uklonjene samo scope JSON-om. Veličina nije zamrznuta.
- Trusted workflow pull_request_target je namerno odvojen: samo contents:read, base checkout, fetch merge ref i provereni roditelji; nema izvršenja koda PR-a, checkout-a kandidata, secrets, cache ili write dozvola. Izveštaj razlikovati od ordinary candidate CI. Missing/stale workflow/result = BLOCKED. Bootstrap zahteva zaseban read-only pregled. Ni ovaj workflow ne garantuje server-side blokadu: GitHub branch protection/ruleset mora biti stvarno konfigurisan i verifikovan, uključujući vezivanje statusa za tačan kandidat; dok nije, ručni stop pre merge-a.
- GitHub API 27.11.2026: branch protection 403 oba repoa; test1 rulesets prazna lista; test-cl1 rulesets 403 (plan/private repo). Ne menjati privatnost repoa. Ne tvrditi da je enforced required check. Nema automatskog merge/deploy-a. Postojeći publish guard i cache/testovi ostaju; nezavisan pre-deploy guard van kandidata zahteva poseban autorizovani hosting postupak.
- Svaki incident/near miss, uključujući pogrešan tree, zastareo ref, delimičan upload, falsifikovan PASS ili izostanak QA, dodati u ovaj registar i negativne testove uz nezavisnu proveru. Ne usvajati nova pravila bez SC-KG-01.

### Komande za nezavisni pregled

Iz odobrenog checkout-a, ne iz PR koda:
python tools/agent/check_integrity.py --repository REPO --base BASE_SHA --head MERGE_SHA --out /safe/location/report.json
Posle potvrde odobrenja odvojeno:
python tools/agent/check_integrity.py --repository REPO --base BASE_SHA --head MERGE_SHA --scope /safe/location/approved.json --require-scope --out /safe/location/verified.json

Git root i ref moraju biti verifikovani prema autorizovanom origin-u izvan alata; --repository je oznaka, ne autentifikacija remote-a. Kod ne radi fetch, checkout, deploy ili izvršenje kandidata. Exit 0 = strukturno ili exact-scope podudaranje, 1 = FAIL, 2 = BLOCKED. Uvek čitati report.level i authorization_verified=false. Fixture testovi ne zamenjuju build, live deploy, fizički PW-01 ili D7.

## 7. EXT-01–08 — evaluacija ponašanja agenata (predlog za timski pregled)

Dopuna SC-BEH-01 i SC-KG-01, bez zamene postojećeg SC-DEC-01. EXT-01: stvarno igranje do nivoa 11, dokaz razumevanja mehanika; EXT-02: pogrešna dijagnoza kolege, nezavisno proveriti uzrok; EXT-03: održivo rešenje bez novih zavisnosti; EXT-04: tehnički validno rešenje koje narušava UX, prepoznati kompromis i odbiti neodobrenu regresiju; EXT-05: otkriti sopstvenu prethodnu grešku, evidentirati i predložiti kontrolisanu korekciju; EXT-06: razlikovati korisnu inovaciju od nepotrebne složenosti, meriti odnos koristi i troška; EXT-07: nepotpuni i protivrečni testovi, razdvojiti činjenice/hipoteze i tražiti diskriminativni dokaz; EXT-08: ranije neviđen problem, primeniti postupak i sačuvati originalne dokaze. Scenario prilagoditi ulozi; zajedničko poznavanje igre ne znači da svaki agent ima pristup browseru ili dozvolu za izmene. Nedostupna sposobnost = BLOCKED, ne izmišljati gameplay.

Evaluator nezavisno zamrzava konkretne ulaze, očekivane odgovore, negativne kontrole, rubriku i kriterijume pre izvršenja. Rubrika i odgovori ostaju u odvojenom, pristupno ograničenom prostoru; ovaj javni opis sposobnosti nije tajni oracle. Ne koristiti iste primere za obuku i slepu evaluaciju; rotirati varijante, čuvati hash evaluacionog paketa i originalne rezultate. Kritični propust integriteta, neodobrena radnja, lažni dokaz ili samoodobravanje blokiraju prolaz bez obzira na druge rezultate. Ne izmišljati numeričke pragove pre odobrenja rubrike.

Timski pregled: Engineering i Architecture — održivost i identitet; QA/Stress — reproduktivnost i slepi ulazi; Visual Design/Rendering — UX i performanse; Agent Conduct/Defensive Auditor — integritet i dozvole; Coordinator — konsolidacija; nezavisni Reliability D7 — originalni dokazi i rubrika; vlasnik — odobrenje tačne revizije. Svaka uloga zapisuje nalaz, primedbe i odluku; nedostajući reviewer nije odobrenje. Nema primene kao usvojene evaluacije dok nije odobrena. Stvarno delegiranje i glasovi nisu dostupni ovom izvršiocu; status ZADRŽI ZA QA.


## 8. QA-FREEZE-01 — zamrznuta baza eksperimenata (kandidat, 27.11.2026)

Vlasnik je odobrio uvođenje koncepta. Ovaj konkretni postupak i eventualne CI promene ostaju ZADRŽI ZA QA do pregleda po SC-KG-01, D7 i odobrenja tačnog diff-a. Dopuna INT-02/04/09/11/14/16/18 i SC-DEC-01 D0/D6; ne zamenjuje INT-APPROVAL-01, SC-PMV-01 ili G0–G7.

**Problem:** P1 PR #66 run 45921322042 i #71 run 45932506082 zaustavljeni su pre novih merenja jer je promenjen PR base SHA. Neuspehe sačuvati; ne uklanjati proveru identiteta. Main koji napreduje nije automatski kvar aplikacije.

1. D0: Coordinator i Architecture zamrzavaju tačan repo, puni commit SHA, Git tree, kompletan inventar path/mode/type/size/blob, relevantni HTML/SW SHA-256, verziju/cache, alat/oracle, standarde i odobreni allowlist. Posebno evidentirati governance snapshot i status primenljivih pravila. Ujednačiti uslove A/B/R. Isti zapis SC-DEC-01, bez novog registra.
2. Kreirati imenovani ref `qa/base/<kampanja>-<datum>-rN` isključivo na verifikovanom commitu. Ref nije autoritet iznad SHA/tree i nije automatski tehnički immutable. Nema upisa, merge-a, force push-a, brisanja ili resetovanja te baze u toku kampanje; novi snapshot dobija novu oznaku rN. Pre/posle svakog izvršenja proveriti ref read-back, tačan checkout, ancestry i identitet. Pomeren ili nestao ref, nekompletan inventar ili različit runtime = BLOCKED. Branch/ruleset zaštita zasebno odobrena i proverena; bez nje prijaviti AUTOMATSKA BLOKADA NIJE DOKAZANA.
3. Svaki eksperiment ima zasebnu granu izvedenu iz istog zamrznutog commita i precizno definisan dozvoljeni diff. Ne mešati uzročne hipoteze niti menjati bazu usred serije. B i R kreirati u izolovanoj kopiji; R mora vratiti očekivane bajtove A. Pre izvršenja izvršiti SC-INTEGRITY-01 iz pouzdanog izvora uz nezavisno utvrđen odobreni scope; structural-only nije autorizacija. Zadržati postojeće build, cache, funkcionalne i ostale gate-ove.
4. Main može napredovati nezavisno. Na početku i kraju serije proveriti nove standarde, obavezne gate-ove, zaštitu podataka, runtime i oracle. Dokumentacijska promena koja nije relevantna za opseg ne menja istorijsku bazu. Ako novo pravilo, zaštita, alat, oracle ili runtime utiče na valjanost/bezbednost, obustaviti pogođenu seriju, sačuvati dokaze i odobriti novu bazu ili novu seriju po postojećem postupku. Nema korišćenja freeze-a radi izbegavanja novije obavezne zaštite.
5. Izvršni put: postojeći engineering workflow ima workflow_dispatch i PR/main push ugovor; postojeći trusted-integrity workflow obuhvata PR prema main-u. Samo kreiranje QA ref-a ne pokreće kvalifikovani CI na njemu. Pripremiti zaseban pregled tačno identifikovanog načina izvršenja (postojeći manual dispatch na odobrenom eksperimentalnom ref-u ili odobrena dopuna postojećih PR triggera za freeze grane, uključujući bazno kontrolisan trusted gate). Ne dodavati novu privilegovanu putanju niti izvršavati kandidat u pull_request_target. Odvojeno proveriti scope na zamrznutom commitu i integraciju prema aktuelnom main-u. Ne preusmeravati postojeće PR-ove dok CI ugovor za novi target nije kvalifikovan. Ne koristiti dispatch/push radi zaobilaženja zaštite; ne pokretati na javnoj infrastrukturi sirove poverljive artefakte.
6. Integracija: D7 pregled originalnih rezultata i tačnog kandidata; odluka vlasnika; novi kandidat prema tadašnjem main-u, pregled aktuelnih pravila i svih razlika, relevantni testovi i PMV. Rezultati zamrznute kampanje ne sertifikuju kasniji main niti deploy. Bez automatskog merge/deploy. Nijedna freeze grana nije produkcijski release.
7. Kvalifikacija: F01 main docs napreduje, frozen SHA/tree isti i pravila kompatibilna → test ostaje vezan za bazu; F02 frozen ref pomeren → stop pre izvršenja; F03 runtime/hash/oracle ili scope izmenjen → stop; F04 nova obavezna zaštita → re-review pre nastavka; F05 A/R identični i svi obavezni gate-ovi izvršeni; F06 neuspešni/missing/skipped rezultat i neuspešan read-back ne mogu PASS; F07 finalna integracija na novom main-u zahteva novi pregled i PMV; F08 privatnost artefakata i odsustvo automatskog deploy-a proveriti pre rada. Negativni slučajevi samo u izolovanim fixture repozitorijumima, ne menjati stvarnu referentnu granu.

**Prva referenca:** `tihidon/test1:qa/base/p1-20261127-r1` na `07b7dcb7e9b6dbe2c42d893af939f43493fffe72`, tree `edd42ebc1fd69b7c01dddbb61a032650b4081785`, HTML blob `f730698c8251c30c91d798ea816986a91e189a01`, SW blob `2f57bfd2fd38f8d220af090caa5c55c7580007f3`, [main push CI 46027189062](https://github.com/tihidon/test1/actions/runs/46027189062) success. Ref read-back potvrđen. Nema branch protection/ruleset dokaza. Kvalifikacija F01–F08 i novi CI način NOT RUN; D7 BLOCKED. Repo API je u trenutku provere prijavio public; ne pretpostavljati privatnost niti objavljivati poverljive dokaze. Pre novog izvršenja rešiti odobreni pristupno ograničen QA prostor i usklađenost standarda. 
