import urllib.request
import os

url = "https://trae-test-1258344700.cos.ap-guangzhou.myqcloud.com/solo_chat_images/t6_juggernaut.jpg"
# Or using the URL of the image from your prompt
path = "/workspace/image/delta_ops/T6Juggernaut.jpg"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        with open(path, 'wb') as f:
            f.write(response.read())
    print("Downloaded")
except:
    pass
