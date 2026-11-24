from pathlib import Path
from urllib.request import urlopen, Request
import re
from concurrent.futures import ThreadPoolExecutor
root=Path(__file__).resolve().parent
urls=(root/'missing-assets.txt').read_text().splitlines()
def download(url):
    rel='assets/tild'+url.split('/tild',1)[1]; target=root/rel
    try:
        target.parent.mkdir(parents=True,exist_ok=True)
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as r:
            data=r.read()
            if not data or 'text/html' in r.headers.get('Content-Type',''): raise ValueError('not an image')
        target.write_bytes(data)
        return url,'/'+rel
    except Exception as e: print('FAILED',url,e); return url,None
with ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(download,urls))
for p in root.glob('*.html'):
    s=p.read_text()
    for url,rel in results:
        if rel: s=s.replace(url,rel)
    p.write_text(s)
print('Downloaded',sum(bool(r) for _,r in results),'of',len(results))
if any(not r for _,r in results):
    raise SystemExit('Some assets failed. Do not delete Tilda yet.')
