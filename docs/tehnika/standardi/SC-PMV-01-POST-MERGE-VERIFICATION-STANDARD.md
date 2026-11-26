# SC-PMV-01 — obavezna post-merge verifikacija

Datum: 2026-11-26. Opseg: svi agenti, svaki merge u main, uključujući dokumentaciju, tooling i CI. Dodatna kontrola zatvaranja uz SC-AGENT-01 G0–G7 i SC-DEC-01 D0–D8; ne menja njihove vlasnike, kriterijume ili obavezna odobrenja. Coordinator vodi PMV; Architecture vodi Git/CI identitet, QA relevantne regresije, Reliability nezavisni pregled kad je obavezan. Jedan SC-DEC-01 zapis, bez paralelnog registra.

## Obavezni postupak

1. Ponovo pročitaj stvarni PR: merged=true, ciljna grana, merge SHA, vreme merge-a, odobren scope. Dokaži da je merge SHA predak stvarnog main HEAD-a (Git/API). Ako je HEAD napredovao, odvojeno proveri originalni merge i novi HEAD; ne zameni dokaz jednog drugim.
2. Ugovor CI: postojeći workflow Snail City engineering gates, jobovi tooling i chromium-runtime; dodatni obavezni jobovi prema stvarnoj konfiguraciji ciljnog commita. Push main ili autorizovani workflow_dispatch na tačnom SHA, nakon merge-a; pull_request nije PMV ni kada se završi kasnije. Proveri stvarni checkout SHA i originalne jobove, korake, logove, artefakte, sve pokušaje i relevantne assertions. Pending/skipped/cancelled/neutral/missing nije PASS. Ne oslanjaj se na aggregate status ni prvi API page; kompletna inventura obavezna. Ako alat filtrira samo pull_request, koristi autorizovani API koji uključuje push ili označi BLOCKED.
3. Proveri odobren diff i izmenjene bajtove na ciljnom SHA, SSOT, relevantne G2–G6, build/publish jednakost i SW/verziju kad su primenljivi. Docs-only: sadržaj, reference i neizmenjen runtime; bez izmišljenog gameplay QA. Dokumentuj N/A sa razlogom.
4. CI i produkcioni deploy su odvojeni. Kada je deploy u scope-u, proveri stvarni deploy ID, commit, origin, publish identitet i relevantan smoke; nema neodobrenog deploy-a, rollback-a ili merge-a.
5. Zabeleži originalne dokaze, sve pokušaje, kontradikcije, preostali rizik i rollback. Nezavisni D7 review kad ga zahtevaju kanonski standardi; isti izvršilac nije nezavisan. Nezatvoreni gate ne sme biti preskočen.

## Status i ovlašćenja

VERIFIED tek kada svi obavezni dokazi prolaze; MERGED—UNVERIFIED kada merge postoji ali nedostaju dokazi; FAIL za utvrđenu neuspešnu kontrolu; BLOCKED za nedostupnu sposobnost/dokaz; NOT RUN za neizvršeno; N/A uz obrazloženje. Coordinator blokira zatvaranje/release i prosleđuje problem vlasniku, ne izdaje samostalnu autorizaciju. CI rezultat sam po sebi nije odobrenje. Post-merge kontrola ne može retroaktivno sprečiti merge; sprečava lažnu potvrdu spremnosti.

## CI implementacija i baseline

Zadržava se jedan postojeći engineering-gates workflow i oba postojeća joba, pull_request i workflow_dispatch; dodaje se push isključivo na main. Obe grane izvršavanja proveravaju HEAD == GITHUB_SHA. Tooling na push-u koristi github.event.before kao prethodni commit, proverava validan SHA (ne nula), postojanje commit objekta i ancestry; ne prelazi tiho na drugi baseline ako provera padne. PR koristi postojeći PR base SHA. Manualni dispatch zadržava postojeće zamrznute baseline reference; postojeći zamrznuti ESLint ratchet ostaje. Ne menja se runtime/SW/Netlify konfiguracija. G7 i D7 ostaju nepromenjeni.

## QA-001 — reprodukcija i granice

PR #41 merged 2026-11-26T08:14:24Z, SHA 8ed4417a6d2e423800a88436b4465a7a28f1dcab; main pri pregledu 2424de0aabf57294b67610c0344b122ac5209652, merge je predak. PR run 45781425134: tooling i chromium-runtime success; B01–B06 imaju 9/22/3/7/4/6 assertions. To je PR CI, ne PMV. GitHub Actions API lista po SHA za oba commita vratila total_count=0; workflow blob e1628219ccf0a878bee03051ac30488b12357865 ima pull_request i workflow_dispatch, nema push. Zato PR #41 ostaje MERGED—UNVERIFIED. Izmena workflow-a je kandidat dok stvarni push CI i relevantna nezavisna provera ne potvrde rad.

ChatGPT timski plugin v0.5.1 je odvojeno objavljen/read-back potvrđen; helper check_pmv_ci.py ispravlja QA-DEF-01–04 i 28 lokalnih unittest slučajeva prolazi (synthetic fixtures, ne agent behavioral eval). Helper nije deo ovog repo workflow-a, nije autentifikator dokaza i konzervativno blokira duple run ID-e (originalne rerun pokušaje pregledati zasebno; ne brisati). D7 nezavisna evaluacija NOT RUN/BLOCKED; ne proglašavati PMV VERIFIED. Dokazi: [PR #41](https://github.com/tihidon/test1/pull/41), [PR run](https://github.com/tihidon/test1/actions/runs/45781425134), [merge commit](https://github.com/tihidon/test1/commit/8ed4417a6d2e423800a88436b4465a7a28f1dcab).
