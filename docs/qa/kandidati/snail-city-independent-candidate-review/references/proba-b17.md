# B17 — mala sintetička proba

## Ulaz

- Kandidat B17 i izolovani profil Q su sintetički.
- Zamrznuti ugovor zahteva oznaku uspeha tek posle potvrđene IndexedDB transakcije i nivo 8 posle hladnog offline pokretanja.
- CI je vratio exit 0. Dve asercije proveravaju vidljivost oznake uspeha i ekrana igre posle ponovnog pokretanja.
- Ulazni trag beleži oznaku na 12 ms, prekid transakcije na 32 ms i nivo 7 posle hladnog offline otvaranja.

## Nalaz odvojenog reviewera

**B17 · ZADRŽI ZA QA.** Reviewer je locirao prvo odstupanje na 12 ms i objasnio zašto exit 0 ne pokriva redosled potvrde i trajnost. Predložio je proveru redosleda uspešnog završetka transakcije i prikaza oznake, kao i proveru nivoa 8 nakon hladnog offline otvaranja.

## Ograničenje

PASS za jednu probu predstavljenu kao tekstualni paket i za sposobnost da se u tom paketu prepozna slaba asercija. Reviewer je dobio sažeto uputstvo u zadatku. Izvršavanje ovog skilla iz repozitorijuma, stvarni Chromium i nezavisni D7 samog skilla nisu provereni. Skill ostaje ZADRŽI ZA QA.
