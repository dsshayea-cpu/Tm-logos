import json, os, time, urllib.request, urllib.parse
UA={"User-Agent":"TM-trivia-image-fetch/1.0 (github.com/dsshayea-cpu/tm-logos)"}
def get(url, tries=4):
    for t in range(tries):
        try:
            req=urllib.request.Request(url,headers=UA)
            with urllib.request.urlopen(req,timeout=30) as r: return r.read()
        except Exception as e:
            time.sleep(3*(t+1)); err=e
    raise err
def api(base, **p):
    p.update(format="json", formatversion=2)
    return json.loads(get(base+"?"+urllib.parse.urlencode(p)))
EN="https://en.wikipedia.org/w/api.php"; CM="https://commons.wikimedia.org/w/api.php"
items=json.load(open("ahl-albar/titles.json"))
os.makedirs("ahl-albar/cand",exist_ok=True)
out={}
for it in items:
    cands=[]
    try:
        r=api(EN,action="query",prop="pageimages",piprop="thumbnail|name",pithumbsize=800,redirects=1,titles=it["title"])
        for pg in r["query"]["pages"]:
            if "thumbnail" in pg: cands.append({"src":"wiki:"+pg.get("title",""),"file":pg.get("pageimage"),"url":pg["thumbnail"]["source"]})
    except Exception as e: print("wiki err",it,e)
    try:
        r=api(CM,action="query",generator="search",gsrsearch=it["title"]+" filetype:bitmap",gsrnamespace=6,gsrlimit=6,prop="imageinfo",iiprop="url|mime",iiurlwidth=800)
        pages=sorted(r.get("query",{}).get("pages",[]),key=lambda p:p.get("index",99))
        for pg in pages:
            ii=pg.get("imageinfo",[{}])[0]
            if ii.get("mime") in ("image/jpeg","image/png","image/webp") and "thumburl" in ii:
                if not any(c["url"]==ii["thumburl"] for c in cands):
                    cands.append({"src":"commons","file":pg["title"],"url":ii["thumburl"]})
            if len(cands)>=4: break
    except Exception as e: print("commons err",it,e)
    for k,c in enumerate(cands):
        small=c["url"]
        # 320px copy for review
        if "/thumb/" in small:
            small=small.rsplit("/",1)[0]+"/"+"320px-"+small.rsplit("/",1)[1].split("px-",1)[-1]
        try:
            data=get(small); fn=f"ahl-albar/cand/{it['id']}_{k}.jpg"
            open(fn,"wb").write(data); c["local"]=fn
        except Exception as e:
            try:
                data=get(c["url"]); fn=f"ahl-albar/cand/{it['id']}_{k}.jpg"; open(fn,"wb").write(data); c["local"]=fn
            except Exception as e2: c["err"]=str(e2)
        time.sleep(0.3)
    out[it["id"]]={"title":it["title"],"cands":cands}
    print(it["id"],it["title"],len(cands),flush=True)
json.dump(out,open("ahl-albar/candidates.json","w"),ensure_ascii=False,indent=1)
