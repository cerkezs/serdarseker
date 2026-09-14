<?php
// Şablon: İlçe Bazlı SEO Sayfası
// Kullanım: Bu dosyayı çoğaltarak "esenler-tabela.php", "aksaray-reklam.php" gibi isimler verebilirsiniz.

$ilce_adi = "Örnek İlçe"; // Buraya ilçenin adını yazın (Örn: Esenler)
$anahtar_kelime = "Tabela ve Reklam"; // Örn: Işıklı Tabela
?>
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Dincel Reklam olarak <?php echo $ilce_adi; ?> bölgesinde <?php echo $anahtar_kelime; ?> hizmetleri sunuyoruz. Kaliteli ve garantili üretim.">
    <title><?php echo $ilce_adi; ?> <?php echo $anahtar_kelime; ?> | Dincel Reklam</title>
    <link rel="icon" href="assets/favikon.webp" type="image/webp">
    <link rel="stylesheet" href="style.css">
</head>
<body class="interactive-body">

    <?php include 'includes/header.php'; ?>

    <main id="main-content">
        <section class="page-header" style="margin-top: 100px; padding: 50px 20px; text-align: center;">
            <div class="container">
                <h1><?php echo $ilce_adi; ?> <span class="heading-line"><?php echo $anahtar_kelime; ?></span> Sistemleri</h1>
                <p>Dincel Reklam olarak <strong><?php echo $ilce_adi; ?></strong> bölgesinde yıllardır en yenilikçi tabela ve reklam çözümlerini sunuyoruz.</p>
            </div>
        </section>

        <!-- İlçe özel içeriği buraya eklenebilir -->
        <section class="local-content">
            <div class="container">
                <h2><?php echo $ilce_adi; ?> Bölgesindeki Hizmetlerimiz</h2>
                <p>Bölgedeki işletmelerin görünürlüğünü artırmak için özel tasarımlar üretiyoruz. Ücretsiz keşif için bizimle iletişime geçin.</p>
            </div>
        </section>
        
        <?php 
        // İsteğe bağlı olarak hizmetler bölümünün bir kısmını buraya çekebilir veya HTML olarak ekleyebilirsiniz.
        ?>
    </main>

    <?php include 'includes/footer.php'; ?>

    <script src="script.js"></script>
</body>
</html>
