import os
import re

def process_sektor_html():
    sektor_dir = 'sektor'
    count = 0
    for file in os.listdir(sektor_dir):
        if not file.endswith('.html'):
            continue
            
        filepath = os.path.join(sektor_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        def replace_card(match):
            href = match.group(1)
            inner_content = match.group(2)
            
            # New <a> tag
            new_a = f'<a href="{href}" class="group max-w-[450px] mx-auto w-full rounded-2xl shadow-soft hover:shadow-elegant transition card-sweep">'
            
            # New inner wrapper
            new_inner = f'\n        <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">\n{inner_content}\n        </div>\n      </a>'
            
            return new_a + new_inner

        # Regex to match the whole card block for sektor htmls
        pattern = r'<a href="(\.\./urunler/[^"]+)" class="group max-w-\[450px\] mx-auto w-full bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant transition">(.*?)</a>'
        
        new_content, num_subs = re.subn(pattern, replace_card, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += num_subs
            
    print(f"Updated {count} cards in sektor directory.")

if __name__ == '__main__':
    process_sektor_html()
