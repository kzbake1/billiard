// опоздавший игрок: встаёт в свободное место, сыгранное не меняется, турнир доигрывается
globalThis.location={hostname:'test.kazbilliard.com',hash:'',origin:'https://test.kazbilliard.com'};const fs=require('fs');const h=fs.readFileSync(__dirname+'/../index.html','utf8');
let js=h.split('<script>')[1].split('/* ============ helpers')[0];js=js.replace(/function save\(\)\{[^\n]*\n/,'function save(){}\n');
eval(js+';globalThis.E={build,simulate,lateSpots};');
let fails=0,cases=0,added=0;
const snap=b=>Object.fromEntries(b.all.filter(m=>m.state==='done').map(m=>[m.id,m.a.id+'|'+m.b.id+'|'+m.res.sa+':'+m.res.sb]));
for(const f of ['se','de','rr','gp'])for(let n=5;n<=30;n++)for(const k of [0,1,3,8]){
  const T={id:'t',results:{},players:[...Array(n)].map((_,i)=>({id:'p'+i,name:'p'+i,no:i+1})),format:f,raceTo:2,status:'live',playoff:'auto',groups:{count:2,advance:2}};
  if(f==='rr'&&n>16)continue;E.simulate(T,k);const b0=E.build(T);const s0=snap(b0);const r=E.lateSpots(T);cases++;
  if(!r.spots)continue;
  for(const sp of r.spots){const T2=JSON.parse(JSON.stringify(T));T2.players.push(Object.assign({id:'L',name:'L',no:99},sp.extra));const b1=E.build(T2);const s1=snap(b1);
    for(const id in s0)if(s1[id]!==s0[id]){fails++;console.log('CHANGED',f,n,k,JSON.stringify(sp.extra),id);break}
    if(!b1.all.some(m=>(m.a.id==='L'||m.b.id==='L')&&m.state==='ready')){fails++;console.log('NOMATCH',f,n,k,JSON.stringify(sp.extra))}
    E.simulate(T2,99999);const b2=E.build(T2);const pl=b2.places?b2.places.flatMap(p=>p.ids):[];
    if(!b2.finished||!pl.includes('L')||new Set(pl).size!==n+1){fails++;console.log('NOFINISH',f,n,k,JSON.stringify(sp.extra),b2.finished,pl.length)}
    added++}
}
console.log('cases',cases,'added',added,'fails',fails);
