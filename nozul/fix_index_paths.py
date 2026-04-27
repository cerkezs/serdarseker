import os
import re

path = r'c:\Users\Serdarowski\Desktop\verisyon 2\index.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Kauçuk Bantlı Konveyör Yolunu Düzelt
c = c.replace('src="assets/images/AS-2.jpg"', 'src="assets/images/kaucukkonveyör/1.jpg"')

# Rulolu Konveyör Yolunu Düzelt
c = c.replace('src="assets/images/3.jpeg"', 'src="assets/images/rulolukonveyör/3.jpeg"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Homepage Image Paths Corrected.")
