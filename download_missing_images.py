import urllib.request
import urllib.parse
import time
import os

def fetch_image(prompt, output_path):
    encoded_prompt = urllib.parse.quote(prompt)
    base_url = f"https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square"
    print(f"Generating: {output_path}...")
    max_retries = 60
    retry_interval = 5

    for i in range(max_retries):
        try:
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
                        time.sleep(retry_interval)
                        continue
                    else:
                        print(f" -> Done! Saved to {output_path}")
                        urllib.request.urlretrieve(location, output_path)
                        return True
                elif status == 200:
                    print(f" -> Done! Saved to {output_path}")
                    with open(output_path, 'wb') as f:
                        f.write(response.read())
                    return True
                else:
                    time.sleep(retry_interval)
        except Exception as e:
            time.sleep(retry_interval)
    print(f" -> Failed to generate {output_path}")
    return False

tasks = {
    "SilverWing.png": "A tactical reconnaissance soldier with a high-tech bow and arrow, futuristic military gear, cyberpunk style, highly detailed",
    "Butterfly.png": "A female combat medic with a healing drone swarm, futuristic tactical gear, cyberpunk style, high quality",
    "Bit.png": "A tactical engineer deploying a robotic spider drone, cyberpunk military style, high tech",
    "Zoya.png": "A female support soldier with toxic smoke grenades and adrenaline syringes, cyberpunk tactical gear, high quality",
    "DeepBlue.png": "A heavy armored juggernaut soldier holding a massive tactical riot shield, cyberpunk military style, highly detailed",
    "Nameless.png": "A stealthy assassin soldier with dual tactical blades and stealth cloak, cyberpunk ninja style, highly detailed",
    "AsaraGuard.png": "A resilient desert mercenary soldier holding an assault rifle, tactical gear, cyberpunk style, highly detailed",
    "AfricanStar.png": "A tactical soldier looking extremely unlucky, opening an empty loot crate, funny cyberpunk style",
    "TearOfOcean.png": "A lucky soldier holding a glowing rare blue gem artifact, cyberpunk style, epic loot",
    "T6Juggernaut.png": "A soldier wearing ridiculously heavy level 6 armor and helmet, walking tank, cyberpunk military, highly detailed",
    "DamGuard.png": "A tactical soldier standing guard at a massive concrete dam, holding a shotgun, cyberpunk style",
    "LongbowSniper.png": "A sniper in a ghillie suit aiming a futuristic sniper rifle from a mountaintop, cyberpunk style",
    "SpaceRat.png": "A tactical soldier with an oversized backpack stuffed with loot hiding in a corner, funny cyberpunk style",
    "ToeClipper.png": "A tactical soldier aiming a shotgun low at the ground, aiming for feet, funny cyberpunk style",
    "OutlineMaster.png": "A tactical soldier shooting wildly but all bullets missing the target and hitting the wall around it, funny cyberpunk style",
    "MedicsDaddy.png": "A heavily wounded soldier crawling on the ground reaching out for a medic, funny cyberpunk style",
    "GrenadeGod.png": "A tactical soldier juggling multiple grenades and explosives, chaotic cyberpunk style",
    "TheRat.png": "A sneaky tactical soldier hiding in a bush or behind a door with a suppressed weapon, funny cyberpunk style"
}

os.makedirs("/workspace/image/delta_ops", exist_ok=True)
for filename, prompt in tasks.items():
    path = f"/workspace/image/delta_ops/{filename}"
    if not os.path.exists(path):
        fetch_image(prompt, path)
    else:
        print(f"Already exists: {path}")

print("All missing images have been processed.")
