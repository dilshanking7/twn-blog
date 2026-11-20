#!/usr/bin/env python3
"""Daily blog article generator (cloud). Gemini se human-like article likhta hai."""
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


def gemini(prompt, key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + key
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 4096},
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    return data["candidates"][0]["content"]["parts"][0]["text"]


def main():
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        print("GEMINI_API_KEY nahi mili — article generate nahi hua.")
        sys.exit(1)

    state = load_state()
    topics = load_topics()
    idx = state.get("next_index", 0)
    if idx >= len(topics):
        idx = 0
    num, topic = topics[idx]

    lang_code = state.get("language_cycle", ["en"])[state.get("language_pos", 0) % len(state.get("language_cycle", ["en"]))]
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
- Output ONLY the article body paragraphs, separated by a blank line. No title, no meta, no bullet points unless the topic needs a list.

Article:"""

    article = gemini(prompt, key).strip()
    today = datetime.now(IST).strftime("%Y-%m-%d")
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower())[:50].strip("-")
    os.makedirs(POSTS, exist_ok=True)
    path = os.path.join(POSTS, f"{today}-{slug}.md")
    with open(path, "w") as f:
        f.write(f"# {topic}\n\n")
        f.write(f"Language: {lang} | Date: {today}\n\n")
        f.write(article + "\n")

    state["next_index"] = idx + 1
    state["language_pos"] = state.get("language_pos", 0) + 1
    state.setdefault("posted", []).append({
        "date": today, "topic_index": idx, "language": lang_code,
        "title": topic, "file": os.path.relpath(path, ROOT),
    })
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f"POST_FILE={os.path.relpath(path, ROOT)}")
    print(f"TOPIC={topic}")
    print(f"LANG={lang_code}")
    print("----ARTICLE----")
    print(article)


if __name__ == "__main__":
    main()
