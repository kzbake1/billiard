globalThis.location={hostname:'test.kazbilliard.com',hash:'',origin:'https://test.kazbilliard.com'};const fs=require('fs');const h=fs.readFileSync('/home/claude/site/index.html','utf8');
let js=h.split('<script>')[1].split('/* ============ helpers')[0];
js=js.replace(/function save\(\)\{[^\n]*\n/,'function save(){}\n');
eval(js+';globalThis.E={build,simulate,demo,mkPlayers,uid};');
let fails=0;
for(const f of ['se','de','rr','gp'])for(let n=2;n<=33;n++){
  if(f==='de'&&n<3)continue;if(f==='rr'&&(n<3||n>16))continue;
  const cfgs=f==='gp'?[[2,1],[2,2],[3,2],[4,2],[4,1],[3,1],[8,2]]:[[0,0]];
  for(const [gc,ga] of cfgs){
    if(f==='gp'&&(n<gc*Math.max(2,ga+1)||ga>=Math.floor(n/gc)))continue;
    const T={id:'t',results:{},players:E.mkPlayers(n,0,'x').map((p,i)=>({...p,id:'p'+i})),format:f,raceTo:3,status:'live',groups:{count:gc,advance:ga}};
    E.simulate(T,5000);const b=E.build(T);
    const placed=b.places?b.places.flatMap(p=>p.ids):[];
    const ok=b.finished&&placed.length===n&&new Set(placed).size===n&&!b.all.some(m=>m.state==='ready'||m.state==='wait'||m.state==='live');
    // rematch check groups in gp first round
    if(!ok){fails++;console.log('FAIL',f,n,gc,ga,b.finished,placed.length,b.all.filter(m=>m.state==='wait').length)}
  }
}
// DE: each player loses at most 2 except champion
for(let n=3;n<=40;n++){const T={results:{},players:[...Array(n)].map((_,i)=>({id:'p'+i,name:'p'+i})),format:'de',raceTo:2,status:'live'};E.simulate(T,9999);const b=E.build(T);const L={};b.all.filter(m=>m.state==='done').forEach(m=>L[m.loser.id]=(L[m.loser.id]||0)+1);if(Object.values(L).some(v=>v>2)||!(Object.values(L).filter(v=>v===2).length===n-1)){fails++;console.log('DE losses fail',n,L)}}
const D=E.demo();D.tournaments.forEach(t=>{const b=E.build(t);console.log(t.title,t.format,'fin',b.finished,'matches',b.all.length,'live',b.all.filter(m=>m.state==='live').length)});
console.log('fails',fails);
// DE with olympic playoff
let f2=0;const cnt={};
for(const dr of [true,undefined])for(const po of ['auto',4,8,16,0])for(let n=3;n<=64;n++){
  const T={id:'t',draw:dr,results:{},players:[...Array(n)].map((_,i)=>({id:'p'+i,name:'p'+i})),format:'de',playoff:po,raceTo:2,status:'live',groups:{count:4,advance:2}};
  E.simulate(T,9999);const b=E.build(T);const placed=b.places?b.places.flatMap(p=>p.ids):[];
  const L={};b.all.filter(m=>m.state==='done').forEach(m=>L[m.loser.id]=(L[m.loser.id]||0)+1);
  const ok=b.finished&&placed.length===n&&new Set(placed).size===n&&!Object.values(L).some(v=>v>2)&&!b.all.some(m=>['ready','wait','live'].includes(m.state));
  const dn=b.all.filter(m=>m.state==='done').length;if(b.K&&dn!==2*n-b.K/2-1){f2++;console.log('COUNT',po,n,dn)}if(!b.K&&dn!==2*n-2&&dn!==2*n-1){f2++;console.log('COUNT0',po,n,dn)}
  if(b.K&&dr&&!b.drawn){f2++;console.log('NODRAW',po,n)}
  if([12,24,48].includes(n)&&b.name)cnt[n+':'+b.name]=dn;
  if(!ok){f2++;console.log('PO FAIL',po,n,b.finished,placed.length)}
  if([8,16,32].includes(n)&&b.name)cnt[b.name]=b.all.filter(m=>m.state==='done').length;
}
console.log('playoff fails',f2,JSON.stringify(cnt));
