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

path = "/workspace/image/delta_ops/T6Juggernaut.jpg"
prompt = "A funny gaming meme showing a soldier wearing ridiculously heavy level 6 armor and helmet, looking like a walking tank, holding a golden gun, covered in money and expensive loot, cyberpunk military style, highly detailed, text 'T6 Juggernaut'"
fetch_image(prompt, path)
