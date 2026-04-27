import os
import urllib.request

urls = {
    "WhatsApp-Image-2024-07-20-at-09.14.02.jpeg": "https://www.nozulmakina.com.tr/wp-content/uploads/2024/07/WhatsApp-Image-2024-07-20-at-09.14.02.jpeg",
    "OTOMATIK-AGIR-RULOLU-KONVEYOR-SISTEMI-1-2048x1152-1-min-png.webp": "https://www.nozulmakina.com.tr/wp-content/uploads/2025/03/OTOMATIK-AGIR-RULOLU-KONVEYOR-SISTEMI-1-2048x1152-1-min-png.webp",
    "WhatsApp-Image-2024-01-16-at-10.40.52-scaled.jpeg": "https://www.nozulmakina.com.tr/wp-content/uploads/2024/01/WhatsApp-Image-2024-01-16-at-10.40.52-scaled.jpeg",
    "IMG_1554_500x540.jpg": "https://www.nozulmakina.com.tr/wp-content/uploads/2024/01/IMG_1554_500x540.jpg",
    "AS-1.jpg": "https://www.nozulmakina.com.tr/wp-content/uploads/2023/11/AS-1.jpg",
    "NM-ELEVATOR-001_600x600_500x540.jpg": "https://www.nozulmakina.com.tr/wp-content/uploads/2023/11/NM-ELEVATOR-001_600x600_500x540.jpg",
    "IMG_1554.jpg": "https://www.nozulmakina.com.tr/wp-content/uploads/2024/01/IMG_1554.jpg", # in case we stripped the suffix
    "NM-ELEVATOR-001_600x600.jpg": "https://www.nozulmakina.com.tr/wp-content/uploads/2023/11/NM-ELEVATOR-001_600x600.jpg"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

if not os.path.exists('assets/images'):
    os.makedirs('assets/images')

for filename, url in urls.items():
    local_path = os.path.join('assets/images', filename)
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Success: {filename}")
    except Exception as e:
        print(f"Failed: {filename} - {e}")
