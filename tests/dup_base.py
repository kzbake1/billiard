# Дубли: игрок с тем же именем уже в общей базе — сайт спрашивает «Это он?» и берёт существующую запись. Ожидается «dup ok» и [].
from playwright.sync_api import sync_playwright
mock=open('/home/claude/site/tests/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_context(viewport={'width':1280,'height':900}).new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    pg.evaluate("""()=>{S.session='c-1';save=()=>{};const c=club('c-1');c.roster=[{id:'old1',first:'Айдос',last:'Сабиров',name:'Сабиров Айдос',birth:'',city:'Семей',rank:'б/р'}];
      const T={id:'dt1',clubId:'c-1',title:'Дубли',format:'se',raceTo:2,status:'reg',date:'2026-11-28',players:[],results:{},applications:[]};S.tournaments.push(T);go('t-dt1');UI.tab['dt1']='people';render();CUR={T,b:build(T)}}""")
    pg.wait_for_timeout(300)
    pg.fill('#np-last','сабиров');pg.fill('#np-first','Айдос')
    pg.evaluate("()=>{A.addP()}");pg.wait_for_timeout(300)
    asked=pg.evaluate("()=>/уже есть в базе/.test(document.getElementById('modal').textContent)")
    pg.click('text=Да, это он');pg.wait_for_timeout(300)
    r1=pg.evaluate("()=>{const T=S.tournaments.find(t=>t.id==='dt1');return T.players.map(p=>p.id).join(',')+'|'+club('c-1').roster.length}")
    # «нет, другой» — создаёт нового
    pg.evaluate("()=>{const T=S.tournaments.find(t=>t.id==='dt1');T.players=[];CUR={T,b:build(T)};render()}");pg.wait_for_timeout(200)
    pg.fill('#np-last','Сабиров');pg.fill('#np-first','Айдос');pg.evaluate("()=>{A.addP()}");pg.wait_for_timeout(300)
    pg.click('text=Нет, другой человек');pg.wait_for_timeout(300)
    r2=pg.evaluate("()=>{const T=S.tournaments.find(t=>t.id==='dt1');return (T.players[0]&&T.players[0].id!=='old1')+'|'+club('c-1').roster.length}")
    # с годом рождения, а в базе без года — тоже спрашивает; с совпадающим годом — берёт молча
    s=f'asked:{asked} yes:{r1} no:{r2}'
    print(('dup ok ' if s=='asked:True yes:old1|1 no:true|2' else 'DUP FAIL ')+s, errs)
