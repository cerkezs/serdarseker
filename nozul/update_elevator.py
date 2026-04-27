import os
import re

path = r'c:\Users\Serdarowski\Desktop\verisyon 2\urunler\elevator.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Galeri HTML'i (7 Resim x 3 = 21 Slayt)
elevator_imgs = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg"]
repeated_imgs = elevator_imgs * 3

slides_html = ""
for img in repeated_imgs:
    slides_html += f'      <div class="swiper-slide"><img src="../assets/images/kovalielevatör/{img}" alt="Elevatör" onclick="openLightbox(this.src)"></div>\n'

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

# 2. CSS, Swiper JS ve Lightbox
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

# 3. Card-Sweep düzeltme (Zaten self-start ayarını bir önceki adımda yapmıştık)
c = re.sub(r'<div class="relative group">\s*<div class="overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-elegant relative z-10">',
           r'<div class="card-sweep rounded-2xl group">\n      <div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100 relative z-10">', c)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Elevatör Page Updated with Gallery.")
