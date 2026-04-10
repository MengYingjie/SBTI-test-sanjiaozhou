import urllib.request
import os

# Let's try downloading the original image by removing the image processing query string
url = "https://p3-pc-sign.douyinpic.com/tos-cn-i-0813/ocaH2fKYgIIADAC5eIjFWBcEQbDAF5AOeAf25k"
path = "/workspace/image/delta_ops/T6Juggernaut.jpg"

try:
    os.system(f"wget -q -U 'Mozilla/5.0' --header 'Referer: https://www.douyin.com/' '{url}' -O {path}")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f"Successfully downloaded T6 Juggernaut image using wget to {path}")
    else:
        print("Failed to download using wget")
except Exception as e:
    print(f"Failed: {e}")
