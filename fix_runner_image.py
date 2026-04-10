import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_images = """    const TYPE_IMAGES = {
      "红狼": "./image/delta_ops/Kai.png",
      "牧羊人": "./image/delta_ops/Terry.png",
      "露娜": "./image/delta_ops/Luna.png",
      "蜂医": "./image/delta_ops/Roy.png",
      "威龙": "./image/delta_ops/Vyron.png",
      "骇爪": "./image/delta_ops/Hackclaw.png",
      "乌鲁鲁": "./image/delta_ops/David.png",
      "曼德尔砖": "./image/delta_ops/MandelBrick.png",
      "摸金校尉": "./image/delta_ops/MandelBrick.png"
    };"""

new_images = """    const TYPE_IMAGES = {
      "红狼": "./image/delta_ops/Kai.png",
      "牧羊人": "./image/delta_ops/Terry.png",
      "露娜": "./image/delta_ops/Luna.png",
      "蜂医": "./image/delta_ops/Roy.png",
      "威龙": "./image/delta_ops/Vyron.png",
      "骇爪": "./image/delta_ops/Hackclaw.png",
      "乌鲁鲁": "./image/delta_ops/David.png",
      "曼德尔砖": "./image/delta_ops/MandelBrick.png",
      "摸金校尉": "./image/delta_ops/Runner.png"
    };"""

if old_images in content:
    content = content.replace(old_images, new_images)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed TYPE_IMAGES runner key in index.html")
else:
    print("Could not find the exact old_images block in index")

with open('generate_all_results.html', 'r', encoding='utf-8') as f:
    content_all = f.read()

old_images_all = """    const TYPE_IMAGES = {
      "Kai": "./image/delta_ops/Kai.png",
      "Terry": "./image/delta_ops/Terry.png",
      "Luna": "./image/delta_ops/Luna.png",
      "Roy": "./image/delta_ops/Roy.png",
      "Vyron": "./image/delta_ops/Vyron.png",
      "Hackclaw": "./image/delta_ops/Hackclaw.png",
      "David": "./image/delta_ops/David.png",
      "MandelBrick": "./image/delta_ops/MandelBrick.png",
      "Runner": "./image/delta_ops/MandelBrick.png"
    };"""

new_images_all = """    const TYPE_IMAGES = {
      "Kai": "./image/delta_ops/Kai.png",
      "Terry": "./image/delta_ops/Terry.png",
      "Luna": "./image/delta_ops/Luna.png",
      "Roy": "./image/delta_ops/Roy.png",
      "Vyron": "./image/delta_ops/Vyron.png",
      "Hackclaw": "./image/delta_ops/Hackclaw.png",
      "David": "./image/delta_ops/David.png",
      "MandelBrick": "./image/delta_ops/MandelBrick.png",
      "Runner": "./image/delta_ops/Runner.png"
    };"""

if old_images_all in content_all:
    content_all = content_all.replace(old_images_all, new_images_all)
    with open('generate_all_results.html', 'w', encoding='utf-8') as f:
        f.write(content_all)
    print("Fixed TYPE_IMAGES runner key in generate_all_results.html")

