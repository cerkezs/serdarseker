import os
import re

path = r'c:\Users\Serdarowski\Desktop\verisyon 2\urunler\kaynak-konumlandirma.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Metin ve Özellikler Güncelleme
new_description = "Proje, tasarımı ve imalatı tarafımızca yapılan kaynak konumlandırma makinesi, dairesel kaynak kalitesini en iyi seviyeye çıkarmak adına geliştirilmiştir. Yatay, Dikey ve Açılı şekilde kaynak yapılabilir. 220V Enerji ile çalışmaktadır. Hız ayarı mevcuttur. Masalı olarak, Masa Üzeri Kullanım ve Ayak Pedallı ( START - STOP ) olarak opsiyonlu fiyatlandırma yapılmaktadır. Ø160 ve Ø250 mm gövde seçenekleri ile imalatını yapmaktayız. Kaynak makinesi otomatik kaynak özelliği ile kullanım yapılabilir. Gazaltı ve Argon Kaynağı kullanımına uygun aparatı mevcuttur. Ayrıca opsiyon olarak Oksijen ve Plazma kesim için aparat sistemi yapılmaktadır."

new_features_html = '''
      <div class="mt-8 bg-gray-50 rounded-2xl p-6 border border-gray-100">
        <h3 class="font-display font-bold text-primary uppercase tracking-wider text-sm mb-4">TEKNİK ÖZELLİKLER</h3>
        <ul class="space-y-3">
          <li class="flex items-center gap-3 text-gray-700 font-medium">
            <i class="fa-solid fa-circle-check text-primary"></i> STATİK FIRIN BOYALI
          </li>
          <li class="flex items-center gap-3 text-gray-700 font-medium">
            <i class="fa-solid fa-circle-check text-primary"></i> SAĞLAM ÇELİK GÖVDE
          </li>
          <li class="flex items-center gap-3 text-gray-700 font-medium">
            <i class="fa-solid fa-circle-check text-primary"></i> AÇI AYARLANABİLİR.
          </li>
          <li class="flex items-center gap-3 text-gray-700 font-medium">
            <i class="fa-solid fa-circle-check text-primary"></i> 220V ENERJİ
          </li>
        </ul>
        <p class="mt-6 text-xs font-bold text-gray-500 italic uppercase">İSTENİLEN ÖZELLİKLERDE ÖZEL TASARIM VE İMALATI YAPILABİLMEKTEDİR.</p>
      </div>
'''

# Mevcut açıklamayı ve tabloyu temizle, yenilerini koy
c = re.sub(r'<p class="mt-4 text-gray-700 leading-relaxed text-lg">.*?</p>', f'<p class="mt-4 text-gray-700 leading-relaxed text-lg">{new_description}</p>', c, flags=re.DOTALL)
c = re.sub(r'<div class="mt-8 bg-gray-50 rounded-2xl p-6 border border-gray-100">.*?</div>\s*<div class="mt-8">', new_features_html + '\n      <div class="mt-8 flex flex-wrap gap-4">', c, flags=re.DOTALL)

# 2. YouTube Butonu Ekleme
youtube_btn = '''
        <a href="https://www.youtube.com/watch?v=2WjBn2GX8aM&t=1s" target="_blank" class="inline-flex items-center gap-2 px-8 py-4 bg-[#FF0000] text-white rounded-xl font-bold hover:bg-[#CC0000] transition shadow-lg shadow-red-200 group">
          <i class="fa-brands fa-youtube text-xl group-hover:scale-110 transition"></i>
          Çalışma Videosunu İzle
        </a>
'''
if 'youtube.com' not in c:
    c = c.replace('<a href="../iletisim.html"', youtube_btn + '\n        <a href="../iletisim.html"')

# 3. Galeri HTML'i (5 Resim x 2 = 10 Slayt)
imgs = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"]
repeated_imgs = imgs * 2
slides_html = ""
for img in repeated_imgs:
    slides_html += f'      <div class="swiper-slide"><img src="../assets/images/kaynakkonumlandırma/{img}" alt="Kaynak" onclick="openLightbox(this.src)"></div>\n'

gallery_html = f'''
<!-- 3D PHOTO GALLERY SECTION -->
<section class="py-6 bg-ink overflow-hidden">
  <div class="max-w-[1400px] mx-auto px-4 lg:px-8 text-center mb-6">
    <h2 class="font-display text-2xl font-bold text-white mb-2 underline decoration-primary decoration-4 underline-offset-8">Ürün Uygulama Galerisi</h2>
    <p class="text-xs text-gray-500 mt-2 italic">Görselleri büyütmek için üzerlerine tıklayabilirsiniz.</p>
  </div>
  
  <div class="swiper mySwiper">
    <div class="swiper-wrapper">
{slides_html}    </div>
    <div class="swiper-pagination"></div>
  </div>
</section>
'''

if 'Ürün Uygulama Galerisi' not in c:
    c = c.replace('<section class="py-16 bg-surface">', gallery_html + '\n<section class="py-16 bg-surface">')

# 4. CSS, Swiper JS ve Lightbox
if 'swiper-bundle.min.css' not in c:
    head_add = '''
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
    c = c.replace('</head>', head_add + '\n</head>')

if 'swiper-bundle.min.js' not in c:
    body_add = '''
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
    if(swiperEl){
      swiperEl.addEventListener('mouseenter', function() { swiper.autoplay.stop(); });
      swiperEl.addEventListener('mouseleave', function() { swiper.autoplay.start(); });
    }
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
    c = c.replace('</body>', body_add + '\n</body>')

# 5. Hizalamalar (self-end) ve Card-Sweep
if 'self-end' not in c:
    c = re.sub(r'</div>\s*<div>\s*<span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>',
                 r'</div>\n    <div class="self-end">\n      <span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>', c)

c = re.sub(r'<div class="relative group">\s*<div class="overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-elegant relative z-10">',
           r'<div class="card-sweep rounded-2xl group">\n      <div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100 relative z-10">', c)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Kaynak Konumlandırma Page Fully Updated.")
