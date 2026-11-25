"""SC-CODE-01 — merenje CSS/DOM/JS pravila i ratchet provera (samo čita, ne menja kod).

Upotreba:
  python3 -I sc_code_metrics.py <index.html>                     # ispis metrika (JSON)
  python3 -I sc_code_metrics.py <index.html> --baseline <b.json> # izlaz 1 ako je neka metrika porasla

Zavisnosti (instalirati u privremeni folder, ne u repo):
  pip install tinycss2==1.5.1          npm install acorn@8.15.0 acorn-walk@8.3.4
  Promenljiva NODE_PATH mora da pokazuje na node_modules sa acorn paketima.
"""
from __future__ import annotations

import argparse
import collections
import html.parser
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TypedDict

import tinycss2

HERE = Path(__file__).resolve().parent
EXEC_TYPES = {'', 'text/javascript', 'application/javascript', 'module'}
BIG_VALUE = 4096  # CSS-01 projektni prag

# Metrike koje smeju samo da padaju (ratchet). Ključ: (izvor, ime).
RATCHET = [
    ('css', 'styleBlocks'), ('css', 'stylesheetLinks'), ('css', 'selectorsOver3Parts'),
    ('css', 'duplicateSelectors'), ('css', 'overriddenDeclarations'), ('css', 'important'),
    ('css', 'idSelectors'), ('css', 'rawHexColors'), ('css', 'bigCustomProperties'),
    ('css', 'distinctMediaQueries'),
    ('js', 'functionsOver60Lines'), ('js', 'functionsOver150Lines'), ('js', 'functionsDepthOver3'),
    ('js', 'functionsOver4Params'), ('js', 'chainedTernary'), ('js', 'innerHTMLAppend'),
    ('js', 'styleWrites'), ('js', 'geometryReads'),
]


class Extract(TypedDict):
    css: list[str]
    js: list[str]
    links: int


class _Extractor(html.parser.HTMLParser):
    """Izvlači tela <style> i izvršnih <script> blokova bez izvršavanja."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.out: Extract = {'css': [], 'js': [], 'links': 0}
        self._target: str | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or '') for k, v in attrs}
        if tag == 'link' and 'stylesheet' in a.get('rel', '').lower().split():
            self.out['links'] += 1
        if tag == 'style':
            self._target, self._buf = 'css', []
        elif tag == 'script' and 'src' not in a and a.get('type', '').lower() in EXEC_TYPES:
            self._target, self._buf = 'js', []

    def handle_data(self, data: str) -> None:
        if self._target:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._target and tag in ('style', 'script'):
            self.out[self._target].append(''.join(self._buf))  # type: ignore[literal-required]
            self._target = None


def selector_parts(selector: str) -> int:
    """Broj složenih delova selektora odvojenih kombinatorima (razmak, >, +, ~)."""
    flat = selector
    while re.search(r'\([^()]*\)', flat):
        flat = re.sub(r'\([^()]*\)', '', flat)  # :is()/:not() sadržaj ne pravi nove delove
    return len([p for p in re.split(r'\s*[>+~]\s*|\s+', flat.strip()) if p])


def css_metrics(blocks: list[str], links: int) -> dict[str, int]:
    css = '\n'.join(blocks)
    selectors: list[tuple[str, str, list]] = []
    media: set[str] = set()

    def walk(rules: list, ctx: str) -> None:
        for rule in rules:
            if rule.type == 'qualified-rule':
                decls = [d for d in tinycss2.parse_declaration_list(rule.content, skip_whitespace=True, skip_comments=True)
                         if d.type == 'declaration']
                for sel in tinycss2.serialize(rule.prelude).split(','):
                    selectors.append((ctx, sel.strip(), decls))
            elif rule.type == 'at-rule' and rule.content is not None:
                kw = rule.lower_at_keyword
                prelude = re.sub(r'\s+', '', tinycss2.serialize(rule.prelude))
                if kw == 'media':
                    media.add(prelude)
                if kw in ('media', 'supports', 'container', 'layer'):
                    walk(tinycss2.parse_rule_list(rule.content, skip_whitespace=True, skip_comments=True), f'{ctx}@{kw}{prelude}')

    walk(tinycss2.parse_stylesheet(css, skip_whitespace=True, skip_comments=True), '')
    seen: set[tuple[str, str, str]] = set()
    overridden = 0
    for ctx, sel, decls in selectors:
        for d in decls:
            key = (ctx, sel, d.lower_name)
            overridden += key in seen and not d.important
            seen.add(key)
    per_selector = collections.Counter((ctx, sel) for ctx, sel, _ in selectors)
    no_strings = re.sub(r'"[^"]*"|\'[^\']*\'|url\([^)]*\)', '', css)
    return {
        'bytes': len(css.encode('utf-8')),
        'styleBlocks': len(blocks),
        'stylesheetLinks': links,
        'selectors': len(selectors),
        'selectorsOver3Parts': sum(selector_parts(s) > 3 for _, s, _ in selectors),
        'maxSelectorParts': max((selector_parts(s) for _, s, _ in selectors), default=0),
        'duplicateSelectors': sum(1 for n in per_selector.values() if n > 1),
        'overriddenDeclarations': overridden,
        'important': sum(d.important for _, _, ds in selectors for d in ds),
        'idSelectors': sum('#' in s for _, s, _ in selectors),
        'rawHexColors': len(re.findall(r'#[0-9a-fA-F]{3,8}\b', no_strings)),
        'bigCustomProperties': sum(1 for _, _, ds in selectors for d in ds
                                   if d.name.startswith('--') and len(tinycss2.serialize(d.value)) > BIG_VALUE),
        'distinctMediaQueries': len(media),
    }


def js_metrics(blocks: list[str]) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        files = []
        for i, body in enumerate(blocks):
            p = Path(tmp) / f'script-{i + 1}.js'
            p.write_text(body, encoding='utf-8')
            files.append(str(p))
        run = subprocess.run(['node', str(HERE / 'js_metrics.cjs'), *files],
                             capture_output=True, text=True, env=os.environ.copy(), check=False)
    if run.returncode != 0:
        sys.exit(f'js_metrics.cjs nije uspeo:\n{run.stderr}')
    return json.loads(run.stdout)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('html', type=Path)
    ap.add_argument('--baseline', type=Path)
    args = ap.parse_args()
    parser = _Extractor()
    parser.feed(args.html.read_text(encoding='utf-8'))
    ex = parser.out
    report = {'file': args.html.name, 'css': css_metrics(ex['css'], ex['links']), 'js': js_metrics(ex['js'])}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not args.baseline:
        return 0
    base = json.loads(args.baseline.read_text(encoding='utf-8'))
    worse = [f'{src}.{key}: {base[src][key]} → {report[src][key]}'
             for src, key in RATCHET if report[src][key] > base[src][key]]
    if worse:
        print('RATCHET FAIL — porasle metrike:\n  ' + '\n  '.join(worse), file=sys.stderr)
        return 1
    print('RATCHET PASS — nijedna praćena metrika nije porasla.', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
