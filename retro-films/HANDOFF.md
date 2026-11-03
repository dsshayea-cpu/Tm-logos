# Retro comic film questions (ما اسم الفيلم او المسلسل ؟) — handoff

Goal: 210 TM picture questions in the قولبها "ريترو أفلام" style: black-and-white halftone comic
drawing of a film's famous scene, made with Gemini (gemini-3.1-flash-image, 16:9).
70 each at 200 / 400 / 600. Answer = English film title only. Question text for all:
"ما اسم الفيلم او المسلسل ؟". Do NOT add to TM yet — show the user a preview artifact first.

Files here:
- prompts.json — 210 items {id r001..r210, diff, answer, prompt} (built by build.py from films*.py)
- img/ — finished pictures (8 so far: r065 r068-r072 r076 r083, all checked OK)
- gen_all.py — `GK=<key> python3 gen_all.py` generates every missing picture into img/

Steps for the new chat:
1. Ask the user for the Gemini API key (never commit it). Test the API is reachable.
2. Run gen_all.py (2 at a time; the account hit Gemini's spend-based rate limit at ~150 fast
   requests, so if 429s keep coming, stop and tell the user).
3. Check every picture (contact sheets): no film title / names written, no corner icons or
   badges, scene recognisable. Regenerate bad ones (`python3 gen_all.py r012 r045`).
4. Commit img/ to this repo, publish a preview artifact (picture + answer, grouped 200/400/600).
5. After approval, add to the TM category the user names (image via raw GitHub link).
