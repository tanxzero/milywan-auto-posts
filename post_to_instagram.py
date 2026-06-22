import os
import json
import time
import requests
from datetime import date, datetime

GRAPH_VERSION = os.getenv("GRAPH_VERSION", "v21.0")
GRAPH_URL = f"https://graph.facebook.com/{GRAPH_VERSION}"

META_ACCESS_TOKEN = os.environ["META_ACCESS_TOKEN"]
IG_USER_ID = os.environ["INSTAGRAM_BUSINESS_ACCOUNT_ID"]
BASE_URL = os.environ["GITHUB_PAGES_BASE_URL"].rstrip("/")
POST_ID = os.getenv("POST_ID")
START_DATE = os.getenv("START_DATE", "2026-06-22")

def api_post(path, data):
    payload = dict(data)
    payload["access_token"] = META_ACCESS_TOKEN
    response = requests.post(f"{GRAPH_URL}/{path}", data=payload, timeout=60)
    try:
        result = response.json()
    except Exception:
        raise RuntimeError(f"Non-JSON response: {response.text}")
    if response.status_code >= 400 or "error" in result:
        raise RuntimeError(json.dumps(result, indent=2))
    return result

def choose_post(posts):
    if POST_ID:
        chosen = next((p for p in posts if p["id"] == POST_ID), None)
        if not chosen:
            raise ValueError(f"POST_ID not found in posts.json: {POST_ID}")
        return chosen

    start = datetime.strptime(START_DATE, "%Y-%m-%d").date()
    index = (date.today() - start).days % len(posts)
    return posts[index]

def build_caption(post):
    hashtags = " ".join(post.get("hashtags", []))
    return f"{post['caption']}\n\n{hashtags}"

def publish_carousel(post):
    post_id = post["id"]
    children = []

    for i in range(1, 6):
        image_url = f"{BASE_URL}/posts/{post_id}/slide_{i}.jpg"
        print(f"Creating carousel item {i}: {image_url}")
        item = api_post(f"{IG_USER_ID}/media", {
            "image_url": image_url,
            "is_carousel_item": "true"
        })
        children.append(item["id"])
        time.sleep(2)

    print("Creating parent carousel...")
    parent = api_post(f"{IG_USER_ID}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(children),
        "caption": build_caption(post)
    })

    time.sleep(5)

    print("Publishing carousel...")
    published = api_post(f"{IG_USER_ID}/media_publish", {
        "creation_id": parent["id"]
    })

    print("Published:", json.dumps(published, indent=2))

def main():
    with open("posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    post = choose_post(posts)
    print(f"Selected post: {post['id']} - {post['topic']}")
    publish_carousel(post)

if __name__ == "__main__":
    main()
