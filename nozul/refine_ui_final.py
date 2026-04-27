import os
import re

product_files = [
    "pvc-bantli-konveyor.html", "kaucuk-bantli-konveyor.html", "rulolu-konveyor.html",
    "zincirli-konveyor.html", "vidali-konveyor.html", "elevator.html",
    "hucre-tekeri.html", "surgu.html", "klape.html", "kaynak-konumlandirma.html"
]

fa_cdn = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />'

wp_button_html = '''
<!-- WhatsApp Floating Button -->
<a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" class="fixed bottom-6 right-6 z-[9999] bg-white text-white w-16 h-16 rounded-full shadow-2xl hover:scale-110 transition-transform flex items-center justify-center border-2 border-gray-100" aria-label="WhatsApp ile İletişime Geçin">
  <i class="fa-brands fa-whatsapp fa-beat-fade" style="color: rgb(52, 224, 13); font-size: 35px;"></i>
</a>
'''

def fix_page(fname):
    fpath = os.path.join(r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler', fname)
    if not os.path.exists(fpath): return
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. FontAwesome Ekle
    if 'font-awesome' not in content:
        content = content.replace('</head>', fa_cdn + '\n</head>')

    # 2. Sweep Efektini Düzelt (Siyah taşmayı engelle ve z-index ayarla)
    # card-sweep efektini tekrar aktifleştiriyoruz ama daha temiz bir div yapısıyla
    # Ayrıca sağ sütunu resmin altıyla hizalamak için self-end ekliyoruz
    
    content = re.sub(r'<div class="relative group">\s*<div class="overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-elegant relative z-10">',
                     r'<div class="card-sweep rounded-2xl group">\n      <div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100 relative z-10">', content)

    # Sağ sütunu alt hizaya çekmek için div class'ını güncelle
    # Eski: <div> ... <span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>
    # Yeni: <div class="self-end">
    content = re.sub(r'</div>\s*<div>\s*<span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>',
                     r'</div>\n    <div class="self-end">\n      <span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>', content)

    # 3. WhatsApp Butonunu Güncelle (Yeni ikonla)
    # Eski butonu temizle
    content = re.sub(r'<!-- WhatsApp Floating Button -->.*?</a>', '', content, flags=re.DOTALL)
    # Yeni butonu ekle
    content = content.replace('</body>', wp_button_html + '\n</body>')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in product_files:
    fix_page(f)
    print(f"Sweep Fixed, WP Updated & Aligned: {f}")
