
(function(){
  'use strict';
  // Diagnostic only: bounded in-memory timings, never stores/uploads player data.
  const events=[],longTasks=[];const CAP=220,LT_CAP=32;
  const now=()=>performance.now();
  function emit(kind,label,start,end,detail){
    if(events.length>=CAP)return;
    const t=Number.isFinite(start)?start:now();
    const row={kind,label,startMs:+t.toFixed(2)};
    if(Number.isFinite(end))row.durationMs=+(end-t).toFixed(2);
    if(detail!==undefined)row.note=String(detail).slice(0,60);
    events.push(row);
    if(kind==='span'&&Number.isFinite(end)){
      try{performance.measure('SC P1: '+label,{start:t,end});}catch(_){ }
    }else if(kind==='mark'){
      try{performance.mark('SC P1: '+label);}catch(_){ }
    }
  }
  const api={
    begin:()=>now(),
    mark:(label,detail)=>emit('mark',label,now(),undefined,detail),
    end:(label,begin,detail)=>emit('span',label,begin,now(),detail),
    // Optional, non-blocking Image.decode() probe. Distorts timings; NEVER enable
    // in the reference run. This is promise latency, not a GPU/decode profiler.
    probeDecode:(image,label)=>{
      if(!location.search.includes('scP1Decode=1')||typeof image?.decode!=='function')return;
      const begin=now();
      Promise.resolve().then(()=>image.decode())
        .then(()=>emit('span','decode.promiseLatency.'+label,begin,now(),'opt-in;may-perturb'))
        .catch(()=>emit('mark','decode.rejected.'+label,now()));
    },
    export:()=>({schema:1,build:'0.8.92-css-unified-p6',timeOrigin:performance.timeOrigin,
      timings:events.slice(),longTasks:longTasks.slice(),
      navigation:performance.getEntriesByType('navigation').map(e=>({
        type:e.type,fetchStart:+e.fetchStart.toFixed(1),responseEnd:+e.responseEnd.toFixed(1),
        domInteractive:+e.domInteractive.toFixed(1),domContentLoadedEventEnd:+e.domContentLoadedEventEnd.toFixed(1),
        loadEventEnd:+e.loadEventEnd.toFixed(1),transferSize:e.transferSize,
        encodedBodySize:e.encodedBodySize,decodedBodySize:e.decodedBodySize
      })),
      paint:performance.getEntriesByType('paint').map(e=>({name:e.name,startMs:+e.startTime.toFixed(1)})),
      note:'Timings only. GPU submit timings exclude GPU completion; image onload != precise image decode; no save payloads.'})
  };
  Object.defineProperty(window,'SC_STARTUP_TRACE',{value:api,configurable:false});
  api.mark('head.traceReady');
  if('PerformanceObserver' in window){
    try{new PerformanceObserver(list=>{
      for(const e of list.getEntries()){
        if(longTasks.length>=LT_CAP)break;
        longTasks.push({startMs:+e.startTime.toFixed(1),durationMs:+e.duration.toFixed(1)});
      }
    }).observe({type:'longtask',buffered:true});}catch(_){ }
  }
  document.addEventListener('DOMContentLoaded',()=>api.mark('document.domContentLoaded'),{once:true});
  window.addEventListener('load',()=>api.mark('window.load'),{once:true});
})();
