# Potvrđeno čišćenje: SAMO šest CSS deklaracija `.map-controls`

> **Stanje identiteta (25.11.2026):** ovaj dokument navodi p1 (`2d66e55`, `index.html` SHA-256 `c19cc1ac…`). Izvršni kod na `main` je **p3** (`5b4b030`, SHA `594026b9…`, `VERSION = '0.8.92-css-unified-p3'`). Tvrdnje o proverama u ovom dokumentu važe za p1 i **nisu ponovo proverene na p3**. Merodavan izvor je [docs/README.md](https://github.com/tihidon/test1/blob/main/docs/README.md).

> **Kopija za `tihidon/test1` (0.8.92-css-unified-p1).** Izvor: [snail-city-test@1e3258f](https://github.com/tihidon/snail-city-test/blob/1e3258f/docs/tehnika/standardi/SC-BRISANJE-3-PROVERE.md). Provereno prema test1 `main` `2d66e55` (`index.html` SHA-256 `c19cc1ac…`) 25.11.2026: **zapis ne opisuje test1.** U test1 selektor `.map-controls` i dalje postoji u dva grupna pravila (`.in-race … .map-controls{display:none}` L157 i `.screen-open … .map-controls` L394). Čišćenje je urađeno u drugom buildu; ovde ostaje presedan postupka, ne činjenica o ovom kodu. Izmene u odnosu na izvor: samo ova napomena. Pregled svih kopija: [docs/README.md](../../README.md).

> **Vrsta dokumenta:** zapis jednog čišćenja (presedan za brisanje CSS-a), **ne opšti standard**. Opšti postupak brisanja po vrstama (CSS, funkcija, sejv, keš, asset, fajl, workflow, dokument, funkcija igre): [SC-RAD-01 §6](./SC-RAD-01-POSTAVKA-IZMENA-BRISANJE.md#6-brisanje-dokaz-po-vrsti). Ime fajla je zadržano jer se na njega pozivaju drugi dokumenti.

1. **Statička analiza:** klasa nije napravljena u HTML/JS sadašnje aplikacije; izvorni stil sadrži šest pojedinačnih blokova.
2. **Runtime:** proverena su 26 ekrana i 390×780 i 840×700 viewport: nula instanci `.map-controls`.
3. **Vizuelna regresija:** u istom Chromium dokumentu vraćena su u memoriji sva uklonjena pravila; u oba viewporta rezultat `ImageChops.difference` je null — nula promenjenih piksela. Zatim su regresioni testovi ponovljeni.

**Rezultat:** 6 deklaracija uklonjeno; 0 JS funkcija, 0 ekonomskih komandi, 0 spriteova i 0 cloud handlera obrisano. Ostali sumnjivi CSS/JS delovi nisu prošli tri nezavisne provere i ostaju.
