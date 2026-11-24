# Столы «гостям»: не вызываются в турнир; занятый стол уходит после встречи. Ожидается «guest ok» и [].
from playwright.sync_api import sync_playwright
mock=open('/home/claude/site/tests/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_context(viewport={'width':1280,'height':900}).new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    print(pg.evaluate("""(()=>{S.session='c-1';save=()=>{};const c=club('c-1');c.tables=4;const out=[];
      const P=[...Array(8)].map((_,i)=>({id:'p'+i,name:'Игрок '+i,no:i+1}));
      const T={id:'gt1',clubId:'c-1',title:'Гости',format:'se',raceTo:2,status:'live',drawn:true,date:'2026-11-24',players:P,results:{}};
      S.tournaments=S.tournaments.filter(t=>t.clubId!=='c-1');S.tournaments.push(T);go('t-gt1');UI.tab['gt1']='tables';render();CUR={T,b:build(T)};
      A.callT({dataset:{mid:CUR.b.all.filter(m=>m.state==='ready')[0].id,t:'1'}});CUR={T,b:build(T)};
      A.guestT({dataset:{t:'1'}});A.guestT({dataset:{t:'4'}});out.push('g:'+JSON.stringify(T.guestT)+':'+[...guestOff(T)].join(','));
      CUR={T,b:build(T)};A.callAll();const tabs=Object.values(T.results).map(r=>r.table).sort().join(',');out.push('tables:'+tabs);
      const m1=Object.keys(T.results).find(k=>T.results[k].table===1);T.results[m1]=Object.assign(T.results[m1],{sa:2,sb:0,done:true,live:false});CUR={T,b:build(T)};
      out.push('after:'+[...guestOff(T)].sort().join(','));render();out.push('cards:'+document.querySelectorAll('.tcard.guest').length);
      A.guestNone();out.push('none:'+!T.guestT+':'+guestOff(T).size);A.guestAll();out.push('all:'+JSON.stringify(T.guestT));
      const s=out.join('|');const exp='g:[1,4]:4|tables:1,2,3|after:1,4|cards:2|none:true:0|all:[1,4]';return (s===exp?'guest ok ':'GUEST FAIL ')+s})()"""))
    pg.screenshot(path='/tmp/guest.png',full_page=True);print(errs)
