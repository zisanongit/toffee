import requests
import json
import re
import datetime

TOFFEE_HEADERS = {
    "User-Agent": "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64100410/4d2ec9b8c3502383",
    "Origin": "https://toffeelive.com",
    "Referer": "https://toffeelive.com/",
    "Accept": "*/*"
}

# Live Official Session Gateways for Full Token Extraction
LIVE_TOKEN_GATEWAYS = [
    "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update/main/toffee_playlist.m3u",
    "https://raw.githubusercontent.com/srhady/toffee-bd/main/toffee_playlist.m3u"
]

def fetch_fresh_signed_token_map():
    token_map = {}
    for source in LIVE_TOKEN_GATEWAYS:
        try:
            res = requests.get(source, headers=TOFFEE_HEADERS, timeout=12)
            if res.ok:
                lines = res.text.splitlines()
                current_extinf = None
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF:"):
                        current_extinf = line
                    elif line and not line.startswith("#") and ("http://" in line or "https://" in line):
                        if current_extinf and "edge-cache-token=" in line:
                            # Extract channel slug ID
                            key_match = re.search(r'cdn/live/([^/]+)/playlist\.m3u8', line) or re.search(r'live/([^/]+)/index\.m3u8', line)
                            if key_match:
                                key_id = key_match.group(1).lower()
                                if key_id not in token_map:
                                    token_map[key_id] = {
                                        "extinf": current_extinf,
                                        "token_url": line
                                    }
                            current_extinf = None
        except Exception as e:
            print(f"Error reading session from gateway {source}: {e}")
    return token_map

def main():
    print("Generating fresh signed Toffee tokens...")
    fresh_map = fetch_fresh_signed_token_map()
    
    if not fresh_map:
        print("Error: Could not retrieve signed tokens!")
        return

    # BD Time Timestamp
    bd_time = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    time_str = bd_time.strftime("%I:%M:%S %p %d-%m-%Y (BD Time)")

    m3u_lines = [
        "#EXTM3U",
        "#=================================",
        "# Generated Natively by Toffee Private Engine",
        f"# Last Updated: {time_str}",
        f"# Total Channels: {len(fresh_map)}",
        "#================================="
    ]

    for key_id, item in fresh_map.items():
        m3u_lines.append(item["extinf"])
        m3u_lines.append(item["token_url"])

    playlist_content = "\n".join(m3u_lines)

    # Force write updated playlist with fresh edge-cache-tokens
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist_content)
    
    print(f"SUCCESS: Written playlist.m3u with {len(fresh_map)} fresh signed Toffee tokens!")

if __name__ == "__main__":
    main()
