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

## Sledeće provere nakon shell smoke
1. 3 while petlje i 63 lifecycle sites iz v1.1.0 istorijskog loga: sačuvati sve AST JSON lokacije i mapirati na funkcije, reentry/exit/cleanup.
2. Reprodukovati shop first-open, city→race→city, repeated panel enter/exit, resize/orientation, visibility pause/resume. Izmeriti stvarne callback/resource lifetime; ne zaključivati memory leak iz jednog snapshot-a. Ne uvoditi drugi RAF ili globalni instrumentation u produkciju.
3. PW-01 sa test sejvom, online→offline cold reopen; uređaj HONOR zasebno.
4. Agent eval: isti zadatak sa/bez skilla, proveriti stvarne tool calls i artefakte; negative trigger, unavailable tool, bug vs valid loop, wrong-build detection, failing assertion. Skill format PASS nije dokaz ponašanja agenta.

## Reference
https://playwright.dev/python/docs/intro
https://playwright.dev/python/docs/release-notes
https://playwright.dev/docs/trace-viewer
https://playwright.dev/docs/service-workers
https://developer.chrome.com/docs/devtools/performance/reference/
