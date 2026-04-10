import urllib.request
import os
import urllib.parse

# Using corsproxy.io
original_url = "https://p3-pc-sign.douyinpic.com/tos-cn-i-0813/ocaH2fKYgIIADAC5eIjFWBcEQbDAF5AOeAf25k~tplv-dy-aweme-images:q75.webp"
proxy_url = f"https://corsproxy.io/?{urllib.parse.quote(original_url)}"
path = "/workspace/image/delta_ops/T6Juggernaut.jpg"

try:
    req = urllib.request.Request(proxy_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    with urllib.request.urlopen(req, timeout=15) as response:
        with open(path, 'wb') as f:
            f.write(response.read())
    print(f"Successfully downloaded T6 Juggernaut image via corsproxy to {path}")
except Exception as e:
    print(f"Failed to download via corsproxy: {e}")
