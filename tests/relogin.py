# Вход истёк во время турнира: сохранение получает 401 → окно «Войдите снова» → после входа результаты уходят в базу. Ожидается «relogin ok» и [].
from playwright.sync_api import sync_playwright
mock=open('/home/claude/site/tests/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_context(viewport={'width':390,'height':844}).new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    out=pg.evaluate("""(async()=>{const W=ms=>new Promise(r=>setTimeout(r,ms));
      await sb.auth.signInWithPassword({email:'club@x.kz',password:'12345678'});await loadSession();
      const T={id:'rl1',clubId:'c-1',pub:true,title:'Т',format:'se',raceTo:2,status:'live',drawn:true,date:'2026-11-25',players:[...Array(4)].map((_,i)=>({id:'p'+i,name:'И '+i,no:i+1})),results:{}};S.tournaments.push(T);await doSave();
      // ломаем вход: запись турнира получает 401, обновление токена не работает
      let fail=true,sent=null;const of=sb.from.bind(sb);sb.from=t=>{const a=of(t);if(t!=='tournament')return a;const ou=a.update.bind(a);a.update=v=>{const r=ou(v);if(fail){const th=r.then.bind(r);r.then=(res,rej)=>Promise.resolve({error:{message:'JWT expired'},status:401}).then(res,rej)}else sent=v;return r};return a};
      sb.auth.refreshSession=()=>Promise.resolve({data:{session:null},error:{message:'Invalid Refresh Token'}});
      CUR={T,b:build(T)};const m=CUR.b.all[0];T.results=Object.assign({},T.results);T.results[m.id]={a:m.a.id,b:m.b.id,sa:2,sb:1,done:true,live:false};await doSave();await W(300);
      const modal=!!document.getElementById('rl-pass');fail=false;
      document.getElementById('rl-pass').value='12345678';await A.relogin(document.querySelector('[data-act=relogin]'));await W(200);
      const ok=modal&&!document.getElementById('rl-pass')&&sent&&sent.data&&sent.data.results&&sent.data.results[m.id]&&sent.data.results[m.id].sa===2;
      return (ok?'relogin ok':'RELOGIN FAIL')+' modal:'+modal+' sent:'+!!sent})()""")
    print(out,errs)
