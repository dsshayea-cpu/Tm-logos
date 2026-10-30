import json, os, time, subprocess, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
UA={"User-Agent":"TM-trivia-image-fetch/1.1 (https://github.com/dsshayea-cpu/tm-logos; contact via GitHub)"}
D="ahl-albahar"
def get(url, tries=3):
    err=None
    for t in range(tries):
        try:
            req=urllib.request.Request(url,headers=UA)
            with urllib.request.urlopen(req,timeout=15) as r: return r.read()
        except Exception as e:
            err=e; time.sleep(2*(t+1))
    raise err
def api(base, **p):
    p.update(format="json", formatversion=2)
    return json.loads(get(base+"?"+urllib.parse.urlencode(p)))
def resize(u,w):
    if "/thumb/" in u:
        head,fn=u.rsplit("/",1)
        return head+"/"+f"{w}px-"+fn.split("px-",1)[1]
    return u
EN="https://en.wikipedia.org/w/api.php"; CM="https://commons.wikimedia.org/w/api.php"
items=json.load(open(f"{D}/titles.json"))
os.makedirs(f"{D}/cand",exist_ok=True)
outp=f"{D}/candidates.json"
out=json.load(open(outp)) if os.path.exists(outp) else {}
def one(it):
    cands=[]
    try:
        r=api(EN,action="query",prop="pageimages",piprop="thumbnail|name",pithumbsize=960,redirects=1,titles=it["title"])
        for pg in r["query"]["pages"]:
            if "thumbnail" in pg: cands.append({"src":"wiki:"+pg.get("title",""),"file":pg.get("pageimage"),"url":pg["thumbnail"]["source"]})
    except Exception as e: print("wiki err",it["id"],e)
    try:
        r=api(CM,action="query",generator="search",gsrsearch=it["title"]+" filetype:bitmap",gsrnamespace=6,gsrlimit=6,prop="imageinfo",iiprop="url|mime",iiurlwidth=960)
        pages=sorted(r.get("query",{}).get("pages",[]),key=lambda p:p.get("index",99))
        for pg in pages:
            ii=pg.get("imageinfo",[{}])[0]
            if ii.get("mime") in ("image/jpeg","image/png","image/webp") and "thumburl" in ii and not any(c["url"]==ii["thumburl"] for c in cands):
                cands.append({"src":"commons","file":pg["title"],"url":ii["thumburl"]})
            if len(cands)>=4: break
    except Exception as e: print("commons err",it["id"],e)
    for k,c in enumerate(cands):
        fn=f"{D}/cand/{it['id']}_{k}.jpg"
        for u in (resize(c["url"],500), resize(c["url"],330), c["url"]):
            try:
                open(fn,"wb").write(get(u,tries=2)); c["local"]=fn; break
            except Exception as e: c["err"]=str(e)
    print(it["id"],it["title"],len(cands),sum(1 for c in cands if "local" in c),flush=True)
    return it["id"],{"title":it["title"],"cands":cands}
todo=[it for it in items if it["id"] not in out]
def save_push(msg):
    json.dump(out,open(outp,"w"),ensure_ascii=False,indent=1)
    subprocess.run("git add %s && git commit -qm '%s' && git push -q"%(D,msg),shell=True)
with ThreadPoolExecutor(3) as ex:
    for n,(i,v) in enumerate(ex.map(one,todo),1):
        out[i]=v
        if n%40==0: save_push(f"{D}: candidates {len(out)}/{len(items)}")
save_push(f"{D}: candidates {len(out)}/{len(items)} done")
