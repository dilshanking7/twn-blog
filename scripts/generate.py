#!/usr/bin/env python3
"""Daily blog article generator (cloud). Gemini ya keyless Pollinations se likhta hai."""
import json, os, re, sys, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state.json")
TOPICS = os.path.join(ROOT, "topics.md")
POSTS = os.path.join(ROOT, "posts")

IST = timezone(timedelta(hours=5, minutes=30))
LANGS = {
    "en": "English",
    "hi": "Hindi (Devanagari)",
    "hinglish": "Hinglish (Roman Hindi mixed with English)",
}


def load_state():
    with open(STATE) as f:
        return json.load(f)


def load_topics():
    topics = []
    with open(TOPICS) as f:
        for line in f:
            m = re.match(r"^(\d+)\.\s+(.*)", line.strip())
            if m:
                topics.append((int(m.group(1)), m.group(2).strip()))
    return topics


GEMINI_MODELS = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3-flash",
                 "gemini-2.5-flash", "gemini-2.0-flash"]


def gen_gemini(prompt, key):
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 4096},
    }).encode()
    last = None
    for model in GEMINI_MODELS:
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               + model + ":generateContent?key=" + key)
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            last = e
    if last:
        raise last
    raise RuntimeError("gemini failed")


def gen_pollinations(prompt):
    url = "https://text.pollinations.ai/"
    body = json.dumps({
        "messages": [{"role": "user", "content": prompt}],
        "model": "openai",
        "temperature": 0.9,
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read().decode()


def generate(prompt):
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        try:
            return gen_gemini(prompt, key), "gemini"
        except Exception as e:
            print("Gemini fail, Pollinations pe ja raha hoon:", e)
    return gen_pollinations(prompt), "pollinations"


def main():
    state = load_state()
    topics = load_topics()
    if not topics:
        print("topics.md me koi topic nahi mila.")
        sys.exit(1)
    idx = state.get("next_index", 0) % len(topics)
    num, topic = topics[idx]

    cyc = state.get("language_cycle", ["en"])
    pos = state.get("language_pos", 0)
    lang_code = cyc[pos % len(cyc)]
    lang = LANGS.get(lang_code, "English")

    prompt = f"""You are writing a blog post for "dilshanking7", a blog by Dilshan, a student and developer from Dhanbad, India.

Topic: {topic}
Language: {lang}

Rules:
- Write like a real person, not an AI. No cliches like "delve", "game-changer", "in today's world", "pivotal".
- No hype, no fluff. Real facts only. If you are not sure about a fact, do not invent it.
- 500-800 words. Short paragraphs.
- Start with a real sentence, not a question or a generic intro.
- Use first person where natural.
- Output ONLY the article body paragraphs, separated by a blank line. No title, no meta.

Article:"""

    article, provider = generate(prompt)
    article = article.strip()

    today = datetime.now(IST).strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower())[:50].strip("-")
    os.makedirs(POSTS, exist_ok=True)
    path = os.path.join(POSTS, f"{today}-{slug}.md")
    with open(path, "w") as f:
        f.write(f"# {topic}\n\n")
        f.write(f"Language: {lang} | Date: {today} | Provider: {provider}\n\n")
        f.write(article + "\n")

    state["next_index"] = idx + 1
    state["language_pos"] = pos + 1
    state.setdefault("posted", []).append({
        "date": today, "topic_index": idx, "language": lang_code,
        "title": topic, "file": os.path.relpath(path, ROOT), "provider": provider,
    })
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f"POST_FILE={os.path.relpath(path, ROOT)}")
    print(f"TOPIC={topic}")
    print(f"LANG={lang_code}")
    print(f"PROVIDER={provider}")
    print("----ARTICLE----")
    print(article)


if __name__ == "__main__":
    main()
