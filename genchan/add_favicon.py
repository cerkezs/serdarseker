import os

files = ['index.html', 'hakkimizda.html', 'hizmetlerimiz.html', 'guzergahlar.html', 'iletisim.html']
favicon_tag = '  <link rel="icon" type="image/png" href="images/favicon.png" />\n'

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Find the title tag
    for i, line in enumerate(lines):
        if '<title>' in line:
            # Check if favicon is already there
            if i + 1 < len(lines) and 'favicon.png' in lines[i+1]:
                break
            lines.insert(i + 1, favicon_tag)
            break
            
    with open(f, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    print(f"Added favicon to {f}")
