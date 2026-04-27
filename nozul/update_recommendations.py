import os
import re

# Ürünlerin tüm datası (Dosya adı: [Başlık, Görsel, Kısa Açıklama])
products_master = {
    "pvc-bantli-konveyor.html": ["PVC Bantlı Konveyör", "IMG_1554_500x540.jpg", "Hafif ve orta yüklü ürünler için ideal taşıma çözümü."],
    "kaucuk-bantli-konveyor.html": ["Kauçuk Bantlı Konveyör", "WhatsApp-Image-2024-07-20-at-09.14.02.jpeg", "Ağır ve aşındırıcı malzemeler için dayanıklı çözüm."],
    "rulolu-konveyor.html": ["Rulolu Konveyör", "OTOMATIK-AGIR-RULOLU-KONVEYOR-SISTEMI-1-2048x1152-1-min-png.webp", "Kutu, palet ve düzgün tabanlı ürünler için verimli sistem."],
    "zincirli-konveyor.html": ["Zincirli Konveyör", "WhatsApp-Image-2024-01-16-at-10.40.52-scaled.jpeg", "Yüksek tonajlı ve sıcak malzeme taşıma çözümü."],
    "vidali-konveyor.html": ["Vidalı Konveyör (Helezon)", "AS-1.jpg", "Toz, granül ve dökme malzeme için kapalı taşıma."],
    "elevator.html": ["Kovalı Elevatör", "NM-ELEVATOR-001_600x600_500x540.jpg", "Düşey yönde dökme malzeme taşıma sistemi."],
    "hucre-tekeri.html": ["Hücre Tekeri (Rotary Valve)", "IMG_2192_1000x1000.jpg", "Basınçlı sistemlerde hassas malzeme besleme."],
    "surgu.html": ["Sürgü (Slide Gate)", "WhatsApp-Image-2022-01-04-at-17.50.02-3_500x540.jpg", "Silo ve hat çıkışlarında akış kontrolü."],
    "klape.html": ["Klape (Flap Valve)", "admin-ajax-1-Photoroom.png", "Yön değiştirme ve akış yönlendirme valfi."],
    "kaynak-konumlandirma.html": ["Kaynak Konumlandırma", "WhatsApp-Image-2024-12-11-at-10.25.50-3-Photoroom_540x500.jpg", "Otomatik kaynak hatları için pozisyoner sistemler."]
}

# Her sayfa için BENZERSİZ 3'lü kombinasyonlar (Kendisi hariç)
combinations = {
    "pvc-bantli-konveyor.html": ["kaucuk-bantli-konveyor.html", "rulolu-konveyor.html", "zincirli-konveyor.html"],
    "kaucuk-bantli-konveyor.html": ["pvc-bantli-konveyor.html", "zincirli-konveyor.html", "vidali-konveyor.html"],
    "rulolu-konveyor.html": ["pvc-bantli-konveyor.html", "zincirli-konveyor.html", "kaynak-konumlandirma.html"],
    "zincirli-konveyor.html": ["kaucuk-bantli-konveyor.html", "rulolu-konveyor.html", "vidali-konveyor.html"],
    "vidali-konveyor.html": ["elevator.html", "hucre-tekeri.html", "surgu.html"],
    "elevator.html": ["vidali-konveyor.html", "hucre-tekeri.html", "klape.html"],
    "hucre-tekeri.html": ["vidali-konveyor.html", "surgu.html", "klape.html"],
    "surgu.html": ["hucre-tekeri.html", "klape.html", "vidali-konveyor.html"],
    "klape.html": ["surgu.html", "hucre-tekeri.html", "elevator.html"],
    "kaynak-konumlandirma.html": ["rulolu-konveyor.html", "zincirli-konveyor.html", "pvc-bantli-konveyor.html"]
}

def update_product_page(fname):
    fpath = os.path.join(r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler', fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Header'daki çift çizgi hatasını düzelt (underline sınıfını kaldır, CSS halleder)
    content = content.replace('text-primary underline decoration-2 underline-offset-8 nav-link', 'text-primary nav-link')

    # 2. Önerilen Ürünler Bölümünü (Diğer Ürünlerimiz) Yeniden İnşa Et
    other_products_fnames = combinations[fname]
    
    cards_html = ""
    for other_fname in other_products_fnames:
        title, img, desc = products_master[other_fname]
        cards_html += f'''
        <div class="card-sweep rounded-2xl group">
          <a href="{other_fname}" class="block bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant transition relative z-10 h-full">
            <div class="aspect-[4/3] overflow-hidden bg-gray-100">
              <img src="../assets/images/{img}" alt="{title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/>
            </div>
            <div class="p-5">
              <h3 class="font-display font-semibold group-hover:text-primary transition">{title}</h3>
              <p class="mt-2 text-xs text-gray-500 leading-relaxed line-clamp-2">{desc}</p>
              <div class="mt-4 flex items-center text-xs font-bold text-primary">Detaylar →</div>
            </div>
          </a>
        </div>'''

    new_section = f'''<section class="py-16 bg-surface">
  <div class="max-w-[1400px] mx-auto px-4 lg:px-8">
    <h2 class="font-display text-2xl font-bold mb-8">Sizin İçin Önerilen Ürünler</h2>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {cards_html}
    </div>
  </div>
</section>'''

    # Mevcut section'ı bul ve değiştir
    content = re.sub(r'<section class="py-16 bg-surface">.*?</section>', new_section, content, flags=re.DOTALL)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

for fname in combinations.keys():
    update_product_page(fname)
    print(f"Product Page Updated with Unique Recommendations: {fname}")
