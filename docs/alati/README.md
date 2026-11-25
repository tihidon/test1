# docs/alati — pomoćni alati dokumentacije

> **Stanje identiteta (25.11.2026):** ovaj dokument navodi p1 (`2d66e55`, `index.html` SHA-256 `c19cc1ac…`). Izvršni kod na `main` je **p3** (`5b4b030`, SHA `594026b9…`, `VERSION = '0.8.92-css-unified-p3'`). Tvrdnje o proverama u ovom dokumentu važe za p1 i **nisu ponovo proverene na p3**. Merodavan izvor je [docs/README.md](https://github.com/tihidon/test1/blob/main/docs/README.md).

| Fajl | Namena |
|---|---|
| `sc-func-01-registar.cjs` | generiše registar funkcija za [SC-FUNC-01 §5](../tehnika/standardi/SC-FUNC-01-REGISTAR-FUNKCIJA-I-POZIVA.md#5-potpuni-registar-imenovanih-funkcija-generisan): moduli, imenovane funkcije, linije, parametri, broj poziva po imenu |

Samo čita `index.html`; ne izvršava igru i ne menja fajlove. Zavisnosti se instaliraju van repoa:

```bash
mkdir -p /tmp/sc-tools && (cd /tmp/sc-tools && npm install acorn@8.19.0 acorn-walk@8.3.5)
NODE_PATH=/tmp/sc-tools/node_modules node docs/alati/sc-func-01-registar.cjs index.html > /tmp/registar.md
```

Izlaz `0` = svi izvršni blokovi parsirani; `1` = greška parsiranja (ispisana na stderr); `2` = pogrešna upotreba. Provereno 25.11.2026 na `2d66e55`: izlaz 0, 5 blokova, 983 funkcijska čvora.

Ostali alati (SC-CODE-01, SC-REND-01, SC-RAD-01) žive u `tihidon/snail-city-test`; komande za pokretanje nad ovim repoom su u [SC-CODE-01 §8](../tehnika/standardi/SC-CODE-01-CSS-DOM-FUNKCIJE.md#8-alat-i-ratchet-provera).
