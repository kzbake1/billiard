# Реклама: вредный код во всех полях баннера — на главной и в админке (ожидается «ads_xss ok»)
import os,json;os.system("/home/claude/test/mkcopy.sh")
from playwright.sync_api import sync_playwright
P=lambda f:"\"'><img src=x onerror=__h('%s')>"%f
A=lambda f:"1 autofocus onfocus=__h('%s') x="%f
ad={'id':'11111111-1111-1111-1111-111111111111','advertiser':P('adv'),'eyebrow':A('eye'),'title':P('title'),'subtitle':P('sub'),'button':P('btn'),
    'link':"https://x.kz/\" onmouseover=__h('link') x=\"",'note':P('note'),'amount':"1<img src=x onerror=__h('amount')>",
    'starts_on':"2020-01-01<img src=x onerror=__h('d1')>",'ends_on':"2099-12-31",'enabled':True,'created_at':'2026-11-26'}
mock=open('/home/claude/test/mock.js').read()
mock=mock.replace("promo_use:[]};","promo_use:[],ad:["+json.dumps(ad)+"],ad_stat:[{ad_id:'11111111-1111-1111-1111-111111111111',day:\"2026<img src=x onerror=__h('day')>\",views:'1<b>',clicks:'x'}]};",1)
mock=mock.replace(" if(!isA)return{data:null,error:{message:'Только для администратора'}};",
 " if(n==='current_ad')return{data:window.__AD?[window.__AD]:[]};if(n==='ad_hit')return{data:null};\n if(!isA)return{data:null,error:{message:'Только для администратора'}};",1)
hits=[];bad=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    def page(a,w=1280):
        pg=b.new_page(viewport={'width':w,'height':900})
        pg.expose_function('__h',lambda x:hits.append(x))
        pg.add_init_script("window.__AD="+a+";")
        pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
        pg.route('**/functions/v1/admin',lambda r:r.fulfill(body='{"clubs":[]}',content_type='application/json'))
        return pg
    def js(pg):return pg.evaluate("[...document.querySelectorAll('a[href]')].filter(a=>/^\\s*javascript:/i.test(a.getAttribute('href'))).length")
    # главная: вредный текст во всех полях, ссылка с кавычкой, ссылка javascript:
    for link in [ad['link'],"https://x.kz/ok","javascript:__h('jslink')"]:
        a=dict(ad);a['link']=link
        for w in (1280,390):
            pg=page(json.dumps(a),w);pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
            for el in pg.query_selector_all('a.hads, a.hfree'):el.hover();el.focus()
            if js(pg):bad.append('jslink home')
            pg.close()
    # админка: таблица, окно «Изменить», «Деньги»
    pg=page('null');pg.goto('file:///home/claude/site_t/index.html#admin');pg.wait_for_timeout(600)
    pg.fill('#lg-email','admin@x.kz');pg.fill('#lg-pass','12345678');pg.click('[data-act=login]');pg.wait_for_timeout(900)
    for h in ('ads','money',''):
        pg.goto('file:///home/claude/site_t/index.html#admin/'+h);pg.wait_for_timeout(900)
    pg.goto('file:///home/claude/site_t/index.html#admin/ads');pg.wait_for_timeout(900)
    if pg.query_selector('[data-act=rkEdit]'):
        pg.click('[data-act=rkEdit]');pg.wait_for_timeout(400)
        for i in pg.query_selector_all('.dlg input'):
            try:i.focus()
            except Exception:pass
    else:bad.append('no edit')
    if js(pg):bad.append('jslink admin')
    pg.close();b.close()
print('hits',hits,'bad',bad)
if not hits and not bad:print('ads_xss ok')
