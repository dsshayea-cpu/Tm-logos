import json, re
from films import F; from films2 import F2; from films3 import F3
A=[f for f in F+F2+F3 if f[2] and f[1] not in ("Inside Man","Heat","The Irishman")]
fix={"Goodfellas":(5,"a pot of tomato sauce, a restaurant with red tablecloths"),
     "Click":(5,"a shopping bag, a frozen ball in the air"),
     "Cast Away":(5,"delivery parcels piled on the sand, a fire made with sticks"),
     "Jaws":(5,"yellow barrels floating on the water, a beach far away")}
A=[tuple(f[:5])+(fix[f[1]][1],) if f[1] in fix else f for f in A]
A.sort(key=lambda f:f[0])
out=[]
for i,(d,ans,scene,q,sfx,h) in enumerate(A,1):
    sfx=re.sub(r"\(.*?\)","",sfx).strip()
    p=("Black and white comic book illustration in a hand-inked style: bold clean outlines, grey shading and newspaper halftone dot texture, high contrast. "
       "Characters are drawn as expressive cartoon caricatures, not realistic portraits and not likenesses of any real actor.\n\n"
       f"Scene: {scene}.\n\n")
    if q: p+=f"Add a comic speech bubble from the main character saying \"{q}\".\n"
    if sfx and sfx.strip('.!? '): p+=f"Add comic sound-effect words \"{sfx}\" around the action.\n"
    p+=(f"\nSmall hidden hints: {h} — drawn as small, subtle details inside the scene itself, not in frames, badges or corner icons.\n\n"
        "Thin plain black border with plain empty corners. No icons, emblems or badges in the corners or on the border. "
        "Do NOT write the film's title or any character or actor names anywhere in the image. Wide 16:9 landscape, single panel, everything clearly visible.")
    out.append({"id":f"r{i:03d}","diff":d,"answer":ans,"prompt":p})
json.dump(out,open("prompts.json","w"),ensure_ascii=False,indent=0)
import collections; print(len(out), collections.Counter(o['diff'] for o in out))
print(out[70]['prompt'])
