import os
import re

def get_depth(filepath):
    parts = os.path.relpath(filepath, '.').split(os.sep)
    if len(parts) == 1:
        return ''
    return '../' * (len(parts) - 1)

def update_favicon(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    depth = get_depth(filepath)
    new_favicon_tag = f'<link rel="icon" href="{depth}favikon2.png" type="image/png" />'
    
    # 1. Eğer halihazırda rel="icon" varsa onu değiştir
    if re.search(r'<link[^>]*rel=["\']icon["\'][^>]*>', content, flags=re.IGNORECASE):
        new_content = re.sub(r'<link[^>]*rel=["\']icon["\'][^>]*>', new_favicon_tag, content, flags=re.IGNORECASE)
    else:
        # 2. Yoksa </head> etiketinden hemen önce ekle
        favicon_tag_with_newline = f'\n{new_favicon_tag}\n</head>'
        new_content = re.sub(r'</head>', favicon_tag_with_newline, content, flags=re.IGNORECASE)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    count = 0
    for root, dirs, files in os.walk('.'):
        if 'components' in root or '.git' in root or '.gemini' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if update_favicon(filepath):
                    print(f"Updated favicon in {filepath}")
                    count += 1
    
    print(f"Process complete. Updated favicon in {count} files.")
