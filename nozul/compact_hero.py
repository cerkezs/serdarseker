import os

root_dir = r'c:\Users\Serdarowski\Desktop\verisyon 2'

def compact_hero_padding(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    c = f.read()
                
                # Sektör Sayfaları (py-20 -> py-12)
                if 'py-20' in c and 'bg-gradient-hero' in c:
                    c = c.replace('py-20', 'py-12')
                    print(f"Compacted hero padding (py-20->py-12) in: {file}")
                
                # Hakkımızda Sayfası (py-16 -> py-12)
                if 'py-16' in c and 'bg-gradient-hero' in c:
                    c = c.replace('py-16', 'py-12')
                    print(f"Compacted hero padding (py-16->py-12) in: {file}")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(c)

compact_hero_padding(root_dir)
