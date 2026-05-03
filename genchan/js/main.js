/* ============================================
   GENÇHAN NAKLİYAT — Interaction & 3D Layer
   ============================================ */

// Year
document.getElementById('yr').textContent = new Date().getFullYear();

// Preloader Logic (Once per session)
const preloader = document.getElementById('preloader');
if (sessionStorage.getItem('genchan_visited')) {
  preloader.style.display = 'none';
} else {
  window.addEventListener('load', () => {
    setTimeout(() => {
      preloader.classList.add('hidden');
      sessionStorage.setItem('genchan_visited', 'true');
    }, 1200);
  });
}

// Header scroll
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 60);
});

// Mobile menu
const burger = document.getElementById('hamburger');
const nav = document.getElementById('nav');
burger.addEventListener('click', () => nav.classList.toggle('open'));
nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => nav.classList.remove('open')));

// Active Nav Link
const currentPath = window.location.pathname.split('/').pop() || 'index.html';
nav.querySelectorAll('a').forEach(link => {
  const linkPath = link.getAttribute('href');
  if (linkPath === currentPath) {
    link.classList.add('active');
  } else {
    link.classList.remove('active');
  }
});

// Custom cursor
const dot = document.querySelector('.cursor-dot');
const ring = document.querySelector('.cursor-ring');
let mx = 0, my = 0, rx = 0, ry = 0;
window.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; dot.style.transform = `translate(${mx}px,${my}px) translate(-50%,-50%)`; });
function loop() { rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18; ring.style.transform = `translate(${rx}px,${ry}px) translate(-50%,-50%)`; requestAnimationFrame(loop); }
loop();
document.querySelectorAll('a, button, .svc-card, .why-card, .contact-card').forEach(el => {
  el.addEventListener('mouseenter', () => ring.classList.add('hover'));
  el.addEventListener('mouseleave', () => ring.classList.remove('hover'));
});

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
  const wpUrl = `https://wa.me/905521495001?text=${wpText}`;
  
  window.open(wpUrl, '_blank');
  form.reset();
}

// Bind to all contact forms
document.querySelectorAll('.contact-form').forEach(f => f.onsubmit = sendToWhatsApp);

// FAQ Accordion
// ... (previous logic if any, but we moved to CSS only)
