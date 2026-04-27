import os
import re

# Dosya yolları
root_dir = r'c:\Users\Serdarowski\Desktop\verisyon 2'
urunler_dir = os.path.join(root_dir, 'urunler')

new_address = "ARI SANAYİ SİTESİ 1418 CADDE NO : 38 İVOKSAN YENİMAHALLE -ANKARA"

# 1. Adres Güncelleme (Her yerde)
def update_address(content):
    # Eski adres kalıplarını bul ve değiştir
    # Örn: "Ostim, Ankara, Türkiye" veya benzeri
    content = re.sub(r'Ankara, Türkiye', new_address, content)
    # Varsa diğer adres satırlarını da hedefleyelim (genel bir temizlik)
    # Bu kısmı daha spesifik yapmak yerine index'teki yapıyı korumaya odaklanacağız footer kısmında.
    return content

# 2. WhatsApp Buton Güncelleme (Beyazlığı kaldır)
def update_wp_button(content):
    new_wp = '''
<!-- WhatsApp Floating Button -->
<a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" class="fixed bottom-6 right-6 z-[9999] text-white w-16 h-16 transition-transform flex items-center justify-center" aria-label="WhatsApp ile İletişime Geçin">
  <i class="fa-brands fa-whatsapp fa-beat-fade" style="color: rgb(52, 224, 13); font-size: 50px; filter: drop-shadow(0 0 10px rgba(0,0,0,0.3));"></i>
</a>
'''
    content = re.sub(r'<!-- WhatsApp Floating Button -->.*?</a>', new_wp, content, flags=re.DOTALL)
    return content

# 3. Footer Sync (PVC ve Rulolu için)
def get_correct_footer():
    with open(os.path.join(root_dir, 'index.html'), 'r', encoding='utf-8') as f:
        idx = f.read()
    # Footer bloğunu çek
    match = re.search(r'<footer.*?</footer>', idx, re.DOTALL)
    if match:
        footer = match.group(0)
        # Linkleri ../ ile güncelle
        footer = footer.replace('href="urunler/', 'href="')
        footer = footer.replace('href="sektor/', 'href="../sektor/')
        footer = footer.replace('href="hakkimizda.html"', 'href="../hakkimizda.html"')
        footer = footer.replace('href="projeler.html"', 'href="../projeler.html"')
        footer = footer.replace('href="referanslar.html"', 'href="../referanslar.html"')
        footer = footer.replace('href="iletisim.html"', 'href="../iletisim.html"')
        footer = footer.replace('href="index.html"', 'href="../index.html"')
        footer = footer.replace('src="nozul', 'src="../nozul')
        # Adresi güncelle
        footer = re.sub(r'Ankara, Türkiye', new_address, footer)
        return footer
    return None

correct_footer = get_correct_footer()

# PVC Sayfası Güncelleme
def fix_pvc():
    path = os.path.join(urunler_dir, 'pvc-bantli-konveyor.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = update_wp_button(c)
    if correct_footer:
        c = re.sub(r'<footer.*?</footer>', correct_footer, c, flags=re.DOTALL)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

# Rulolu Sayfası Güncelleme (Galeri Dahil)
def fix_rulolu():
    path = os.path.join(urunler_dir, 'rulolu-konveyor.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Ana Resmi değiştir
    c = re.sub(r'src="\.\./assets/images/.*?" alt="Rulolu Konveyör"', r'src="../assets/images/rulolukonveyör/3.jpeg" alt="Rulolu Konveyör"', c)
    
    # Galeriyi ekle
    gallery_html = '''
<!-- 3D PHOTO GALLERY SECTION -->
<section class="py-6 bg-ink overflow-hidden">
  <div class="max-w-[1400px] mx-auto px-4 lg:px-8 text-center mb-6">
    <h2 class="font-display text-2xl font-bold text-white mb-2 underline decoration-primary decoration-4 underline-offset-8">Ürün Uygulama Galerisi</h2>
    <p class="text-xs text-gray-500 mt-2 italic">Görselleri büyütmek için üzerlerine tıklayabilirsiniz.</p>
  </div>
  
  <div class="swiper mySwiper">
    <div class="swiper-wrapper">
      <div class="swiper-slide"><img src="../assets/images/rulolukonveyör/1.jpg" alt="Rulolu" onclick="openLightbox(this.src)"></div>
      <div class="swiper-slide"><img src="../assets/images/rulolukonveyör/2.jpg" alt="Rulolu" onclick="openLightbox(this.src)"></div>
      <div class="swiper-slide"><img src="../assets/images/rulolukonveyör/3.jpeg" alt="Rulolu" onclick="openLightbox(this.src)"></div>
      <div class="swiper-slide"><img src="../assets/images/rulolukonveyör/4.jpg" alt="Rulolu" onclick="openLightbox(this.src)"></div>
      <div class="swiper-slide"><img src="../assets/images/rulolukonveyör/5.jpg" alt="Rulolu" onclick="openLightbox(this.src)"></div>
      <div class="swiper-slide"><img src="../assets/images/rulolukonveyör/6.jpg" alt="Rulolu" onclick="openLightbox(this.src)"></div>
      <div class="swiper-slide"><img src="../assets/images/rulolukonveyör/7.jpg" alt="Rulolu" onclick="openLightbox(this.src)"></div>
      <div class="swiper-slide"><img src="../assets/images/rulolukonveyör/8.jpeg" alt="Rulolu" onclick="openLightbox(this.src)"></div>
      <div class="swiper-slide"><img src="../assets/images/rulolukonveyör/9.jpg" alt="Rulolu" onclick="openLightbox(this.src)"></div>
    </div>
    <div class="swiper-pagination"></div>
  </div>
</section>
'''
    # Önerilen ürünler section'ının üstüne ekle
    if 'Ürün Uygulama Galerisi' not in c:
        c = c.replace('<section class="py-16 bg-surface">', gallery_html + '\n<section class="py-16 bg-surface">')

    # CSS ve Swiper JS ekle (Head ve Body sonuna)
    if 'swiper-bundle.min.css' not in c:
        swiper_css = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
<style>
  .swiper { width: 100%; padding-top: 20px; padding-bottom: 40px; }
  .swiper-slide { background-position: center; background-size: cover; width: 320px; height: 320px; background-color: #fff; overflow: hidden; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
  .swiper-slide img { display: block; width: 100%; height: 100%; object-fit: cover; cursor: zoom-in; }
  .swiper-pagination-bullet-active { background: #ff7a2d !important; }
  #lightbox { display: none; position: fixed; z-index: 9999; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); justify-content: center; align-items: center; backdrop-filter: blur(8px); }
  #lightbox img { max-width: 90%; max-height: 85%; border-radius: 8px; border: 2px solid #333; }
  #lightbox .close { position: absolute; top: 25px; right: 35px; color: #fff; font-size: 50px; cursor: pointer; transition: 0.3s; }
</style>
'''
        c = c.replace('</head>', swiper_css + '\n</head>')

    if 'swiper-bundle.min.js' not in c:
        swiper_js = '''
<div id="lightbox">
  <span class="close" onclick="document.getElementById('lightbox').style.display='none'">&times;</span>
  <img id="lightbox-img" src="" alt="Büyük Görsel">
</div>
<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    var swiper = new Swiper(".mySwiper", {
      effect: "coverflow", grabCursor: true, centeredSlides: true, slidesPerView: "auto", loop: true,
      coverflowEffect: { rotate: 40, stretch: 0, depth: 100, modifier: 1, slideShadows: true },
      autoplay: { delay: 2000, disableOnInteraction: false },
      pagination: { el: ".swiper-pagination", clickable: true }
    });
    var swiperEl = document.querySelector('.mySwiper');
    swiperEl.addEventListener('mouseenter', function() { swiper.autoplay.stop(); });
    swiperEl.addEventListener('mouseleave', function() { swiper.autoplay.start(); });
  });
  function openLightbox(src) {
    const lb = document.getElementById('lightbox');
    const lbImg = document.getElementById('lightbox-img');
    lbImg.src = src; lb.style.display = 'flex';
  }
  window.onclick = function(event) {
    const lb = document.getElementById('lightbox');
    if (event.target == lb) { lb.style.display = 'none'; }
  }
</script>
'''
        c = c.replace('</body>', swiper_js + '\n</body>')

    c = update_wp_button(c)
    if correct_footer:
        c = re.sub(r'<footer.*?</footer>', correct_footer, c, flags=re.DOTALL)
    
    # Hizalama (self-end)
    c = re.sub(r'</div>\s*<div>\s*<span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>',
                 r'</div>\n    <div class="self-end">\n      <span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>', c)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

# Genel Adres Güncelleme (Tüm Sayfalar)
def update_global_address():
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                p = os.path.join(root, file)
                with open(p, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Adresi güncelle
                updated = re.sub(r'Ankara, Türkiye', new_address, content)
                # İletişim sayfasındaki veya footer'daki diğer Ankara kalıplarını da hedefleyelim
                updated = re.sub(r'İvedik Osb.*?Ankara', new_address, updated, flags=re.IGNORECASE)
                
                if updated != content:
                    with open(p, 'w', encoding='utf-8') as f:
                        f.write(updated)
                    print(f"Address Updated in: {file}")

fix_pvc()
fix_rulolu()
update_global_address()
