// SC-CODE-01 — JS i DOM metrike (samo merenje, ne menja kod).
// Upotreba: node js_metrics.cjs <fajl.js> [...]   → JSON na stdout
// Zavisnosti (van repoa, u privremenom folderu): acorn@8.15.0, acorn-walk@8.3.4
'use strict';
const fs = require('fs');
const acorn = require('acorn');
const walk = require('acorn-walk');

const CONTROL = new Set(['IfStatement', 'ForStatement', 'ForInStatement', 'ForOfStatement',
  'WhileStatement', 'DoWhileStatement', 'SwitchStatement', 'TryStatement']);
const FN = new Set(['FunctionDeclaration', 'FunctionExpression', 'ArrowFunctionExpression']);
const GEOMETRY = new Set(['getBoundingClientRect', 'getComputedStyle', 'offsetWidth', 'offsetHeight',
  'offsetTop', 'offsetLeft', 'clientWidth', 'clientHeight', 'scrollWidth', 'scrollHeight', 'scrollTop']);
const CALLS = ['addEventListener', 'removeEventListener', 'createElement', 'insertAdjacentHTML',
  'querySelector', 'querySelectorAll', 'requestAnimationFrame', 'setInterval', 'setTimeout'];

/** Najveća dubina if/petlje/switch/try u telu funkcije; else-if lanac se broji kao jedan nivo,
 *  ugnježdene funkcije se mere zasebno. */
function controlDepth(fnNode) {
  let max = 0;
  const visit = (node, depth, elseIf) => {
    if (!node || typeof node.type !== 'string') return;
    if (node !== fnNode && FN.has(node.type)) return;
    const d = CONTROL.has(node.type) && !elseIf ? depth + 1 : depth;
    if (d > max) max = d;
    for (const [key, value] of Object.entries(node)) {
      if (key === 'loc') continue;
      const children = Array.isArray(value) ? value : [value];
      for (const child of children) {
        if (!child || typeof child.type !== 'string') continue;
        const isElseIf = node.type === 'IfStatement' && key === 'alternate' && child.type === 'IfStatement';
        visit(child, d, isElseIf);
      }
    }
  };
  visit(fnNode, 0, false);
  return max;
}

const isIife = (fnNode, parent) => parent && parent.type === 'CallExpression' && parent.callee === fnNode;

function nameOf(fnNode, parent) {
  if (fnNode.id) return fnNode.id.name;
  if (!parent) return '(anon)';
  if (parent.type === 'VariableDeclarator' && parent.id.type === 'Identifier') return parent.id.name;
  if ((parent.type === 'Property' || parent.type === 'MethodDefinition') && parent.key) return parent.key.name || String(parent.key.value);
  return '(anon)';
}

const functions = [];
const counts = { chainedTernary: 0, innerHTMLAssign: 0, innerHTMLAppend: 0, textContentAssign: 0,
  styleWrites: 0, geometryReads: 0 };
for (const c of CALLS) counts[c] = 0;

for (const file of process.argv.slice(2)) {
  const ast = acorn.parse(fs.readFileSync(file, 'utf8'), { ecmaVersion: 'latest', sourceType: 'script', locations: true, allowHashBang: true });
  walk.fullAncestor(ast, (node, _state, ancestors) => {
    const parent = ancestors[ancestors.length - 2];
    if (FN.has(node.type) && !isIife(node, parent)) {
      functions.push({ file: file.split('/').pop(), line: node.loc.start.line, name: nameOf(node, parent),
        lines: node.loc.end.line - node.loc.start.line + 1, params: node.params.length, depth: controlDepth(node) });
    }
    if (node.type === 'ConditionalExpression'
      && (node.consequent.type === 'ConditionalExpression' || node.alternate.type === 'ConditionalExpression')
      && !(parent && parent.type === 'ConditionalExpression')) counts.chainedTernary++;
    if (node.type === 'CallExpression') {
      const callee = node.callee;
      const name = callee.type === 'Identifier' ? callee.name
        : callee.type === 'MemberExpression' && !callee.computed ? callee.property.name : null;
      if (name && Object.hasOwn(counts, name) && CALLS.includes(name)) counts[name]++;
    }
    if (node.type === 'MemberExpression' && !node.computed) {
      const prop = node.property.name;
      const assigned = parent && parent.type === 'AssignmentExpression' && parent.left === node;
      if (GEOMETRY.has(prop)) counts.geometryReads++;
      if (prop === 'innerHTML' && assigned) counts[parent.operator === '+=' ? 'innerHTMLAppend' : 'innerHTMLAssign']++;
      if (prop === 'textContent' && assigned) counts.textContentAssign++;
      if (assigned && node.object.type === 'MemberExpression' && !node.object.computed && node.object.property.name === 'style') counts.styleWrites++;
    }
  });
}

const sorted = (key) => [...functions].sort((a, b) => b[key] - a[key] || b.lines - a.lines);
const label = (f) => `${f.name}@${f.file}:L${f.line}`;
const result = {
  functions: functions.length,
  functionsOver60Lines: functions.filter((f) => f.lines > 60).length,
  functionsOver150Lines: functions.filter((f) => f.lines > 150).length,
  functionsDepthOver3: functions.filter((f) => f.depth > 3).length,
  maxControlDepth: Math.max(0, ...functions.map((f) => f.depth)),
  functionsOver4Params: functions.filter((f) => f.params > 4).length,
  ...counts,
  topLongest: sorted('lines').slice(0, 8).map((f) => `${label(f)} ${f.lines} lin.`),
  topDeepest: sorted('depth').filter((f) => f.depth > 3).map((f) => `${label(f)} dubina ${f.depth}`),
};
process.stdout.write(JSON.stringify(result, null, 2) + '\n');
