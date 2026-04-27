import os
import re

# Orijinal 6 ürünlük liste
original_6_products = [
    ("PVC Bantlı Konveyör", "pvc-bantli-konveyor.html"),
    ("Kauçuk Bantlı Konveyör", "kaucuk-bantli-konveyor.html"),
    ("Rulolu Konveyör", "rulolu-konveyor.html"),
    ("Zincirli Konveyör", "zincirli-konveyor.html"),
    ("Vidalı Konveyör (Helezon)", "vidali-konveyor.html"),
    ("Kovalı Elevatör", "elevator.html")
]

def revert_footer(fpath, is_subfolder=False):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    prefix = "../urunler/" if not is_subfolder else ""
    
    new_footer_links = ""
    for name, link in original_6_products:
        new_footer_links += f'        <li><a href="{prefix}{link}" class="hover:text-primary transition-colors">{name}</a></li>\n'

    pattern = r'<h3 class="text-sm font-semibold uppercase tracking-wider text-primary mb-4">Ürünler</h3>\s*<ul class="space-y-2 text-sm text-white">.*?</ul>'
    replacement = f'<h3 class="text-sm font-semibold uppercase tracking-wider text-primary mb-4">Ürünler</h3>\n      <ul class="space-y-2 text-sm text-white">\n{new_footer_links}      </ul>'
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

# Ana dizindeki dosyalar
root_files = ["index.html", "urunler.html", "hakkimizda.html", "projeler.html", "referanslar.html", "iletisim.html", "teklif-al.html"]
for fname in root_files:
    fpath = os.path.join(r'C:\Users\Serdarowski\Desktop\verisyon 2', fname)
    if os.path.exists(fpath):
        revert_footer(fpath, is_subfolder=False)
        print(f"Footer Reverted: {fname}")

# urunler/ klasöründeki dosyalar
products_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler'
for fname in os.listdir(products_dir):
    if fname.endswith('.html'):
        fpath = os.path.join(products_dir, fname)
        revert_footer(fpath, is_subfolder=True)
        print(f"Footer Reverted (Sub): {fname}")
