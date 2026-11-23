from playwright.sync_api import sync_playwright
mock=open('/home/claude/test/mock.js').read()
P='"\'><img src=x onerror=__h(1)>'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_context(viewport={'width':1300,'height':900}).new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.__hits=0;window.__h=()=>{window.__hits++}")
    pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html#cabinet');pg.wait_for_timeout(600)
    pg.fill('#lg-email','club@x.kz');pg.fill('#lg-pass','12345678');pg.press('#lg-pass','Enter');pg.wait_for_timeout(1200)
    pg.evaluate("S.pwOk=true;location.hash='#create'");pg.wait_for_timeout(300);pg.click('[data-act=wSave]');pg.wait_for_timeout(400)
    # inject raw (bypassing UI) as if written via API, then reload through tFromRow path
    pg.evaluate("""(P)=>{const T=CUR.T;const raw=JSON.parse(JSON.stringify(tData(T)));raw.title=P;raw.discipline=P;raw.orgName=P;raw.video='javascript:__h(2)';raw.link='javascript:__h(3)';raw.category=P;
      raw.players=[...Array(8)].map((_,i)=>({id:'x'+i,name:P+i,first:P,last:P,city:P,club:P,rank:P,birth:'1990',no:i+1,lvl:P,sex:P}));raw.drawn=true;raw.format='se';raw.status='live';raw.pub=true;raw.results={};
      onRemote({new:{id:T.id,club_id:'other',data:Object.assign(raw,{_v:5,_r:999,_w:'zz'})}});}""",P)
    pg.wait_for_timeout(400)
    tid=pg.evaluate("S.tournaments.find(t=>t.orgName&&t.orgName.includes('img'))?.id||S.tournaments[S.tournaments.length-1].id")
    for h in ['#','#t-'+tid,'#tablo-x-1','#cabinet']:
        pg.evaluate("location.hash=%r"%h);pg.wait_for_timeout(500)
        for tab in ['grid','people','result','about','tables','sheet']:
            if h.startswith('#t-'):
                pg.evaluate("UI.tab[%r]=%r;render()"%(tid,tab));pg.wait_for_timeout(200)
    js=pg.evaluate("[...document.querySelectorAll('[href]')].filter(a=>/^\\s*javascript:/i.test(a.getAttribute('href'))).length")
    print('hits',pg.evaluate("__hits"),'jslinks',js,'title',pg.evaluate("S.tournaments.find(t=>t.id==%r).title"%tid)[:40],errs[:3])
