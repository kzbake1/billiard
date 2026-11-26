# Реклама: баннер под обложкой главной и вкладка «Реклама» в админке (ожидается «ads ok»)
import os;os.system("/home/claude/test/mkcopy.sh")
from playwright.sync_api import sync_playwright
U='https://dhsrklircobualygdacz.supabase.co/storage/v1/object/public/ad-image/11111111-1111-1111-1111-111111111111/'
mock=open('/home/claude/test/mock.js').read()
mock=mock.replace("promo_use:[]};","promo_use:[],site_day:[{day:'2026-11-20',visits:40,mobile:30}],ad:[],ad_stat:[{ad_id:'11111111-1111-1111-1111-111111111111',day:'2026-11-20',views:100,clicks:3}]};",1)
mock=mock.replace(" if(!isA)return{data:null,error:{message:'Только для администратора'}};",
 " if(n==='current_ad_v2'){window.__hits=window.__hits||[];return{data:window.__AD?[window.__AD]:[]}}if(n==='ad_hit'){(window.__hits=window.__hits||[]).push(a.p_kind);return{data:null}}if(n==='site_hit'){(window.__sv=window.__sv||[]).push(a.p_mobile);return{data:null}}\n if(!isA)return{data:null,error:{message:'Только для администратора'}};",1)
assert 'current_ad' in mock
AD="{id:'11111111-1111-1111-1111-111111111111',advertiser:'Кий-Мастер',link:'https://example.kz/kiy',eyebrow:'КИЙ-МАСТЕР · АЛМАТЫ',title:'Наклейки <b>и</b> ремонт',subtitle:'За один день',button:'Подробнее'}"
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');errs=[]
    def page(ad,w=1280):
        pg=b.new_page(viewport={'width':w,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.add_init_script("window.__AD="+ad+";")
        pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
        pg.route('**/functions/v1/admin',lambda r:r.fulfill(body='{"clubs":[]}',content_type='application/json'))
        return pg
    # 1. баннер есть, стоит после обложки, подпись «Реклама», ссылка рекламодателя, показ засчитан
    pg=page(AD);pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    a=pg.query_selector('a.hads')
    if not a:bad.append('no banner')
    else:
        if a.get_attribute('href')!='https://example.kz/kiy':bad.append('href')
        if 'Реклама' not in a.inner_text():bad.append('label')
        if 'Наклейки <b>и</b> ремонт' not in a.inner_text():bad.append('title escaped')
        if pg.evaluate("getComputedStyle(document.querySelector('a.hads')).backgroundColor")!='rgb(22, 103, 255)':bad.append('not blue')
        if not pg.evaluate("document.querySelector('.hhero').nextElementSibling.classList.contains('hads')"):bad.append('not after hero')
        if pg.evaluate("(window.__hits||[]).filter(x=>x==='view').length")!=1:bad.append('view count')
        pg.evaluate("document.querySelector('a.hads').addEventListener('click',e=>e.preventDefault())");a.click();pg.wait_for_timeout(200)
        if 'click' not in pg.evaluate("window.__hits||[]"):bad.append('click count')
    pg.close()
    # 1б. посещаемость: один заход в день с браузера, не больше
    pg=page('null');pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900);pg.reload();pg.wait_for_timeout(900)
    if pg.evaluate("(window.__sv||[]).length")!=0 and pg.evaluate("localStorage.length")==0:bad.append('sv storage')
    pg.close()
    pg=page('null');pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    if pg.evaluate("(window.__sv||[]).length")!=1:bad.append('sv hit %r'%pg.evaluate("window.__sv"))
    pg.reload();pg.wait_for_timeout(900)
    if pg.evaluate("(window.__sv||[]).length")!=0:bad.append('sv twice')
    pg.close()
    # 2. нет рекламы — жёлтая полоса «Здесь может быть ваша реклама» с WhatsApp, на телефоне тоже
    pg=page('null');pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    if pg.query_selector('.hads'):bad.append('banner without ad')
    f=pg.query_selector('a.hfree')
    if not f or 'Здесь может быть ваша реклама' not in f.inner_text() or not f.get_attribute('href').startswith('https://wa.me/77764308322'):bad.append('free banner')
    elif not pg.evaluate("document.querySelector('.hhero').nextElementSibling.classList.contains('hfree')"):bad.append('free not after hero')
    pg.close()
    pg=page('null',390);pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    bx=pg.query_selector('a.hfree').bounding_box()
    if bx['height']>100:bad.append('free phone height %r'%bx['height'])
    pg.close()
    # 3. чужая картинка или ссылка javascript: — не показываем
    pg=page(AD.replace("https://example.kz/kiy","javascript:alert(1)"));pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    if pg.query_selector('.hads') or not pg.query_selector('.hfree'):bad.append('bad link shown')
    pg.close()
    pg=page(AD.replace("title:'Наклейки <b>и</b> ремонт'","title:''"));pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    if pg.query_selector('.hads'):bad.append('empty title shown')
    pg.close()
    # 3б. картинка только для телефона: на телефоне картинка с «Реклама», на компьютере жёлтая полоса
    IMG=AD.replace("title:'Наклейки <b>и</b> ремонт'","title:'',img_mobile:'/ads/chimba-m.webp'")
    for w,want in ((390,'img'),(1280,'free')):
        pg=page(IMG,w);pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
        vi=pg.evaluate("(()=>{const v=s=>{const e=document.querySelector(s);return !!e&&e.getBoundingClientRect().height>0};return{img:v('.hads-img'),free:v('a.hfree')}})()")
        if want=='img' and not (vi['img'] and not vi['free']):bad.append('phone img %r'%vi)
        if want=='free' and not (vi['free'] and not vi['img']):bad.append('desktop free %r'%vi)
        if want=='img':
            if 'Реклама' not in pg.inner_text('.hads-img'):bad.append('img label')
            bx=pg.query_selector('.hads-img').bounding_box()
            if abs(bx['width']/bx['height']-4.5)>0.1:bad.append('img ratio')
        pg.close()
    pg=page(IMG.replace("img_mobile:'/ads/chimba-m.webp'","img_mobile:'https://evil.kz/x.webp'"),390);pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    if pg.query_selector('.hads-img'):bad.append('foreign img shown')
    pg.close()
    # 4. телефон: баннер на всю ширину, текст в столбик
    pg=page(AD,390);pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    bx=pg.query_selector('a.hads').bounding_box()
    if bx['width']>360 or bx['height']<170:bad.append('phone size %r'%bx)
    pg.close()
    # 5. админка: вкладка, пустой список, новый баннер, предпросмотр
    pg=page('null');pg.goto('file:///home/claude/site_t/index.html#admin');pg.wait_for_timeout(700)
    pg.fill('#lg-email','admin@x.kz');pg.fill('#lg-pass','12345678');pg.click('[data-act=login]');pg.wait_for_timeout(900)
    pg.goto('file:///home/claude/site_t/index.html#admin/ads');pg.wait_for_timeout(900)
    if 'Реклама' not in pg.inner_text('.adm-tabs'):bad.append('no tab')
    if 'Баннеров пока нет' not in pg.inner_text('body'):bad.append('empty state')
    pg.goto('file:///home/claude/site_t/index.html#admin');pg.wait_for_timeout(900)
    if 'Посещаемость сайта' not in pg.inner_text('body') or 'С телефона' not in pg.inner_text('body'):bad.append('sv admin block')
    pg.goto('file:///home/claude/site_t/index.html#admin/ads');pg.wait_for_timeout(900)
    pg.click('[data-act=rkNew]');pg.wait_for_timeout(200)
    pg.fill('#rk-n','Кий-Мастер');pg.fill('#rk-l','https://example.kz');pg.fill('#rk-e','2099-12-31')
    pg.click('[data-act=rkSave]');pg.wait_for_timeout(200)
    if 'заголовок' not in pg.inner_text('#rk-err'):bad.append('needs title')
    pg.fill('#rk-h','Наклейки и ремонт киев');pg.wait_for_timeout(100)
    if 'Наклейки и ремонт киев' not in pg.inner_text('.rk-pv'):bad.append('preview')
    pg.click('[data-act=rkSave]');pg.wait_for_timeout(1200)
    row=pg.evaluate("window.__DB&&window.__DB.ad&&window.__DB.ad[0]")
    if not row:bad.append('not saved')
    else:
        if row['title']!='Наклейки и ремонт киев' or row['button']!='Подробнее':bad.append('row %r'%row)
        if row['enabled'] is not True:bad.append('enabled')
    pg.wait_for_timeout(500)
    if 'Кий-Мастер' not in pg.inner_text('body'):bad.append('not in list')
    pg.click('[data-act=rkToggle]');pg.wait_for_timeout(800)
    if pg.evaluate("window.__DB.ad[0].enabled")!=False:bad.append('toggle')
    pg.close()
    b.close()
print(errs,bad)
if not errs and not bad:print('ads ok')
