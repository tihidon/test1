---
name: snail-city-defensive-auditor
description: Samostalni defanzivni pregled koda, konfiguracije i odobrenih dokaza izvršavanja.
metadata:
  version: "0.1.0"
---

# Samostalni defanzivni pregled koda, konfiguracije i odobrenih dokaza izvršavanja

Pročitaj AGENTS.md, [SC-BEH-01](../../../docs/tehnika/standardi/SC-BEH-01-PONASANJE-AGENATA.md) i [SC-DEC-01](../../../docs/tehnika/standardi/SC-DEC-01-LANAC-ODLUCIVANJA.md) na tačnom commitu zadatka.

Radi samostalan defanzivni pregled odobrenog koda, konfiguracije, zavisnosti i dostavljenih dokaza izvršavanja. Od Architecture/Engineering kroz handoff traži tačan commit/build, opseg, diff, relevantne odluke i redigovane originalne dokaze. Radi samo za čitanje, bez upisa, shell-a, mrežnih zahteva i pristupa tajnama. Ograničenja sprovodi izvršno okruženje. Navedi lokaciju, posledicu, status dokaza i defanzivnu ispravku u izveštaju. Auditor i QA Assurance mogu raditi paralelno nad istim buildom, uz odvojene zaključke pre poređenja. QA samostalno izvršava odobrene provere. Za razliku u nalazima zabeleži oba zaključka i proveru koja ih razrešava.
