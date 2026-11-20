#!/usr/bin/env python3
"""Generated article ko platforms pe post karta hai (agar API token milta hai).

Supported (free tokens):
- DEV.to        -> DEV_API_KEY
- Medium        -> MEDIUM_TOKEN
- Hashnode      -> HASHNODE_KEY + HASHNODE_PUBLICATION_ID

WordPress.com / Blogger / Substack ke liye alag tokens chahiye — wo local cron se hote hain.
"""
import json, os, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "posts")


def http_json(url, data=None, headers=None, method="POST"):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return 0, str(e)


def latest_post():
    files = sorted(f for f in os.listdir(POSTS) if f.endswith(".md"))
    if not files:
        return None, None
    p = os.path.join(POSTS, files[-1])
    with open(p) as f:
        txt = f.read()
    lines = txt.splitlines()
    title = lines[0].lstrip("# ").strip() if lines else files[-1]
    body = "\n".join(lines[2:]).strip() if len(lines) > 2 else txt
    return title, body


def post_dev(title, body):
    key = os.environ.get("DEV_API_KEY")
    if not key:
        return "skip (no DEV_API_KEY)"
    data = {"article": {"title": title, "published": True,
                        "body_markdown": body, "tags": ["blog", "ai", "tech"]}}
    st, resp = http_json("https://dev.to/api/articles", data,
                         {"api-key": key, "Content-Type": "application/json"})
    return f"{st} {resp.get('url','') if isinstance(resp,dict) else resp}"


def post_medium(title, body):
    tok = os.environ.get("MEDIUM_TOKEN")
    if not tok:
        return "skip (no MEDIUM_TOKEN)"
    st, resp = http_json("https://api.medium.com/v1/me", None,
                         {"Authorization": f"Bearer {tok}"})
    if not isinstance(resp, dict) or "data" not in resp:
        return f"{st} {resp}"
    uid = resp["data"]["id"]
    data = {"title": title, "format": "markdown", "content": body,
            "publishStatus": "public", "tags": ["AI", "Tech", "Blog"]}
    st, resp = http_json(f"https://api.medium.com/v1/users/{uid}/posts", data,
                         {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    return f"{st} {resp.get('data',{}).get('url','') if isinstance(resp,dict) else resp}"


def post_hashnode(title, body):
    key = os.environ.get("HASHNODE_KEY")
    pub = os.environ.get("HASHNODE_PUBLICATION_ID")
    if not key or not pub:
        return "skip (no HASHNODE_KEY/PUBLICATION_ID)"
    q = """mutation($i: CreateStoryInput!){ createStory(input:$i){ story{ url } } }"""
    data = {"query": q, "variables": {"i": {
        "title": title, "contentMarkdown": body, "publicationId": pub,
        "tags": [], "isPublished": True}}}
    st, resp = http_json("https://gql.hashnode.com", data,
                         {"Authorization": key, "Content-Type": "application/json"})
    return f"{st} {resp}"


def main():
    title, body = latest_post()
    if not title:
        print("Koi post nahi mili.")
        return
    print("Title:", title)
    print("DEV.to     :", post_dev(title, body))
    print("Medium     :", post_medium(title, body))
    print("Hashnode   :", post_hashnode(title, body))


if __name__ == "__main__":
    main()
