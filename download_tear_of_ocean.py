import urllib.request
import os

# Extracting the actual image URL from the Baidu image search detail URL
# The 'objurl' parameter contains the original image URL for Tear of Ocean:
url = "https://i0.hdslb.com/bfs/archive/47634107c8b5cd6e56c8e4b17e6d4bf58d970228.jpg"
path = "/workspace/image/delta_ops/TearOfOcean.jpg"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=10) as response:
        with open(path, 'wb') as f:
            f.write(response.read())
    print(f"Successfully downloaded Tear of Ocean image from Bilibili to {path}")
except Exception as e:
    print(f"Failed to download: {e}")
