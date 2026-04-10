import os
import json
import urllib.request
import urllib.parse
import re

# Specific URLs found for the new operators
operator_urls = {
    "SilverWing.jpg": "https://p3-sdbk2-media.byteimg.com/tos-cn-i-xv4ileqgde/ff63ee42a0fb4e8185a4d28592e75f1c~tplv-xv4ileqgde-resize-w:360.image",
    "Butterfly.jpg": "https://game.gtimg.cn/images/dfm/cp/a20240906main/p4_img13.jpg",
    "Bit.jpg": "https://game.gtimg.cn/images/dfm/cp/a20240906main/p4_img12.jpg",
    "Zoya.jpg": "https://img1.ali213.net/glpic/2024/11/18/8bbf8347-9602-81e7-abf8-82fe0b972ee2.jpg",
    "DeepBlue.jpg": "https://syimg.3dmgame.com/uploadimg/upload/image/20250116/20250116130429_60946.jpg",
    "Nameless.jpg": "https://img1.gamersky.com/image2025/11/20251129_cej_668_12/10_S.jpg",
    "AsaraGuard.jpg": "https://wegame.gtimg.com/tgp_act/release/release/df20240926/images//feature/img-feature-01.jpg" # Generic soldiers
}

meme_queries = {
    "AfricanStar.jpg": "非洲黑人 搞笑 表情包",
    "TearOfOcean.jpg": "钻石 宝石 极品 游戏 截图",
    "T6Juggernaut.jpg": "重装步兵 全身防弹衣 游戏",
    "DamGuard.jpg": "水坝 保安 搞笑",
    "LongbowSniper.jpg": "伏地魔 狙击手 游戏 搞笑",
    "SpaceRat.jpg": "仓鼠 屯物资 表情包",
    "ToeClipper.jpg": "修脚 搞笑 表情包",
    "OutlineMaster.jpg": "人体描边 射击 搞笑",
    "MedicsDaddy.jpg": "医疗兵 救命 搞笑",
    "GrenadeGod.jpg": "爆炸 艺术 炸弹 搞笑",
    "TheRat.jpg": "老六 蹲草丛 搞笑 游戏"
}

def download_image(url, path):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        print(f"Downloaded: {path}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def fetch_image_from_duckduckgo(query, path):
    print(f"Searching web for: {query}")
    try:
        # Very simple DuckDuckGo HTML search for images
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query + " image")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        
        # Find image urls in the html
        images = re.findall(r'src="(//external-content\.duckduckgo\.com/iu/\?u=[^"]+)"', html)
        if images:
            img_url = "https:" + images[0].replace("&amp;", "&")
            return download_image(img_url, path)
    except Exception as e:
        print(f"Search failed for {query}: {e}")
    
    # Fallback to a placeholder if search fails
    print(f"Using placeholder for {query}")
    return download_image(f"https://placehold.co/400x400/1a1d1e/fbbf24.png?text={urllib.parse.quote(query.split()[0])}", path)

os.makedirs("/workspace/image/delta_ops", exist_ok=True)

# Download operator images
for filename, url in operator_urls.items():
    path = f"/workspace/image/delta_ops/{filename}"
    if not os.path.exists(path):
        download_image(url, path)
    else:
        print(f"Already exists: {path}")

# Download meme images by searching the web
for filename, query in meme_queries.items():
    path = f"/workspace/image/delta_ops/{filename}"
    if not os.path.exists(path):
        fetch_image_from_duckduckgo(query, path)
    else:
        print(f"Already exists: {path}")

print("Web search and download complete.")
