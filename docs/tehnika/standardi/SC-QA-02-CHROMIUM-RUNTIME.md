# SC-QA-02 — Chromium Runtime QA i pouzdanost dokaza

Status: predloženi operativni standard, dodatak SC-AGENT-01, SC-LOOP-01, PL-01, PW-01. Baseline 325ff6a9965a4081bda55f55eb7a35a1881b2e10. Ne zamenjuje postojeće vlasnike ni gate-ove. Zaseban skill chromium-runtime-qa; postojeći snail-city-engineering ostaje centralni coding skill.

## R1–R8: dokaz
R1: commit, dirty status, SHA-256 HTML/SW, stvarni response hash, startup build, title, diagnostic version, active controller, cache name and scope, browser/version/viewport/DPR, network, profile. Version family nije isto što i puna verzija. Za Netlify dokazati stvarne HTTP bytes zasebno.
R2: pre izvršavanja zabeleži očekivanje, testne podatke i razlog eventualnog FAIL; nezavisni oracle. Ne prilagođavati assertion rezultatu kandidata.
R3: stvarni korisnički korak → handler → app/domain/storage/renderer → asinhroni redosled → promena stanja → vidljivi rezultat. Prva divergencija uz source anchor, stack i relevantne pre/posle vrednosti; CPU hotspot sam po sebi nije uzrok.
R4: isti reproducer na broken/fixed; očekivani FAIL iz pravog razloga, PASS kandidata, pozitivna i negativna kontrola, relevantni regresioni testovi. Nereprodukovan kvar nije popravljen. Bez testova ne tvrditi stabilnost.
R5: watchdog izvan browser JS; ograničeni koraci i ukupan proces. Timeout = simptom, ne uzrok. Sačuvati parcijalne artefakte i poslednji korak. Linux procesna grupa; Windows nije podržan ovim wrapperom (BLOCKED). Ne dodavati watchdog u runtime igre.
R6: Playwright trace prikazuje akcije/DOM/network; CDP CPU profile uzorkuje JS stack; Chrome Performance trace/precizni function-scoped probes po potrebi. Ne tvrditi broj poziva iz sampling profila, niti GPU completion iz CPU vremena. Instrumentacija menja timing; odvojiti dijagnostiku od PL-01 A/B/R (20–30 ponavljanja kad je zahtevano).
R7: izolovan origin i svež browser context, bez pravog sejva i naloga. Lokalni publish whitelist, zabrana page-origin spoljnih requestova u testu; SW routing ima ograničenja, ovaj test se oslanja na pregledan SW koji ne pravi spoljne fetch-e. Ne koristiti pravi cloud. Offline shell nije dokaz save migracije, Force Stop, fizičkog Androida ili Netlify HTTPS. Za puni PW-01 proveriti saveId/revision/level/inventory i cold relaunch, upgrade/rollback zasebno.
R8: status PASS samo kada su assertioni stvarno izvršeni. FAIL za povredu, BLOCKED za nedostupan alat/uslov, NOT RUN za neizvršeno, N/A sa razlogom. Ne sabirati istorijske rezultate i ne skrivati flaky ponavljanja. Posle tri neuspešne hipoteze prijaviti blocker. Privatni artefakti sa sanitizovanim test profilom; ne slati trace javnom servisu.

## Izvršni alati
`tools/qa/runtime_watchdog.py` nadzire izdvojeni proces; `runtime_smoke.py` pokreće stvarni Chromium nad kopijom publish whitelist. Proverava SHA-256 online/offline navigacije i očekivani aktivni SW keš, dijagnostiku, pageerror, HTTP lokalne greške, screenshot, Playwright trace i CPU profile. Ne dokazuje kompletnu igru, FPS, save durability ili odsustvo svih petlji. Default je shell smoke; dodatni JSON scenario omogućava pregledane UI korake. Za funkcionalni bag dopuniti assertion stvarnim domain contract-om, bez novog game API samo radi testiranja.

Linux/POSIX u root-u repoa, izolovane zavisnosti:
```bash
python -m venv /tmp/sc-qa-venv
source /tmp/sc-qa-venv/bin/activate
python -m pip install -r tools/qa/requirements.txt
python -m playwright install --with-deps chromium
python -m unittest discover -s tools/qa -p 'test_*.py' -v
python tools/qa/runtime_watchdog.py --out /tmp/sc-qa-run
python -m playwright show-trace /tmp/sc-qa-run/trace.zip
```
Output direktorijum mora biti nov, izvan repo-a. CI koristi poseban job i privatni artifact. Zahtev za mrežu/dependencies = BLOCKED ako nije dostupan. Pinned direktni Playwright paket; tranzitivne zavisnosti još nisu zaključane; CI beleži pip freeze. Ne dodavati npm u game build.

## Scenario stres-test specijaliste

Prvi prioritet je `grad → trka → povratak na mapu → prvi tap`. Koristi stvarni UI i unapred definiši element, vidljiv odziv i očekivanu tranziciju stanja. Kontrola izvršava istu radnju na mapi bez prethodne trke. Naziv scenarija, početno stanje i profil, identitet builda i browsera, zamrznuta provera, očekivani razlog pada i kontrola ulaze u zajednički zapis pre pokretanja. Za svaki pokušaj sačuvaj poslednji završen korak, ishod imenovanih provera, razlog pada i izvorne artefakte. Sam broj koraka ne dokazuje pokrivenost tražene akcije. Postojeći `--scenario` koristi klik, vidljivost i tekst. Po potrebi proširi postojeći QA runner nezavisnom proverom domenskog stanja.

- **Dijagnostika.** Kreni od handlera stvarne akcije i asinhronog redosleda do prvog opaženog odstupanja od očekivanog ponašanja. Beleži očekivano i stvarno stanje, simbol, source anchor i pozivaoca. Biraj trace, logpoint, brojač aktivnih resursa ili ciljanu CDP sondu prema hipotezi. Precise coverage sa `callCount` remeti optimizaciju JS-a. CSS Coverage važi za obuhvaćene scenarije i služi ručnom pregledu.
- **Performanse.** Meri od tap-a do prvog vidljivog odziva u posebnom prolazu po PL-01 A/B/R, bez trace-a, precise coverage-a i dijagnostičkih omotača. Beleži uslove i sva ponavljanja. Koristi postojeći Python watchdog, sa svežim testnim kontekstom za nezavisne pokušaje. Node Playwright Test opcije `--repeat-each` i `--fail-on-flaky-tests` nisu opcije tog watchdoga. Pet pokušaja je početna provera nestabilnosti, a broj merenja performansi određuje PL-01. Fizički HONOR ima zaseban rezultat.
- **Trajnost sejva.** Za puni PW-01 zatvori browser i ponovo pokreni isti izolovani diskovni profil na istom originu. Proveri saveId/revision/level/inventory. Za offline proveri stvarni odgovor SW-a. Prenos IndexedDB snapshot-a služi za pripremu testnih podataka. Reload u istom kontekstu pokriva uži slučaj.
- **Granica istorijskog dokaza.** Za `cef0990` (`0.8.92-css-unified-p10`, Chromium `141.0.7390.37`) isti HTML je potvrđen online, u kešu i offline. `scenario_steps_executed: 0` daje shell PASS. Gameplay, trajnost sejva i fizički Android su NOT RUN u tom izveštaju. Izvor je istorijski lokalni artefakt `report(1).json`. Online, cache i offline HTML SHA-256 je `7e6213ecadcaa08e8d62a87628b37942c38b8a603fc78e97e3395d62605ded6c`.

## Sledeće provere nakon shell smoke
1. 3 while petlje i 63 lifecycle sites iz v1.1.0 istorijskog loga: sačuvati sve AST JSON lokacije i mapirati na funkcije, reentry/exit/cleanup.
2. Reprodukovati shop first-open, city→race→city, repeated panel enter/exit, resize/orientation, visibility pause/resume. Izmeriti stvarne callback/resource lifetime; ne zaključivati memory leak iz jednog snapshot-a. Ne uvoditi drugi RAF ili globalni instrumentation u produkciju.
3. PW-01 sa test sejvom, online→offline cold reopen; uređaj HONOR zasebno.
4. Agent eval: isti zadatak sa/bez skilla, proveriti stvarne tool calls i artefakte; negative trigger, unavailable tool, bug vs valid loop, wrong-build detection, failing assertion. Skill format PASS nije dokaz ponašanja agenta.

## Reference
https://chromedevtools.github.io/devtools-protocol/tot/Profiler/#method-startPreciseCoverage
https://developer.chrome.com/docs/devtools/coverage/
https://playwright.dev/python/docs/api/class-browsertype#browser-type-launch-persistent-context
https://playwright.dev/python/docs/api/class-browsercontext#browser-context-storage-state
https://playwright.dev/docs/test-cli
https://playwright.dev/python/docs/intro
https://playwright.dev/python/docs/release-notes
https://playwright.dev/docs/trace-viewer
https://playwright.dev/docs/service-workers
https://developer.chrome.com/docs/devtools/performance/reference/

## CI incident 25.11.2026 — v1.0.1
Run 45703980206, job 139522291296: package installation succeeded but Playwright 1.56.0 rejected Ubuntu 26.04 (ubuntu-latest). Browser, watchdog fixtures and shell smoke did not run. Artifact upload also failed because runtime directory did not exist. Classification: infrastructure FAIL; game runtime BLOCKED/NOT RUN. Pin browser job to ubuntu-24.04, preserve setup log/status even when browser setup fails, retain fail-fast checks. Do not interpret absence of game report as PASS. No game files changed. Exact new candidate CI must prove compatibility.

## Chrome DevTools MCP integration candidate
SC-CLI-01 owns pinned setup. Use exploratory UI, logpoints, heap retaining paths and raw trace on isolated test browser. Existing Playwright watchdog remains regression owner. Discovery/fixture PASS cannot replace B01–B06, physical Android, PW-01 or D7. Record actual tool/browser versions, source hash, target, raw artifacts and oracle. Separate diagnostics from PL-01 timing runs. NS01/NS02 first targets after live capability verification. No game modification based on tooling smoke.
