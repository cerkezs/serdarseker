import os
import re

path = r'c:\Users\Serdarowski\Desktop\verisyon 2\urunler\elevator.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Galeri HTML'i (7 Resim x 2 = 14 Slayt)
elevator_imgs = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg"]
repeated_imgs = elevator_imgs * 2

new_slides_html = ""
for img in repeated_imgs:
    new_slides_html += f'      <div class="swiper-slide"><img src="../assets/images/kovalielevatör/{img}" alt="Elevatör" onclick="openLightbox(this.src)"></div>\n'

# Mevcut swiper-wrapper içeriğini 14 slaytla değiştir
c = re.sub(r'<div class="swiper-wrapper">.*?</div>\s*<div class="swiper-pagination">', 
           f'<div class="swiper-wrapper">\n{new_slides_html}    </div>\n    <div class="swiper-pagination">', 
           c, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Elevatör Page Slide Count Adjusted to 14.")
