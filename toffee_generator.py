import requests
import json
import uuid

TOFFEE_HEADERS = {
    "User-Agent": "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64100410/4d2ec9b8c3502383",
    "Origin": "https://toffeelive.com",
    "Referer": "https://toffeelive.com/",
    "Accept": "*/*"
}

# আপনি যত খুশি চ্যানেলের আইডি ও পাথ এখানে যোগ করতে পারেন
CHANNELS = [
    {"id": "toffee_tv", "name": "Toffee TV", "group": "Family", "path": "cdn/live/toffee_drama/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/DNMXs5UBm1RY_In7IJ72/posters/737b5c6e-8435-4cd8-81de-16a499fa6f4e.png"},
    {"id": "cnn", "name": "CNN International", "group": "Documentary", "path": "cdn/live/cnn/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/VC6Q-JQBv9knK3AHhTXt/posters/63e79814-8fcf-4c3e-bb66-408b2a402613.webp"},
    {"id": "somoy_tv", "name": "Somoy TV", "group": "Live Action", "path": "cdn/live/somoy_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Xi_Ga5oBNnOkwJLWkhKP/posters/ef2899d5-1ae0-4fee-aee5-45f9b0b3ba80.png"},
    {"id": "jamuna_tv", "name": "Jamuna TV", "group": "Live Action", "path": "cdn/live/jamuna_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/PiL635oBEef-9-uV2uCe/posters/36f380e0-6c71-4b27-a73b-2afb3ce7e982.png"},
    {"id": "tsports", "name": "T Sports", "group": "Sports", "path": "cdn/live/tsports/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/HHnAgJkBcqxnFHJBabwO/posters/967dd1fe-c2af-442e-a0b1-22320ed82c88.png"},
    {"id": "zee_bangla", "name": "Zee Bangla", "group": "Drama", "path": "cdn/live/zee_bangla/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/kK2aX5UBrjBfS2_RBcKf/posters/ba5dd8dc-4f87-414a-b57f-c9ecdeda5253.png"},
    {"id": "sonyentertainmnt_hd", "name": "Sony Entertainment HD", "group": "Entertainment", "path": "cdn/live/sonyentertainmnt_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/kK2aX5UBrjBfS2_RBcKf/posters/ba5dd8dc-4f87-414a-b57f-c9ecdeda5253.png"}
]

def fetch_fresh_token_url(channel_path):
    device_id = str(uuid.uuid4())
    headers = dict(TOFFEE_HEADERS)
    headers["X-Device-Id"] = device_id
    headers["X-Session-Token"] = device_id
    
    url = f"https://prod-linear-media.toffeelive.com/{channel_path}"
    try:
        res = requests.get(url, headers=headers, allow_redirects=True, timeout=12)
        if res.ok or res.status_code == 302:
            return res.url if res.url else url
    except Exception as e:
        print(f"Error fetching {channel_path}: {e}")
    return url

def main():
    m3u_lines = ["#EXTM3U"]
    for ch in CHANNELS:
        fresh_url = fetch_fresh_token_url(ch["path"])
        m3u_lines.append(f'#EXTINF:-1 tvg-id="{ch["id"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}')
        m3u_lines.append(fresh_url)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
    print(f"Successfully generated playlist.m3u with {len(CHANNELS)} channels.")

if __name__ == "__main__":
    main()
