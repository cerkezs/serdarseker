import os
import re

sektor_dir = r'c:\Users\Serdarowski\Desktop\verisyon 2\sektor'

def fix_sektor_hero(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    c = f.read()
                
                # Başlık düzeltme
                c = re.sub(r'<h1 class="font-display text-4xl md:text-5xl font-bold mt-2 max-w-3xl">(.*?)</h1>', 
                           r'<h1 class="font-display text-4xl md:text-5xl font-bold mt-2 whitespace-nowrap">\1</h1>', c)
                
                # Alt metin düzeltme
                c = re.sub(r'<p class="mt-4 max-w-2xl text-gray-300 leading-relaxed">(.*?)</p>', 
                           r'<p class="mt-4 text-gray-300 leading-relaxed whitespace-nowrap">\1</p>', c)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(c)
                print(f"Fixed hero text wrapping in: {file}")

fix_sektor_hero(sektor_dir)
