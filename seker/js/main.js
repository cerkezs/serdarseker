/* ============================================
   ŞEKER KARDEŞLER — Interaction & Logic
   ============================================ */

// Year
if (document.getElementById('yr')) {
  document.getElementById('yr').textContent = new Date().getFullYear();
}

// Preloader Logic (Once per session)
const preloader = document.getElementById('preloader');
if (sessionStorage.getItem('seker_visited')) {
  if (preloader) preloader.style.display = 'none';
} else {
  window.addEventListener('load', () => {
    setTimeout(() => {
      if (preloader) preloader.classList.add('hidden');
      sessionStorage.setItem('seker_visited', 'true');
    }, 2000);
  });
}

// Header scroll
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  if (header) header.classList.toggle('scrolled', window.scrollY > 60);
});

// Mobile menu
const burger = document.getElementById('hamburger');
const nav = document.getElementById('nav');

if (burger && nav) {
  burger.addEventListener('click', (e) => {
    e.stopPropagation();
    burger.classList.toggle('is-active');
    nav.classList.toggle('open');
  });

  // Linklere tıklayınca kapat
  nav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      burger.classList.remove('is-active');
      nav.classList.remove('open');
    });
  });

  // Dışarı tıklayınca kapat
  window.addEventListener('click', (e) => {
    if (nav.classList.contains('open') && !nav.contains(e.target) && !burger.contains(e.target)) {
      burger.classList.remove('is-active');
      nav.classList.remove('open');
    }
  });
}

// Active Nav Link
const currentPath = window.location.pathname.split('/').pop() || 'index.html';
if (nav) {
  nav.querySelectorAll('a').forEach(link => {
    const linkPath = link.getAttribute('href');
    if (linkPath === currentPath) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

// Custom cursor
const dot = document.querySelector('.cursor-dot');
const ring = document.querySelector('.cursor-ring');
if (dot && ring) {
  let mx = 0, my = 0, rx = 0, ry = 0;
  window.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; dot.style.transform = `translate(${mx}px,${my}px) translate(-50%,-50%)`; });
  function cursorLoop() { rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18; ring.style.transform = `translate(${rx}px,${ry}px) translate(-50%,-50%)`; requestAnimationFrame(cursorLoop); }
  cursorLoop();
  document.querySelectorAll('a, button, .svc-card, .why-card, .contact-card').forEach(el => {
    el.addEventListener('mouseenter', () => ring.classList.add('hover'));
    el.addEventListener('mouseleave', () => ring.classList.remove('hover'));
  });
}

// Reveal on scroll (Staggered)
let staggerCounter = 0;
let staggerTimer = null;

const io = new IntersectionObserver((entries) => {
  entries.forEach(en => { 
    if (en.isIntersecting) { 
      en.target.style.transitionDelay = `${staggerCounter * 0.15}s`;
      en.target.classList.add('in'); 
      
      // Counter animation trigger
      const counterSpan = en.target.querySelector('.counter');
      if (counterSpan) animateCounter(counterSpan);

      io.unobserve(en.target); 
      
      staggerCounter++;
      clearTimeout(staggerTimer);
      staggerTimer = setTimeout(() => { staggerCounter = 0; }, 150);
    } 
  });
}, { threshold: 0.12 });

function animateCounter(el) {
  const target = +el.getAttribute('data-target');
  const duration = 2000;
  const start = 0;
  let startTime = null;

  function step(timestamp) {
    if (!startTime) startTime = timestamp;
    const progress = Math.min((timestamp - startTime) / duration, 1);
    el.textContent = Math.floor(progress * (target - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      el.textContent = target;
    }
  }
  window.requestAnimationFrame(step);
}

document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// WhatsApp Form Handler
function sendToWhatsApp(e) {
  e.preventDefault();
  const form = e.target;
  const name = form.querySelector('input[type="text"]').value;
  const phone = form.querySelector('input[type="tel"]').value;
  const email = form.querySelector('input[type="email"]').value;
  const msg = form.querySelector('textarea').value;
  
  const wpText = `*Yeni İletişim Formu Mesajı*%0A%0A*Ad Soyad:* ${name}%0A*Telefon:* ${phone}%0A*E-Posta:* ${email}%0A*Mesaj:* ${msg}`;
  const wpUrl = `https://wa.me/905442240303?text=${wpText}`;
  
  window.open(wpUrl, '_blank');
  form.reset();
}

// Bind to all contact forms
document.querySelectorAll('.contact-form').forEach(f => f.onsubmit = sendToWhatsApp);

// Image Zoom & Gallery Lightbox
const galleryTriggers = document.querySelectorAll('.gallery-trigger, .zoom-img');
if (galleryTriggers.length > 0) {
  let currentGalleryIndex = 0;
  const galleryImages = Array.from(galleryTriggers).map(img => ({
    src: img.src,
    alt: img.alt
  }));

  // Create Modal element if it doesn't exist
  let modal = document.getElementById('imgModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'imgModal';
    modal.className = 'img-modal';
    modal.innerHTML = `
      <span class="close-modal">&times;</span>
      <button class="modal-nav modal-prev" id="prevBtn"><i class="fa-solid fa-chevron-left"></i></button>
      <div class="modal-content-wrapper">
        <img class="modal-content" id="modalImg">
      </div>
      <button class="modal-nav modal-next" id="nextBtn"><i class="fa-solid fa-chevron-right"></i></button>
      <div id="caption"></div>
    `;
    document.body.appendChild(modal);
  }

  const modalImg = document.getElementById('modalImg');
  const captionText = document.getElementById('caption');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');

  const updateModalImage = (index) => {
    currentGalleryIndex = index;
    const imgData = galleryImages[index];
    modalImg.style.opacity = '0';
    setTimeout(() => {
      modalImg.src = imgData.src;
      captionText.innerHTML = imgData.alt;
      modalImg.style.opacity = '1';
    }, 200);
  };

  galleryTriggers.forEach((img, idx) => {
    img.addEventListener('click', () => {
      modal.style.display = 'flex';
      updateModalImage(idx);
    });
  });

  const nextImage = () => {
    let nextIdx = (currentGalleryIndex + 1) % galleryImages.length;
    updateModalImage(nextIdx);
  };

  const prevImage = () => {
    let prevIdx = (currentGalleryIndex - 1 + galleryImages.length) % galleryImages.length;
    updateModalImage(prevIdx);
  };

  if (nextBtn) nextBtn.onclick = (e) => { e.stopPropagation(); nextImage(); };
  if (prevBtn) prevBtn.onclick = (e) => { e.stopPropagation(); prevImage(); };

  const closeBtn = modal.querySelector('.close-modal');
  if (closeBtn) closeBtn.onclick = () => modal.style.display = 'none';
  
  modal.onclick = (e) => { if (e.target === modal || e.target.classList.contains('modal-content-wrapper')) modal.style.display = 'none'; };

  // Keyboard support
  window.addEventListener('keydown', (e) => {
    if (modal.style.display === 'flex') {
      if (e.key === 'ArrowRight') nextImage();
      if (e.key === 'ArrowLeft') prevImage();
      if (e.key === 'Escape') modal.style.display = 'none';
    }
  });
}
