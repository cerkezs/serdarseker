import os
import re

# Ürünlerin Zenginleştirilmiş Verileri
enriched_data = {
    "pvc-bantli-konveyor.html": {
        "TITLE": "PVC Bantlı Konveyör",
        "INTRO": "Nozul Makina PVC bantlı konveyörleri, hafif ve orta tonajlı ürünlerin sarsıntısız, güvenli ve hijyenik bir şekilde taşınması için tasarlanmıştır. Sessiz çalışma prensibi ve modüler yapısı sayesinde özellikle gıda, ilaç ve ambalaj sektörlerinde yüksek verimlilik sunar.",
        "TABLE": [
            ("Şasi Yapısı", "Paslanmaz Çelik / Elektrostatik Boyalı Sac"),
            ("Bant Tipi", "Gıda Uyumlu PVC / PU / Antistatik"),
            ("Tahrik Sistemi", "Yüksek Verimli Redüktörlü Motor"),
            ("Opsiyonlar", "Hız Kontrolü, Kenar Korkuluk, Ayarlanabilir Ayak")
        ],
        "AREAS": ["Gıda İşleme", "İlaç ve Kozmetik", "Lojistik Paketleme", "Elektronik Montaj"]
    },
    "kaucuk-bantli-konveyor.html": {
        "TITLE": "Kauçuk Bantlı Konveyör",
        "INTRO": "Ağır hizmet tipi kauçuk bantlı konveyörlerimiz, madencilik ve taş kırma gibi en zorlu saha koşullarında kesintisiz performans sergilemek üzere üretilmiştir. Yüksek darbe dayanımı ve aşınma direnci ile dökme malzemelerin uzun mesafeli transferinde maksimum güven sağlar.",
        "TABLE": [
            ("Şasi Yapısı", "Ağır Hizmet Tipi Çelik Konstrüksiyon"),
            ("Bant Tipi", "EP Serisi Yüksek Mukavemetli Kauçuk"),
            ("Rulo Tipi", "Toz Sızdırmaz Labirent Keçeli Rulolar"),
            ("Kapasite Aralığı", "50 - 1500 Ton/Saat (Projeye Özel)")
        ],
        "AREAS": ["Maden Ocakları", "Çimento Tesisleri", "Liman Yükleme", "Geri Dönüşüm"]
    },
    "rulolu-konveyor.html": {
        "TITLE": "Rulolu Konveyör",
        "INTRO": "Kutu, palet ve düz tabanlı ürünlerin transferinde en düşük enerji tüketimi ile en yüksek verimi sunan sistemlerdir. Tahrikli veya serbest rulo seçenekleri ile üretim hatlarınızda esnek ve sessiz bir akış sağlar.",
        "TABLE": [
            ("Rulo Malzemesi", "Galvaniz Kaplı Çelik / Paslanmaz / PVC"),
            ("Tahrik Tipi", "Zincir Aktarmalı / Kayışlı / Serbest"),
            ("Yataklama", "Yüksek Kaliteli Rulmanlı Yataklar"),
            ("Taşıma Kapasitesi", "Ürün Ağırlığına Göre Optimize Edilir")
        ],
        "AREAS": ["Depolama ve Lojistik", "Otomotiv Yan Sanayi", "Beyaz Eşya Üretimi", "Sevkiyat Hatları"]
    },
    "zincirli-konveyor.html": {
        "TITLE": "Zincirli Konveyör",
        "INTRO": "Özellikle paletli ürünler, ağır metal parçalar ve yüksek sıcaklıktaki malzemelerin taşınması için geliştirilmiş, dayanıklılığı kanıtlanmış sistemlerdir. Zincir mekanizması sayesinde en ağır yüklerde bile kayma yapmadan stabil transfer sunar.",
        "TABLE": [
            ("Zincir Tipi", "Ağır Hizmet Tipi Çelik Baklalı Zincir"),
            ("Tahrik Ünitesi", "Yüksek Torklu Motor ve Redüktör"),
            ("Ray Yapısı", "Aşınmaya Dayanıklı Polietilen / Çelik"),
            ("Modülerlik", "Hat Boyuna Göre Eklenebilir Şasiler")
        ],
        "AREAS": ["Otomotiv Montaj", "Ağır Metal Sanayi", "Geri Dönüşüm Tesisleri", "Dökümhaneler"]
    },
    "vidali-konveyor.html": {
        "TITLE": "Vidalı Konveyör (Helezon)",
        "INTRO": "Toz ve granül yapıdaki malzemelerin kapalı bir gövde içerisinde, dış ortamdan tamamen izole edilerek transferini sağlayan sistemlerdir. Dozajlama ve transfer işlemlerinde %100 sızdırmazlık ve yüksek kontrol imkanı sunar.",
        "TABLE": [
            ("Gövde Tasarımı", "Boru Tipi veya U Tipi (Açılabilir Kapak)"),
            ("Yaprak Malzemesi", "Hardox / Paslanmaz / Karbon Çelik"),
            ("Sızdırmazlık", "Özel Salmastra ve Rulman Yataklama"),
            ("Uygulama", "Hassas Dozajlama ve Besleme")
        ],
        "AREAS": ["Un ve Yem Fabrikaları", "Kimya Sanayi", "Arıtma Tesisleri", "Plastik Granül Transferi"]
    },
    "elevator.html": {
        "TITLE": "Kovalı Elevatör",
        "INTRO": "Dökme malzemelerin dikey yönde, minimum taban alanı kullanarak yüksek irtifalara taşınması için en ekonomik çözümdür. Toz sızdırmaz kapalı yapısı sayesinde çevre kirliliğini önlerken malzeme kaybını minimize eder.",
        "TABLE": [
            ("Taşıyıcı Eleman", "Yüksek Mukavemetli Bant veya Zincir"),
            ("Kova Malzemesi", "Polietilen / Çelik / Paslanmaz"),
            ("Güvenlik", "Geri Dönüş Kilidi ve Devir Sensörü"),
            ("Yükseklik", "40 Metreye Kadar Tek Seferde Erişim")
        ],
        "AREAS": ["Hububat Siloları", "Bakliyat Tesisleri", "Maden Zenginleştirme", "Çimento ve Alçı"]
    },
    "hucre-tekeri.html": {
        "TITLE": "Hücre Tekeri (Rotary Valve)",
        "INTRO": "Pnömatik taşıma sistemlerinin ve filtre altlarının kritik bir parçası olan hücre tekerleri, malzeme akışını kontrol ederken sistem içindeki basıncı koruyan bir hava kilidi görevi görür. Hassas toleransları ile maksimum performans sunar.",
        "TABLE": [
            ("Rotor Tasarımı", "8-10 Kanatlı / Değiştirilebilir Kanat Ucu"),
            ("Malzeme", "Pik Döküm / Paslanmaz Çelik / Alüminyum"),
            ("Sızdırmazlık", "Yüksek Hassasiyetli İşlenmiş Gövde"),
            ("Tahrik", "Doğrudan veya Zincir Aktarmalı")
        ],
        "AREAS": ["Pnömatik Taşıma", "Toz Toplama (Jet Pulse)", "Silo Altı Besleme", "Hammadde Dozajlama"]
    },
    "surgu.html": {
        "TITLE": "Sürgü (Slide Gate)",
        "INTRO": "Silo, bunker ve konveyör çıkışlarında malzeme akışını durdurmak veya debiyi kontrol etmek amacıyla kullanılan yüksek mukavemetli valflerdir. Toz ve granül malzemeler için sızdırmaz bıçak tasarımı ile güvenli çalışma sağlar.",
        "TABLE": [
            ("Kontrol Tipi", "Pnömatik / Elektrikli / Manuel"),
            ("Bıçak Malzemesi", "AISI 304 Paslanmaz / Karbon Çelik"),
            ("Gövde Yapısı", "Kompakt ve Düşük Montaj Yüksekliği"),
            ("Sızdırmazlık", "Hassas Ayarlı Sızdırmazlık Fitilleri")
        ],
        "AREAS": ["Silo Çıkışları", "Tartım Sistemleri", "Bunker Tahliye", "Konveyör Boşaltma"]
    },
    "klape.html": {
        "TITLE": "Klape (Flap Valve)",
        "INTRO": "Malzeme akışının iki veya daha fazla yöne yönlendirilmesi gereken hatlarda kullanılan yön değiştirme valfleridir. Pnömatik tahriki sayesinde otomasyon sistemlerine tam uyum sağlar ve akış yönünü anlık olarak değiştirir.",
        "TABLE": [
            ("Kontrol Tipi", "Pnömatik Aktüatörlü / Manuel"),
            ("İç Yapı", "Aşınmaya Dayanıklı Polimer / Çelik Dil"),
            ("Bağlantı", "Standart Boru veya Kare Flanş"),
            ("Çalışma", "Hızlı ve Kesin Yön Değiştirme")
        ],
        "AREAS": ["Hat Ayrıştırma", "Paketleme Dağıtım", "Silo Dolum Hatları", "Pnömatik Sistemler"]
    },
    "kaynak-konumlandirma.html": {
        "TITLE": "Kaynak Konumlandırma",
        "INTRO": "İş parçalarının kaynak işlemi sırasında en uygun açıda döndürülmesini ve konumlandırılmasını sağlayan profesyonel sistemlerdir. Kaynak kalitesini artırırken, robotik kaynak hatlarında kesintisiz çalışma imkanı sunar.",
        "TABLE": [
            ("Kontrol Sistemi", "Hassas Servo Motor / Inverter Kontrol"),
            ("Taşıma Kapasitesi", "500 Kg - 50.000 Kg Arası Seçenekler"),
            ("Dönüş Hızı", "Kademesiz Ayarlanabilir Hassas Hız"),
            ("Platform", "Fikstür Bağlantısına Uygun T Kanallı Tablo")
        ],
        "AREAS": ["Otomotiv Şasi Kaynağı", "Boru ve Tank İmalatı", "Savunma Sanayi", "Robotik Kaynak Hücreleri"]
    }
}

def update_content(fname, data):
    fpath = os.path.join(r'C:\Users\Serdarowski\Desktop\verisyon 2\urunler', fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Teknik Tablo HTML'i oluştur
    table_rows = "".join([f'<tr><td class="py-3 pr-4 font-semibold text-gray-900 border-b border-gray-100">{k}</td><td class="py-3 text-gray-600 border-b border-gray-100">{v}</td></tr>' for k, v in data["TABLE"]])
    
    specs_table_html = f'''
      <div class="mt-8 bg-gray-50/50 rounded-2xl p-6 border border-gray-100">
        <h2 class="font-display font-bold text-lg mb-4 text-primary uppercase tracking-wider">Teknik Özellikler</h2>
        <table class="w-full text-sm">
          <tbody>
            {table_rows}
          </tbody>
        </table>
      </div>'''

    areas_html = "".join([f'<span class="px-3 py-1 bg-white border border-gray-200 rounded-full text-xs font-medium text-gray-600">{a}</span>' for a in data["AREAS"]])

    new_info_html = f'''<div>
      <span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>
      <h1 class="font-display text-3xl md:text-4xl font-bold mt-2">{data["TITLE"]}</h1>
      <p class="mt-4 text-gray-700 leading-relaxed text-lg">{data["INTRO"]}</p>
      
      {specs_table_html}

      <div class="mt-8">
        <h2 class="font-display font-bold text-sm mb-3 text-gray-400 uppercase tracking-widest">Uygulama Alanları</h2>
        <div class="flex flex-wrap gap-2">
          {areas_html}
        </div>
      </div>

      <div class="mt-10 flex flex-wrap gap-4">
        <a href="../teklif-al.html" class="bg-gradient-primary text-white px-8 py-4 rounded-xl font-bold shadow-soft hover:shadow-elegant transition-all flex items-center gap-2 group">
          Bu ürün için teklif al
          <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
        </a>
        <a href="https://api.whatsapp.com/send/?phone=905333305285" target="_blank" rel="noreferrer" class="bg-white border-2 border-gray-100 px-8 py-4 rounded-xl font-bold hover:border-primary hover:text-primary transition-all flex items-center gap-2">
          WhatsApp ile sor
        </a>
      </div>
    </div>'''

    # Mevcut içerik bloğunu bul ve değiştir (h1'den butonlara kadar olan bölge)
    # Regex ile main içindeki ilk sütunu hedefleyelim
    pattern = r'<div>\s*<span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>.*?</div>\s*</div>\s*</div>\s*</section>'
    # Bu regex biraz riskli olabilir, daha spesifik bir aralık seçelim
    # Header'dan main sonuna kadar olan kısmı koruyup ortayı değiştirelim.
    
    # Alternatif: <main> içindeki ilk <div> den sonrasını hedefle
    content = re.sub(r'<div>\s*<span class="text-xs font-semibold text-primary uppercase tracking-wider">Ürün</span>.*?</div>\s*</div>\s*</div>\s*</section>', new_info_html + '\n  </div>\n</section>', content, flags=re.DOTALL)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

for fname, data in enriched_data.items():
    update_content(fname, data)
    print(f"Content Enriched: {fname}")
