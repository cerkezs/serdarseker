import os
import re

for root, dirs, files in os.walk('.'):
    if 'assets' in root or '.git' in root or '.gemini' in root or 'components' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace aspect-[4/3] with aspect-video (16:9 ratio)
            new_content = content.replace('aspect-[4/3]', 'aspect-video')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated aspect ratio in {filepath}")
