import urllib.request
import os

url = "https://img.18183.com/uploads/allimg/251117/520-25111G62518.jpg"
path = "/workspace/image/delta_ops/HeartOfAfrica.jpg"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=10) as response:
        with open(path, 'wb') as f:
            f.write(response.read())
    print(f"Successfully downloaded Heart of Africa image to {path}")
except Exception as e:
    print(f"Failed to download: {e}")
