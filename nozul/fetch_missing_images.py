import urllib.request
import re
import os

url = "https://www.nozulmakina.com.tr/urunler/"
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    img_urls = re.findall(r'src="(https://www\.nozulmakina\.com\.tr/wp-content/uploads/[^"]+)"', html)
    
    # We are missing 4 specific images:
    # IMG_2192_1000x1000.jpg
    # WhatsApp-Image-2022-01-04-at-17.50.02-3_500x540.jpg
    # admin-ajax-1-Photoroom.png
    # WhatsApp-Image-2024-12-11-at-10.25.50-3-Photoroom_540x500.jpg
    
    # Actually, they might be in the source. Let's just download ANY missing image that we have in the HTML files.
    # Let's read urunler.html to get all required images
    with open('urunler.html', 'r', encoding='utf-8') as f:
        urunler_html = f.read()
        
    required_images = set(re.findall(r'assets/images/([^"]+)', urunler_html))
    existing_images = set(os.listdir('assets/images'))
    
    missing_images = required_images - existing_images
    print("Missing images:", missing_images)
    
    for img_url in img_urls:
        filename = img_url.split('/')[-1]
        if filename in missing_images:
            local_path = os.path.join('assets/images', filename)
            print(f"Downloading {filename} from {img_url}...")
            try:
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req) as img_res, open(local_path, 'wb') as out_file:
                    out_file.write(img_res.read())
                print(f"Success: {filename}")
            except Exception as e:
                print(f"Failed to download {filename}: {e}")
                
except Exception as e:
    print(f"Error: {e}")
