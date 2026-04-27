import os
import re

root_dir = r'c:\Users\Serdarowski\Desktop\verisyon 2'

def refine_hero_wrapping(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    c = f.read()
                
                # whitespace-nowrap'i kaldır ama max-w'ları da kapalı tut (veya çok genişlet)
                # Başlıklar
                c = c.replace('whitespace-nowrap">Mühendislik Deneyimi ve Yenilikçi Çözümler</h1>', 
                              'max-w-none">Mühendislik Deneyimi ve Yenilikçi Çözümler</h1>')
                c = c.replace('whitespace-nowrap">Gıda Sektörü için Konveyör Sistemleri</h1>', 
                              'max-w-none">Gıda Sektörü için Konveyör Sistemleri</h1>')
                
                # Sektör Sayfaları İçin Genel Regex (Başlık)
                c = re.sub(r'<h1 class="font-display text-4xl md:text-5xl font-bold mt-2 whitespace-nowrap">(.*?)</h1>', 
                           r'<h1 class="font-display text-4xl md:text-5xl font-bold mt-2 max-w-none">\1</h1>', c)
                
                # Alt Metinler (Tüm Sayfalar)
                c = re.sub(r'whitespace-nowrap">(.*?)</p>', 
                           r'max-w-none">\1</p>', c)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(c)
                print(f"Refined hero wrapping in: {file}")

refine_hero_wrapping(root_dir)
