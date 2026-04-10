import urllib.request
import re

url = "https://df.qq.com/main.shtml"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    print("Fetched main page. Looking for images...")
    img_files = re.findall(r'(https?://[^"]+\.(?:png|jpg|webp))', response)
    for img in img_files:
        if "role" in img.lower() or "hero" in img.lower() or "character" in img.lower() or "p" in img.lower():
            print(img)
except Exception as e:
    print(e)
