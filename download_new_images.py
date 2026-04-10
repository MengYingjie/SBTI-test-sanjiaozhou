import urllib.request
import time
import os

def fetch_image(base_url, output_path):
    print(f"Starting fetch for {base_url}")
    max_retries = 60
    retry_interval = 5

    for i in range(max_retries):
        try:
            # Add timestamp to bypass cache
            url = f"{base_url}&t={int(time.time())}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

            class NoRedirection(urllib.request.HTTPErrorProcessor):
                def http_response(self, request, response):
                    return response
                https_response = http_response

            opener = urllib.request.build_opener(NoRedirection)
            with opener.open(req) as response:
                status = response.status
                if status == 302:
                    location = response.headers.get('Location', '')
                    if 'default.jpeg' in location:
                        print(f"[{i+1}/{max_retries}] Still generating... (302 to default)")
                        time.sleep(retry_interval)
                        continue
                    else:
                        print(f"Done! Image URL: {location}")
                        urllib.request.urlretrieve(location, output_path)
                        print(f"Saved to {output_path}")
                        return True
                elif status == 200:
                    print(f"Done! Received 200 OK")
                    with open(output_path, 'wb') as f:
                        f.write(response.read())
                    return True
                else:
                    print(f"[{i+1}/{max_retries}] Unexpected status: {status}")
                    time.sleep(retry_interval)

        except Exception as e:
            print(f"[{i+1}/{max_retries}] Error: {e}")
            time.sleep(retry_interval)

    print(f"Failed to download image for {output_path} after maximum retries.")
    return False

# Ensure directory exists
os.makedirs("/workspace/image/delta_ops", exist_ok=True)

import urllib.parse

# List of prompts for missing operators and meme characters
prompts = {
    "Yinyi": "A futuristic recon soldier with a sniper rifle and a drone, cyberpunk tactical gear, realistic",
    "Die": "A female medic soldier with a medical drone, tactical cyberpunk uniform, realistic",
    "Bite": "A tactical engineer soldier deploying smart spider mines, cyberpunk style, realistic",
    "Zuoya": "A female support soldier with adrenaline stims and a drone swarm, cyberpunk tactical, realistic",
    "Shenlan": "A heavy juggernaut soldier with a massive riot shield, tactical armor, realistic",
    "Wuming": "A stealth assassin soldier with throwing blades and cloaking device, tactical cyberpunk, realistic",
    "AsaraGuard": "A heavily armored elite NPC guard soldier, tactical combat gear, realistic",
    "AfricanStar": "A sad soldier opening an empty loot box, funny tactical meme, realistic",
    "TearOfOcean": "A glowing blue futuristic gem in a tactical briefcase, cyberpunk style",
    "T6Juggernaut": "A massive soldier wearing top tier heavy armor made of solid gold, funny tactical meme",
    "DamGuard": "A soldier sitting on a folding chair guarding a massive concrete dam, funny tactical meme",
    "LongbowSniper": "A sniper covered in ghillie suit covered in moss, aiming from a mountain top, funny tactical meme",
    "SpaceRat": "A soldier with a ridiculously oversized backpack overflowing with loot, hiding in a corner, funny tactical meme",
    "ToeClipper": "A soldier aiming a shotgun specifically at someone's toes, funny tactical meme",
    "OutlineMaster": "A soldier shooting wildly but every bullet perfectly misses the target, funny tactical meme",
    "MedicsDaddy": "A medic soldier dragging a heavily wounded reckless teammate, funny tactical meme",
    "GrenadeGod": "A soldier carrying 50 grenades strapped to their chest, laughing maniacally, funny tactical meme",
    "TheRat": "A soldier hiding inside a bush with just their eyes peeking out, funny tactical meme"
}

for name, prompt_text in prompts.items():
    output_file = f"/workspace/image/delta_ops/{name}.png"
    if os.path.exists(output_file):
        print(f"Skipping {name}, already exists.")
        continue
    
    encoded_prompt = urllib.parse.quote(prompt_text)
    url = f"https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square"
    fetch_image(url, output_file)

