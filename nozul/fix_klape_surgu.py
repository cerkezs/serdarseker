import os
import re

# Ürünlerin datası
products_master = {
    "klape.html": {
        "TITLE": "Klape (Flap Valve)",
        "IMG": "admin-ajax-1-Photoroom.png",
        "DESC": "Yön değiştirme ve akış yönlendirme valfi.",
        "SPECS": ["Pnömatik veya manuel", "Aşınmaya dayanıklı dil", "Sızdırmaz conta yapısı", "Hızlı geçiş özelliği"],
        "AREAS": ["Hat ayırıcılar", "Silo çıkışları", "Dökme malzeme hatları", "Pnömatik sistemler"]
    },
    "surgu.html": {
        "TITLE": "Sürgü (Slide Gate)",
        "IMG": "WhatsApp-Image-2022-01-04-at-17.50.02-3_500x540.jpg",
        "DESC": "Silo ve hat çıkışlarında hassas akış kontrolü sağlar.",
        "SPECS": ["Sızdırmaz conta sistemi", "Paslanmaz bıçak opsiyonu", "Pnömatik / Manuel sürüş", "Kolay temizlenebilir"],
        "AREAS": ["Silo boşaltma", "Tartım bunkeri", "Helezon besleme", "Konveyör ara çıkışlar"]
    }
}

# Öneri kombinasyonları
combinations = {
    "klape.html": ["surgu.html", "hucre-tekeri.html", "elevator.html"],
    "surgu.html": ["hucre-tekeri.html", "klape.html", "vidali-konveyor.html"]
}

def fix_specific_pages(fname):
    fpath = os.path.join(r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler', fname)
    
    # Bu sayfaları baştan tertemiz inşa edelim (En güvenli yol)
    data = products_master[fname]
    other_fnames = combinations[fname]
    
    cards_html = ""
    # Master listeyi burada da kullanabilmek için (kısa bir kopya)
    full_master = {
        "surgu.html": ["Sürgü (Slide Gate)", "WhatsApp-Image-2022-01-04-at-17.50.02-3_500x540.jpg", "Silo ve hat çıkışlarında akış kontrolü."],
        "hucre-tekeri.html": ["Hücre Tekeri (Rotary Valve)", "IMG_2192_1000x1000.jpg", "Basınçlı sistemlerde hassas malzeme besleme."],
        "elevator.html": ["Kovalı Elevatör", "NM-ELEVATOR-001_600x600_500x540.jpg", "Düşey yönde dökme malzeme taşıma sistemi."],
        "klape.html": ["Klape (Flap Valve)", "admin-ajax-1-Photoroom.png", "Yön değiştirme ve akış yönlendirme valfi."],
        "vidali-konveyor.html": ["Vidalı Konveyör (Helezon)", "AS-1.jpg", "Toz, granül ve dökme malzeme için kapalı taşıma."]
    }

    for o_fname in other_fnames:
        o_title, o_img, o_desc = full_master[o_fname]
        cards_html += f'''
        <div class="card-sweep rounded-2xl group">
          <a href="{o_fname}" class="block bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant transition relative z-10 h-full">
            <div class="aspect-[4/3] overflow-hidden bg-gray-100"><img src="../assets/images/{o_img}" alt="{o_title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/></div>
            <div class="p-5">
              <h3 class="font-display font-semibold group-hover:text-primary transition">{o_title}</h3>
              <p class="mt-2 text-xs text-gray-500 leading-relaxed line-clamp-2">{o_desc}</p>
              <div class="mt-4 flex items-center text-xs font-bold text-primary">Detaylar →</div>
            </div>
          </a>
        </div>'''

    # index.html'den footer'ı al (zaten sync etmiştik ama burada da sağlam olsun)
    with open(r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler\vidali-konveyor.html', 'r', encoding='utf-8') as f:
        v_content = f.read()
    footer_text = re.search(r'<footer.*?</footer>', v_content, flags=re.DOTALL).group(0)
    header_text = re.search(r'<!DOCTYPE html>.*?<main>', v_content, flags=re.DOTALL).group(0).replace('Vidalı Konveyör (Helezon)', data["TITLE"])

    html = f'''{header_text}
<section class="py-12">
  <div class="max-w-[1400px] mx-auto px-4 lg:px-8 grid lg:grid-cols-2 gap-10">
    <div class="card-sweep rounded-2xl group">
      <div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100 relative z-10">
        <img src="../assets/images/{data["IMG"]}" alt="{data["TITLE"]}" class="w-full h-auto group-hover:scale-105 transition duration-500"/>
      </div>
    </div>
    <div>
      <span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>
      <h1 class="font-display text-3xl md:text-4xl font-bold mt-2">{data["TITLE"]}</h1>
      <p class="mt-4 text-gray-600 leading-relaxed">{data["DESC"]}</p>
      <div class="mt-8 grid sm:grid-cols-2 gap-6">
        <div><h2 class="font-display font-semibold mb-3">Özellikler</h2><ul class="space-y-2 text-sm text-gray-700">{"".join([f'<li class="flex gap-2"><span class="text-primary mt-0.5">✓</span>{s}</li>' for s in data["SPECS"]])}</ul></div>
        <div><h2 class="font-display font-semibold mb-3">Uygulama Alanları</h2><ul class="space-y-2 text-sm text-gray-700">{"".join([f'<li class="flex gap-2"><span class="text-primary mt-0.5">→</span>{a}</li>' for a in data["AREAS"]])}</ul></div>
      </div>
      <div class="mt-8 flex flex-wrap gap-3">
        <a href="../teklif-al.html" class="bg-gradient-primary text-white px-6 py-3 rounded-md font-semibold shadow-soft hover:shadow-elegant transition flex items-center gap-2">Bu ürün için teklif al</a>
        <a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" rel="noreferrer" class="border border-gray-200 px-6 py-3 rounded-md font-semibold hover:border-primary hover:text-primary transition flex items-center gap-2">WhatsApp ile sor</a>
      </div>
    </div>
  </div>
</section>

<section class="py-16 bg-surface">
  <div class="max-w-[1400px] mx-auto px-4 lg:px-8">
    <h2 class="font-display text-2xl font-bold mb-8">Sizin İçin Önerilen Ürünler</h2>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {cards_html}
    </div>
  </div>
</section>
</main>
{footer_text}
<script src="../assets/js/main.js"></script>
</body>
</html>'''
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

# Klape ve Sürgü'yü düzelt
fix_specific_pages("klape.html")
fix_specific_pages("surgu.html")

# Tüm sayfalardaki çift sembolleri temizle
products_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler'
for fname in os.listdir(products_dir):
    if fname.endswith('.html'):
        fpath = os.path.join(products_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('✓✓', '✓').replace('→→', '→')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)

print("Klape and Surgu fixed. Double symbols cleaned everywhere.")
