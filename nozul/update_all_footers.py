import os

# Tüm 10 ürünün listesi (Footer ve navigasyon için)
all_products_list = [
    ("PVC Bantlı Konveyör", "pvc-bantli-konveyor.html"),
    ("Kauçuk Bantlı Konveyör", "kaucuk-bantli-konveyor.html"),
    ("Rulolu Konveyör", "rulolu-konveyor.html"),
    ("Zincirli Konveyör", "zincirli-konveyor.html"),
    ("Vidalı Konveyör (Helezon)", "vidali-konveyor.html"),
    ("Kovalı Elevatör", "elevator.html"),
    ("Hücre Tekeri", "hucre-tekeri.html"),
    ("Sürgü (Slide Gate)", "surgu.html"),
    ("Klape (Flap Valve)", "klape.html"),
    ("Kaynak Konumlandırma", "kaynak-konumlandirma.html")
]

def update_footer_in_file(fpath, is_subfolder=False):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Footer ürün listesi bölümünü hedefle
    prefix = "../urunler/" if not is_subfolder else ""
    
    new_footer_links = ""
    for name, link in all_products_list:
        new_footer_links += f'        <li><a href="{prefix}{link}" class="hover:text-primary transition-colors">{name}</a></li>\n'

    # Mevcut footer listesini bul ve değiştir
    pattern = r'<h3 class="text-sm font-semibold uppercase tracking-wider text-primary mb-4">Ürünler</h3>\s*<ul class="space-y-2 text-sm text-white">.*?</ul>'
    replacement = f'<h3 class="text-sm font-semibold uppercase tracking-wider text-primary mb-4">Ürünler</h3>\n      <ul class="space-y-2 text-sm text-white">\n{new_footer_links}      </ul>'
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

import re

# Ana dizindeki dosyalar
root_files = ["index.html", "urunler.html", "hakkimizda.html", "projeler.html", "referanslar.html", "iletisim.html", "teklif-al.html"]
for fname in root_files:
    fpath = os.path.join(r'C:\Users\Serdarowski\Desktop\verisyon 2', fname)
    if os.path.exists(fpath):
        update_footer_in_file(fpath, is_subfolder=False)
        print(f"Footer Updated: {fname}")

# urunler/ klasöründeki dosyalar
products_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler'
for fname in os.listdir(products_dir):
    if fname.endswith('.html'):
        fpath = os.path.join(products_dir, fname)
        update_footer_in_file(fpath, is_subfolder=True)
        print(f"Footer Updated (Sub): {fname}")
