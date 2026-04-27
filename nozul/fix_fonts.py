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
            
            # Use regex to find <p class="..."> and replace text-lg with text-base
            def replace_in_p(match):
                p_tag = match.group(0)
                # We only change text-lg to text-base in paragraphs, not in h1, h2, h3
                return p_tag.replace('text-lg', 'text-base')
                
            new_content = re.sub(r'<p\s+[^>]*class="[^"]*"[^>]*>', replace_in_p, content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated font size in {filepath}")
