// Редкие случаи: ТП (одному и обоим), отбор с остановкой. Ожидается «edge fails 0».
globalThis.location={hostname:'test.kazbilliard.com',hash:'',origin:'https://test.kazbilliard.com'};const fs=require('fs');const h=fs.readFileSync(__dirname+'/../index.html','utf8');
let js=h.split('<script>')[1].split('/* ============ helpers')[0];js=js.replace(/function save\(\)\{[^\n]*\n/,'function save(){}\n');
eval(js+';globalThis.E={build,simulate,maybeDraw};');
const P=n=>[...Array(n)].map((_,i)=>({id:'p'+i,name:'p'+i}));let fails=0;const F=(...a)=>{fails++;console.log('FAIL',...a)};
const open=b=>b.all.filter(m=>['ready','wait','live'].includes(m.state)).length;
for(const f of ['se','de','rr','gp'])for(const po of (f==='de'?['auto',0]:[null]))for(let n=3;n<=36;n++){if(f==='rr'&&n>16||f==='gp'&&n<8)continue;
 for(let rep=0;rep<5;rep++){const T={id:'t',draw:true,results:{},players:P(n),format:f,playoff:po,raceTo:2,status:'live',groups:{count:2,advance:2}};
  for(let i=0;i<9999;i++){const r=E.build(T).all.filter(m=>m.state==='ready');if(!r.length)break;const m=r[0],x=Math.random();
   T.results[m.id]=x<.1?{a:m.a.id,b:m.b.id,sa:0,sb:0,tp:'both',done:true}:x<.25?{a:m.a.id,b:m.b.id,sa:0,sb:0,tp:Math.random()<.5?'a':'b',done:true}:{a:m.a.id,b:m.b.id,sa:2,sb:Math.floor(Math.random()*2),done:true};E.maybeDraw(T)}
  const b=E.build(T);const pl=b.places?b.places.flatMap(p=>p.ids):[];
  if(!b.finished||open(b))F('stuck',f,po,n);else if(new Set(pl).size!==pl.length||pl.some(x=>!x))F('places',f,po,n)}}
for(let n=6;n<=64;n++)for(const po of ['auto',8,16,32]){const T0={id:'t',draw:true,results:{},players:P(n),format:'de',playoff:po,raceTo:2,status:'live'};const K=E.build(T0).K;if(!K)continue;
 for(const s of [K,K/2,K/4].filter(x=>x>=4)){const T={...T0,results:{},stopAt:s};E.simulate(T,9999);const b=E.build(T);const q=(b.q||[...(b.up||[]),...(b.low||[])]).filter(x=>x.t==='p');
  if(!b.finished||open(b))F('stop stuck',n,K,s);else if(q.length!==s)F('stop q',n,K,s,q.length)}}
console.log('edge fails',fails);
