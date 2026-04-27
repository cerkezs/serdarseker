import os

for root, dirs, files in os.walk('.'):
    if 'assets' in root or '.git' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. Revert container sizes back to 1650px
            content = content.replace('max-w-7xl', 'max-w-[1650px]')
            
            # 2. Add max-w-[450px] mx-auto w-full to the product cards
            # We find the exact class prefix of the cards
            old_card_class = 'class="group bg-white border border-gray-100 rounded-2xl overflow-hidden'
            new_card_class = 'class="group max-w-[450px] mx-auto w-full bg-white border border-gray-100 rounded-2xl overflow-hidden'
            
            content = content.replace(old_card_class, new_card_class)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"Processed {filepath}")
