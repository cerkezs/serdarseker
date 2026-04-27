import os
import re

root_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler'

def final_fix(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ana Ürün Görseli Bölümünü Temizle ve Düzelt
    # Bu regex, card-sweep olsa da olmasa da ana görsel divini bulur ve tertemiz yeniden yazar.
    main_img_match = re.search(r'<img src="\.\./assets/images/(.*?)" alt="(.*?)" class="w-full h-auto"/>', content)
    if main_img_match:
        img_src = main_img_match.group(1)
        img_alt = main_img_match.group(2)
        new_main_img_block = f'''<div class="card-sweep rounded-2xl group">
      <div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100 relative z-10">
        <img src="../assets/images/{img_src}" alt="{img_alt}" class="w-full h-auto group-hover:scale-105 transition duration-500"/>
      </div>
    </div>'''
        # Eski bozuk blokları hedefle
        content = re.sub(r'<div class="card-sweep rounded-2xl group">\s*<div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100">.*?</div>\s*</div>', new_main_img_block, content, flags=re.DOTALL)
        # Eğer yukarıdaki eşleşmezse (bozuk halini yakala)
        content = re.sub(r'<div class="card-sweep rounded-2xl group">\s*<div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100">.*?relative z-10">.*?</div>\s*</div>', new_main_img_block, content, flags=re.DOTALL)

    # 2. Butonlar Kısmını Düzelt (Div kapanış hatasını gider)
    # Mevcut butonları bulup temiz bir div içine alalım
    btn_block_pattern = r'<div class="mt-8 flex flex-wrap gap-3">.*?</div>\s*</div>\s*</div>\s*</div>'
    # Bu biraz riskli, o yüzden butonları doğrudan hedefleyelim
    
    # Önce tüm buton alanını bulup sıfırlayalım
    if 'pvc-bantli-konveyor.html' in fpath:
        video_url = "https://www.youtube.com/watch?v=LccY1DQg67I&t=51s"
        video_btn = f'''<a href="{video_url}" target="_blank" rel="noreferrer" class="bg-red-600 text-white px-6 py-3 rounded-md font-semibold shadow-soft hover:bg-red-700 transition flex items-center gap-2 group">
          <svg class="w-5 h-5 transition-transform group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
          Videoyu İzle
        </a>\n        '''
    elif 'kaynak-konumlandirma.html' in fpath:
        video_url = "https://www.youtube.com/watch?v=2WjBn2GX8aM&t=5s"
        video_btn = f'''<a href="{video_url}" target="_blank" rel="noreferrer" class="bg-red-600 text-white px-6 py-3 rounded-md font-semibold shadow-soft hover:bg-red-700 transition flex items-center gap-2 group">
          <svg class="w-5 h-5 transition-transform group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
          Videoyu İzle
        </a>\n        '''
    else:
        video_btn = ""

    new_btns_block = f'''<div class="mt-8 flex flex-wrap gap-3">
        {video_btn}<a href="../teklif-al.html" class="bg-gradient-primary text-white px-6 py-3 rounded-md font-semibold shadow-soft hover:shadow-elegant transition relative z-10">Bu ürün için teklif al</a>
        <a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" rel="noreferrer" class="border border-gray-200 px-6 py-3 rounded-md font-semibold hover:border-primary hover:text-primary transition flex items-center gap-2">WhatsApp ile sor</a>
      </div>'''
    
    content = re.sub(r'<div class="mt-8 flex flex-wrap gap-3">.*?WhatsApp ile sor</a>\s*</div>\s*</div>', new_btns_block + '\n    </div>', content, flags=re.DOTALL)

    # 3. Diğer Ürünler Kısmını Tertemiz Yeniden İnşa Et
    other_products_pattern = r'<section class="py-16 bg-surface">.*?</section>'
    
    # Önce mevcut ürünleri çekelim (href, img, title, desc)
    items = re.findall(r'<a href="(.*?)" class="group.*?img src="(.*?)" alt="(.*?)" loading="lazy".*?<h3.*?>(.*?)</h3><p.*?>(.*?)</p>', content, flags=re.DOTALL)
    
    if items:
        new_items_html = ""
        for item in items:
            href, img, alt, title, desc = item
            new_items_html += f'''
        <div class="card-sweep rounded-2xl group max-w-[450px] mx-auto w-full">
          <a href="{href}" class="block bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant transition relative z-10">
            <div class="aspect-[4/3] overflow-hidden bg-gray-100"><img src="{img}" alt="{alt}" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"/></div>
            <div class="p-5"><h3 class="font-display font-semibold group-hover:text-primary">{title}</h3><p class="mt-1 text-sm text-gray-600">{desc}</p></div>
          </a>
        </div>'''
        
        new_section = f'''<section class="py-16 bg-surface">
  <div class="max-w-[1400px] mx-auto px-4 lg:px-8">
    <h2 class="font-display text-2xl font-bold mb-6">Diğer Ürünlerimiz</h2>
    <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {new_items_html}
    </div>
  </div>
</section>'''
        content = re.sub(other_products_pattern, new_section, content, flags=re.DOTALL)

    # 4. Footer Temizliği (Eğer bozulduysa)
    content = content.replace('<div class="card-sweep rounded-2xl group max-w-[450px] mx-auto w-full">\n        <a href="https://www.instagram.com', '<a href="https://www.instagram.com')
    content = content.replace('<div class="card-sweep rounded-2xl group max-w-[450px] mx-auto w-full">\n        <a href="https://www.youtube.com/@nozulmakina', '<a href="https://www.youtube.com/@nozulmakina')
    # Yanlışlıkla kapanan divleri temizle
    content = re.sub(r'</a>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</footer>', '</a>\n      </div>\n    </div>\n  </div>\n</footer>', content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

for fname in os.listdir(root_dir):
    if fname.endswith('.html'):
        final_fix(os.path.join(root_dir, fname))
        print(f"Fixed: {fname}")
