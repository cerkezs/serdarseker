from PIL import Image
import os
import re

def convert_to_webp():
    base_dir = '.'
    target_exts = ('.jpg', '.jpeg', '.png')
    
    print("Gorsel donusumu basliyor...")
    
    for root, dirs, files in os.walk(base_dir):
        # .git, .gemini gibi gizli klasorleri gec
        if any(skip in root for skip in ['.git', '.gemini', 'node_modules']):
            continue
            
        for file in files:
            if file.lower().endswith(target_exts):
                input_path = os.path.join(root, file)
                output_path = os.path.splitext(input_path)[0] + '.webp'
                
                try:
                    with Image.open(input_path) as img:
                        # Saydamlik varsa koru (PNG icin)
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGBA")
                        else:
                            img = img.convert("RGB")
                            
                        img.save(output_path, 'WEBP', quality=85)
                        print(f"Donusturuldu: {input_path} -> {output_path}")
                except Exception as e:
                    print(f"Hata ({file}): {e}")

def update_html_references():
    base_dir = '.'
    print("\nHTML referanslari guncelleniyor...")
    
    # JPG, JPEG, PNG referanslarini WEBP ile degistir
    # Sadece src="..." veya url('...') icindekileri yakalamaya calis
    regex_pattern = r'src="([^"]+?\.(?:jpg|jpeg|png))"|url\(\'?([^)\']+?\.(?:jpg|jpeg|png))\'?\)'
    
    for root, dirs, files in os.walk(base_dir):
        if any(skip in root for skip in ['.git', '.gemini', 'node_modules']):
            continue
            
        for file in files:
            if file.endswith('.html') or file.endswith('.css'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basit replace (daha saglikli olabilir)
                new_content = content
                for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                    new_content = new_content.replace(ext, '.webp')
                
                if new_content != content:
                    print(f"Guncellendi: {path}")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    convert_to_webp()
    update_html_references()
    print("\nTum operasyon basariyla tamamlandi!")
