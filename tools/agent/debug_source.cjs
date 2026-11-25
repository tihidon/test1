'use strict';
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process'),crypto=require('node:crypto');
const ROOT=path.resolve(__dirname,'../..'),hash=s=>crypto.createHash('sha256').update(s).digest('hex');
function read(root,commit,file){
 if(commit){if(!/^[a-f0-9]{40}$/.test(commit))throw Error('full baseline SHA required');
 return cp.execFileSync('git',['show',commit+':'+file],{cwd:root,encoding:'utf8',maxBuffer:32*1024*1024,timeout:30000});}
 const p=fs.realpathSync(path.resolve(root,file));
 if(!p.startsWith(fs.realpathSync(root)+path.sep))throw Error('source outside checkout');
 return fs.readFileSync(p,'utf8');
}
function inputs(root=ROOT,commit=null){
 const m=JSON.parse(read(root,commit,'src/html/blocks.json')),out=[];
 for(const b of m){
  if(b.element!=='script')continue;
  const type=(/\btype\s*=\s*["']([^"']*)["']/i.exec(b.open_tag)?.[1]||'').toLowerCase().trim();
  if(!['','text/javascript','application/javascript','module'].includes(type))continue;
  if(!/^src\/js\/[a-zA-Z0-9_-]+\.js$/.test(b.file)||/\bsrc\s*=/i.test(b.open_tag))throw Error('unsupported script '+b.file);
  out.push({file:b.file,type:type==='module'?'module':'script',source:read(root,commit,b.file)});
 }
 if(!out.length||new Set(out.map(x=>x.file)).size!==out.length)throw Error('zero/duplicate scripts');
 out.push({file:'sw.js',type:'script',source:read(root,commit,'sw.js')});
 return out;
}
module.exports={ROOT,hash,inputs};
