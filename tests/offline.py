# Нет связи при сохранении: плашка «Не сохранено», копия в памяти браузера переживает перезагрузку и уходит в базу. Ожидается «offline ok» и [].
from playwright.sync_api import sync_playwright
mock=open('/home/claude/site/tests/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');ctx=b.new_context(viewport={'width':390,'height':844});pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    ctx.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    r1=pg.evaluate("""(async()=>{const W=ms=>new Promise(r=>setTimeout(r,ms));
      await sb.auth.signInWithPassword({email:'club@x.kz',password:'12345678'});await loadSession();
      const T={id:'of1',clubId:'c-1',pub:true,title:'Т',format:'se',raceTo:2,status:'live',drawn:true,date:'2026-11-25',players:[...Array(4)].map((_,i)=>({id:'p'+i,name:'И '+i,no:i+1})),results:{}};S.tournaments.push(T);save();await W(300);
      const of=sb.from.bind(sb);sb.from=t=>{const a=of(t);if(t!=='tournament')return a;const ou=a.update.bind(a);a.update=v=>{const r=ou(v);r.then=(res,rej)=>Promise.resolve({error:{message:'Failed to fetch'},status:0}).then(res,rej);return r};return a};
      CUR={T,b:build(T)};const m=CUR.b.all[0];T.results=Object.assign({},T.results);T.results[m.id]={a:m.a.id,b:m.b.id,sa:2,sb:0,done:true,live:false};save();await W(400);
      const pill=(document.getElementById('svst')||{}).innerText||'';const bk=localStorage.getItem('kb-pend');return {pill,bk:!!bk&&bk.includes('"sa":2'),mid:m.id}})()""")
    # перезагрузка страницы: в памяти ничего нет, mock-база «пустая» по-новой; добавим турнир в базу заново (без результата) и проверим восстановление
    pg.reload();pg.wait_for_timeout(900)
    r2=pg.evaluate("""(async(mid)=>{const W=ms=>new Promise(r=>setTimeout(r,ms));
      await sb.auth.signInWithPassword({email:'club@x.kz',password:'12345678'});
      const p=JSON.parse(localStorage.getItem('kb-pend')||'{}');const d=p.of1&&JSON.parse(p.of1.b);await sb.from('tournament').insert({id:'of1',club_id:'c-1',data:d});
      await load();await W(500);const T=S.tournaments.find(t=>t.id==='of1');const db=(await sb.from('tournament').select('data').eq('id','of1').maybeSingle()).data;
      return {local:!!(T&&T.results[mid]&&T.results[mid].sa===2),db:!!(db&&db.data.results&&db.data.results[mid]&&db.data.results[mid].sa===2),left:localStorage.getItem('kb-pend')}})""",r1['mid'])
    ok=r1['pill'].startswith('Не сохранено') and r1['bk'] and r2['local'] and r2['db'] and not r2['left']
    print('offline ok' if ok else 'OFFLINE FAIL',r1,r2,errs)
