import urllib.request
import os

base_url = "https://game.gtimg.cn/images/dfm/cp/a20240906main/"

mapping = {
    "p4_img1.jpg": "Hackclaw_official.jpg", # 骇爪
    "p4_img2.jpg": "Vyron_official.jpg",    # 威龙
    "p4_img3.jpg": "David_official.jpg",    # 乌鲁鲁
    "p4_img4.jpg": "Luna_official.jpg",     # 露娜
    "p4_img5.jpg": "Roy_official.jpg",      # 蜂医
    "p4_img6.jpg": "Kai_official.jpg",      # 红狼
    "p4_img7.jpg": "Terry_official.jpg"     # 牧羊人
}

os.makedirs("/workspace/image/delta_ops", exist_ok=True)

for src_name, dest_name in mapping.items():
    url = base_url + src_name
    path = f"/workspace/image/delta_ops/{dest_name}"
    print(f"Downloading {url} to {path}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        print("Success.")
    except Exception as e:
        print(f"Failed: {e}")

