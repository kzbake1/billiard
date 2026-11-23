import os;os.system("/home/claude/test/mkcopy.sh")
from playwright.sync_api import sync_playwright
mock=open('/home/claude/test/mock.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome');pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/supabase-js@*/**',lambda r:r.fulfill(body=mock,content_type='application/javascript'))
    pg.goto('file:///home/claude/site_t/index.html#cabinet');pg.wait_for_timeout(800);print(errs)
