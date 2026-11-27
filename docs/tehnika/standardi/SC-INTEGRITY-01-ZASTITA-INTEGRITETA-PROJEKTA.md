# SC-INTEGRITY-01 — Zaštita integriteta projekta

Revizija 0.1, 27.11.2026. Prioritet P0. **PREDLOG ZA USVAJANJE; nije implementiran izvršni gate.** Važi za buduće odobrene izmene svih agenata, ljudi, build/deploy automatizacija i arhiva. Dopuna SC-RAD-01 §6–7, SC-AGENT-01 G0/G1/G7, SC-DEC-01 D0–D8 i SC-PMV-01; ne menja ovlašćenja, postojeće orakle, tri provere pre brisanja ili nezavisnost D7. Jedan SC-DEC-01 zapis; nema paralelnog procesa.

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

## 3. Izvršni ugovor kandidata (nije implementiran)

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

Ovaj dokument je definicija. Stvarni checker, test fixtures, integracija u postojeći CI, trusted preflight, deploy guard, mogućnost platformskog enforcement-a, D7 i sinhronizacija u test-cl1 nisu izvršeni/odobreni ovim zadatkom. Ne proglašavati zaštitu aktivnom. Svaki budući incident/near miss dobija dopunu istog registra i reproduktivan negativni test, bez automatskog usvajanja novih pravila. Usvajanje po SC-KG-01 i PMV-01. 
