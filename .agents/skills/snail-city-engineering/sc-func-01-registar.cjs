#!/usr/bin/env node
// SC-FUNC-01 — generator registra funkcija za jedan izvršni index.html.
// Samo čita fajl; ne izvršava igru. Upotreba:
//   NODE_PATH=<folder sa acorn i acorn-walk> node docs/alati/sc-func-01-registar.cjs index.html > izlaz.md
// Zavisnosti (van repoa): npm install acorn@8.19.0 acorn-walk@8.3.5
'use strict';
const fs = require('fs');
const crypto = require('crypto');
const acorn = require('acorn');
const walk = require('acorn-walk');

const file = process.argv[2];
if (!file) { console.error('upotreba: sc-func-01-registar.cjs <index.html>'); process.exit(2); }
const html = fs.readFileSync(file, 'utf8');
const sha = crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const EXEC = new Set(['', 'text/javascript', 'application/javascript', 'module']);

const blocks = [];
const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
for (let m; (m = re.exec(html));) {
  const t = /\btype\s*=\s*["']([^"']*)["']/i.exec(m[1]);
  if (!EXEC.has(t ? t[1].trim().toLowerCase() : '')) continue;
  const bodyStart = m.index + m[0].indexOf('>') + 1;
  const id = (/\bid\s*=\s*["']([^"']*)["']/i.exec(m[1]) || [])[1] || null;
  blocks.push({ id, line: html.slice(0, bodyStart).split('\n').length, src: m[2] });
}

// Granice modula: linija dodele `modules.<ime>=` ili `i18n=` u glavnom bloku.
const lines = html.split('\n');
const starts = [];
lines.forEach((l, i) => {
  const mm = /^\s*(?:modules\.([A-Za-z0-9]+)\s*=|(?:const |let )?(i18n)\s*=)/.exec(l);
  if (mm) starts.push({ name: mm[1] || mm[2], line: i + 1 });
});
const moduleOf = (line, block) => {
  let cur = null;
  for (const s of starts) if (s.line <= line && s.line >= block.line) cur = s.name;
  return cur || (block.id ? `#${block.id}` : `blok@L${block.line}`);
};

const fns = [];
const callNames = new Map();
const bump = (n) => n && callNames.set(n, (callNames.get(n) || 0) + 1);
let parseErrors = 0;
for (const b of blocks) {
  let ast;
  try { ast = acorn.parse(b.src, { ecmaVersion: 'latest', sourceType: 'script', locations: true, allowHashBang: true }); }
  catch (e) { parseErrors++; console.error(`parse greška u bloku @L${b.line}: ${e.message}`); continue; }
  const L = (n) => b.line + n.loc.start.line - 1;
  const E = (n) => b.line + n.loc.end.line - 1;
  walk.fullAncestor(ast, (node, _st, anc) => {
    if (node.type === 'CallExpression' || node.type === 'NewExpression') {
      const c = node.callee;
      bump(c.type === 'Identifier' ? c.name : c.type === 'MemberExpression' && !c.computed ? c.property.name : null);
    }
    if (!/Function/.test(node.type) || node.type === 'FunctionBody') return;
    const parent = anc[anc.length - 2];
    let name = node.id?.name || null;
    if (!name && parent) {
      if (parent.type === 'VariableDeclarator' && parent.id.type === 'Identifier') name = parent.id.name;
      else if ((parent.type === 'Property' || parent.type === 'MethodDefinition' || parent.type === 'PropertyDefinition') && !parent.computed)
        name = parent.key.name ?? parent.key.value;
      else if (parent.type === 'AssignmentExpression' && parent.left.type === 'MemberExpression' && !parent.left.computed)
        name = parent.left.property.name;
    }
    const params = node.params.map((p) => b.src.slice(p.start, p.end).replace(/\s+/g, ' ')).join(', ');
    fns.push({ name, module: moduleOf(L(node), b), start: L(node), end: E(node), params });
  });
}
fns.sort((a, b) => a.start - b.start);

const esc = (s) => String(s).replace(/\|/g, '\\|').replace(/`/g, "'");
const out = [];
const byMod = new Map();
for (const f of fns) { if (!byMod.has(f.module)) byMod.set(f.module, []); byMod.get(f.module).push(f); }
out.push(`<!-- generisano: sc-func-01-registar.cjs; ne menjati ručno (SC-F08) -->`);
out.push(`Fajl: \`${file}\` · SHA-256 \`${sha}\` · izvršnih blokova: ${blocks.length} · greške parsiranja: ${parseErrors}`);
out.push(`Funkcijskih čvorova: ${fns.length} (imenovanih ${fns.filter((f) => f.name).length}, anonimnih ${fns.filter((f) => !f.name).length}).`);
out.push('');
out.push('| Modul | Funkcija | Imenovanih | Od linije |');
out.push('|---|---:|---:|---:|');
for (const [m, list] of byMod) out.push(`| ${esc(m)} | ${list.length} | ${list.filter((f) => f.name).length} | ${list[0].start} |`);
for (const [m, list] of byMod) {
  out.push('', `### ${esc(m)}`, '', '| Ime | Linije | Parametri | Poziva po imenu |', '|---|---|---|---:|');
  for (const f of list.filter((x) => x.name))
    out.push(`| \`${esc(f.name)}\` | L${f.start}–${f.end} | ${f.params ? '`' + esc(f.params.slice(0, 80)) + '`' : '—'} | ${callNames.get(f.name) || 0} |`);
}
process.stdout.write(out.join('\n') + '\n');
process.exit(parseErrors ? 1 : 0);
