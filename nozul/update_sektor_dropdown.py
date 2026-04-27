import os
import re

# New dropdown content for ROOT level pages (index.html, urunler.html etc)
NEW_PANEL_ROOT = '''<div class="bg-white rounded-2xl shadow-elegant border border-gray-100 p-2 flex flex-col gap-0.5 w-72">
              <a href="sektor/gida.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-800 group-hover:text-primary transition-colors">Gıda Sektörü</span>
                <span class="text-xs text-gray-400 mt-0.5">Hijyen ve verimlilik birlikte</span>
              </a>
              <a href="sektor/madencilik.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-800 group-hover:text-primary transition-colors">Madencilik Sektörü</span>
                <span class="text-xs text-gray-400 mt-0.5">Aşındırıcı yüklere dayanıklı çözümler</span>
              </a>
              <a href="sektor/lojistik.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-800 group-hover:text-primary transition-colors">Lojistik &amp; Depo</span>
                <span class="text-xs text-gray-400 mt-0.5">Sevkiyat hızını katlayın</span>
              </a>
              <a href="sektor/insaat-cimento.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-800 group-hover:text-primary transition-colors">İnşaat &amp; Çimento</span>
                <span class="text-xs text-gray-400 mt-0.5">Toz ve dökme malzeme uzmanlığı</span>
              </a>
            </div>'''

# New dropdown content for SUB level pages (sektor/, urunler/, blog/)
NEW_PANEL_SUB = '''<div class="bg-white rounded-2xl shadow-elegant border border-gray-100 p-2 flex flex-col gap-0.5 w-72">
              <a href="../sektor/gida.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-800 group-hover:text-primary transition-colors">Gıda Sektörü</span>
                <span class="text-xs text-gray-400 mt-0.5">Hijyen ve verimlilik birlikte</span>
              </a>
              <a href="../sektor/madencilik.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-800 group-hover:text-primary transition-colors">Madencilik Sektörü</span>
                <span class="text-xs text-gray-400 mt-0.5">Aşındırıcı yüklere dayanıklı çözümler</span>
              </a>
              <a href="../sektor/lojistik.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-800 group-hover:text-primary transition-colors">Lojistik &amp; Depo</span>
                <span class="text-xs text-gray-400 mt-0.5">Sevkiyat hızını katlayın</span>
              </a>
              <a href="../sektor/insaat-cimento.html" class="flex flex-col px-4 py-3 rounded-xl hover:bg-orange-50 transition-colors group">
                <span class="text-sm font-semibold text-gray-800 group-hover:text-primary transition-colors">İnşaat &amp; Çimento</span>
                <span class="text-xs text-gray-400 mt-0.5">Toz ve dökme malzeme uzmanlığı</span>
              </a>
            </div>'''

# Regex patterns to match the old inner panel div
# For root: href="sektor/...
PATTERN_ROOT = re.compile(
    r'<div class="bg-white rounded-xl shadow-elegant border border-gray-100 p-2 flex flex-col gap-1">\s*'
    r'<a href="sektor/madencilik\.html"[^>]*>Madencilik ve Cevher Hazırlama</a>\s*'
    r'<a href="sektor/insaat-cimento\.html"[^>]*>İnşaat ve Çimento</a>\s*'
    r'<a href="sektor/lojistik\.html"[^>]*>Lojistik ve Depolama</a>\s*'
    r'<a href="sektor/gida\.html"[^>]*>Gıda ve Tarım</a>\s*'
    r'</div>',
    re.DOTALL
)

# For sub: href="../sektor/...
PATTERN_SUB = re.compile(
    r'<div class="bg-white rounded-xl shadow-elegant border border-gray-100 p-2 flex flex-col gap-1">\s*'
    r'<a href="\.\./sektor/madencilik\.html"[^>]*>Madencilik ve Cevher Hazırlama</a>\s*'
    r'<a href="\.\./sektor/insaat-cimento\.html"[^>]*>İnşaat ve Çimento</a>\s*'
    r'<a href="\.\./sektor/lojistik\.html"[^>]*>Lojistik ve Depolama</a>\s*'
    r'<a href="\.\./sektor/gida\.html"[^>]*>Gıda ve Tarım</a>\s*'
    r'</div>',
    re.DOTALL
)

# Also fix the outer wrapper width (w-64 → auto, will be set by content)
WRAPPER_OLD = 'class="absolute top-full left-0 w-64 pt-2'
WRAPPER_NEW = 'class="absolute top-full left-0 pt-2'

root_dir = r'C:\Users\Serdarowski\Desktop\verisyon 2'
updated = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules']]
    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        rel = os.path.relpath(fpath, root_dir)
        depth = rel.count(os.sep)

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content

        if depth == 0:
            new_content = PATTERN_ROOT.sub(NEW_PANEL_ROOT, new_content)
        else:
            new_content = PATTERN_SUB.sub(NEW_PANEL_SUB, new_content)

        # Fix dropdown wrapper width
        new_content = new_content.replace(WRAPPER_OLD, WRAPPER_NEW)

        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Updated: {rel}")
            updated += 1

print(f"\nTotal files updated: {updated}")
