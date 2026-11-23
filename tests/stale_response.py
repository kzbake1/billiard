from playwright.sync_api import sync_playwright
mock=open('/home/claude/test/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_context(viewport={'width':1200,'height':900}).new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    print(pg.evaluate("""(()=>{const T={id:'tst1'};const d={title:'x',players:[],results:{},status:'reg',format:'se',date:'2026-11-22',pub:true};
      const mk=(r,t)=>({id:T.id,club_id:'zz',data:Object.assign({},d,{_v:5,_r:r,_w:'x'+r,title:t})});
      onRemote({new:mk(50,'NEW')});const a=S.tournaments.find(x=>x.id===T.id).title;
      onRemote({new:mk(49,'OLD')});const b=S.tournaments.find(x=>x.id===T.id).title;
      onRemote({new:mk(51,'NEWER')});const c=S.tournaments.find(x=>x.id===T.id).title;return [a,b,c].join(' ')})()"""))
    print(errs)
