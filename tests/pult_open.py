# Нажатие на пару в сетке открывает пульт (компьютер и телефон). Ожидается «pult ok» дважды и [].
from playwright.sync_api import sync_playwright
mock=open('/home/claude/site/tests/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for mob in [False,True]:
        ctx=b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True) if mob else b.new_context(viewport={'width':1280,'height':900})
        pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
        pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
        pg.evaluate("""(()=>{S.session='c-1';save=()=>{};const T={id:'e1',clubId:'c-1',title:'Т',format:'de',playoff:'auto',raceTo:2,status:'live',drawn:true,date:'2026-11-24',players:[...Array(6)].map((_,i)=>({id:'p'+i,name:'Игрок Номер'+i,no:i+1})),results:{}};S.tournaments.push(T);go('t-e1');UI.tab['e1']='grid';render()})()""")
        pg.wait_for_timeout(400);el=pg.query_selector('.zm .m.s-ready .row[data-pid] .n');el.scroll_into_view_if_needed()
        (el.tap() if mob else el.click());pg.wait_for_timeout(500)
        ok=pg.evaluate("document.getElementById('modal').classList.contains('open')&&document.getElementById('modal').innerText.includes('Матч №')")
        print('pult ok' if ok and not errs else 'PULT FAIL', 'mobile' if mob else 'desktop', errs)
