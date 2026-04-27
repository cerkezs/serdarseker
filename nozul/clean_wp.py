import os
import re

root_dir = r'c:\Users\Serdarowski\Desktop\verisyon 2'

# Sadece istediğimiz yeni, hareketli WP butonu kodu
correct_wp_button = '''
<!-- WhatsApp Floating Button -->
<a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" class="fixed bottom-6 right-6 z-[9999] text-white w-16 h-16 transition-transform flex items-center justify-center" aria-label="WhatsApp ile İletişime Geçin">
  <i class="fa-brands fa-whatsapp fa-beat-fade" style="color: rgb(52, 224, 13); font-size: 50px; filter: drop-shadow(0 0 10px rgba(0,0,0,0.3));"></i>
</a>
'''

def clean_wp_icons(content):
    # Önce tüm olası yüzen wp butonlarını (eski/yeni) temizle
    # WhatsApp linklerini içeren yüzen yapıları hedefle
    # Farklı yazımları yakalamak için daha geniş bir regex
    content = re.sub(r'<!-- WhatsApp Floating Button -->.*?</a>', '', content, flags=re.DOTALL)
    content = re.sub(r'<a href="https://api.whatsapp.com/send/.*?</a>', '', content, flags=re.DOTALL)
    
    # Şimdi en alta doğru sadece 1 tane doğru olanı ekle (body kapatmadan önce)
    if '</body>' in content:
        content = content.replace('</body>', correct_wp_button + '\n</body>')
    
    return content

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            p = os.path.join(root, file)
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Eğer içinde whatsapp linki varsa temizlik yap
            if 'whatsapp' in content.lower():
                new_content = clean_wp_icons(content)
                if new_content != content:
                    with open(p, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Cleaned & Fixed WP in: {file}")
