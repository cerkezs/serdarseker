import os
import shutil

def organize_backups():
    backup_dir = 'Yedek ve Düzenleme Dosyaları'
    img_backup_dir = os.path.join(backup_dir, 'Eski Görseller')
    script_backup_dir = os.path.join(backup_dir, 'Scriptler')
    
    # Klasorleri olustur
    os.makedirs(img_backup_dir, exist_ok=True)
    os.makedirs(script_backup_dir, exist_ok=True)
    
    print("Duzenleme basliyor...")
    
    # 1. Scriptleri tasi (.py)
    for file in os.listdir('.'):
        if file.endswith('.py') and file != 'organize_backups.py':
            print(f"Tasiniyor (Script): {file}")
            shutil.move(file, os.path.join(script_backup_dir, file))
            
    # 2. Eski gorselleri tasi (.jpg, .jpeg, .png)
    # Tum alt klasorleri de tara
    for root, dirs, files in os.walk('.'):
        # Yedek klasorunu tarama
        if backup_dir in root or '.git' in root or '.gemini' in root:
            continue
            
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                source_path = os.path.join(root, file)
                # Klasor yapisini koruyarak tasimak istersek karmasiklasabilir, 
                # Simdilik sadece dosya ismiyle tasimanin en temizi oldugunu dusunuyorum.
                # Isim cakismasi olmamasi icin basina klasor ismini ekleyelim
                rel_root = root.replace('.', '').replace('\\', '_').replace('/', '_').strip('_')
                new_name = f"{rel_root}_{file}" if rel_root else file
                
                target_path = os.path.join(img_backup_dir, new_name)
                print(f"Tasiniyor (Gorsel): {source_path}")
                shutil.move(source_path, target_path)

    # 3. Boşa çıkan HTML'leri taşı
    for file in ['teklif-al.html', 'preleader1_test.webp']:
        if os.path.exists(file):
            print(f"Tasiniyor (Eski Dosya): {file}")
            shutil.move(file, os.path.join(backup_dir, file))

if __name__ == "__main__":
    organize_backups()
    print("\nTum dosyalar 'Yedek ve Düzenleme Dosyaları' klasorunde toplandi. Ana dizin tertemiz!")
