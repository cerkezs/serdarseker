<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İletişim | Dincel Reklam</title>
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
            <div class="page-hero-label">Bize Ulaşın</div>
            <h1>
                <span class="heading-line"><span class="heading-line-inner">Hemen</span></span>
                <span class="heading-line"><span class="heading-line-inner title-outline">Başlayalım</span></span>
            </h1>
        </div>
    </section>

    <section class="contact-section">
        <div class="container">
            <div class="contact-cards-grid reveal-up" style="transition-delay: 0.2s;">
                <a href="https://wa.me/905415324726" class="contact-card whatsapp" target="_blank" rel="noopener">
                    <div class="card-icon">WhatsApp</div>
                    <h3>Mesaj Gönder</h3>
                    <p>Hızlı ve kolay iletişim için bize WhatsApp'tan yazın.</p>
                </a>
                <a href="tel:+905415324726" class="contact-card phone">
                    <div class="card-icon">Telefon</div>
                    <h3>Bizi Arayın</h3>
                    <p>0541 532 47 26<br>Hemen arayın, detayları görüşelim.</p>
                </a>
                <a href="mailto:info@dincelreklam.com" class="contact-card email">
                    <div class="card-icon">E-Posta</div>
                    <h3>Mail Gönderin</h3>
                    <p>info@dincelreklam.com<br>Teklif ve projeleriniz için mail atın.</p>
                </a>
                <a href="https://instagram.com/dincelreklam" class="contact-card insta" target="_blank" rel="noopener">
                    <div class="card-icon">Instagram</div>
                    <h3>Takip Edin</h3>
                    <p>@dincelreklam<br>Son işlerimizi ve portföyümüzü inceleyin.</p>
                </a>
            </div>
            
            <div class="contact-map reveal-up" style="transition-delay: 0.4s; margin-top: 4rem;">
                <h3 class="contact-info-title">Konumumuz</h3>
                <div class="map-container" style="width: 100%; height: 400px; border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05);">
                    <iframe 
                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d153018.67566271966!2d29.060965!3d40.982555!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14cac790b17ba8bf%3A0x7394ebc5169a240d!2zxLBzdGFuYnVs!5e0!3m2!1str!2str!4v1700000000000!5m2!1str!2str" 
                        width="100%" 
                        height="100%" 
                        style="border:0; filter: invert(90%) hue-rotate(180deg) brightness(80%) contrast(120%);" 
                        allowfullscreen="" 
                        loading="lazy" 
                        referrerpolicy="no-referrer-when-downgrade">
                    </iframe>
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


