import os
import re

def get_depth(filepath):
    parts = os.path.relpath(filepath, '.').split(os.sep)
    if len(parts) == 1:
        return ''
    return '../' * (len(parts) - 1)

if not os.path.exists('components'):
    os.makedirs('components')

# 1. Extract header and footer from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

header_match = re.search(r'<header.*?</header>', index_html, flags=re.DOTALL)
footer_match = re.search(r'<footer.*?</footer>', index_html, flags=re.DOTALL)

if header_match and footer_match:
    header_content = header_match.group(0)
    footer_content = footer_match.group(0)
    
    # We need to make links relative-ready. 
    # In index.html, paths look like "index.html", "nozulmakyenilogo.png", "sektor/gida.html"
    # We will prefix them with {{BASE_URL}} where appropriate.
    
    # It's safer to just replace known local links
    local_links = [
        'index.html', 'hakkimizda.html', 'urunler.html', 'projeler.html', 'referanslar.html', 'iletisim.html', 'blog.html',
        'sektor/gida.html', 'sektor/madencilik.html', 'sektor/lojistik.html', 'sektor/insaat-cimento.html',
        'urunler/pvc-bantli-konveyor.html', 'urunler/kaucuk-bantli-konveyor.html', 'urunler/rulolu-konveyor.html', 
        'urunler/zincirli-konveyor.html', 'urunler/vidali-konveyor.html', 'urunler/elevator.html',
        'nozulmakyenilogo.png', 'nozulfooterlogo.png'
    ]
    
    for link in local_links:
        # regex to replace href="link" or src="link"
        header_content = re.sub(f'href="{link}"', f'href="{{{{BASE_URL}}}}{link}"', header_content)
        header_content = re.sub(f'src="{link}"', f'src="{{{{BASE_URL}}}}{link}"', header_content)
        
        footer_content = re.sub(f'href="{link}"', f'href="{{{{BASE_URL}}}}{link}"', footer_content)
        footer_content = re.sub(f'src="{link}"', f'src="{{{{BASE_URL}}}}{link}"', footer_content)

    with open('components/header.html', 'w', encoding='utf-8') as f:
        f.write(header_content)
    with open('components/footer.html', 'w', encoding='utf-8') as f:
        f.write(footer_content)

    print("Created components/header.html and components/footer.html")

    # 2. Inject into all HTML files
    for root, dirs, files in os.walk('.'):
        if 'components' in root or '.git' in root or '.gemini' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                depth = get_depth(filepath)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Process the component templates
                local_header = header_content.replace('{{BASE_URL}}', depth)
                local_footer = footer_content.replace('{{BASE_URL}}', depth)

                # Replace header
                content = re.sub(r'<header.*?</header>', local_header, content, flags=re.DOTALL)
                # Replace footer
                content = re.sub(r'<footer.*?</footer>', local_footer, content, flags=re.DOTALL)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
    print("Updated all HTML files with new components.")
else:
    print("Could not find header or footer in index.html")
