import os

for root, dirs, files in os.walk('.'):
    if 'assets' in root or '.git' in root or '.gemini' in root or 'components' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content.replace('aspect-video', 'aspect-[4/3]')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
