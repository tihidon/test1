# SC-CLI-01 — instalacija i validacija agenta

Datum 25.11.2026. Projektni skill v1.1.0 u `.agents/skills/snail-city-engineering/SKILL.md` je Codex repository-local instalacija, ne dokaz učitavanja u već otvorenom ChatGPT/Codex hostu. Pokrenuti novu Codex sesiju u checkout-u odgovarajuće grane i eksplicitno pozvati `$snail-city-engineering`. GitHub commit ne može sam instalirati CLI na korisnički Windows računar ili aktivirati postojeći ChatGPT skill.

## Zavisnosti (odvojene od igre)
- Python >=3.11 i Git; Node.js za syntax/AST; Acorn 8.19.0 + acorn-walk 8.3.5 prema postojećem docs/alati. Instalirati u zaseban dev direktorijum; ne dodavati package.json u igru.
- Official skills-ref 0.1.0 iz upstream agentskills/agentskills commita 83021e2be457a9b6679148719c1f6074f0ad975e; upstream traži click>=8.0, strictyaml>=1.7.3 i hatchling za build. Mrežni pristup GitHub/PyPI, virtualenv, pip i PATH za CLI. Pinned upstream, direktni parser paketi; za punu reproduktivnost posebno zaključati i tranzitivne Python/Node zavisnosti nakon odobrene provere. Ne instalirati neproverenu zamenu.
- Codex CLI ili desktop kompatibilan host, autorizovan nalog, checkout repoa i shell permissions. Nije isto što i skills-ref. Chromium/Playwright za stvarni runtime QA; fizički Android za device dokaz.

## Komande (PowerShell, u root repoa)
```powershell
$venv = Join-Path $env:TEMP 'sc-skill-venv'
python -m venv $venv
& "$venv\Scripts\python.exe" -m pip install "git+https://github.com/agentskills/agentskills.git@83021e2be457a9b6679148719c1f6074f0ad975e#subdirectory=skills-ref"
$env:Path = "$venv\Scripts;$env:Path"
skills-ref validate .agents/skills/snail-city-engineering
skills-ref read-properties .agents/skills/snail-city-engineering
skills-ref to-prompt .agents/skills/snail-city-engineering
$nodeDir = Join-Path $env:TEMP 'sc-agent-node'
npm install --prefix $nodeDir --ignore-scripts --no-audit --no-fund acorn@8.19.0 acorn-walk@8.3.5
$env:NODE_PATH = Join-Path $nodeDir 'node_modules'
python tools/agent/check_build.py --require-publish-match
python tools/test_roundtrip.py
node tools/agent/audit_loops.cjs
python -m unittest discover -s tools/agent -p 'test_*.py'
node --test tools/agent/test_audit_loops.cjs
```

POSIX analog: python -m venv izvan repoa, source venv/bin/activate, npm --prefix u privremeni direktorijum, export NODE_PATH. Pokretati samo pouzdan pregledan checkout; shell nije security sandbox. Ne slati privatne logove/sejvove/token u javne servise.

## Provera stvarnog agenta
Pokrenuti sveže sesije, zabeležiti agent/CLI verziju, model, target SHA, task, stvarne alate i rezultat (bez privatnih podataka). Deset scenarija: postojeći owner pre novog; dinamički callback ne brisati; dupli CSS/cascade; zaglavljen while; validna RAF petlja; timer/listener nakon close; resize/invalidation PL-01; neispravan save; old reference overwrite; nedostupan alat = BLOCKED. Testirati i negativni trigger na nepovezan zadatak. Izvršenje alata i artefakti, ne samo odgovor agenta, moraju potvrditi gate. Testirati u izolovanom checkout-u; nikad stvarni main/igrački save. Oceni PASS/FAIL/BLOCKED za svaku tvrdnju. Uporediti agent sa i bez skilla na istom fixture-u kad je moguće. CLI format validacija nije agent eval.
 
## Izvori
- https://github.com/agentskills/agentskills/tree/83021e2be457a9b6679148719c1f6074f0ad975e/skills-ref
- https://agentskills.io/specification
- https://developers.openai.com/api/reference/cli
- https://developers.openai.com/blog/eval-skills

## Stanje ovog kandidata
Repository source inspection izvedena; stvarno izvršenje nove Python/JS implementacije, official CLI, agent activation, Chromium i uređaj zahtevaju izvršno okruženje. Ne prepisivati ranijih 11/11 fixture testova sa drugog overlay-a kao rezultate ovog commita. GitHub CI logovi kada postoje su merodavni; bez njih NOT RUN/BLOCKED.

## Chrome DevTools MCP — P0 kandidat (26.11.2026)
Upstream release [1.14.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases/tag/chrome-devtools-mcp-v1.14.0), 24.11.2026. Node engine ^20.19.0 / ^22.12.0 / >=23; use supported LTS, official Chrome 149+ for URL allowlist. Tooling only. Opt-in configuration: `tools/agent/chrome-devtools-mcp.toml`; merge table into trusted Codex host config without overwriting existing settings. Or run `codex mcp add chrome-devtools -- npx -y chrome-devtools-mcp@1.14.0 --headless --isolated --no-usage-statistics --no-performance-crux --allowed-url-pattern=http://127.0.0.1:*/*`; verify `codex mcp list` and actual fresh-session invocation. Do not duplicate server through plugin and CLI. No remote debugging port, personal profile, production origin or credentials. Use local synthetic save and loopback publish copy; allowlist is defense in depth, not process/network isolation. Do not disable sandbox or TLS checks. PWA OS tooling requires separate reviewed pipe-connected profile and `--category-pwa`; headless smoke does not prove installed PWA.
Official skills: chrome-devtools, chrome-devtools-cli, memory-leak-debugging, troubleshooting, debug-optimize-lcp, a11y-debugging, cookie-debugging. Use matching release's skills; actual host installation separate. Sources: [release config](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/chrome-devtools-mcp-v1.14.0/docs/configuration.md), [client config](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/chrome-devtools-mcp-v1.14.0/docs/client-configurations.md), [Codex MCP](https://developers.openai.com/codex/mcp/). Direct package pinned; transitive lock/integrity not independently verified.
Separate CI candidate workflow: `python tools/agent/mcp_smoke.py /tmp/sc-mcp-new` on Linux with dependencies. Requires MCP initialize, complete tools/list and actual DOM marker on synthetic loopback page; preserves RPC and stderr. No gameplay, actual Codex agent eval, PWA or memory/trace execution claim from discovery. Failures follow SC-DEBUG-01 pivot. No automatic upgrade or merge.
