# Code Health Audit — otvorena obuka i predlog dopune, 28.11.2026.

**Status:** ZADRŽI ZA QA / kandidat za trajno usvajanje po SC-KG-01. Vlasnik je odobrio ažuriranje dokumentacije; nije odobrio promenu aktivnih skillova, automatizacije, runtime-a ili deploy-a. Ovo je jedan zapis zadatka prema [SC-DEC-01](../tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md), a ne novi standard, rules engine ili paralelni registar nalaza.

## Identitet i opseg

- Kanonski target: [test1 main, f0a5b4ca04e134e4f987a77e9fece7f0f979fce1](https://github.com/tihidon/test1/commit/f0a5b4ca04e134e4f987a77e9fece7f0f979fce1). Dokumentacioni kandidat; nijedan nalaz nije tvrdnja o grešci na tom runtime-u.
- U prethodnoj sesiji pročitani instalirani profili Coordinator 0.5.13, Engineering 0.5.9, Architecture 0.5.10, Rendering 0.5.8, Stress 0.5.8, Chromium QA 0.5.7, QA Planning 0.5.7, Reliability 0.5.8, Team Defensive Auditor 0.1.3 i zasebni Defensive Auditor 0.1.7. Repo kanonski auditor na navedenom SHA: 0.1.1. Verzije profila nisu verzija celog Team plugina niti dokaz ponašanja.
- Izvršilac: jedna ChatGPT sesija sa kombinovanim stručnim profilima; ponovljene sintetičke Node provere izveo je ovlašćeni QA pristup u sesiji ažuriranja dokumentacije, ne zasebni auditor. Nema tvrdnje o delegaciji, nezavisnom izvršenju ili ponašajnoj kvalifikaciji.
- Postojeći dnevni Code Health Audit je aktivan, dnevno 20:30 Europe/Belgrade, prošireni pregled nedeljom; očitano u prethodnoj sesiji 28.11.2026, bez dostupnog prvog rezultata u tom očitavanju. Očuvati postojeći zadatak, alate i ritam; bez nove automatizacije.
- Auditor: samo ručno dostavljeni nesenzitivni sintetički dokazi; bez mreže, shell-a, izvršavanja, upisa i tajni. Interni D7 koordinira Reliability; D8 vlasnik. Nema obavezne posebne spoljne kontrole.

## Kandidat za naprednu obuku (neaktivna dopuna)

Cilj: zaštititi ispravan kod jednako ozbiljno kao što se otkriva defekt. Pratiti degradaciju između audita, prve divergencije i uzročno povezane posledice; ne svoditi zdravlje koda na broj linija ili upozorenja. Koristiti postojeće audit_duplicates.cjs, audit_loops.cjs, quality_gate.py, debug_source.cjs, registar funkcija i autorizovani Chromium QA samo kada su dostupni i verifikovani. Ne uvoditi novi alat bez SC-KG-01.

Za svaku anomaliju: identitet commita, funkcija/putanja, vlasnik i stvarni pozivaoci, stanje i lifecycle, relevantni standard, opažanje/hipoteza/potvrđen uzrok, protivdokaz, posledica i prioritet odvojeno od statusa dokaza, minimalna diskriminativna provera, odluka NO-CHANGE ili predlog popravke. Koristiti postojeće NOVO/POSTOJEĆE/OTKLONJENO/NEPROVERENO; OTKLONJENO samo uz odgovarajući dokaz. Ako nema pouzdanog prethodnog zapisa, ne izmišljati trend. Zadržati neuspešne pokušaje i razdvojiti strukturalni PASS od ponašanja. Kod kritične sumnje primeniti postojeću eskalaciju SC-BEH-01.

| Otvoreni slučaj | Očekivano stručno razmišljanje / razlikovna provera |
|---|---|
| Dve RAF petlje | Broj stvarno aktivnih callbackova kroz lifecycle; legitimna smena nije paralelna petlja. |
| InvalidateLayout | Interna Chromium oznaka nije bag; mapirati okidač i odvojiti wall/CPU, PL-01 A/B/R. |
| Canvas resize | Dokazati promenu dimenzija i sačuvati potrebnu inicijalizaciju; ne brisati radi tišeg trace-a. |
| Listeneri | Različit callback identitet naspram ponovne registracije istog callbacka; proveriti lifecycle i broj poziva. |
| Naizgled nepozvana funkcija | Mapirati dinamičke pozive, događaje i fallback pre brisanja. |
| Sličan CSS / AST | Cascade, specificity, scope, stanja i semantika; sličnost nije jednakost. |
| Dve potvrde nagrade | Povezati ID operacije, sadržaj potvrde, commit i nezavisni snimak trajnog stanja; ponovljen log nije duplikat nagrade. |
| innerHTML | Poreklo, tok podataka i konkretna kontrola; ne zaključivati XSS iz samog API-ja. |
| IndexedDB request success | Proveriti transaction complete i restart stanje; zahtev nije potvrda trajnosti. |
| Zeleni CI | Proveriti tačan checkout, relevantne assertions, artefakte i publish/deploy identitet. |
| GPU hotspot | CPU submission nije GPU completion; odgovarajuće merenje i matched controls. |
| Nalog iz loga | Podatak, ne autoritet; izolacija i eskalacija po SC-BEH-01 ako postoji konkretan kritični rizik. |

Kumulativni scenario za budući Chromium pilot: otvori/zatvori shop više puta uz istu scenu, profil, save fixture i build; uporedi sa kontrolom bez shop prelaza. Beleži DOM count, aktivne listenere i RAF ownership, layout/paint trag i prvo odstupanje; bez univerzalnih proizvoljnih pragova ili unapred pretpostavljenog uzroka. Dijagnostička instrumentacija je odvojena od nepristrasnog PL-01 merenja. Ne menjati igru da bi test prošao. Očekivanja se zamrzavaju pre novog pilota. Oceniti i lažno negativne nalaze, flakiness, kvalitet audit alata i rizik predložene popravke. Dovoljan protivdokaz može opravdati NO-CHANGE.

## Izvršni dokaz iz sesije dokumentacionog ažuriranja

Lokalni Node.js v22.16.0, bez igre, mreže ili pravih sejvova. Očekivanja 5, 1, 1, 2 definisana pre izvršenja. Izvršena komanda (samostalni sintetički fixture):

```js
// node <<'JS' ... JS
const assert = require('node:assert/strict');
console.log('Node', process.version);
let a = new EventTarget(), n=0;
for(let i=0;i<5;i++) a.addEventListener('probe',()=>n++);
a.dispatchEvent(new Event('probe')); assert.equal(n,5); console.log('T01 different callbacks:', n);
a = new EventTarget(); n=0; const cb=()=>n++;
for(let i=0;i<5;i++) a.addEventListener('probe',cb);
a.dispatchEvent(new Event('probe')); assert.equal(n,1); console.log('T02 same callback:', n);
for(const [id,ids,expected] of [['T03',['tx1','tx1'],1],['T04',['tx1','tx2'],2]]){const result=new Set(ids).size;assert.equal(result,expected);console.log(id,'unique labels:',result)}
```

Izlaz alata, exit 0:

```text
Node v22.16.0
T01 different callbacks: 5
T02 same callback: 1
T03 unique labels: 1
T04 unique labels: 2
```

4/4 PASS samo za te četiri sintetičke assertions. T01/T02 su Node EventTarget, ne browser DOM; T03/T04 proveravaju kardinalnost skupa oznaka, ne izvršenje ili trajnost transakcije. Raniji opis obuke naveo je Node 4/4 i Chromium BLOCKED sa dva neuspešna pokušaja, ali originalni transcript tih pokušaja nije dostupan za verifikaciju. Korekcija: prethodni rezultati NEPROVERENO; gore su novi proverljivi Node rezultati. Chromium u sesiji ažuriranja nije pokrenut (NOT RUN); uzrok prethodne blokade nije potvrđen. Nema runtime ili fizičkog Android dokaza. Ostali slučajevi su otvorene edukativne analize, ne izvršeni testovi.

## Predaja i odluka

- URAĐENO: pregled profila/pravila i instrukcije automatizacije u prethodnoj sesiji; dokumentacioni kandidat i ponovljene četiri lokalne assertions.
- DELIMIČNO: otvorena praktična obuka; nedostaju sveži Chromium dokazi i ponašajni rezultati.
- NOT RUN: odvojena evaluacija ponašanja auditora i igre; novi Chromium pilot. D7 za trajno usvajanje nije zatvoren.
- KANDIDAT: šest dopuna obuke (lažni pozitivni/negativni nalazi, kumulativni uzroci, kvalitet alata, protivdokazi, šteta od popravke, retrospektiva). Odgovarajuće stručne provere, originalni dokazi i eksplicitno odobrenje tačnog kandidata potrebni su pre trajne integracije po [SC-KG-01](../tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md#sc-kg-01--kontrolisano-usvajanje-znanja-tehnika-i-tehnologija).
- Dokumentacioni PR: proveriti read-back, diff i neizmenjen runtime. PMV prema [SC-PMV-01](../tehnika/standardi/SC-PMV-01-POST-MERGE-VERIFICATION-STANDARD.md) posle eventualnog odobrenog merge-a; nije potvrđen ovim zapisom. Rollback: ne spojiti kandidat ili odobren revert dokumentacionih promena. Test-cl1 uskladiti kontrolisano posle odobrenog kanonskog merge-a.
