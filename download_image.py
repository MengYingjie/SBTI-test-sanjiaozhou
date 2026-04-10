import urllib.request
import time
import sys
import json

def fetch_image(url, output_path):
    print(f"Starting fetch for {url}")
    max_retries = 30
    retry_interval = 2
    
    for i in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content_type = response.headers.get('Content-Type', '')
                
                # If it's returning JSON, it might be the "generating" status
                if 'application/json' in content_type:
                    data = json.loads(response.read().decode('utf-8'))
                    print(f"[{i+1}/{max_retries}] Status: {data}")
                    time.sleep(retry_interval)
                    continue
                    
                # If we get actual image content
                if 'image/' in content_type:
                    with open(output_path, 'wb') as f:
                        f.write(response.read())
                    print(f"Successfully saved image to {output_path}")
                    return True
                    
        except Exception as e:
            print(f"[{i+1}/{max_retries}] Error: {e}")
            time.sleep(retry_interval)
            
    print("Failed to download image after maximum retries.")
    return False

if __name__ == "__main__":
    prompt1 = "A%20glowing%20high-tech%20golden%20brick%20in%20a%20tactical%20briefcase%2C%20cyberpunk%20style"
    url1 = f"https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt={prompt1}&image_size=square"
    fetch_image(url1, "/workspace/image/delta_ops/MandelBrick.png")

    prompt2 = "A%20lone%20soldier%20with%20a%20combat%20knife%20running%20away%20with%20a%20backpack%20full%20of%20loot%2C%20cyberpunk%20style"
    url2 = f"https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt={prompt2}&image_size=square"
    fetch_image(url2, "/workspace/image/delta_ops/Runner.png")
