import urllib.request
import os

# Extracting the actual image URL from the Baidu image search detail URL
# The 'objurl' parameter contains the original image URL:
url = "https://i2.hdslb.com/bfs/archive/21558010714e4bd4b617c9da7a0e90a804cb82e5.jpg"
path = "/workspace/image/delta_ops/HeartOfAfrica.jpg"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=10) as response:
        with open(path, 'wb') as f:
            f.write(response.read())
    print(f"Successfully downloaded Heart of Africa image from Bilibili to {path}")
except Exception as e:
    print(f"Failed to download: {e}")
