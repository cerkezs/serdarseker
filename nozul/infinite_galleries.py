import os
import re

# Sayfa yolları
root_dir = r'c:\Users\Serdarowski\Desktop\verisyon 2\urunler'

def make_infinite(fname, img_list):
    path = os.path.join(root_dir, fname)
    if not os.path.exists(path): return
    
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Mevcut swiper-wrapper içeriğini bul ve değiştir
    # Resim sayısına göre kaç kat çoğaltacağımıza karar verelim (En az 15 slayt idealdir)
    multiplier = 1
    if len(img_list) < 6: multiplier = 3
    elif len(img_list) < 10: multiplier = 2
    
    repeated_imgs = img_list * multiplier
    
    new_slides_html = ""
    for img in repeated_imgs:
        alt = fname.split('-')[0].capitalize()
        new_slides_html += f'      <div class="swiper-slide"><img src="../assets/images/{img}" alt="{alt}" onclick="openLightbox(this.src)"></div>\n'

    # Regex ile swiper-wrapper'ın içini değiştir
    c = re.sub(r'<div class="swiper-wrapper">.*?</div>\s*<div class="swiper-pagination">', 
               f'<div class="swiper-wrapper">\n{new_slides_html}    </div>\n    <div class="swiper-pagination">', 
               c, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

# Zincirli (5 resim -> 15 slayt)
zincirli_imgs = [
    "zincirlikonveyör/1.jpg", "zincirlikonveyör/2.jpg", "zincirlikonveyör/3.jpg", 
    "zincirlikonveyör/4.jpg", "zincirlikonveyör/5.jpeg"
]
make_infinite('zincirli-konveyor.html', zincirli_imgs)

# Rulolu (9 resim -> 18 slayt)
rulolu_imgs = [
    "rulolukonveyör/1.jpg", "rulolukonveyör/2.jpg", "rulolukonveyör/3.jpeg",
    "rulolukonveyör/4.jpg", "rulolukonveyör/5.jpg", "rulolukonveyör/6.jpg",
    "rulolukonveyör/7.jpg", "rulolukonveyör/8.jpeg", "rulolukonveyör/9.jpg"
]
make_infinite('rulolu-konveyor.html', rulolu_imgs)

print("Galleries updated to be truly infinite.")
