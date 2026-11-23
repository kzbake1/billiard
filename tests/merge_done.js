// Регресс 22.11: завершённый матч на сервере не должен затираться незавершённым из старой вкладки
const h=require('fs').readFileSync(__dirname+'/../index.html','utf8');
const i=h.indexOf('function merge3'),j=h.indexOf('function applyData');
const jsq=v=>JSON.stringify(v,(k,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.keys(v).sort().reduce((o,kk)=>(o[kk]=v[kk],o),{}):v);
eval(h.slice(i,j).replace('function merge3','globalThis.merge3=function'));
let f=0;const ok=(c,m)=>{if(!c){f++;console.log('FAIL',m)}};
const b={results:{x:{live:true,done:false,ts:1}}},s={results:{x:{done:true,ts:3,sa:2}}};
ok(merge3(b,{results:{x:{live:true,done:false,table:3,ts:5}}},s).results.x.done===true,'старая вкладка затёрла завершённый матч');
ok(merge3(b,{results:{}},s).results.x===undefined,'сброс результата должен работать');
ok(merge3(b,{results:{x:{done:true,ts:9,sa:1}}},s).results.x.sa===1,'новее завершённый выигрывает');
console.log('merge_done fails',f);process.exitCode=f?1:0;
