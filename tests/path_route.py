import http.server,threading,os
from playwright.sync_api import sync_playwright
R='/home/claude/site'
class H(http.server.SimpleHTTPRequestHandler):
  def __init__(s,*a,**k):super().__init__(*a,directory=R,**k)
  def log_message(s,*a):pass
  def do_GET(s):
    p=s.path.split('?')[0]
    if p.startswith('/t/'):s.path='/index.html'
    return super().do_GET()
srv=http.server.ThreadingHTTPServer(('127.0.0.1',8765),H);threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright() as pw:
  b=pw.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://127.0.0.1:8765/t/243ztul?s=l');pg.wait_for_timeout(2500)
  print('1',pg.url)
  pg.evaluate("location.hash='home'");pg.wait_for_timeout(500);print('2',pg.url)
  pg.evaluate("location.hash='t-243ztul'");pg.wait_for_timeout(500);print('3',pg.url)
  pg.goto('http://127.0.0.1:8765/#t-243ztul');pg.wait_for_timeout(1500);print('4',pg.url)
  print('errs',errs);b.close()
srv.shutdown()
