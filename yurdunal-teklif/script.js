document.addEventListener("DOMContentLoaded", () => {
    initItemsForm();
    setupEventListeners();
});

let currentItemCount = 0;
let currentCurrencySymbol = "₺"; // Varsayılan: Türk Lirası

// Para birimi değiştirme fonksiyonu
function setCurrency(btn) {
    // Aktif butonu güncelle
    document.querySelectorAll(".currency-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    // Sembolü güncelle
    currentCurrencySymbol = btn.getAttribute("data-symbol");

    // Tüm önizleme satırlarındaki sembolü güncelle
    document.querySelectorAll(".currency").forEach(el => {
        el.textContent = currentCurrencySymbol;
    });

    // Hesaplamaları yeniden yap (tutarlar aynı kalır, sembol değişir)
    calculateTotals();
}

// İlgili satırları oluşturmak için (hem sol forma hem sağ tabloya)
function addNewItemRow() {
    currentItemCount++;
    const i = currentItemCount;

    // Form tarafı
    const formContainer = document.getElementById("items-container");
    const formHtml = `
        <div class="item-row" id="form-item-${i}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h4 style="margin-bottom: 0;"><span class="item-number-badge">${i}</span> Ürün / İş Kalemi</h4>
                <button type="button" class="btn-delete-item" onclick="removeItemRow(${i})">Sil</button>
            </div>
            <div class="form-group">
                <textarea id="in-name-${i}" placeholder="İşin Adı" rows="2" style="resize: vertical;"></textarea>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <input type="number" id="in-qty-${i}" placeholder="Miktarı" min="0" step="1">
                </div>
                <div class="form-group">
                    <input type="number" id="in-price-${i}" placeholder="Br. Fiyatı (₺)" min="0" step="0.01">
                </div>
            </div>
        </div>
    `;
    formContainer.insertAdjacentHTML('beforeend', formHtml);

    // Önizleme tarafı
    const tbody = document.getElementById("out-items-body");
    const previewHtml = `
        <tr id="preview-item-${i}" class="preview-item-row">
            <td class="preview-number-cell">${i}</td>
            <td id="out-name-${i}"></td>
            <td id="out-qty-${i}"></td>
            <td><span class="currency">${currentCurrencySymbol}</span><span id="out-price-${i}">-</span></td>
            <td><span class="currency">${currentCurrencySymbol}</span><span id="out-total-${i}">-</span></td>
        </tr>
    `;
    tbody.insertAdjacentHTML('beforeend', previewHtml);

    // Event listener'ları bağla
    const nameInput = document.getElementById(`in-name-${i}`);
    const qtyInput = document.getElementById(`in-qty-${i}`);
    const priceInput = document.getElementById(`in-price-${i}`);

    nameInput.addEventListener("input", (e) => document.getElementById(`out-name-${i}`).textContent = e.target.value);
    qtyInput.addEventListener("input", calculateTotals);
    priceInput.addEventListener("input", calculateTotals);
}

// Kalem silme fonksiyonu
function removeItemRow(id) {
    const formRow = document.getElementById(`form-item-${id}`);
    const previewRow = document.getElementById(`preview-item-${id}`);
    
    if (formRow) formRow.remove();
    if (previewRow) previewRow.remove();
    
    renumberItems();
    calculateTotals();
}

// Kalan satırları yeniden numaralandırma
function renumberItems() {
    const formBadges = document.querySelectorAll(".item-number-badge");
    formBadges.forEach((badge, index) => {
        badge.textContent = index + 1;
    });

    const previewCells = document.querySelectorAll(".preview-number-cell");
    previewCells.forEach((cell, index) => {
        cell.textContent = index + 1;
    });
}

// Başlangıçta 7 kalem ekle
function initItemsForm() {
    for (let i = 0; i < 7; i++) {
        addNewItemRow();
    }
}

// Statik alanların event listener'ları
function setupEventListeners() {
    // Statik alanlar
    const staticFields = [1, 2, 4, 5, 6, 7];
    staticFields.forEach(num => {
        const input = document.getElementById(`input-${num}`);
        if(input) {
            input.addEventListener("input", (e) => {
                let val = e.target.value;
                if(num === 5 && val) {
                    // Tarih formatını gg.aa.yyyy yap
                    const d = new Date(val);
                    if(!isNaN(d)) {
                        val = d.toLocaleDateString('tr-TR');
                    }
                }
                document.getElementById(`out-${num}`).textContent = val;
            });
        }
    });

    // Telefon ve Email alanları
    const telInput = document.getElementById("input-3-tel");
    if(telInput) {
        telInput.addEventListener("input", (e) => {
            document.getElementById("out-3-tel").textContent = e.target.value || "+90 535 576 31 59";
        });
    }

    const emailInput = document.getElementById("input-3-email");
    if(emailInput) {
        emailInput.addEventListener("input", (e) => {
            document.getElementById("out-3-email").textContent = e.target.value || "info@yurdunal.com.tr";
        });
    }

    // Açıklama alanı
    const aciklamaInput = document.getElementById("input-aciklama");
    if(aciklamaInput) {
        aciklamaInput.addEventListener("input", (e) => {
            document.getElementById("out-aciklama").textContent = e.target.value;
        });
    }
}

// Para birimi formatlama
function formatMoney(amount) {
    if (isNaN(amount) || amount === 0) return "-";
    return amount.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// Tutarları ve KDV'yi hesaplar
function calculateTotals() {
    let subtotal = 0;

    for (let i = 1; i <= currentItemCount; i++) {
        const qtyEl = document.getElementById(`in-qty-${i}`);
        const priceEl = document.getElementById(`in-price-${i}`);
        
        if (!qtyEl || !priceEl) continue; // Silinmiş satırları atla
        
        const qtyStr = qtyEl.value;
        const priceStr = priceEl.value;
        
        const qty = parseFloat(qtyStr) || 0;
        const price = parseFloat(priceStr) || 0;
        
        let rowTotal = 0;
        
        if (qty > 0 && price > 0) {
            rowTotal = qty * price;
            subtotal += rowTotal;
            document.getElementById(`out-qty-${i}`).textContent = qty;
            document.getElementById(`out-price-${i}`).textContent = formatMoney(price);
            document.getElementById(`out-total-${i}`).textContent = formatMoney(rowTotal);
        } else {
            document.getElementById(`out-qty-${i}`).textContent = qtyStr ? qty : "";
            document.getElementById(`out-price-${i}`).textContent = priceStr ? formatMoney(price) : "-";
            document.getElementById(`out-total-${i}`).textContent = "-";
        }
    }

    const kdv = subtotal * 0.20;
    const grandTotal = subtotal + kdv;

    document.getElementById("out-toplam").textContent = formatMoney(subtotal);
    document.getElementById("out-kdv").textContent = formatMoney(kdv);
    document.getElementById("out-genel-toplam").textContent = formatMoney(grandTotal);
}

// Yazdırma Fonksiyonu
function printPage() {
    window.print();
}

// Kaşe/İmza aç/kapat
function toggleKaseSimza() {
    const kaseChecked = document.getElementById("check-kase").checked;
    const simzaChecked = document.getElementById("check-simza").checked;
    
    document.getElementById("out-kase").style.display = kaseChecked ? "block" : "none";
    document.getElementById("out-simza").style.display = simzaChecked ? "block" : "none";
}

// Görseli base64'e dönüştürür (file:// protokolü sorunundan kaçınmak için)
function getImageAsBase64(imgId) {
    return new Promise((resolve) => {
        const img = document.getElementById(imgId);
        // Görsel yoksa veya görünür değilse boş dön
        if (!img || img.style.display === "none") { resolve(null); return; }

        const canvas = document.createElement("canvas");
        canvas.width = img.naturalWidth || img.width || 200;
        canvas.height = img.naturalHeight || img.height || 100;
        const ctx = canvas.getContext("2d");
        try {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            resolve(canvas.toDataURL("image/png"));
        } catch(e) {
            // Canvas taint hatası durumunda fetch ile dene
            fetch(img.src)
                .then(r => r.blob())
                .then(blob => {
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.readAsDataURL(blob);
                })
                .catch(() => resolve(null));
        }
    });
}

// PDF İndirme Fonksiyonu
async function downloadPDF() {
    const btn = document.querySelector(".btn-download");
    const originalText = btn.innerHTML;
    btn.innerHTML = "<span>Hazırlanıyor...</span>";
    btn.disabled = true;

    // Görsellerin src'lerini geçici olarak base64 ile değiştir
    const imgIds = ["company-logo", "out-kase", "out-simza"];
    const originalSrcs = {};
    
    for (const id of imgIds) {
        const imgEl = document.getElementById(id);
        if (imgEl && imgEl.style.display !== "none") {
            try {
                const base64 = await getImageAsBase64(id);
                if (base64) {
                    originalSrcs[id] = imgEl.src;
                    imgEl.src = base64;
                }
            } catch(e) { }
        }
    }

    const element = document.getElementById("pdf-content");
    const musteriAdi = document.getElementById("input-1").value || "Musteri";
    const teklifNo = document.getElementById("input-4").value || "Teklif";
    const fileName = `YM - ${musteriAdi} - ${teklifNo}.pdf`;

    const opt = {
        margin:       0,
        filename:     fileName,
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, useCORS: false, allowTaint: true, logging: false },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    try {
        await html2pdf().set(opt).from(element).save();
    } catch(e) {
        alert("PDF oluşturulurken bir hata oluştu. Yazdır butonunu kullanarak PDF olarak kaydedebilirsiniz.");
    } finally {
        // Görsellerin orijinal src'lerine geri dön
        for (const [id, src] of Object.entries(originalSrcs)) {
            const imgEl = document.getElementById(id);
            if (imgEl) imgEl.src = src;
        }
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// ==========================================
// MOBİL ÖNİZLEME VE PAYLAŞMA İŞLEMLERİ
// ==========================================

function openMobilePreview() {
    const previewContainer = document.getElementById("preview-container");
    const fixedBar = document.getElementById("mobile-fixed-bar");
    if (previewContainer) {
        previewContainer.classList.add("mobile-active");
        previewContainer.scrollTop = 0;
    }
    if (fixedBar) fixedBar.style.display = "none";
}

function closeMobilePreview() {
    const previewContainer = document.getElementById("preview-container");
    const fixedBar = document.getElementById("mobile-fixed-bar");
    if (previewContainer) {
        previewContainer.classList.remove("mobile-active");
    }
    if (fixedBar) fixedBar.style.display = "block";
}

async function sharePDFMobile() {
    const btn = document.getElementById("btn-share-preview");
    const originalText = btn.innerHTML;
    btn.innerHTML = "<span>Hazırlanıyor...</span>";
    btn.disabled = true;

    // Görsellerin src'lerini geçici olarak base64 ile değiştir
    const imgIds = ["company-logo", "out-kase", "out-simza"];
    const originalSrcs = {};
    
    for (const id of imgIds) {
        const imgEl = document.getElementById(id);
        if (imgEl && imgEl.style.display !== "none") {
            try {
                const base64 = await getImageAsBase64(id);
                if (base64) {
                    originalSrcs[id] = imgEl.src;
                    imgEl.src = base64;
                }
            } catch(e) { }
        }
    }

    const element = document.getElementById("pdf-content");
    const musteriAdi = document.getElementById("input-1").value || "Musteri";
    const teklifNo = document.getElementById("input-4").value || "Teklif";
    const fileName = `YM - ${musteriAdi} - ${teklifNo}.pdf`;

    const opt = {
        margin:       0,
        filename:     fileName,
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, useCORS: false, allowTaint: true, logging: false },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    try {
        const worker = html2pdf().set(opt).from(element);
        const pdfBlob = await worker.output('blob');
        
        const file = new File([pdfBlob], fileName, { type: "application/pdf" });
        
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            await navigator.share({
                files: [file],
                title: 'Fiyat Teklifi',
                text: 'Müşteri teklif formu ektedir.'
            });
        } else {
            alert("Cihazınız bu tür dosya paylaşımını desteklemiyor. PDF İndir butonunu kullanabilirsiniz.");
        }
    } catch(e) {
        console.error(e);
        alert("PDF oluşturulurken veya paylaşılırken bir hata oluştu.");
    } finally {
        // Görsellerin orijinal src'lerine geri dön
        for (const [id, src] of Object.entries(originalSrcs)) {
            const imgEl = document.getElementById(id);
            if (imgEl) imgEl.src = src;
        }
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}
