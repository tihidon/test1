# tools/sc-code-01 — merenje pravila SC-CODE-01

Statičko merenje CSS, DOM i JS pravila iz
[SC-CODE-01](../../docs/tehnika/standardi/SC-CODE-01-CSS-DOM-FUNKCIJE.md) i ratchet provera:
nijedna praćena metrika ne sme da poraste u odnosu na polazno stanje.
Alat samo čita `index.html`. Ne menja kod, ne pokreće igru i ne meri performanse.

## Fajlovi

| Fajl | Namena |
|---|---|
| `sc_code_metrics.py` | izvlači `<style>` i izvršne `<script>` blokove, meri CSS (`tinycss2`), poziva JS merenje, poredi sa baseline-om |
| `js_metrics.cjs` | AST merenje JS-a (`acorn`): dužina, dubina, parametri, ternari, DOM API pozivi |
| `baseline-0.8.90.json` | polazno stanje `snail-city-test/main` (`index.html` SHA-256 `a4d53277…a3bd7`) |
| `baseline-0.8.92-css-unified-p1.json` | polazno stanje `test-2/dist` (`index.html` SHA-256 `c19cc1ac…b7c5d`) |

## Pokretanje

Zavisnosti se instaliraju u privremeni folder, ne u repo:

```bash
mkdir -p /tmp/sc-tools && (cd /tmp/sc-tools && npm install acorn@8.19.0 acorn-walk@8.3.5)
pip install tinycss2==1.5.1
export NODE_PATH=/tmp/sc-tools/node_modules

python3 -I tools/sc-code-01/sc_code_metrics.py index.html \
  --baseline tools/sc-code-01/baseline-0.8.90.json
```

Izlaz `0` = `RATCHET PASS`. Izlaz `1` = `RATCHET FAIL` sa spiskom metrika koje su porasle.
Bez `--baseline` alat samo ispisuje JSON.

## Ažuriranje baseline-a

Samo u PR-u prihvaćenog kandidata za raščišćavanje (SC-CODE-01 §7), sa obrazloženjem.
Nikada da bi prošla nova funkcionalnost.

## Ograničenja i rešavanje problema

- `Cannot find module 'acorn'`: `NODE_PATH` ne pokazuje na `node_modules` sa instaliranim paketima.
- `js_metrics.cjs nije uspeo` uz `SyntaxError`: skript u HTML-u nije validan JS za `ecmaVersion: latest`; proveriti `node --check`.
- Statička analiza ne vidi klase koje JS sklapa iz delova i ne zna koliko se pravila primenjuje u runtime-u.
- Kontrolna dubina ne broji ternare i logičke izraze (`&&`, `||`).
- DOM veličina se meri u Chromiumu po ekranu (komanda u SC-CODE-01 §8).
