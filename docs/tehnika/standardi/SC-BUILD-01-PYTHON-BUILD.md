# SC-BUILD-01 — Python build i zaštita izvora

Status: vlasnik prihvatio nadogradnju 25.11.2026; kandidat za proveru u test1. Osnova: 360efc7a88897c50a7d58305e1cbef0794191c53. Ne menja SC-RAD, SC-AGENT, ARCH, FUNC, CODE, REND, PL-01, PW-01.

## Dokazane činjenice (pregled izvora, ne runtime test)

- tools/build.py čita src/html/index.template.html i blocks.json, ubacuje blokove i piše dist/index.html.
- tools/split.py čita reference/index-p3-main.html i piše src/. Stari tools/test_roundtrip.py poziva split u aktivnom checkout-u; tako se mogu izgubiti novije izmene i dobiti lažni PASS starog koda. Referenca P3: SHA-256 594026b9ffab62ceb8dbbfa181c887edea3f903ff84a27151a2330fb978dc58a.
- Netlify build trenutno kopira korenski index.html u dist/, ne pokreće tools/build.py. Jednakost src i korenskog HTML-a mora biti dokazana; ne menjati deploy konfiguraciju bez odobrenja.
- blocks.json ima 23 zapisa; id 22 je umetnut između 05 i 06. Redosled je definisan manifestom, ne numeričkim sortiranjem. Postojeći sha256 po bloku može opisivati istorijsku ekstrakciju, ne nužno trenutnu sadržinu.

## Obavezno

1. Posle potvrđene migracije src/ je razvojni izvor, generisani HTML je artefakt; istorijska referenca je zamrznuta. Dok trenutni build i publish nisu identični, prijavi konflikt i ne proglašavaj migraciju završenom. Ne menjaj istorijsku referencu.
2. Normalni build nikad ne pokreće split. Istorijski roundtrip samo u privremenom stablu. Nova ekstrakcija isključivo uz odobrenje, u praznom odvojenom direktorijumu.
3. Python standard library, bez npm zavisnosti za build igre. Ne menjaj format, redosled, asset bytes ni verzijske tačke nepotrebno.
4. `python tools/agent/check_build.py --require-publish-match` na pouzdanom checkout-u: validacija manifest putanja i markera, nezavisno sklapanje, dva builda u izolovanoj kopiji, provera SHA-256 i nepromenjenog izvora, Node syntax svih izvršnih blokova i SW, poređenje root publish HTML-a. Timeout za spoljne komande. Nema lažnog PASS ako nema Node ili ako checker ne čita sve navedene blokove. Privremeni direktorijum nije sigurnosni sandbox.
5. `python tools/test_roundtrip.py` isključivo istorijski P3 test. Ne služi za validaciju sadašnjeg izvora. Očuvanje korisničkih izmena prioritet.
6. Statičke i build provere ne dokazuju CSS semantiku, gameplay, PW-01 ili vizuelni QA. Zadržati sve primenljive postojeće gate-ove. Pri runtime izmeni proveriti šest mesta verzije iz AGENTS.md. Ne dodavati version.json samo zbog checkera.

## P0 publish identity gate candidate (26.11.2026)

Incident: PR #49 merged source P11 with P10 root; [push CI 45807116303](https://github.com/tihidon/test1/actions/runs/45807116303) failed exact equality. PR #53 repaired the artifact and advanced cache to P11-r2. [Push CI 45811647016](https://github.com/tihidon/test1/actions/runs/45811647016) on `73a58e45a996ca1f3fb48f4af9befa785a8e0be4`: both jobs succeeded, P11 SHA-256 `492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a`, B01–B06 51 assertions and QA-003 67 checks across 5 cases. D7 and production deployment identity not verified.

Candidate Netlify command uses existing Python build, then exact byte comparison with committed root before copying the remaining unchanged publish whitelist. Nonzero exit on mismatch; no automatic root overwrite or cache deletion. Two isolated real-command regression tests join existing tools/agent unittest discovery: valid exact whitelist, deliberately stale root rejected for the expected reason. No duplicate job, runtime change, cache bump or new dependency. This mitigates mismatched HTML deployment only, not all unsafe merges or release gates. Actual Netlify preview and owner approval of deployment configuration required; no deployment authorized by this draft. Private repository branch protection API unavailable (403; rulesets plan restriction); do not make repository public to bypass it.
