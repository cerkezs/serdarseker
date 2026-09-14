<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Çalışmalarımız | Dincel Reklam</title>
    <link rel="icon" href="assets/favikon.webp" type="image/webp">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body class="interactive-body">

    <!-- Page Transition Overlay -->
    <div class="page-transition" id="page-transition"></div>

    <?php include 'includes/header.php'; ?>

<main id="main-content">

    <main>

    <section class="page-hero">
        <div class="hero-bg"><div class="hero-gradient"></div></div>
        <div class="page-hero-content reveal-up">
            <div class="page-hero-label">Portfolyo</div>
            <h1>
                <span class="heading-line"><span class="heading-line-inner">Seçkin</span></span>
                <span class="heading-line"><span class="heading-line-inner title-outline">Çalışmalarımız</span></span>
            </h1>
        </div>
    </section>

    <!-- Before / After Section -->
    <section class="before-after-section reveal-up">
        <div class="container">
            <h2 style="text-align:center; color: var(--white); font-family: var(--font-heading); margin-bottom: 3rem;">
                <span class="heading-line title-outline">Mükemmel</span>
                <span class="heading-line">Dönüşüm</span>
            </h2>
            <div class="ba-wrapper">
                <div class="ba-container">
                    <img src="assets/aura_totem.jpg" alt="Sonrası" class="ba-img ba-after">
                    <!-- Gerçek resminiz yoksa şimdilik Before resmini siyah beyaz yaptık -->
                    <div class="ba-before-wrapper">
                        <img src="assets/aura_totem.jpg" alt="Öncesi" class="ba-img ba-before" style="filter: grayscale(100%) brightness(50%);">
                    </div>
                    <div class="ba-slider">
                        <div class="ba-slider-btn">
                            <span style="display:inline-block; transform: rotate(180deg);">&#10148;</span>
                            <span style="display:inline-block;">&#10148;</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="portfolio-section">
        <div class="container">
            <div class="portfolio-filters reveal-up" style="transition-delay: 0.2s;">
                <button class="filter-btn active" data-filter="all">Tümü</button>
                <button class="filter-btn" data-filter="tabela">Işıklı Tabela</button>
                <button class="filter-btn" data-filter="kutu-harf">Kutu Harf</button>
                <button class="filter-btn" data-filter="dijital-baski">Dijital Baskı</button>
                <button class="filter-btn" data-filter="arac-giydirme">Araç Giydirme</button>
            </div>

            <div class="portfolio-masonry reveal-up" style="transition-delay: 0.4s;">
                <div class="portfolio-card" data-category="tabela">
                    <picture><source srcset="assets/aura_totem.jpg" type="image/webp"><img src="assets/aura_totem.jpg" alt="Aura AVM Totem" class="portfolio-card-img" loading="lazy"></picture>
                    <div class="portfolio-card-visual"></div>
                    <div class="portfolio-card-info">
                        <h4>Aura AVM Totem</h4>
                        <span>Totem Tabela</span>
                    </div>
                </div>
                <div class="portfolio-card" data-category="kutu-harf">
                    <picture><source srcset="assets/novatech_kutu_harf.jpg" type="image/webp"><img src="assets/novatech_kutu_harf.jpg" alt="NovaTech Kutu Harf" class="portfolio-card-img" loading="lazy"></picture>
                    <div class="portfolio-card-visual"></div>
                    <div class="portfolio-card-info">
                        <h4>NovaTech Kutu Harf</h4>
                        <span>Kutu Harf</span>
                    </div>
                </div>
                <div class="portfolio-card" data-category="tabela">
                    <picture><source srcset="assets/cyber_plaza_isikli.jpg" type="image/webp"><img src="assets/cyber_plaza_isikli.jpg" alt="Cyber Plaza Işıklı" class="portfolio-card-img" loading="lazy"></picture>
                    <div class="portfolio-card-visual"></div>
                    <div class="portfolio-card-info">
                        <h4>Cyber Plaza Işıklı</h4>
                        <span>Işıklı Tabela</span>
                    </div>
                </div>
                <div class="portfolio-card" data-category="dijital-baski">
                    <picture><source srcset="assets/zen_cafe_baski.jpg" type="image/webp"><img src="assets/zen_cafe_baski.jpg" alt="Natura Resort" class="portfolio-card-img" loading="lazy"></picture>
                    <div class="portfolio-card-visual"></div>
                    <div class="portfolio-card-info">
                        <h4>Natura Resort</h4>
                        <span>Yönlendirme</span>
                    </div>
                </div>
                <div class="portfolio-card" data-category="dijital-baski">
                    <picture><source srcset="assets/zen_cafe_baski.jpg" type="image/webp"><img src="assets/zen_cafe_baski.jpg" alt="Zen Cafe" class="portfolio-card-img" loading="lazy"></picture>
                    <div class="portfolio-card-visual"></div>
                    <div class="portfolio-card-info">
                        <h4>Zen Cafe</h4>
                        <span>Dijital Baskı</span>
                    </div>
                </div>
                <div class="portfolio-card" data-category="arac-giydirme">
                    <picture><source srcset="assets/matrix_filo_arac.jpg" type="image/webp"><img src="assets/matrix_filo_arac.jpg" alt="Matrix Filo" class="portfolio-card-img" loading="lazy"></picture>
                    <div class="portfolio-card-visual"></div>
                    <div class="portfolio-card-info">
                        <h4>Matrix Filo</h4>
                        <span>Araç Giydirme</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    </main>

    </main>

<?php include 'includes/footer.php'; ?>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
    <script src="script.js"></script>
</body>
</html>



