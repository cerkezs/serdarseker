import os
import re

# Ürün dosyaları listesi
product_files = [
    "pvc-bantli-konveyor.html", "kaucuk-bantli-konveyor.html", "rulolu-konveyor.html",
    "zincirli-konveyor.html", "vidali-konveyor.html", "elevator.html",
    "hucre-tekeri.html", "surgu.html", "klape.html", "kaynak-konumlandirma.html"
]

wp_button_html = '''
<!-- WhatsApp Floating Button -->
<a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" class="fixed bottom-6 right-6 z-[9999] bg-[#25d366] text-white p-4 rounded-full shadow-lg hover:scale-110 transition-transform flex items-center justify-center group" aria-label="WhatsApp ile İletişime Geçin">
  <svg class="w-7 h-7" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-2.203 0-3.991 1.789-3.991 3.991 0 .585.131 1.153.381 1.66l-.033.115-1.03 3.766 3.844-1.009.119-.028c.504.225 1.056.344 1.62.344 2.203 0 3.991-1.789 3.991-3.991 0-2.203-1.788-3.991-3.991-3.991zm2.347 5.62c-.06.154-.346.291-.482.31-.137.019-.312.034-.504-.029-.24-.079-.537-.215-.863-.357-1.38-.605-2.277-2.022-2.346-2.115-.069-.092-.563-.748-.563-1.428 0-.68.354-1.014.481-1.153.126-.138.275-.173.367-.173h.263c.083 0 .157.001.226.004.072.003.17.027.259.243.1.243.344.838.374.898.03.06.05.13.01.21-.04.08-.06.13-.12.2-.06.07-.126.157-.18.21-.06.06-.12.124-.05.25.07.125.312.514.67.833.46.41 1.025.539 1.173.539.148 0 .235-.11.321-.21l.374-.539c.086-.123.167-.104.281-.063.114.041.724.341.848.403.125.062.208.093.238.145.03.052.03.3-.03.454zM12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm.017 19.12c-1.132 0-2.235-.272-3.22-.79l-4.542 1.192 1.213-4.436c-.604-.982-.924-2.116-.924-3.284 0-3.528 2.87-6.4 6.4-6.4 3.529 0 6.4 2.872 6.4 6.4 0 3.529-2.872 6.398-6.4 6.398z"/></svg>
  <span class="absolute right-full mr-3 bg-white text-ink text-xs font-bold px-3 py-1.5 rounded-lg shadow-xl opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap border border-gray-100">WhatsApp ile Sorun</span>
</a>
'''

def fix_page(fname):
    fpath = os.path.join(r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler', fname)
    if not os.path.exists(fpath): return
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. card-sweep'i temizle ve resmi sadeleştir
    # Eski: <div class="card-sweep rounded-2xl group"> <div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100 relative z-10">
    # Yeni: <div class="relative group"> <div class="overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-elegant relative z-10">
    
    content = re.sub(r'<div class="card-sweep rounded-2xl group">\s*<div class="overflow-hidden rounded-2xl border border-gray-100 bg-gray-100 relative z-10">', 
                     r'<div class="relative group">\n      <div class="overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-elegant relative z-10">', content)

    # 2. WhatsApp Butonunu Ekle (Eğer yoksa)
    if 'WhatsApp ile İletişime Geçin' not in content:
        content = content.replace('</body>', wp_button_html + '\n</body>')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in product_files:
    fix_page(f)
    print(f"Fixed & WP Added: {f}")
