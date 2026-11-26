# Animacije u test1 0.8.92 — stvarni inventar

> **Stanje identiteta (25.11.2026):** ovaj dokument navodi p1 (`2d66e55`, `index.html` SHA-256 `c19cc1ac…`). Istorijski snapshot izvršnog koda bio je **p3** (`5b4b030`, SHA `594026b9…`, `VERSION = '0.8.92-css-unified-p3'`). Tvrdnje o proverama u ovom dokumentu važe za p1 i **nisu ponovo proverene na p3 niti P10**. Merodavan izvor je [docs/README.md](https://github.com/tihidon/test1/blob/main/docs/README.md).

**Datum:** 25.11.2026. **Build:** `tihidon/test1` `main` `2d66e55`, `index.html` SHA-256 `c19cc1ac…`. **Vrsta:** statički popis iz CSS-a (`@keyframes` i `animation` pravila). Nije pokretana igra; nijedna animacija nema novi PASS. Pregled dokumenata: [docs/README.md](../README.md).

## 1. Zašto ovaj dokument zamenjuje matricu „42 animacije“

Projektni dokument *Faza 4, revizija v2* (23.11.2026, cilj 0.8.87) nosi matricu od 42 istorijske animacije sa imenima iz stare aplikacije v174 (`ti`, `fall`, `shake`, `tutin`…). Ta imena **nisu inventar ovog builda**: od 37 CSS imena, u test1 pod istim imenom postoji 6, za još 6 postoji jasan naslednik pod drugim imenom, a za 2 verovatan (§3). Zato se ta matrica ne prenosi kao važeća za test1; ovde je popis onoga što kod stvarno ima. Istorijska matrica ostaje u projektu kao izvor zahteva.

## 2. `@keyframes` u test1 (26)

Svaki ima tačno jedno `animation` pravilo u CSS-u, osim `lvring` (3). Kolona „Svojstva“ je ono što keyframe menja; sve van `transform`/`opacity` traži više rada pregledača ([SC-CODE-01 C08](../tehnika/standardi/SC-CODE-01-CSS-DOM-FUNKCIJE.md#c08--animacije-mora-za-nov-kod)).

| `@keyframes` | Svojstva | Napomena |
|---|---|---|
| `btfloat` | opacity, transform | Arena: broj štete odleti nagore |
| `btshield` | opacity, transform | Arena: zaštita |
| `gfp` | transform | kosmički poklon |
| `hatch-rays` | opacity, transform | izleganje |
| `impact-pop` | opacity, transform | udarac |
| `logo-fill` | **clip-path** | logo pri pokretanju |
| `lvbg` | opacity | novi nivo: pozadina |
| `lvburst` | opacity, transform | novi nivo |
| `lvglow` | opacity, transform | novi nivo |
| `lvring` | opacity, transform | novi nivo (3 pravila) |
| `lvstar` | opacity, transform | novi nivo |
| `lvstill` | opacity | novi nivo bez pokreta (reduced-motion) |
| `lvtx` | opacity, transform | novi nivo: natpis |
| `meteor-fall-l` | transform | meteor sleva |
| `meteor-fall-r` | transform | meteor zdesna |
| `popin` | opacity, transform | otvaranje prozora |
| `ring` | opacity, transform | prsten |
| `sc079-claim-glow` | **filter** | sjaj preuzimanja |
| `sc079-ready-glow` | **box-shadow, filter** | sjaj spremnosti |
| `sc080-boilbubble` | opacity, transform | rezervoar: mehurići |
| `sc080-boilshine` | opacity | rezervoar: sjaj |
| `sc080-rdybob` | transform | oznaka spremnosti / kap |
| `shell-hit` | transform | kućica: udarac |
| `shell-reveal` | opacity, transform | kućica: otkrivanje |
| `shell-strike` | transform | kućica: udar |
| `toastpop` | opacity, transform | poruka (toast) |

Napomene u poslednjoj koloni su izvedene iz imena i nisu proverene u igri.

## 3. Veza sa istorijskim imenima

| Istorijsko ime (v174) | U test1 |
|---|---|
| `gfp`, `lvtx`, `lvbg`, `lvstill`, `btfloat`, `btshield` | postoji pod istim imenom |
| `fall`, `fallL`, `fallD` | `meteor-fall-l`, `meteor-fall-r` |
| `boilbubble`, `boilshine`, `rdybob` | `sc080-boilbubble`, `sc080-boilshine`, `sc080-rdybob` |
| `ti` | `toastpop` (verovatan naslednik, nije potvrđeno) |
| `pop` | `popin` (verovatan naslednik, nije potvrđeno) |
| ostalih 23 CSS imena (`shake`, `carewobble`, `careheart`, `roamcrawl`, `lamp`, `incz`, `mbob`, `tutin`, `tutp`, `tutarrow`, `tutptr`, `tbshake`, `tbl`, `tbr`, `slzpulse`, `stkpulse`, `crbreathe`, `creglow`, `crhop`, `btlU`, `btlD`, `bthit`, `btglow`) | nema `@keyframes` tog imena; efekat je uklonjen, preimenovan ili rađen drugačije (npr. na canvasu) — NIJE PROVERENO |
| JS efekti `rewardFly`, `tutGhost`, `tutIco` | ime ne postoji u kodu |
| JS efekti `chipPulse`, `levelUp` | ime postoji u kodu (1 i 5 pogodaka); da li je to isti efekat, nije provereno |

Brojanje: `python3` pretraga `@keyframes\s+([\w-]+)` u `<style>` bloku i pretraga imena u izvršnim skriptama, 25.11.2026.

## 4. Šta treba za PASS jedne animacije

Isto kao ranije ([SC-AGENT-01 §10](../tehnika/standardi/SC-AGENT-01-OBAVEZNI-STANDARD-AGENATA.md#10-sc-a10--ui-pristupačnost-grafika-i-animacije)): stvarni okidač u igri, najmanje 3 uzastopna kadra iz stvarnog rendera („Pogledaj kretanje“), završno stanje, ponašanje uz `prefers-reduced-motion`, čišćenje posle završetka i bez dodatnih rAF/DOM resursa pri ponavljanju. Pokrivenost `prefers-reduced-motion` po animaciji ovde **nije proverena**.
