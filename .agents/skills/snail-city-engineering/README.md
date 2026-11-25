# Snail City Engineering v1.1.0 portable skill
This is an archive-only skill tree, not game source; never merge or deploy this branch. Extract GitHub ZIP, rename extracted outer directory to snail-city-engineering if installing manually, then import the directory or ZIP into compatible host. SKILL.md, agents/, assets/, references/, scripts/ at root. Do not overwrite actual project source or AGENTS.md. Private project materials, do not publish publicly.
Activate with $snail-city-engineering; tools need trusted checkout and shell permissions. Upload alone does not run scripts. Read current project rules first.
Windows PowerShell in extracted skill root:
    $venv = Join-Path $env:TEMP 'sc-skill-venv'
    python -m venv $venv
    & "$venv\Scripts\python.exe" -m pip install "git+https://github.com/agentskills/agentskills.git@83021e2be457a9b6679148719c1f6074f0ad975e#subdirectory=skills-ref"
    $env:Path = "$venv\Scripts;$env:Path"
    python scripts/validate_skill.py
    $nodeDir = Join-Path $env:TEMP 'sc-agent-node'
    npm install --prefix $nodeDir --ignore-scripts --no-audit --no-fund acorn@8.19.0 acorn-walk@8.3.5
    $env:NODE_PATH = Join-Path $nodeDir 'node_modules'
    python scripts/run_checks.py --fixtures
    python scripts/run_checks.py --repo "C:\path\to\test1"
No new game dependencies. See references/cli.md and VALIDATION.md.
