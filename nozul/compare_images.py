from PIL import Image
import os

def compare_images():
    original_path = 'assets/images/preleader1.jpg'
    output_path = 'assets/images/preleader1_test.webp'
    
    if not os.path.exists(original_path):
        print("Dosya bulunamadi.")
        return

    # Görseli aç
    img = Image.open(original_path)
    
    # WebP olarak kaydet (Kalite %80 - Görsel olarak kayıpsız sayılır)
    img.save(output_path, 'WEBP', quality=80)
    
    original_size = os.path.getsize(original_path) / (1024 * 1024)
    new_size = os.path.getsize(output_path) / (1024 * 1024)
    
    print(f"Orijinal Boyut: {original_size:.2f} MB")
    print(f"Yeni Boyut (WebP): {new_size:.2f} MB")
    print(f"Kazanc: %{((original_size - new_size) / original_size) * 100:.1f}")

if __name__ == "__main__":
    compare_images()
