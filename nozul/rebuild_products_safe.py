import os
import re

# Ürün bilgileri sözlüğü (Dosya adı: [Başlık, Görsel, Açıklama, Özellikler, Alanlar])
products_data = {
    "elevator.html": ["Kovalı Elevatör", "NM-ELEVATOR-001_600x600_500x540.jpg", "Düşey yönde dökme malzeme taşıma sistemi.", ["✓ Yüksek irtifa kapasitesi", "✓ Toz sızdırmaz tasarım"], ["→ Hububat", "→ Madencilik"]],
    "hucre-tekeri.html": ["Hücre Tekeri (Rotary Valve)", "IMG_2192_1000x1000.jpg", "Basınçlı sistemlerde hassas malzeme besleme.", ["✓ Hassas dozajlama", "✓ Hava kilidi özelliği"], ["→ Pnömatik taşıma", "→ Filtre altları"]],
    "kaucuk-bantli-konveyor.html": ["Kauçuk Bantlı Konveyör", "WhatsApp-Image-2024-07-20-at-09.14.02.jpeg", "Ağır ve aşındırıcı malzemeler için dayanıklı çözüm.", ["✓ Yüksek aşınma direnci", "✓ Darbe sönümleyici rulolar"], ["→ Maden ocakları", "→ Taş kırma tesisleri"]],
    "klape.html": ["Klape (Flap Valve)", "admin-ajax-1-Photoroom.png", "Yön değiştirme ve akış yönlendirme valfi.", ["✓ Pnömatik veya manuel", "✓ Aşınmaya dayanıklı dil"], ["→ Hat ayırıcılar", "→ Silo çıkışları"]],
    "rulolu-konveyor.html": ["Rulolu Konveyör", "OTOMATIK-AGIR-RULOLU-KONVEYOR-SISTEMI-1-2048x1152-1-min-png.webp", "Kutu, palet ve düzgün tabanlı ürünler için.", ["✓ Tahrikli veya serbest", "✓ Modüler yapı"], ["→ Lojistik", "→ Otomotiv montaj"]],
    "surgu.html": ["Sürgü (Slide Gate)", "WhatsApp-Image-2022-01-04-at-17.50.02-3_500x540.jpg", "Silo ve hat çıkışlarında akış kontrolü.", ["✓ Sızdırmaz conta sistemi", "✓ Hassas akış ayarı"], ["→ Silo boşaltma", "→ Tartım bunkeri"]],
    "vidali-konveyor.html": ["Vidalı Konveyör (Helezon)", "AS-1.jpg", "Toz, granül ve dökme malzeme için kapalı taşıma.", ["✓ Tozsuz çalışma", "✓ Paslanmaz seçenekler"], ["→ Çimento", "→ Gıda & Un"]],
    "zincirli-konveyor.html": ["Zincirli Konveyör", "WhatsApp-Image-2024-01-16-at-10.40.52-scaled.jpeg", "Yüksek tonajlı ve sıcak malzeme taşıma çözümü.", ["✓ Ağır hizmet tipi zincir", "✓ Kapalı veya açık gövde"], ["→ Geri dönüşüm", "→ Enerji santralleri"]]
}

def generate_clean_page(fname, data):
    title, img, desc, specs, areas = data
    
    # Video butonu sadece PVC ve Kaynak Konumlandırma'da olacak (PVC'yi zaten manuel yaptım, buraya eklemiyorum)
    video_btn = ""
    if fname == "kaynak-konumlandirma.html":
        video_btn = '<a href="https://www.youtube.com/watch?v=2WjBn2GX8aM&t=5s" target="_blank" rel="noreferrer" class="bg-red-600 text-white px-6 py-3 rounded-md font-semibold shadow-soft hover:bg-red-700 transition flex items-center gap-2 group"><svg class="w-5 h-5 transition-transform group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>Videoyu İzle</a>'

    html_content = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title} — Nozul Makina</title>
<link rel="stylesheet" href="../assets/css/style.css" />
<script src="https://cdn.tailwindcss.com?plugins=typography,forms,aspect-ratio"></script>
<script src="../assets/js/tailwind-config.js"></script>
<link rel="icon" href="../favikon2.png" type="image/png" />
</head>
<body class="bg-white text-ink">
<header class="sticky top-0 z-50 bg-white/85 backdrop-blur-lg border-b border-gray-100">
  <div class="max-w-[1650px] mx-auto px-4 lg:px-8 h-20 flex items-center justify-between">
    <a href="../index.html"><img src="../nozulmakyenilogo.png" alt="Logo" class="h-12 w-auto object-contain"></a>
    <nav class="hidden lg:flex items-center gap-2">
      <a href="../index.html" class="px-4 py-2.5 rounded-md text-base font-semibold text-gray-700 hover:text-primary">Anasayfa</a>
      <a href="../hakkimizda.html" class="px-4 py-2.5 rounded-md text-base font-semibold text-gray-700 hover:text-primary">Hakkımızda</a>
      <a href="../urunler.html" class="px-4 py-2.5 rounded-md text-base font-semibold text-primary underline decoration-2 underline-offset-8">Ürünler</a>
      <a href="../projeler.html" class="px-4 py-2.5 rounded-md text-base font-semibold text-gray-700 hover:text-primary">Projeler</a>
      <a href="../iletisim.html" class="px-4 py-2.5 rounded-md text-base font-semibold text-gray-700 hover:text-primary">İletişim</a>
    </nav>
    <a href="tel:905333305285" class="bg-gray-50 px-4 py-2 rounded-lg font-bold text-gray-700 border border-gray-100">+90 533 330 52 85</a>
  </div>
</header>
<main>
<section class="py-12">
  <div class="max-w-[1400px] mx-auto px-4 lg:px-8 grid lg:grid-cols-2 gap-10">
    <div class="card-sweep rounded-2xl group">
      <div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100 relative z-10">
        <img src="../assets/images/{img}" alt="{title}" class="w-full h-auto group-hover:scale-105 transition duration-500"/>
      </div>
    </div>
    <div>
      <span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>
      <h1 class="font-display text-3xl md:text-4xl font-bold mt-2">{title}</h1>
      <p class="mt-4 text-gray-600 leading-relaxed">{desc}</p>
      <div class="mt-8 grid sm:grid-cols-2 gap-6">
        <div><h2 class="font-display font-semibold mb-3">Özellikler</h2><ul class="space-y-2 text-sm text-gray-700">{"".join([f'<li class="flex gap-2"><span class="text-primary mt-0.5">✓</span>{s}</li>' for s in specs])}</ul></div>
        <div><h2 class="font-display font-semibold mb-3">Uygulama Alanları</h2><ul class="space-y-2 text-sm text-gray-700">{"".join([f'<li class="flex gap-2"><span class="text-primary mt-0.5">→</span>{a}</li>' for a in areas])}</ul></div>
      </div>
      <div class="mt-8 flex flex-wrap gap-3">
        {video_btn}
        <a href="../teklif-al.html" class="bg-gradient-primary text-white px-6 py-3 rounded-md font-semibold shadow-soft hover:shadow-elegant transition">Teklif Al</a>
        <a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" class="border border-gray-200 px-6 py-3 rounded-md font-semibold hover:border-primary hover:text-primary transition">WhatsApp</a>
      </div>
    </div>
  </div>
</section>
</main>
<footer class="bg-ink text-white py-12">
  <div class="max-w-[1400px] mx-auto px-4 text-center">
    <img src="../nozulfooterlogo.png" alt="Logo" class="h-10 mx-auto mb-6 object-contain">
    <p class="text-sm text-white/70">© Nozul Makina. Tüm hakları saklıdır.</p>
  </div>
</footer>
<script src="../assets/js/main.js"></script>
</body>
</html>'''
    return html_content

root_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler'
for fname, data in products_data.items():
    fpath = os.path.join(root_dir, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(generate_clean_page(fname, data))
    print(f"Cleanly Rebuilt: {fname}")
