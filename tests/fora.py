# Фора во встрече: у каждого игрока своя цель в шарах (например 9:7). Ожидается «fora ok» и [].
from playwright.sync_api import sync_playwright
mock=open('/home/claude/site/tests/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_context(viewport={'width':1200,'height':900}).new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    print(pg.evaluate("""(()=>{S.session='c-1';save=()=>{};const out=[];
      const T={id:'mf1',clubId:'c-1',title:'Встреча',match:true,balls:true,discipline:'Свободная пирамида',format:'se',raceTo:3,status:'reg',date:'2026-11-23',players:[{id:'pa',name:'Аман Арман'},{id:'pb',name:'Болат Бек'}],results:{}};
      S.tournaments.push(T);go('t-mf1');render();
      const ins=[...document.querySelectorAll('[data-act=prepFo]')];if(ins.length!==2)return 'no prep inputs';ins[0].value='9';A.prepFo(ins[0]);ins[1].value='7';A.prepFo(ins[1]);out.push('prep:'+JSON.stringify(T.foP));
      A.matchStart();CUR={T,b:build(T)};let m=CUR.b.all[0];T.results[m.id]={a:'pa',b:'pb',sa:0,sb:0,ba:0,bb:0,live:true,done:false,table:1,ts:Date.now()};
      const bl=(sd,d)=>{CUR={T,b:build(T)};A.bl({dataset:{mid:m.id,side:sd,d:String(d)}})};const r=()=>T.results[m.id];
      for(let i=0;i<7;i++)bl('b',1);out.push('b7:'+r().sb+':'+JSON.stringify(r().fr[0]));
      for(let i=0;i<8;i++)bl('a',1);out.push('a8:'+r().sa+':'+r().ba);bl('a',1);out.push('a9:'+r().sa+':'+r().ba);
      CUR={T,b:build(T)};m=CUR.b.all[0];UI.pm=m.id;openModal(pultHTML(T,m));const fa=document.getElementById('pm-foa'),fb=document.getElementById('pm-fob');out.push('pult:'+fa.value+':'+fb.value);
      fa.value='8';fb.value='8';A.pmFo(fa);out.push('off:'+(foT(T,CUR.b.all[0])===null));{const x=document.getElementById("pm-foa"),y=document.getElementById("pm-fob");x.value="9";y.value="6";A.pmFo(x)}CUR={T,b:build(T)};m=CUR.b.all[0];
      out.push('labels:'+pultHTML(T,m).includes('фора 9:6')+protoHTML(T,m).includes('фора 9:6')+viewMatchHTML(T,CUR.b,m).includes('фора 9:6')+matchBody(T,CUR.b).includes('до 9 шаров'));
      const L={a:'x',b:'y',res:{fo:{s:'a',n:3}}};out.push('legacy:'+tgt(T,L,'a')+':'+tgt(T,L,'b'));
      const exp='prep:{"pa":9,"pb":7}|b7:1:{"w":"b","a":0,"b":7}|a8:0:8|a9:1:0|pult:9:7|off:true|labels:truetruetruetrue|legacy:5:8';
      const s=out.join('|');return (s===exp?'fora ok ':'FORA FAIL ')+s})()"""))
    print(errs)
