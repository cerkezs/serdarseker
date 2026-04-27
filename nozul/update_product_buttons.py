import os
import re

def update_product_buttons():
    # Ürünler klasöründeki tüm HTML dosyalarını tara
    urunler_path = './urunler'
    if not os.path.exists(urunler_path):
        print("Urunler klasoru bulunamadi.")
        return

    for root, dirs, files in os.walk(urunler_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Eski buton metni ve yönlendirmesi için regex veya replace
                # Genellikle şu formatta: <a href="..." ...>Bu ürün için teklif al ...</a>
                # Veya <button ...>Bu ürün için teklif al</button>
                
                # Hem linki hem metni tek seferde güncelliyoruz
                # 'Bu ürün için teklif al' veya 'Bu Ürün İçin Teklif Al' varyasyonlarını yakala
                pattern = r'(<a\s+[^>]*?href=")([^"]*)("[^>]*?>\s*)(Bu [üÜ]rün [iİ]çin [tT]eklif [aA]l)(\s*→?\s*</a>)'
                
                new_content = re.sub(pattern, r'\1../iletisim.html\3Bu Ürün İçin Teklif Al\5', content, flags=re.IGNORECASE)
                
                # Eğer buton <a> değilse (nadiren), metni de düzeltelim
                if new_content == content:
                     new_content = content.replace('Bu ürün için teklif al', 'Bu Ürün İçin Teklif Al')
                
                if new_content != content:
                    print(f"Güncelleniyor: {file_path}")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    update_product_buttons()
