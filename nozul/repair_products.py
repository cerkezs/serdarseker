import os
import re

root_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler'

def repair_page(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Hatalı ana görsel divini düzelt
    content = re.sub(r'<div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100">\s*relative z-10">', 
                     r'<div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100 relative z-10">', content)

    # 2. Footer ve yanlış yerlerdeki card-sweep yapılarını temizle
    # Yanlışlıkla eklenen card-sweep divlerini kaldır
    content = content.replace('<div class="card-sweep rounded-2xl group max-w-[450px] mx-auto w-full">\n        <a href="https://api.whatsapp.com', '<a href="https://api.whatsapp.com')
    content = content.replace('<div class="card-sweep rounded-2xl group max-w-[450px] mx-auto w-full">\n        <a href="https://www.instagram.com', '<a href="https://www.instagram.com')
    content = content.replace('<div class="card-sweep rounded-2xl group max-w-[450px] mx-auto w-full">\n        <a href="https://www.youtube.com/@nozulmakina', '<a href="https://www.youtube.com/@nozulmakina')
    
    # Fazladan kapanan divleri temizle (Sadece footer sosyal medya kısmındakiler)
    # Bu kısım manuel düzeltme gerektirebilir ama genel bir temizlik yapalım
    content = content.replace('</a>\n        </div>\n    </div>\n    <div>', '</a>\n    </div>\n    <div>')
    content = content.replace('</a>\n        </div>\n    </div>\n  </div>\n</footer>', '</a>\n      </div>\n    </div>\n  </div>\n</footer>')

    # Diğer ürünler kısmındaki div dengesini sağla
    # Her </a> sonrasındaki </div>'i sadece "Diğer Ürünlerimiz" section'ında kontrol etmeliyiz.
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

# Önce genel bir temizlik yapalım
for fname in os.listdir(root_dir):
    if fname.endswith('.html'):
        repair_page(os.path.join(root_dir, fname))
        print(f"Repaired: {fname}")
