import urllib.request

url = "https://img1.gamersky.com/image2024/09/20240926_jqy_367_1/924.jpg" # Delta Force inventory screenshot
path = "/workspace/image/delta_ops/T6Juggernaut.jpg"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        with open(path, 'wb') as f:
            f.write(response.read())
    print("Successfully downloaded an inventory screenshot for T6 Juggernaut.")
except Exception as e:
    print(e)
