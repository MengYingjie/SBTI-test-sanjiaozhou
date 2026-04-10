import urllib.request
import os
import ssl

url = "https://p3-pc-sign.douyinpic.com/tos-cn-i-0813/ocaH2fKYgIIADAC5eIjFWBcEQbDAF5AOeAf25k~tplv-dy-aweme-images:q75.webp"
path = "/workspace/image/delta_ops/T6Juggernaut.jpg"

try:
    # Set up SSL context to ignore certificate errors if any
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Add extensive headers to mimic a real browser from Baidu/Douyin
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://image.baidu.com/',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site'
    }
    
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
        with open(path, 'wb') as f:
            f.write(response.read())
    print(f"Successfully downloaded T6 Juggernaut image with advanced headers to {path}")
except Exception as e:
    print(f"Failed to download: {e}")
