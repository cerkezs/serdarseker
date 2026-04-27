import os
import re

path = r'c:\Users\Serdarowski\Desktop\verisyon 2\index.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Bozuk testimonial bölümünü bul ve tertemiz yenisiyle değiştir
testimonial_section_pattern = r'<div class="grid lg:grid-cols-3 gap-8">.*?</div>\s*</div>\s*</section>'
new_testimonial_section = r'''<div class="grid lg:grid-cols-3 gap-8">
      <!-- Müşteri 1 -->
      <div class="card-sweep rounded-2xl group">
        <div class="bg-white border border-gray-100 rounded-[inherit] p-6 shadow-soft relative z-10 h-full">
          <div class="text-primary text-3xl">"</div>
          <p class="text-gray-700 leading-relaxed">Sahaya özel mühendislik yaklaşımları sayesinde projemiz hem zamanında hem de tahminden düşük maliyetle tamamlandı. Saha ekibi çok profesyonel.</p>
          <div class="mt-6 pt-4 border-t border-gray-100">
            <div class="font-semibold">Mehmet K.</div>
            <div class="text-sm text-gray-500">Üretim Müdürü • Demir-Çelik Sektörü</div>
          </div>
        </div>
      </div>

      <!-- Müşteri 2 -->
      <div class="card-sweep rounded-2xl group">
        <div class="bg-white border border-gray-100 rounded-[inherit] p-6 shadow-soft relative z-10 h-full">
          <div class="text-primary text-3xl">"</div>
          <p class="text-gray-700 leading-relaxed">24 saat içinde teklif aldık, 6 hafta içinde devreye aldık. Bu hızda ve kalitede başka bir üretici bulamadık. Tavsiye ediyorum.</p>
          <div class="mt-6 pt-4 border-t border-gray-100">
            <div class="font-semibold">Ayşe Y.</div>
            <div class="text-sm text-gray-500">Satın Alma Yöneticisi • Gıda Sektörü</div>
          </div>
        </div>
      </div>

      <!-- Müşteri 3 -->
      <div class="card-sweep rounded-2xl group">
        <div class="bg-white border border-gray-100 rounded-[inherit] p-6 shadow-soft relative z-10 h-full">
          <div class="text-primary text-3xl">"</div>
          <p class="text-gray-700 leading-relaxed">Hijyen standartlarımıza tam uyum sağlayan paslanmaz hatlar teslim edildi. Denetimden tam puan aldık. Çok memnunuz.</p>
          <div class="mt-6 pt-4 border-t border-gray-100">
            <div class="font-semibold">Ahmet D.</div>
            <div class="text-sm text-gray-500">Kalite Müdürü • Tavukçuluk Sektörü</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>'''

c = re.sub(testimonial_section_pattern, new_testimonial_section, c, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Testimonial Grid Fixed and Cleaned.")
