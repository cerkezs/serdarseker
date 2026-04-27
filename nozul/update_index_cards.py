import os
import re

path = r'c:\Users\Serdarowski\Desktop\verisyon 2\index.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Ürün Kartları Bölümünü Bul ve Güncelle
# Kart Yapısı Örneği:
# <a href="..." class="group ... card-sweep">
#   <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">
#     ...
#   </div>
# </a>

# 1. PVC Bantlı Konveyör
c = re.sub(r'<a href="urunler/pvc-bantli-konveyor.html".*?</a>', 
r'''<a href="urunler/pvc-bantli-konveyor.html" class="group max-w-[450px] mx-auto w-full rounded-2xl shadow-soft hover:shadow-elegant hover:-translate-y-1 transition flex flex-col card-sweep">
          <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">
          <div class="aspect-[4/3] overflow-hidden bg-gray-100">
            <img src="assets/images/IMG_1554_500x540.jpg" alt="PVC Bantlı Konveyör" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/>
          </div>
          <div class="p-5 text-left">
            <h3 class="font-display font-semibold text-lg group-hover:text-primary transition">PVC Bantlı Konveyör</h3>
            <p class="mt-2 text-sm text-gray-600 line-clamp-2">Hafif ve orta tonajlı ürünler için sessiz, hijyenik taşıma.</p>
            <span class="inline-flex items-center gap-1 mt-4 text-sm font-medium text-primary">Detaylar →</span>
          </div>
          </div>
        </a>''', c, flags=re.DOTALL)

# 2. Kauçuk Bantlı Konveyör
c = re.sub(r'<a href="urunler/kaucuk-bantli-konveyor.html".*?</a>', 
r'''<a href="urunler/kaucuk-bantli-konveyor.html" class="group max-w-[450px] mx-auto w-full rounded-2xl shadow-soft hover:shadow-elegant hover:-translate-y-1 transition flex flex-col card-sweep">
          <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">
          <div class="aspect-[4/3] overflow-hidden bg-gray-100">
            <img src="assets/images/AS-2.jpg" alt="Kauçuk Bantlı Konveyör" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/>
          </div>
          <div class="p-5 text-left">
            <h3 class="font-display font-semibold text-lg group-hover:text-primary transition">Kauçuk Bantlı Konveyör</h3>
            <p class="mt-2 text-sm text-gray-600 line-clamp-2">Ağır hizmet ve dökme malzeme transferi için dayanıklı çözüm.</p>
            <span class="inline-flex items-center gap-1 mt-4 text-sm font-medium text-primary">Detaylar →</span>
          </div>
          </div>
        </a>''', c, flags=re.DOTALL)

# 3. Rulolu Konveyör
c = re.sub(r'<a href="urunler/rulolu-konveyor.html".*?</a>', 
r'''<a href="urunler/rulolu-konveyor.html" class="group max-w-[450px] mx-auto w-full rounded-2xl shadow-soft hover:shadow-elegant hover:-translate-y-1 transition flex flex-col card-sweep">
          <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">
          <div class="aspect-[4/3] overflow-hidden bg-gray-100">
            <img src="assets/images/3.jpeg" alt="Rulolu Konveyör" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/>
          </div>
          <div class="p-5 text-left">
            <h3 class="font-display font-semibold text-lg group-hover:text-primary transition">Rulolu Konveyör</h3>
            <p class="mt-2 text-sm text-gray-600 line-clamp-2">Kutu, palet ve düzgün tabanlı ürünler için.</p>
            <span class="inline-flex items-center gap-1 mt-4 text-sm font-medium text-primary">Detaylar →</span>
          </div>
          </div>
        </a>''', c, flags=re.DOTALL)

# 4. Zincirli Konveyör
c = re.sub(r'<a href="urunler/zincirli-konveyor.html".*?</a>', 
r'''<a href="urunler/zincirli-konveyor.html" class="group max-w-[450px] mx-auto w-full rounded-2xl shadow-soft hover:shadow-elegant hover:-translate-y-1 transition flex flex-col card-sweep">
          <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">
          <div class="aspect-[4/3] overflow-hidden bg-gray-100">
            <img src="assets/images/WhatsApp-Image-2024-01-16-at-10.40.52-scaled.jpeg" alt="Zincirli Konveyör" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/>
          </div>
          <div class="p-5 text-left">
            <h3 class="font-display font-semibold text-lg group-hover:text-primary transition">Zincirli Konveyör</h3>
            <p class="mt-2 text-sm text-gray-600 line-clamp-2">Yüksek tonajlı ve sıcak malzeme taşıma çözümü.</p>
            <span class="inline-flex items-center gap-1 mt-4 text-sm font-medium text-primary">Detaylar →</span>
          </div>
          </div>
        </a>''', c, flags=re.DOTALL)

# 5. Vidalı Konveyör
c = re.sub(r'<a href="urunler/vidali-konveyor.html".*?</a>', 
r'''<a href="urunler/vidali-konveyor.html" class="group max-w-[450px] mx-auto w-full rounded-2xl shadow-soft hover:shadow-elegant hover:-translate-y-1 transition flex flex-col card-sweep">
          <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">
          <div class="aspect-[4/3] overflow-hidden bg-gray-100">
            <img src="assets/images/AS-1.jpg" alt="Vidalı Konveyör (Helezon)" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/>
          </div>
          <div class="p-5 text-left">
            <h3 class="font-display font-semibold text-lg group-hover:text-primary transition">Vidalı Konveyör (Helezon)</h3>
            <p class="mt-2 text-sm text-gray-600 line-clamp-2">Toz, granül ve dökme malzeme için kapalı taşıma.</p>
            <span class="inline-flex items-center gap-1 mt-4 text-sm font-medium text-primary">Detaylar →</span>
          </div>
          </div>
        </a>''', c, flags=re.DOTALL)

# 6. Kovalı Elevatör
c = re.sub(r'<a href="urunler/elevator.html".*?</a>', 
r'''<a href="urunler/elevator.html" class="group max-w-[450px] mx-auto w-full rounded-2xl shadow-soft hover:shadow-elegant hover:-translate-y-1 transition flex flex-col card-sweep">
          <div class="relative z-10 flex flex-col h-full w-full bg-white rounded-[inherit] overflow-hidden border border-gray-100">
          <div class="aspect-[4/3] overflow-hidden bg-gray-100">
            <img src="assets/images/NM-ELEVATOR-001_600x600_500x540.jpg" alt="Kovalı Elevatör" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/>
          </div>
          <div class="p-5 text-left">
            <h3 class="font-display font-semibold text-lg group-hover:text-primary transition">Kovalı Elevatör</h3>
            <p class="mt-2 text-sm text-gray-600 line-clamp-2">Düşey yönde dökme malzeme taşıma sistemi.</p>
            <span class="inline-flex items-center gap-1 mt-4 text-sm font-medium text-primary">Detaylar →</span>
          </div>
          </div>
        </a>''', c, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Homepage Product Cards Updated with Card-Sweep Effect.")
