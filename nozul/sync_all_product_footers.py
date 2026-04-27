import os
import re

# index.html'den tam footer yapısını alalım
with open(r'C:\Users\Serdarowski\Desktop\verisyon 2\index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

footer_match = re.search(r'<footer.*?</footer>', index_content, flags=re.DOTALL)
if not footer_match:
    print("Error: Could not find footer in index.html")
    exit()

original_footer = footer_match.group(0)

# Alt klasör (urunler/) için linkleri ve resimleri güncelleyelim
def adjust_footer_for_subfolder(footer_text):
    # Resim yolları
    footer_text = footer_text.replace('src="nozulfooterlogo.png"', 'src="../nozulfooterlogo.png"')
    # Ana dizin linkleri
    footer_text = footer_text.replace('href="index.html"', 'href="../index.html"')
    footer_text = footer_text.replace('href="hakkimizda.html"', 'href="../hakkimizda.html"')
    footer_text = footer_text.replace('href="urunler.html"', 'href="../urunler.html"')
    footer_text = footer_text.replace('href="projeler.html"', 'href="../projeler.html"')
    footer_text = footer_text.replace('href="referanslar.html"', 'href="../referanslar.html"')
    footer_text = footer_text.replace('href="iletisim.html"', 'href="../iletisim.html"')
    footer_text = footer_text.replace('href="blog.html"', 'href="../blog.html"')
    # Ürün linkleri (urunler/ klasöründeki dosyalar için prefix'i kaldıralım)
    footer_text = footer_text.replace('href="urunler/', 'href="')
    return footer_text

adjusted_footer = adjust_footer_for_subfolder(original_footer)

# urunler/ klasöründeki TÜM dosyaları hedefle
products_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler'

for fname in os.listdir(products_dir):
    if fname.endswith('.html'):
        fpath = os.path.join(products_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Dosyadaki mevcut footer'ı bul ve değiştir
        new_content = re.sub(r'<footer.*?</footer>', adjusted_footer, content, flags=re.DOTALL)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Footer Synchronized: {fname}")
