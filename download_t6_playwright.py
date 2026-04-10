import asyncio
from playwright.async_api import async_playwright

async def download_image():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate to the Baidu image search page provided by the user
        url = "https://image.baidu.com/search/detail?adpicid=0&b_applid=10789415293926948748&bdtype=0&commodity=&copyright=&cs=3087122125%2C3389458262&di=7620110360720179201&fr=click-pic&fromurl=http%253A%252F%252Fwww.douyin.com%252Fnote%252F7504118076172061964&gsm=1e&hd=&height=0&hot=&ic=&ie=utf-8&imgformat=&imgratio=&imgspn=0&is=0%2C0&isImgSet=&latest=&lid=&lm=&objurl=https%253A%252F%252Fp3-pc-sign.douyinpic.com%252Ftos-cn-i-0813%252FocaH2fKYgIIADAC5eIjFWBcEQbDAF5AOeAf25k~tplv-dy-aweme-images%253Aq75.webp&os=2996707877%2C2331102216&pd=image_content&pi=0&pn=3&rn=1&simid=3087122125%2C3389458262&tn=baiduimagedetail&width=0&word=%E5%85%AD%E5%A5%97%E6%88%98%E7%A5%9E&z="
        
        # We can intercept the image response
        image_data = None
        
        async def handle_response(response):
            nonlocal image_data
            if "p3-pc-sign.douyinpic.com" in response.url or "hdslb.com" in response.url or response.request.resource_type == "image":
                if response.status == 200 and int(response.headers.get("content-length", 0)) > 5000:
                    try:
                        buffer = await response.body()
                        if len(buffer) > 10000: # Ensure it's the main image
                            image_data = buffer
                    except:
                        pass

        page.on("response", handle_response)
        
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(5000) # Wait a bit for images to load
        
        # If interception failed, let's try to find the main image element and get its src, then fetch it via page.evaluate
        if not image_data:
            img_element = await page.query_selector("img.currentImg")
            if img_element:
                img_src = await img_element.get_attribute("src")
                print(f"Found image src: {img_src}")
                # Fetch it from within the page context
                base64_data = await page.evaluate('''async (url) => {
                    const response = await fetch(url);
                    const blob = await response.blob();
                    return new Promise((resolve, reject) => {
                        const reader = new FileReader();
                        reader.onloadend = () => resolve(reader.result);
                        reader.onerror = reject;
                        reader.readAsDataURL(blob);
                    });
                }''', img_src)
                
                import base64
                if base64_data.startswith('data:'):
                    base64_data = base64_data.split(',')[1]
                image_data = base64.b64decode(base64_data)
        
        if image_data:
            with open("/workspace/image/delta_ops/T6Juggernaut.jpg", "wb") as f:
                f.write(image_data)
            print("Successfully saved image via Playwright.")
        else:
            print("Failed to capture image.")
            
        await browser.close()

asyncio.run(download_image())
