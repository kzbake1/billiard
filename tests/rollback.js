// старая вкладка с давним снимком не должна откатывать счёт идущего матча
const fs=require('fs');const src=fs.readFileSync(__dirname+'/../index.html','utf8');
const jsq=eval('('+src.match(/const jsq=(x=>[^\n]*);/)[1]+')');
const m3=src.match(/function merge3[\s\S]*?out\.results=R;return out\}/)[0];eval(m3);
let f=0;const ok=(c,t)=>{if(!c){f++;console.log('FAIL',t)}};
// без отметок: сервер 0:1, старая вкладка 0:0 -> 0:1
let r=merge3({results:{}},{results:{m:{sa:0,sb:0,live:true}}},{results:{m:{sa:0,sb:1,live:true}}});ok(r.results.m.sb===1,'legacy progress');
// с отметками: свежая правка «−» на сервере сохраняется
r=merge3({results:{}},{results:{m:{sa:0,sb:2,live:true,et:1}}},{results:{m:{sa:0,sb:1,live:true,et:5}}});ok(r.results.m.sb===1,'server newer et');
r=merge3({results:{}},{results:{m:{sa:0,sb:1,live:true,et:9}}},{results:{m:{sa:0,sb:2,live:true,et:5}}});ok(r.results.m.sb===1,'local newer et');
// новая вкладка (et) против старой без et -> новая
r=merge3({results:{}},{results:{m:{sa:0,sb:3,live:true}}},{results:{m:{sa:0,sb:1,live:true,et:5}}});ok(r.results.m.sb===1,'old tab loses');
console.log('fails',f);process.exit(f?1:0)
