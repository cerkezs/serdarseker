document.addEventListener('DOMContentLoaded', function() {
    const mapWrapper = document.getElementById('svg-map-container');
    if (!mapWrapper) return;
    
    const rcTitle = document.getElementById('rc-title');
    const rcCities = document.getElementById('rc-cities');
    const marqueeContent = document.getElementById('marquee-content');

    const regions = {
        "marmara": ["Edirne", "Kırklareli", "Tekirdağ", "İstanbul", "Kocaeli", "Yalova", "Sakarya", "Bilecik", "Bursa", "Balıkesir", "Çanakkale"],
        "ege": ["İzmir", "Manisa", "Aydın", "Denizli", "Muğla", "Afyonkarahisar", "Uşak", "Kütahya"],
        "akdeniz": ["Antalya", "Isparta", "Burdur", "Mersin", "Adana", "Osmaniye", "Hatay", "Kahramanmaraş"],
        "ic_anadolu": ["Ankara", "Konya", "Kayseri", "Eskişehir", "Sivas", "Kırıkkale", "Aksaray", "Karaman", "Kırşehir", "Niğde", "Nevşehir", "Yozgat", "Çankırı"],
        "karadeniz": ["Bolu", "Düzce", "Zonguldak", "Karabük", "Bartın", "Kastamonu", "Çorum", "Sinop", "Samsun", "Amasya", "Tokat", "Ordu", "Giresun", "Gümüşhane", "Trabzon", "Bayburt", "Rize", "Artvin"],
        "dogu_anadolu": ["Erzurum", "Erzincan", "Elazığ", "Malatya", "Tunceli", "Bingöl", "Muş", "Bitlis", "Van", "Hakkari", "Şırnak", "Ağrı", "Iğdır", "Kars", "Ardahan"],
        "guneydogu_anadolu": ["Gaziantep", "Şanlıurfa", "Diyarbakır", "Mardin", "Siirt", "Batman", "Adıyaman", "Kilis"]
    };

    const names = {
        "marmara": "Marmara Bölgesi",
        "ege": "Ege Bölgesi",
        "akdeniz": "Akdeniz Bölgesi",
        "ic_anadolu": "İç Anadolu Bölgesi",
        "karadeniz": "Karadeniz Bölgesi",
        "dogu_anadolu": "Doğu Anadolu Bölgesi",
        "guneydogu_anadolu": "Güneydoğu Anadolu Bölgesi"
    };

    function normalize(str) {
        if (!str) return "";
        return str.toLowerCase()
            .replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ş/g, 's')
            .replace(/ı/g, 'i').replace(/ö/g, 'o').replace(/ç/g, 'c')
            .trim();
    }

    const cityToRegion = {};
    Object.entries(regions).forEach(([regionId, cities]) => {
        cities.forEach(city => {
            cityToRegion[normalize(city)] = regionId;
        });
    });

    const overrides = {
        "sirnak": "dogu_anadolu",
        "kinkkale": "ic_anadolu",
        "zinguldak": "karadeniz",
        "gumushane": "karadeniz",
        "k. maras": "akdeniz"
    };

    const svg = mapWrapper.querySelector('svg');
    if (svg) {
        const paths = svg.querySelectorAll('path');
        paths.forEach(path => {
            const cityName = path.getAttribute('name');
            const normName = normalize(cityName);
            const regionId = overrides[normName] || cityToRegion[normName];
            
            if (regionId) {
                path.setAttribute('data-region', regionId);
                path.classList.add('province-path');
            }

            path.addEventListener('mouseenter', function() {
                const rId = this.getAttribute('data-region');
                if (rId) highlightRegion(rId);
            });
        });

        // Initial highlight
        highlightRegion('marmara');
    }

    function highlightRegion(regionId) {
        const allProvinces = document.querySelectorAll('.province-path');
        allProvinces.forEach(p => p.classList.remove('active'));
        
        const regionProvinces = document.querySelectorAll(`.province-path[data-region="${regionId}"]`);
        regionProvinces.forEach(p => p.classList.add('active'));

        const regionName = names[regionId];
        const regionCities = regions[regionId];
        
        if (regionName && regionCities) {
            rcTitle.innerText = regionName;
            rcCities.innerText = regionCities.join(', ') + '.';
            
            rcTitle.classList.remove('active-anim');
            void rcTitle.offsetWidth;
            rcTitle.classList.add('active-anim');
        }
    }

    if (marqueeContent) {
        const allCities = [].concat(...Object.values(regions)).sort((a, b) => a.localeCompare(b, 'tr'));
        marqueeContent.innerHTML = allCities.concat(allCities).map(city => `<span><i class="fa-solid fa-circle"></i> ${city.toUpperCase()}</span>`).join('');
    }
});
