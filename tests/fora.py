# Фора в шарах во встрече. Ожидается: «fora ok» и [] ошибок.
from playwright.sync_api import sync_playwright
mock=open('/home/claude/site/tests/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_context(viewport={'width':1200,'height':900}).new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    print(pg.evaluate("""(()=>{S.session='c-1';const T={id:'mf1',clubId:'c-1',title:'Встреча',match:true,balls:true,discipline:'Свободная пирамида',format:'se',raceTo:3,status:'live',drawn:true,date:'2026-11-23',
      players:[{id:'pa',name:'Аман Арман',no:1},{id:'pb',name:'Болат Бек',no:2}],results:{'s1-0':{a:'pa',b:'pb',sa:1,sb:0,ba:0,bb:3,live:true,done:false,fr:[{w:'a',a:8,b:2}],table:1,ts:Date.now()}}};
      S.tournaments.push(T);save=()=>{};CUR={T,b:build(T)};const m=CUR.b.all[0];UI.pm=m.id;openModal(pultHTML(T,m));const out=[];
      const sel=document.getElementById('pm-fos'),num=document.getElementById('pm-fon');if(!sel)return 'no control';
      sel.value='a';num.value='3';A.pmFo(sel);let r=T.results['s1-0'];out.push('set:'+r.ba+':'+r.bb);
      const bl=(sd,d)=>{CUR={T,b:build(T)};A.bl({dataset:{mid:'s1-0',side:sd,d:String(d)}})};
      for(let i=0;i<3;i++)bl('a',-1);out.push('minclamp:'+r.ba);
      for(let i=0;i<5;i++)bl('a',1);r=T.results['s1-0'];out.push('frame:'+r.sa+' new:'+r.ba+':'+r.bb+' last:'+JSON.stringify(r.fr[r.fr.length-1]));
      CUR={T,b:build(T)};const m2=CUR.b.all[0];const hd=pultHTML(T,m2).includes('фора 3');const pr=protoHTML(T,m2).includes('фора 3');const vw=viewMatchHTML(T,CUR.b,m2).includes('фора 3');out.push('labels:'+hd+pr+vw);
      openModal(pultHTML(T,m2));const s2=document.getElementById('pm-fos');s2.value='';A.pmFo(s2);r=T.results['s1-0'];out.push('off:'+r.ba+':'+r.bb+':'+!!r.fo);
      const ok=out.join('|')==='set:3:3|minclamp:3|frame:2 new:3:0 last:{"w":"a","a":8,"b":3}|labels:truetruetrue|off:0:0:false';return (ok?'fora ok ':'FORA FAIL ')+out.join('|')})()"""))
    print(errs)
