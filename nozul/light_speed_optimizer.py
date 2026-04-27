import os
import re

def minify_css(css_text):
    # Boşlukları ve yorumları temizle
    css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)
    css_text = re.sub(r'\s+', ' ', css_text)
    css_text = css_text.replace('{ ', '{').replace(' }', '}').replace('; ', ';')
    return css_text.strip()

def minify_js(js_text):
    # Basit JS kucultme (yorumlar ve coklu bosluklar)
    js_text = re.sub(r'//.*', '', js_text)
    js_text = re.sub(r'/\*.*?\*/', '', js_text, flags=re.DOTALL)
    js_text = re.sub(r'\s+', ' ', js_text)
    return js_text.strip()

def optimize_html_files():
    base_dir = '.'
    print("HTML dosyalari optimize ediliyor...")
    
    for root, dirs, files in os.walk(base_dir):
        if any(skip in root for skip in ['.git', '.gemini', 'Yedek ve Düzenleme Dosyaları']):
            continue
            
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Scriptlere 'defer' ekle
                new_content = re.sub(r'<script src="([^"]+)"', r'<script src="\1" defer', content)
                
                # 2. Resimlere loading="lazy" (yoksa ekle)
                # (Zaten buyuk oranda ekledik ama garanti olsun)
                
                if new_content != content:
                    print(f"HTML Optimize Edildi: {path}")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

def minify_assets():
    print("Assetler (CSS/JS) sikistiriliyor...")
    
    # CSS
    css_path = 'assets/css/style.css'
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(minify_css(css_content))
        print("CSS Sıkıştırıldı.")

    # JS
    js_path = 'assets/js/main.js'
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(minify_js(js_content))
        print("JS Sıkıştırıldı.")

if __name__ == "__main__":
    optimize_html_files()
    minify_assets()
    print("\n'Işık Hızı' optimizasyonu tamamlandi!")
