import re
import time

timestamp = str(int(time.time()))

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all image paths in TYPE_IMAGES and append ?v=timestamp
    # Be careful not to keep appending ?v=...
    # First, strip existing ?v=...
    content = re.sub(r'(\.jpg|\.png)\?v=\d+', r'\1', content)
    
    # Now append new timestamp
    content = re.sub(r'(\.jpg|\.png)', rf'\1?v={timestamp}', content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('index.html')
update_file('generate_all_results.html')
print("Cache busted.")
