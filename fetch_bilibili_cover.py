import urllib.request
import json
import urllib.parse
import os

keyword = urllib.parse.quote("三角洲行动 六套 装备 满改")
url = f"https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={keyword}"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))
    
    # Get the first video thumbnail
    pic_url = data['data']['result'][0]['pic']
    if pic_url.startswith('//'):
        pic_url = 'https:' + pic_url
        
    print(f"Found Bilibili cover image: {pic_url}")
    
    req_img = urllib.request.Request(pic_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_img) as resp_img:
        with open('/workspace/image/delta_ops/T6Juggernaut.jpg', 'wb') as f:
            f.write(resp_img.read())
            
    print("Downloaded successfully.")
except Exception as e:
    print(f"Error: {e}")
