# twn-blog — dilshanking7 daily blog (cloud)

Laptop band hone pe bhi har subah 8:00 baje (IST) article generate hota hai.

## Kaise chalta hai
- GitHub Actions `.github/workflows/daily.yml` roz 8:00 IST chalta hai.
- `scripts/generate.py` Gemini se human-like article likhta hai, `posts/` me save karta hai.
- `scripts/publish.py` article ko DEV.to / Medium / Hashnode pe daalta hai (agar tokens hon).

## Secrets (repo Settings -> Secrets and actions)
- `GEMINI_API_KEY` — article generation (zaroori)
- `DEV_API_KEY` — dev.to settings se
- `MEDIUM_TOKEN` — medium.com/me/settings/integration-tokens se
- `HASHNODE_KEY` + `HASHNODE_PUBLICATION_ID` — hashnode developer settings se

## Language cycle
English, English, Hindi, English, English, Hinglish — rotate.

## Local bhi chalana
```
python3 scripts/generate.py     # GEMINI_API_KEY env me chahiye
python3 scripts/publish.py
```
