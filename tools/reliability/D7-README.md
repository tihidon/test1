# Lokalna D7 proba

Pokreni iz repozitorijuma sa Python 3, bez dodatnih paketa.

```powershell
$d7 = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'A snail city\D7'
py -3 tools/reliability/d7_local.py generate --root "$d7" --candidate "model; puna revizija skilla" --controller "ime kontrolora"
```

Ako su Dokumenti sinhronizovani ili dostupni evaluatoru, koristi privatni lokalni folder koji nije povezan sa njegovom sesijom. Runda dobija novi folder i 60 sintetičkih slučajeva, po 20 po klasi. Opcija `--pilot` pravi šest za probu prenosa.

Predaj evaluatoru samo `ulazi.json`. `zakljucano.json` beleži vreme i hash ulaza, alata i ključa. Folder `kontrolor` ostaje kod internog kontrolora. Novi razgovor dobija samo ulaz, bez pristupa privatnoj putanji. Zabeleži stvarni ID sesije, model, učitanu reviziju i dozvole odvojeno u SC-DEC-01.

```powershell
py -3 tools/reliability/d7_local.py grade "PUTANJA_RUNDE" "PUTANJA_PONUDJENOG_JSON_ODGOVORA" --session "STVARNI_ID_SESIJE"
```

Ocenjivač prvo čuva originalne bajtove predaje i njihov hash. Zatim poredi status, razlog i tačne lokatore. Svaki pokušaj dobija zaseban zapis. Prag je 57/60, najmanje 19/20 u svakoj klasi i sve označene kritične kontrole tačne. Izveštaj izdvaja neslaganja za interni pregled.

Ovaj generator pokriva sintetičke varijante trajnosti rezultata trke. Formalni ugovor mora odobriti pokrivenost i kritične slučajeve za traženi domen pre predaje. Automatski rezultat sam ne potvrđuje identitet sesije, E0–E7 ili D7 ovlašćenje. Prethodni ZIP sa šest objavljenih rešenja služi za vežbu.
