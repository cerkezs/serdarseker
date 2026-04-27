import os

root_dir = r'c:\Users\Serdarowski\Desktop\verisyon 2'

# 1. urunler.html güncelleme
urunler_path = os.path.join(root_dir, 'urunler.html')
if os.path.exists(urunler_path):
    with open(urunler_path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('Klape (Flap Valve)', 'Klape')
    with open(urunler_path, 'w', encoding='utf-8') as f:
        f.write(c)

# 2. klape.html güncelleme
klape_path = os.path.join(root_dir, 'urunler', 'klape.html')
if os.path.exists(klape_path):
    with open(klape_path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('Klape (Flap Valve)', 'Klape')
    # Title kısmını da kontrol et
    c = c.replace('<title>Klape (Flap Valve)', '<title>Klape')
    with open(klape_path, 'w', encoding='utf-8') as f:
        f.write(c)

print("Klape (Flap Valve) updated to Klape in both files.")
