import os
import re

path = r'c:\Users\Serdarowski\Desktop\verisyon 2\index.html'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Müşteri Yorumları Kartlarını Bul ve Card-Sweep ekle
testimonial_pattern = r'<div class="bg-white border border-gray-100 rounded-2xl p-6 shadow-soft">'
replacement = r'''<div class="card-sweep rounded-2xl group">
        <div class="bg-white border border-gray-100 rounded-[inherit] p-6 shadow-soft relative z-10 h-full">'''

# Her bir kartı tek tek değiştir
c = c.replace(testimonial_pattern, replacement)

# Kapanış divlerini düzenle (z-index divi için ek bir </div> eklemek gerekiyor)
# Her bir kartın sonuna bir </div> eklemeliyiz.
# Mevcut kart yapısı: <div>...</div> (toplam 3 div kapanışı var sonunda)
# Yeni yapıda 4 div kapanışı olmalı: ... </div> (footer-t) </div> (relative) </div> (card-sweep)
# Aslında kartların bitişini bulup ekleyelim.

# Kart bitişlerini tespit et: Üretim Müdürü • Demir-Çelik Sektörü</div>\n        </div>\n      </div>
c = c.replace('Sektörü</div>\n        </div>\n      </div>', 'Sektörü</div>\n        </div>\n      </div>\n      </div>')
c = c.replace('Sektörü</div>\n        </div>\n      </div>', 'Sektörü</div>\n        </div>\n      </div>\n      </div>')
c = c.replace('Sektörü</div>\n        </div>\n      </div>', 'Sektörü</div>\n        </div>\n      </div>\n      </div>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Testimonial Cards Updated with Card-Sweep Effect.")
