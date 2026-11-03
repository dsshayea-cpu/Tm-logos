# Generate the retro comic film pictures with the Gemini API.
# Usage: GK=<gemini key> python3 gen_all.py [ids...]   (default: all missing)
import json, os, sys, time, base64, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
HERE=os.path.dirname(os.path.abspath(__file__)); KEY=os.environ['GK']
P=json.load(open(f'{HERE}/prompts.json'))
want=set(sys.argv[1:]) or {p['id'] for p in P if not os.path.exists(f"{HERE}/img/{p['id']}.jpg")}
def gen(p):
    body={"contents":[{"parts":[{"text":p['prompt']}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9"}}}
    for t in range(4):
        try:
            req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image:generateContent",
                data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":KEY})
            r=json.load(urllib.request.urlopen(req,timeout=300))
            for part in r["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    open(f"{HERE}/img/{p['id']}.jpg","wb").write(base64.b64decode(part["inlineData"]["data"])); return p['id'],'ok'
            return p['id'],'noimage:'+json.dumps(r)[:200]
        except urllib.error.HTTPError as e:
            msg=e.read().decode()[:200]
            if e.code==429: time.sleep(60); continue
            return p['id'],f'http{e.code}:{msg}'
        except Exception as e: time.sleep(5); err=str(e)
    return p['id'],'fail'
with ThreadPoolExecutor(2) as ex:
    for i,s in ex.map(gen,[p for p in P if p['id'] in want]): print(i,s,flush=True)
