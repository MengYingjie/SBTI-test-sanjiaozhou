import urllib.request
import os

url = "https://syimg.3dmgame.com/uploadimg/xiaz/2025/0520/1747704461568.jpg"
path = "/workspace/image/delta_ops/HeartOfAfrica.jpg"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=10) as response:
        with open(path, 'wb') as f:
            f.write(response.read())
    print(f"Successfully downloaded Heart of Africa image to {path}")
except Exception as e:
    print(f"Failed to download: {e}")
