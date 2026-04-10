import urllib.request
import os

url = "https://i1.hdslb.com/bfs/archive/e42cde2f91e5d0ae08f7a151e2ebdd1339a1d5c0.jpg"
path = "/workspace/image/delta_ops/DamGuard.jpg"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=10) as response:
        with open(path, 'wb') as f:
            f.write(response.read())
    print(f"Successfully downloaded Dam Guard image to {path}")
except Exception as e:
    print(f"Failed to download: {e}")
