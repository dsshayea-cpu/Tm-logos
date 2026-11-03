# Retro comic film questions (ما اسم الفيلم او المسلسل ؟) — handoff

Goal: 210 TM picture questions in the قولبها "ريترو أفلام" style: black-and-white halftone comic
drawing of a film's famous scene, made with Gemini (gemini-3.1-flash-image, 16:9).
70 each at 200 / 400 / 600. Answer = English film title only. Question text for all:
"ما اسم الفيلم او المسلسل ؟". Do NOT add to TM yet — show the user a preview artifact first.

Files here:
- prompts.json — 210 items {id r001..r210, diff, answer, prompt} (built by build.py from films*.py)
- img/ — finished pictures: all 210 generated and checked (2026-11-03). Redone after review:
  r016 r045 r054 r084 r106 r113 r148 r164 r172 r187 r201 (title written, corner badges, garbled text).
  Prompts tweaked for r054 (Bad Boys), r164 (Groundhog Day), r172 (Seven), r187 (Moulin Rouge!).
  Some have colour accents (r027 r029 r036 r122 r193 …; r178 Her is red on purpose) — user to decide.
  Status: preview shown to user; waiting for approval + TM category name (step 5).
- gen_all.py — `GK=<key> python3 gen_all.py` generates every missing picture into img/

Steps for the new chat:
1. Ask the user for the Gemini API key (never commit it). Test the API is reachable.
2. Run gen_all.py (2 at a time; the account hit Gemini's spend-based rate limit at ~150 fast
   requests, so if 429s keep coming, stop and tell the user).
3. Check every picture (contact sheets): no film title / names written, no corner icons or
   badges, scene recognisable. Regenerate bad ones (`python3 gen_all.py r012 r045`).
4. Commit img/ to this repo, publish a preview artifact (picture + answer, grouped 200/400/600).
5. After approval, add to the TM category the user names (image via raw GitHub link).
