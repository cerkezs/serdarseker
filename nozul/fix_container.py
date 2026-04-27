import os

for root, dirs, files in os.walk('.'):
    if 'assets' in root or '.git' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Change all max-w-[1650px] to max-w-7xl (1280px)
            new_content = content.replace('max-w-[1650px]', 'max-w-7xl')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated container width in {filepath}")
