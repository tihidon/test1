/* Snail City v0.8.92 — PW-01 offline bootstrap and deterministic app shell.
 * One SW for current registration scope. No dynamic/API caching. Offline data in
 * IndexedDB is never removed or modified by this script.
 */
'use strict';
const CACHE_NAME = 'snail-city-shell-0.8.92-css-unified-p8-r1';
const OWNED_PREFIXES = ['snail-city-08', 'snail-city-shell-'];
const CORE_PATHS = [
  './index.html', './manifest.webmanifest',
  './img/icon-192.png','./img/icon-512.png','./img/icon-maskable.png',
  './privacy.html','./delete-account.html'
];
const CORE_SIZE_LIMIT = 16 * 1024 * 1024;
const PER_RESOURCE_LIMIT = 12 * 1024 * 1024;
const SCOPE = new URL(self.registration.scope);
const CORE = new Map(CORE_PATHS.map(path => {
  const url = new URL(path,SCOPE);
  return [url.href, url];
}));
const ENTRY = new URL('./index.html', SCOPE).href;
if (CORE.size !== CORE_PATHS.length) throw Error('Duplicate PWA resources');
function isWithinScope(url){return url.origin===SCOPE.origin && url.pathname.startsWith(SCOPE.pathname);}
function isCore(url){return CORE.has(url.href);}
function isEntryNavigation(url){
  return url.pathname===SCOPE.pathname || url.pathname===new URL('./index.html',SCOPE).pathname;
}
self.addEventListener('install',event=>{
  event.waitUntil((async()=>{
    const cache=await caches.open(CACHE_NAME);
    let total=0;
    try{
      for (const [href] of CORE){
        const response=await fetch(new Request(href,{cache:'reload',credentials:'same-origin'}));
        if (!response.ok || response.type==='opaque' || response.redirected) throw Error('Offline resource unavailable: '+href);
        const bytes=(await response.clone().blob()).size;
        total+=bytes;
        if (bytes>PER_RESOURCE_LIMIT || total>CORE_SIZE_LIMIT) throw Error('Offline shell exceeds bounded budget');
        const type=(response.headers.get('content-type')||'').toLowerCase();
        if (href.endsWith('.png') && !type.includes('image/')) throw Error('PNG returned unexpected MIME type: '+href);
        if (href.endsWith('.webmanifest') && !(/json|manifest/.test(type))) throw Error('Manifest returned unexpected MIME type: '+href);
        if (href.endsWith('.html') && !type.includes('text/html')) throw Error('HTML returned unexpected MIME type: '+href);
        await cache.put(href,response);
      }
      // No partial release is activated; a successful fully cached install can update old installs.
      await self.skipWaiting();
    }catch(error){
      await caches.delete(CACHE_NAME);
      throw error;
    }
  })());
});
self.addEventListener('activate',event=>{
  event.waitUntil((async()=>{
    const names=await caches.keys();
    await Promise.all(names.filter(name=>name!==CACHE_NAME && OWNED_PREFIXES.some(prefix=>name.startsWith(prefix)))
      .map(name=>caches.delete(name)));
    await self.clients.claim();
  })());
});
self.addEventListener('fetch',event=>{
  const req=event.request;
  if(req.method!=='GET')return;
  const url=new URL(req.url);
  if(!isWithinScope(url))return;
  if(req.mode==='navigate'){
    // SPA entry only. Other pages have exact offline copies; unknown routes are not rewritten.
    if(isEntryNavigation(url)){
      event.respondWith((async()=>{
        try{
          const live=await fetch(req);
          if(live.ok)return live;
        }catch(_){}
        const cached=await (await caches.open(CACHE_NAME)).match(ENTRY);
        return cached || Response.error();
      })());
    }else if(isCore(url)){
      event.respondWith((async()=>{
        try{const live=await fetch(req);if(live.ok)return live;}catch(_){}
        return (await (await caches.open(CACHE_NAME)).match(url.href)) || Response.error();
      })());
    }
    return;
  }
  if(!isCore(url))return; // Never cache CDN/Supabase, saves, arbitrary assets, query variants.
  event.respondWith((async()=>{
    const cached=await (await caches.open(CACHE_NAME)).match(url.href);
    return cached || fetch(req);
  })());
});
