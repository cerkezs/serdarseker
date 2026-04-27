import os

# Orijinal Header ve Footer bölümlerini tanımlayalım (index.html'den referansla)
# Not: Yolları ../ ile güncelleyeceğiz.

HEADER_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{TITLE} — Nozul Makina</title>
<link rel="stylesheet" href="../assets/css/style.css" />
<script src="https://cdn.tailwindcss.com?plugins=typography,forms,aspect-ratio"></script>
<script src="../assets/js/tailwind-config.js"></script>
<link rel="icon" href="../favikon2.png" type="image/png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" />
</head>
<body class="bg-white text-ink">
<header class="sticky top-0 z-50 bg-white/85 backdrop-blur-lg border-b border-gray-100">
  <div class="max-w-[1650px] mx-auto px-4 lg:px-8 h-20 flex items-center justify-between">
   <a href="../index.html" class="flex items-center">
    <img src="../nozulmakyenilogo.png" alt="Nozul Makina Logo" class="h-12 w-auto object-contain">
   </a>
    <nav class="hidden lg:flex items-center gap-2">
      <a href="../index.html" class="px-4 py-2.5 rounded-md text-base font-semibold transition text-gray-700 hover:text-primary hover:bg-gray-50 nav-link">Anasayfa</a>
      <a href="../hakkimizda.html" class="px-4 py-2.5 rounded-md text-base font-semibold transition text-gray-700 hover:text-primary hover:bg-gray-50 nav-link">Hakkımızda</a>
      <a href="../urunler.html" class="px-4 py-2.5 rounded-md text-base font-semibold transition text-primary underline decoration-2 underline-offset-8 nav-link">Ürünler</a>
      <div class="relative group">
        <button class="px-4 py-2.5 rounded-md text-base font-semibold transition text-gray-700 hover:text-primary hover:bg-gray-50 flex items-center gap-1 nav-link">
          Sektörler
          <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        </button>
        <div class="absolute top-full left-0 pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
          <div class="bg-white rounded-2xl shadow-elegant border border-gray-100 p-2 flex flex-col gap-0.5 w-72">
              <a href="../sektor/gida.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-900 transition-colors">Gıda Sektörü</span>
                <span class="text-xs text-gray-400 mt-0.5">Hijyen ve verimlilik birlikte</span>
              </a>
              <a href="../sektor/madencilik.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-900 transition-colors">Madencilik Sektörü</span>
                <span class="text-xs text-gray-400 mt-0.5">Aşındırıcı yüklere dayanıklı çözümler</span>
              </a>
              <a href="../sektor/lojistik.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-900 transition-colors">Lojistik &amp; Depo</span>
                <span class="text-xs text-gray-400 mt-0.5">Sevkiyat hızını katlayın</span>
              </a>
              <a href="../sektor/insaat-cimento.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-900 transition-colors">İnşaat &amp; Çimento</span>
                <span class="text-xs text-gray-400 mt-0.5">Toz ve dökme malzeme uzmanlığı</span>
              </a>
            </div>
        </div>
      </div>
      <a href="../projeler.html" class="px-4 py-2.5 rounded-md text-base font-semibold transition text-gray-700 hover:text-primary hover:bg-gray-50 nav-link">Projeler</a>
      <a href="../referanslar.html" class="px-4 py-2.5 rounded-md text-base font-semibold transition text-gray-700 hover:text-primary hover:bg-gray-50 nav-link">Referanslar</a>
      <a href="../iletisim.html" class="px-4 py-2.5 rounded-md text-base font-semibold transition text-gray-700 hover:text-primary hover:bg-gray-50 nav-link">İletişim</a>
    </nav>
    <div class="flex items-center gap-3">
      <a href="tel:905333305285" class="slide-btn inline-flex items-center gap-2 px-4 py-2.5 text-base font-bold text-gray-700 hover:text-white transition-colors duration-300 bg-gray-50 rounded-lg border border-gray-100 shadow-sm group">
        <svg class="w-5 h-5 text-primary group-hover:text-white group-hover:scale-110 transition-all duration-300" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.33 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>
        <span class="hidden sm:inline">+90 533 330 52 85</span>
      </a>
    </div>
  </div>
</header>
"""

FOOTER_TEMPLATE = """<footer class="bg-ink text-white mt-20">
  <div class="max-w-[1650px] mx-auto px-4 lg:px-8 py-16 grid gap-10 md:grid-cols-2 lg:grid-cols-4">
    <div>
      <a href="../index.html" class="flex items-center gap-3 font-display font-bold text-xl text-white leading-none">
        <img src="../nozulfooterlogo.png" alt="Nozul Makina Logo" class="h-12 w-auto object-contain">
      </a>
      <p class="mt-6 text-sm leading-relaxed text-white">2001'den beri endüstriyel konveyör ve taşıma sistemleri üretiyoruz. Gıda, madencilik, inşaat ve genel sanayi için güvenilir çözümler.</p>
      <div class="flex gap-3 mt-6">
        <a href="https://www.linkedin.com/in/nozul-makina-29576a219/" target="_blank" rel="noreferrer" class="w-9 h-9 grid place-items-center rounded-md bg-white/10 hover:bg-primary transition-all group" aria-label="LinkedIn">
          <svg class="w-4 h-4 transition-colors text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
        </a>
        <a href="https://www.instagram.com/nozulmakina.tr/" target="_blank" rel="noreferrer" class="w-9 h-9 grid place-items-center rounded-md bg-white/10 hover:bg-primary transition-all group" aria-label="Instagram">
          <svg class="w-4 h-4 transition-colors text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
        </a>
      </div>
    </div>
    <div>
      <h3 class="text-sm font-semibold uppercase tracking-wider text-primary mb-4">Kurumsal</h3>
      <ul class="space-y-2 text-sm text-white">
        <li><a href="../hakkimizda.html" class="hover:text-primary transition-colors">Hakkımızda</a></li>
        <li><a href="../projeler.html" class="hover:text-primary transition-colors">Projeler</a></li>
        <li><a href="../referanslar.html" class="hover:text-primary transition-colors">Referanslar</a></li>
        <li><a href="../iletisim.html" class="hover:text-primary transition-colors">İletişim</a></li>
      </ul>
    </div>
    <div>
      <h3 class="text-sm font-semibold uppercase tracking-wider text-primary mb-4">Ürünler</h3>
      <ul class="space-y-2 text-sm text-white">
        <li><a href="pvc-bantli-konveyor.html" class="hover:text-primary transition-colors">PVC Bantlı Konveyör</a></li>
        <li><a href="rulolu-konveyor.html" class="hover:text-primary transition-colors">Rulolu Konveyör</a></li>
        <li><a href="vidali-konveyor.html" class="hover:text-primary transition-colors">Vidalı Konveyör</a></li>
      </ul>
    </div>
    <div>
      <h3 class="text-sm font-semibold uppercase tracking-wider text-primary mb-4">İletişim</h3>
      <ul class="space-y-3 text-sm text-white">
        <li class="flex items-center gap-2">📞 <a href="tel:905333305285" class="hover:text-primary">+90 533 330 52 85</a></li>
        <li class="flex items-center gap-2">✉️ <a href="mailto:info@nozulmakina.com.tr" class="hover:text-primary">info@nozulmakina.com.tr</a></li>
      </ul>
    </div>
  </div>
  <div class="border-t border-white/10 py-8 text-center text-xs text-white/50">
    <p>© Nozul Makina. Tüm hakları saklıdır.</p>
  </div>
</footer>
<a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" class="fixed bottom-6 right-6 z-40 w-14 h-14 rounded-full bg-emerald-500 text-white grid place-items-center shadow-elegant hover:scale-110 transition"><svg class="w-7 h-7" fill="currentColor" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg></a>
<script src="../assets/js/main.js"></script>
</body>
</html>"""

# Ürün verileri (Gerçek içerikler)
products = {
    "pvc-bantli-konveyor.html": {
        "TITLE": "PVC Bantlı Konveyör",
        "IMG": "IMG_1554_500x540.jpg",
        "DESC": "PVC bantlı konveyörler, gıda, ambalaj ve montaj hatlarında yaygın olarak kullanılır. Motor gücüyle hareket eden bant sistemi, sessiz ve hijyenik çalışma sağlar.",
        "SPECS": ["Gıda uyumlu bant seçenekleri", "Ayarlanabilir hız ve eğim", "Paslanmaz veya boyalı sac şasi", "Yan korkuluk ve örtü opsiyonu"],
        "AREAS": ["Gıda paketleme", "Ambalaj hatları", "Montaj hatları", "Lojistik & sevkiyat"],
        "VIDEO": "https://www.youtube.com/watch?v=LccY1DQg67I&t=51s"
    },
    "kaucuk-bantli-konveyor.html": {
        "TITLE": "Kauçuk Bantlı Konveyör",
        "IMG": "WhatsApp-Image-2024-07-20-at-09.14.02.jpeg",
        "DESC": "Ağır hizmet tipi kauçuk bantlı konveyörler, madencilik ve taş kırma tesisleri gibi zorlu koşullar için tasarlanmıştır.",
        "SPECS": ["Yüksek aşınma direnci", "Darbe sönümleyici rulolar", "Ağır hizmet tipi tahrik ünitesi", "Toz sızdırmaz yataklama"],
        "AREAS": ["Maden ocakları", "Taş kırma tesisleri", "Geri dönüşüm merkezleri", "Liman yükleme"],
        "VIDEO": None
    },
    "rulolu-konveyor.html": {
        "TITLE": "Rulolu Konveyör",
        "IMG": "OTOMATIK-AGIR-RULOLU-KONVEYOR-SISTEMI-1-2048x1152-1-min-png.webp",
        "DESC": "Kutu, palet ve düzgün tabanlı ürünlerin taşınması için en verimli çözümdür. Tahrikli veya serbest rulo seçenekleri mevcuttur.",
        "SPECS": ["Modüler tasarım", "Tahrikli veya serbest rulolar", "Sessiz çalışma", "Kolay bakım"],
        "AREAS": ["Lojistik merkezleri", "Otomotiv montaj", "Depolama sistemleri", "Üretim hatları"],
        "VIDEO": None
    },
    "vidali-konveyor.html": {
        "TITLE": "Vidalı Konveyör (Helezon)",
        "IMG": "AS-1.jpg",
        "DESC": "Toz ve granül malzemelerin kapalı bir gövde içinde tozsuz bir şekilde taşınmasını sağlar.",
        "SPECS": ["Toz sızdırmaz gövde", "Paslanmaz veya karbon çelik", "Yüksek dozaj hassasiyeti", "Kolay temizlenebilir"],
        "AREAS": ["Çimento sektörü", "Gıda & Un fabrikaları", "Kimya sanayi", "Atık su arıtma"],
        "VIDEO": None
    },
    "zincirli-konveyor.html": {
        "TITLE": "Zincirli Konveyör",
        "IMG": "WhatsApp-Image-2024-01-16-at-10.40.52-scaled.jpeg",
        "DESC": "Yüksek tonajlı ve sıcak malzemelerin güvenli taşınması için geliştirilmiş ağır hizmet konveyörleridir.",
        "SPECS": ["Ağır hizmet zinciri", "Isıya dayanıklı yapı", "Yüksek taşıma kapasitesi", "Kapalı gövde opsiyonu"],
        "AREAS": ["Geri dönüşüm", "Enerji santralleri", "Demir-Çelik", "Ağır sanayi"],
        "VIDEO": None
    },
    "elevator.html": {
        "TITLE": "Kovalı Elevatör",
        "IMG": "NM-ELEVATOR-001_600x600_500x540.jpg",
        "DESC": "Dökme malzemelerin dikey yönde, minimum alanda yüksek irtifalara taşınmasını sağlar.",
        "SPECS": ["Yüksek irtifa kapasitesi", "Toz sızdırmaz yapı", "Dayanıklı kovalar", "Geri dönüş kilidi"],
        "AREAS": ["Hububat siloları", "Maden tesisleri", "Yem fabrikaları", "Kimya sektörü"],
        "VIDEO": None
    },
    "hucre-tekeri.html": {
        "TITLE": "Hücre Tekeri (Rotary Valve)",
        "IMG": "IMG_2192_1000x1000.jpg",
        "DESC": "Pnömatik taşıma sistemlerinde ve filtre altlarında hassas malzeme besleme ve hava kilidi görevi görür.",
        "SPECS": ["Hassas dozajlama", "Hava kilidi özelliği", "Aşınmaya dayanıklı kanatlar", "Farklı rotor seçenekleri"],
        "AREAS": ["Pnömatik taşıma", "Toz toplama sistemleri", "Silo altları", "Dozajlama üniteleri"],
        "VIDEO": None
    },
    "kaynak-konumlandirma.html": {
        "TITLE": "Kaynak Konumlandırma",
        "IMG": "WhatsApp-Image-2024-12-11-at-10.25.50-3-Photoroom_540x500.jpg",
        "DESC": "İş parçasının istenen açıda döndürülmesini sağlayarak kaynak kalitesini ve hızını artıran sistemlerdir.",
        "SPECS": ["Hassas servo kontrol", "Yüksek tonaj kapasitesi", "Robot kaynağa uyumlu", "Özel tasarım fikstür"],
        "AREAS": ["Otomotiv", "Makine imalatı", "Boru üretimi", "Çelik konstrüksiyon"],
        "VIDEO": "https://www.youtube.com/watch?v=2WjBn2GX8aM&t=5s"
    }
}

def build_page(fname, data):
    # Main Content Area
    video_btn_html = ""
    if data["VIDEO"]:
        video_btn_html = f'''<a href="{data["VIDEO"]}" target="_blank" rel="noreferrer" class="bg-red-600 text-white px-6 py-3 rounded-md font-semibold shadow-soft hover:bg-red-700 transition flex items-center gap-2 group">
          <svg class="w-5 h-5 transition-transform group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
          Videoyu İzle
        </a>'''

    main_content = f'''
<main>
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
        <div>
          <h2 class="font-display font-semibold mb-3">Özellikler</h2>
          <ul class="space-y-2 text-sm text-gray-700">
            {"".join([f'<li class="flex gap-2"><span class="text-primary mt-0.5">✓</span>{s}</li>' for s in data["SPECS"]])}
          </ul>
        </div>
        <div>
          <h2 class="font-display font-semibold mb-3">Uygulama Alanları</h2>
          <ul class="space-y-2 text-sm text-gray-700">
            {"".join([f'<li class="flex gap-2"><span class="text-primary mt-0.5">→</span>{a}</li>' for a in data["AREAS"]])}
          </ul>
        </div>
      </div>
      <div class="mt-8 flex flex-wrap gap-3">
        {video_btn_html}
        <a href="../teklif-al.html" class="bg-gradient-primary text-white px-6 py-3 rounded-md font-semibold shadow-soft hover:shadow-elegant transition flex items-center gap-2">Bu ürün için teklif al</a>
        <a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" rel="noreferrer" class="border border-gray-200 px-6 py-3 rounded-md font-semibold hover:border-primary hover:text-primary transition flex items-center gap-2">WhatsApp ile sor</a>
      </div>
    </div>
  </div>
</section>

<section class="py-16 bg-surface">
  <div class="max-w-[1400px] mx-auto px-4 lg:px-8">
    <h2 class="font-display text-2xl font-bold mb-6">Diğer Ürünlerimiz</h2>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div class="card-sweep rounded-2xl group">
          <a href="pvc-bantli-konveyor.html" class="block bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant transition relative z-10">
            <div class="aspect-[4/3] overflow-hidden bg-gray-100"><img src="../assets/images/IMG_1554_500x540.jpg" alt="PVC" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/></div>
            <div class="p-5"><h3 class="font-display font-semibold group-hover:text-primary">PVC Bantlı Konveyör</h3></div>
          </a>
        </div>
        <div class="card-sweep rounded-2xl group">
          <a href="rulolu-konveyor.html" class="block bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant transition relative z-10">
            <div class="aspect-[4/3] overflow-hidden bg-gray-100"><img src="../assets/images/OTOMATIK-AGIR-RULOLU-KONVEYOR-SISTEMI-1-2048x1152-1-min-png.webp" alt="Rulolu" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/></div>
            <div class="p-5"><h3 class="font-display font-semibold group-hover:text-primary">Rulolu Konveyör</h3></div>
          </a>
        </div>
        <div class="card-sweep rounded-2xl group">
          <a href="vidali-konveyor.html" class="block bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant transition relative z-10">
            <div class="aspect-[4/3] overflow-hidden bg-gray-100"><img src="../assets/images/AS-1.jpg" alt="Vidalı" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/></div>
            <div class="p-5"><h3 class="font-display font-semibold group-hover:text-primary">Vidalı Konveyör</h3></div>
          </a>
        </div>
    </div>
  </div>
</section>
</main>
'''
    full_html = HEADER_TEMPLATE.replace("{TITLE}", data["TITLE"]) + main_content + FOOTER_TEMPLATE
    return full_html

root_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler'
for fname, data in products.items():
    fpath = os.path.join(root_dir, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(build_page(fname, data))
    print(f"Professionally Restored: {fname}")
