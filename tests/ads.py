# Реклама: баннер под обложкой главной и вкладка «Реклама» в админке (ожидается «ads ok»)
import os;os.system("/home/claude/test/mkcopy.sh")
from playwright.sync_api import sync_playwright
U='https://dhsrklircobualygdacz.supabase.co/storage/v1/object/public/ad-image/11111111-1111-1111-1111-111111111111/'
mock=open('/home/claude/test/mock.js').read()
mock=mock.replace("promo_use:[]};","promo_use:[],ad:[],ad_stat:[{ad_id:'11111111-1111-1111-1111-111111111111',day:'2026-11-20',views:100,clicks:3}]};",1)
mock=mock.replace(" if(!isA)return{data:null,error:{message:'Только для администратора'}};",
 " if(n==='current_ad'){window.__hits=window.__hits||[];return{data:window.__AD?[window.__AD]:[]}}if(n==='ad_hit'){(window.__hits=window.__hits||[]).push(a.p_kind);return{data:null}}\n if(!isA)return{data:null,error:{message:'Только для администратора'}};",1)
assert 'current_ad' in mock
AD="{id:'11111111-1111-1111-1111-111111111111',advertiser:'Кий-Мастер',link:'https://example.kz/kiy',img_desktop:'"+U+"d.webp?v=1',img_mobile:'"+U+"m.webp?v=1'}"
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');errs=[]
    def page(ad,w=1280):
        pg=b.new_page(viewport={'width':w,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.add_init_script("window.__AD="+ad+";")
        pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
        pg.route('**/functions/v1/admin',lambda r:r.fulfill(body='{"clubs":[]}',content_type='application/json'))
        pg.route('https://dhsrklircobualygdacz.supabase.co/storage/**',lambda r:r.fulfill(body=b'',content_type='image/webp'))
        return pg
    # 1. баннер есть, стоит после обложки, подпись «Реклама», ссылка рекламодателя, показ засчитан
    pg=page(AD);pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    a=pg.query_selector('a.hads')
    if not a:bad.append('no banner')
    else:
        if a.get_attribute('href')!='https://example.kz/kiy':bad.append('href')
        if 'Реклама' not in a.inner_text():bad.append('label')
        if not pg.evaluate("document.querySelector('.hhero').nextElementSibling.classList.contains('hads')"):bad.append('not after hero')
        if pg.evaluate("(window.__hits||[]).filter(x=>x==='view').length")!=1:bad.append('view count')
        pg.evaluate("document.querySelector('a.hads').addEventListener('click',e=>e.preventDefault())");a.click();pg.wait_for_timeout(200)
        if 'click' not in pg.evaluate("window.__hits||[]"):bad.append('click count')
    pg.close()
    # 2. нет рекламы — блока нет
    pg=page('null');pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    if pg.query_selector('.hads'):bad.append('banner without ad')
    pg.close()
    # 3. чужая картинка или ссылка javascript: — не показываем
    pg=page(AD.replace("https://example.kz/kiy","javascript:alert(1)"));pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    if pg.query_selector('.hads'):bad.append('bad link shown')
    pg.close()
    pg=page(AD.replace(U+"d.webp","https://evil.kz/d.webp"));pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    if pg.query_selector('.hads'):bad.append('bad img shown')
    pg.close()
    # 4. телефон: баннер 2:1
    pg=page(AD,390);pg.goto('file:///home/claude/site_t/index.html');pg.wait_for_timeout(900)
    bx=pg.query_selector('a.hads').bounding_box()
    if abs(bx['width']/bx['height']-2)>0.05:bad.append('phone ratio %.2f'%(bx['width']/bx['height']))
    pg.close()
    # 5. админка: вкладка, пустой список, новый баннер с картинками
    pg=page('null');pg.goto('file:///home/claude/site_t/index.html#admin');pg.wait_for_timeout(700)
    pg.fill('#lg-email','admin@x.kz');pg.fill('#lg-pass','12345678');pg.click('[data-act=login]');pg.wait_for_timeout(900)
    pg.goto('file:///home/claude/site_t/index.html#admin/ads');pg.wait_for_timeout(900)
    if 'Реклама' not in pg.inner_text('.adm-tabs'):bad.append('no tab')
    if 'Баннеров пока нет' not in pg.inner_text('body'):bad.append('empty state')
    pg.click('[data-act=rkNew]');pg.wait_for_timeout(200)
    pg.fill('#rk-n','Кий-Мастер');pg.fill('#rk-l','https://example.kz');pg.fill('#rk-e','2099-12-31')
    pg.click('[data-act=rkSave]');pg.wait_for_timeout(200)
    if 'обе картинки' not in pg.inner_text('#rk-err'):bad.append('needs images')
    png=pg.evaluate("""(async()=>{const c=document.createElement('canvas');c.width=1600;c.height=400;const x=c.getContext('2d');x.fillStyle='#FFF4D6';x.fillRect(0,0,1600,400);return c.toDataURL('image/png')})()""")
    import base64;open('/tmp/rk.png','wb').write(base64.b64decode(png.split(',')[1]))
    pg.set_input_files('input[data-rkf=d]','/tmp/rk.png');pg.wait_for_timeout(200)
    pg.set_input_files('input[data-rkf=m]','/tmp/rk.png');pg.wait_for_timeout(200)
    if pg.input_value('#rk-n')!='Кий-Мастер':bad.append('field lost after upload')
    pg.click('[data-act=rkSave]');pg.wait_for_timeout(1500)
    row=pg.evaluate("window.__DB&&window.__DB.ad&&window.__DB.ad[0]")
    if not row:bad.append('not saved '+pg.inner_text('#rk-err') if pg.query_selector('#rk-err') else 'not saved')
    else:
        if not row['img_desktop'].startswith(U[:-37]):bad.append('img url')
        if row['enabled'] is not True:bad.append('enabled')
    up=pg.evaluate("window.__up")
    if not up or up[0]!='ad-image' or not up[1].endswith('/m.webp'):bad.append('upload %r'%(up,))
    pg.wait_for_timeout(500)
    if 'Кий-Мастер' not in pg.inner_text('body'):bad.append('not in list')
    pg.click('[data-act=rkToggle]');pg.wait_for_timeout(800)
    if pg.evaluate("window.__DB.ad[0].enabled")!=False:bad.append('toggle')
    pg.close()
    b.close()
print(errs,bad)
if not errs and not bad:print('ads ok')
