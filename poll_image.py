import urllib.request
import time
import sys

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
            
    print("Failed to download image after maximum retries.")
    return False

prompt1 = "A%20glowing%20high-tech%20golden%20brick%20in%20a%20tactical%20briefcase%2C%20cyberpunk%20style"
url1 = f"https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt={prompt1}&image_size=square"
fetch_image(url1, "/workspace/image/delta_ops/MandelBrick.png")

prompt2 = "A%20lone%20soldier%20with%20a%20combat%20knife%20running%20away%20with%20a%20backpack%20full%20of%20loot%2C%20cyberpunk%20style"
url2 = f"https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt={prompt2}&image_size=square"
fetch_image(url2, "/workspace/image/delta_ops/Runner.png")
