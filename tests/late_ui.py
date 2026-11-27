# Опоздавший: панель на вкладке «Участники», жребий места, игрок встаёт в сетку. Ожидается «late ok» и [].
from playwright.sync_api import sync_playwright
mock=open('/home/claude/site/tests/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg=b.new_page(viewport={'width':1280,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    pg.evaluate("""(()=>{S.session='c-1';save=()=>{};const T={id:'e1',clubId:'c-1',title:'Т',format:'se',raceTo:2,status:'live',drawn:true,date:'2026-11-24',players:[...Array(14)].map((_,i)=>({id:'p'+i,first:'Имя'+i,last:'Игрок',name:'Игрок Имя'+i,no:i+1})),results:{}};S.tournaments.push(T);go('t-e1');UI.tab['e1']='people';render()})()""")
    pg.wait_for_timeout(400)
    pg.fill('#lt-last','Опоздалов');pg.fill('#lt-first','Ерлан');pg.click('[data-act="lateFind"]');pg.wait_for_timeout(300)
    txt=pg.inner_text('#modal');pg.screenshot(path='/tmp/late1.png')
    pg.click('[data-act="lateOk"]');pg.wait_for_timeout(300)
    r=pg.evaluate("(()=>{const T=tById('e1');const L=T.players.find(p=>p.last==='Опоздалов');const b=build(T);const m=b.all.find(m=>m.a.id===L.id||m.b.id===L.id);return {seat:L.seat,n:T.players.length,st:m&&m.state}})()")
    print('late ok' if r['n']==15 and r['seat'] in (15,16) and r['st']=='ready' and 'Добавить опоздавшего' in txt else 'LATE FAIL',r,errs)
