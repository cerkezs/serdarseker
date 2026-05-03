import os

files = ['index.html', 'hakkimizda.html', 'hizmetlerimiz.html', 'guzergahlar.html', 'iletisim.html']

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    old_credit = '<div class="designer-credit">Designed by <a href="https://serdarseker.com.tr" target="_blank">Serdar ŞEKER</a></div>'
    new_credit = '<div class="designer-credit"><a href="https://serdarseker.com.tr" target="_blank">Designed by <span>Serdar ŞEKER</span></a></div>'
    
    content = content.replace(old_credit, new_credit)
    
    # Just in case there are subtle whitespace differences
    old_credit_2 = '<div class="designer-credit">Designed by <a href="https://serdarseker.com.tr" target="_blank">Serdar EKER</a></div>'
    new_credit_2 = '<div class="designer-credit"><a href="https://serdarseker.com.tr" target="_blank">Designed by <span>Serdar ŞEKER</span></a></div>'
    content = content.replace(old_credit_2, new_credit_2)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Updated {f}")
