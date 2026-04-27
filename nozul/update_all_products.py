import os
import re

root_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler'
pvc_video_url = "https://www.youtube.com/watch?v=LccY1DQg67I&t=51s"

def update_product_page(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ana Ürün Görselini Wrap Et
    # Pattern: <div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100">\n      <img src="(.*?)" alt="(.*?)" class="w-full h-auto"/>\n    </div>
    img_pattern = r'(<div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100">)\s*(<img src=".*?" alt=".*?" class="w-full h-auto"/>)\s*(</div>)'
    img_replacement = r'<div class="card-sweep rounded-2xl group">\n    \1 relative z-10">\n      \2\n    \3\n    </div>'
    
    if 'card-sweep' not in content[:content.find('</h1>')+500]: # Sadece ana görsel için kontrol
        content = re.sub(img_pattern, img_replacement, content, count=1)

    # 2. Diğer Ürünler Kartlarını Wrap Et
    # Pattern: <a href="(.*?)" class="group max-w-\[450px\] mx-auto w-full bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant transition">
    card_pattern = r'(<a href=".*?" class="group max-w-\[450px\] mx-auto w-full bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-soft hover:shadow-elegant transition">)'
    card_replacement = r'<div class="card-sweep rounded-2xl group max-w-[450px] mx-auto w-full">\n        \1'
    
    # Kapanış etiketini de wrap etmeliyiz. Bu biraz daha karmaşık.
    # Önce tüm <a> bloklarını bulup değiştirelim.
    content = content.replace('shadow-soft hover:shadow-elegant transition">', 'shadow-soft hover:shadow-elegant transition relative z-10">')
    
    # Tekrar eden yapıları düzeltelim (zaten wrap edilmemişse)
    if 'card-sweep rounded-2xl group max-w-[450px]' not in content:
        content = re.sub(card_pattern, card_replacement, content)
        # Kapanış etiketlerini ekle (Her </a> sonrasına </div>)
        # Sadece "Diğer Ürünlerimiz" section'ı içindekileri hedeflemek için basitleştirilmiş bir yaklaşım:
        content = content.replace('</a>\n        <a', '</a>\n        </div>\n        <div class="card-sweep rounded-2xl group max-w-[450px] mx-auto w-full">\n        <a')
        # Sonuncuyu kapat
        content = content.replace('</a>\n    </div>\n  </div>\n</section>', '</a>\n        </div>\n    </div>\n  </div>\n</section>')

    # 3. PVC Video Butonu Ekle
    if "pvc-bantli-konveyor.html" in fpath:
        video_btn = f'''<a href="{pvc_video_url}" target="_blank" rel="noreferrer" class="bg-red-600 text-white px-6 py-3 rounded-md font-semibold shadow-soft hover:bg-red-700 transition flex items-center gap-2 group">
          <svg class="w-5 h-5 transition-transform group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
          Videoyu İzle
        </a>'''
        
        old_btns = '<div class="mt-8 flex flex-wrap gap-3">\n        <a href="../teklif-al.html"'
        new_btns = f'<div class="mt-8 flex flex-wrap gap-3">\n        <a href="../teklif-al.html"'
        
        if 'Videoyu İzle' not in content:
            content = content.replace('<a href="../teklif-al.html"', video_btn + '\n        <a href="../teklif-al.html"')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

for fname in os.listdir(root_dir):
    if fname.endswith('.html') and fname != 'kaynak-konumlandirma.html':
        update_product_page(os.path.join(root_dir, fname))
        print(f"Updated: {fname}")
