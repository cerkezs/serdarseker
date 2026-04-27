import os
import re

# Yeni, akordiyonlu ve şık mobil menü HTML'i
mmenu_html_v2 = """
<!-- MOBİL MENÜ PANELİ -->
<div id="mmenu" class="hidden fixed inset-0 z-[100] bg-white lg:hidden">
  <div class="flex flex-col h-full">
    <div class="flex items-center justify-between px-4 h-20 border-b border-gray-100">
      <img src="nozulmakyenilogo.png" alt="Nozul Makina Logo" class="h-10 w-auto">
      <button onclick="document.getElementById('mmenu').classList.add('hidden')" class="w-10 h-10 grid place-items-center rounded-lg bg-gray-50 text-ink">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    </div>
    
    <div class="flex-1 overflow-y-auto py-8 px-4">
      <nav class="flex flex-col gap-5">
        <a href="index.html" class="text-xl font-bold text-ink">Anasayfa</a>
        <a href="hakkimizda.html" class="text-xl font-bold text-ink">Hakkımızda</a>
        <a href="urunler.html" class="text-xl font-bold text-ink">Ürünler</a>
        
        <!-- Sektörler Akordiyon -->
        <div class="border-y border-gray-50 py-2">
          <button onclick="document.getElementById('mobile-sektor-list').classList.toggle('hidden'); this.querySelector('svg').classList.toggle('rotate-180')" 
                  class="flex items-center justify-between w-full text-xl font-bold text-ink py-2">
            Sektörler
            <svg class="w-5 h-5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>
          <div id="mobile-sektor-list" class="hidden mt-3 flex flex-col gap-3 pl-4 border-l-2 border-primary/20">
            <a href="sektor/gida.html" class="text-lg font-medium text-gray-600">Gıda Sektörü</a>
            <a href="sektor/madencilik.html" class="text-lg font-medium text-gray-600">Madencilik Sektörü</a>
            <a href="sektor/lojistik.html" class="text-lg font-medium text-gray-600">Lojistik & Depo</a>
            <a href="sektor/insaat-cimento.html" class="text-lg font-medium text-gray-600">İnşaat & Çimento</a>
          </div>
        </div>

        <a href="projeler.html" class="text-xl font-bold text-ink">Projeler</a>
        <a href="referanslar.html" class="text-xl font-bold text-ink">Referanslar</a>
        <a href="blog.html" class="text-xl font-bold text-ink">Blog</a>
        <a href="iletisim.html" class="text-xl font-bold text-ink">İletişim</a>
      </nav>
    </div>

    <div class="p-4 border-t border-gray-100 bg-gray-50">
      <a href="tel:905333305285" class="flex items-center justify-center gap-3 w-full bg-gradient-primary text-white py-4 rounded-xl font-bold shadow-soft">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.33 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>
        <span>+90 533 330 52 85</span>
      </a>
    </div>
  </div>
</div>
"""

def update_all_menus():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Eğer eski mmenu varsa veya mnav butonu varsa güncelle
                if 'id="mmenu"' in content or 'id="mnav"' in content:
                    print(f"Güncelleniyor: {path}")
                    
                    # Önce varsa eski mmenu bloğunu temizle
                    content = re.sub(r'<!-- MOBİL MENÜ PANELİ -->.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
                    content = re.sub(r'<div id="mmenu".*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
                    
                    # Header kapanışından sonra yeni menüyü ekle
                    new_content = content.replace('</header>', '</header>' + mmenu_html_v2)
                    
                    # Alt klasör yollarını düzelt
                    if any(sub in root for sub in ['sektor', 'urunler', 'blog']):
                        new_content = new_content.replace('src="nozulmakyenilogo.png"', 'src="../nozulmakyenilogo.png"')
                        new_content = new_content.replace('href="index.html"', 'href="../index.html"')
                        new_content = new_content.replace('href="hakkimizda.html"', 'href="../hakkimizda.html"')
                        new_content = new_content.replace('href="urunler.html"', 'href="../urunler.html"')
                        new_content = new_content.replace('href="projeler.html"', 'href="../projeler.html"')
                        new_content = new_content.replace('href="referanslar.html"', 'href="../referanslar.html"')
                        new_content = new_content.replace('href="blog.html"', 'href="../blog.html"')
                        new_content = new_content.replace('href="iletisim.html"', 'href="../iletisim.html"')
                        new_content = new_content.replace('href="sektor/', 'href="../sektor/')

                    # mnav butonuna tetikleyiciyi doğrudan ekle (JS dosyasına bağımlılığı azaltmak için garanti yöntem)
                    new_content = new_content.replace('id="mnav"', 'id="mnav" onclick="document.getElementById(\'mmenu\').classList.toggle(\'hidden\')"')
                    
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    update_all_menus()
