
  // PW-01: register the ONE existing scoped Service Worker independently of game boot.
  // This must run before large embedded art and before any game/render/save errors.
  (function(){
    'use strict';
    var diagnostic={version:'0.8.92',state:'unsupported',ready:false,controlled:false,error:null};
    window.SC_PWA_STATUS=diagnostic;
    if(!('serviceWorker' in navigator) ||
       !(location.protocol==='https:'||location.hostname==='localhost'||location.hostname==='127.0.0.1') ||
       globalThis.Capacitor?.isNativePlatform?.()) return;
    diagnostic.state='registering';
    var nav=navigator.serviceWorker;
    diagnostic.controlled=Boolean(nav.controller);
    nav.addEventListener('controllerchange',function(){diagnostic.controlled=Boolean(nav.controller);});
    nav.register('./sw.js',{scope:'./',updateViaCache:'none'}).then(function(reg){
      diagnostic.state='registered';
      diagnostic.scope=reg.scope;
      return nav.ready;
    }).then(function(){
      diagnostic.ready=true;
      diagnostic.controlled=Boolean(nav.controller);
      diagnostic.state='offline-ready';
      console.info('[Snail City] PW-01 offline shell ready');
    }).catch(function(err){
      diagnostic.state='failed';diagnostic.error=String(err&&err.message||err);
      console.error('[Snail City] PW-01 offline installation failed:',err);
    });
  })();
  