// ========================================
// DINCEL REKLAM — INTERACTIVE ENGINE
// ========================================

// --- LENIS SMOOTH SCROLL ---
const lenis = new Lenis({
    duration: 1.2, 
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    orientation: 'vertical',
    smoothWheel: true,
});

function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

gsap.registerPlugin(ScrollTrigger);
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => { lenis.raf(time * 1000); });
gsap.ticker.lagSmoothing(0);

// --- FLASHLIGHT MOUSE TRACKING ---
document.addEventListener('mousemove', (e) => {
    // Update CSS variables for the mask-image center
    document.documentElement.style.setProperty('--mouse-x', e.clientX + 'px');
    document.documentElement.style.setProperty('--mouse-y', e.clientY + 'px');
});

// Expand flashlight on click/mousedown
document.addEventListener('mousedown', () => {
    document.documentElement.style.setProperty('--mask-size', '450px');
});
document.addEventListener('mouseup', () => {
    document.documentElement.style.setProperty('--mask-size', '300px');
});


// --- TEXT SPLITTING (KINETIC TYPOGRAPHY) ---
// Simple custom text splitter to wrap characters in spans
const splitElements = document.querySelectorAll('[data-split]');
splitElements.forEach(el => {
    const text = el.innerText;
    el.innerHTML = '';
    // Split by words first to keep spaces
    const words = text.split(' ');
    words.forEach((word, wordIndex) => {
        const wordSpan = document.createElement('span');
        wordSpan.style.display = 'inline-block';
        wordSpan.style.whiteSpace = 'nowrap';
        
        // Split word into chars
        const chars = word.split('');
        chars.forEach(char => {
            const charSpan = document.createElement('span');
            charSpan.className = 'kinetic-char';
            charSpan.innerText = char;
            wordSpan.appendChild(charSpan);
        });
        
        el.appendChild(wordSpan);
        
        // Add a space after the word (except the last one)
        if (wordIndex < words.length - 1) {
            const spaceSpan = document.createElement('span');
            spaceSpan.innerHTML = '&nbsp;';
            el.appendChild(spaceSpan);
        }
    });
});

// --- GSAP KINETIC ANIMATIONS ---
const scenes = document.querySelectorAll('.kinetic-scene');

scenes.forEach((scene, index) => {
    const textContainer = scene.querySelector('.kinetic-text-container');
    const chars = scene.querySelectorAll('.kinetic-char');
    const sub = scene.querySelector('.kinetic-sub');
    
    // Set initial state for characters (scattered randomly in 3D space)
    gsap.set(chars, {
        opacity: 0,
        x: () => gsap.utils.random(-800, 800),
        y: () => gsap.utils.random(-800, 800),
        z: () => gsap.utils.random(-1000, 500),
        rotationX: () => gsap.utils.random(-180, 180),
        rotationY: () => gsap.utils.random(-180, 180),
        rotationZ: () => gsap.utils.random(-90, 90)
    });
    
    const tl = gsap.timeline({
        scrollTrigger: {
            trigger: scene,
            start: "top 60%", 
            end: "bottom 40%", 
            scrub: 1.5, // Smooth scrubbing
            // pin text while animating
            onEnter: () => gsap.to(textContainer, { opacity: 1, duration: 0.5 }),
            onLeave: () => gsap.to(textContainer, { opacity: 0, duration: 0.5 }),
            onEnterBack: () => gsap.to(textContainer, { opacity: 1, duration: 0.5 }),
            onLeaveBack: () => gsap.to(textContainer, { opacity: 0, duration: 0.5 })
        }
    });

    // Assemble the characters
    tl.to(chars, {
        opacity: 1,
        x: 0,
        y: 0,
        z: 0,
        rotationX: 0,
        rotationY: 0,
        rotationZ: 0,
        duration: 2,
        stagger: {
            each: 0.05,
            from: "random"
        },
        ease: "power4.out"
    }, 0); // Start at beginning of timeline

    // Fade in the subtitle after characters assemble
    if(sub) {
        tl.to(sub, {
            opacity: 1,
            y: -10,
            duration: 1,
            ease: "power2.out"
        }, "-=0.5"); // Start slightly before chars finish
    }

    // Disassemble (explode) as we continue scrolling down past the center
    tl.to(chars, {
        opacity: 0,
        x: () => gsap.utils.random(-800, 800),
        y: () => gsap.utils.random(-500, -1000), // fly upwards/outwards
        z: () => gsap.utils.random(-1000, 1000),
        rotationX: () => gsap.utils.random(-180, 180),
        rotationY: () => gsap.utils.random(-180, 180),
        rotationZ: () => gsap.utils.random(-90, 90),
        duration: 2,
        ease: "power3.in"
    }, "+=1"); // Hold for a bit, then explode
    
    if(sub) {
        tl.to(sub, {
            opacity: 0,
            y: -30,
            duration: 1
        }, "<"); // Sync with explosion
    }
});

// --- PRELOADER EXIT ---
window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    if(preloader) {
        gsap.to(preloader, {
            delay: 0.8, opacity: 0, duration: 1, ease: 'power2.inOut',
            onComplete: () => preloader.style.display = 'none'
        });
    }
});

// --- NAVBAR SCROLL STATE ---
const nav = document.getElementById('nav');
if (nav) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 80) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
    });
}

// --- MOBILE MENU LOGIC ---
const mobileBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
if(mobileBtn && mobileMenu) {
    mobileBtn.addEventListener('click', () => {
        mobileBtn.classList.toggle('open');
        mobileMenu.classList.toggle('active');
        // Prevent background scrolling when menu is open
        if (mobileMenu.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
            if (typeof lenis !== 'undefined') lenis.stop();
        } else {
            document.body.style.overflow = '';
            if (typeof lenis !== 'undefined') lenis.start();
        }
    });
}

// --- SCROLL REVEAL ANIMATIONS (Intersection Observer) ---
const revealElements = document.querySelectorAll('.reveal-up');
const revealOptions = {
    threshold: 0.15,
    rootMargin: "0px 0px -50px 0px"
};

const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
    });
}, revealOptions);

revealElements.forEach(el => {
    revealObserver.observe(el);
});

// --- PORTFOLIO FILTER LOGIC ---
const filterBtns = document.querySelectorAll('.filter-btn');
const portfolioCards = document.querySelectorAll('.portfolio-card');

if (filterBtns.length > 0 && portfolioCards.length > 0) {
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active to clicked
            btn.classList.add('active');

            const filterValue = btn.getAttribute('data-filter');

            portfolioCards.forEach(card => {
                const category = card.getAttribute('data-category');
                
                if (filterValue === 'all' || filterValue === category) {
                    card.style.display = 'flex';
                    // Quick fade in
                    gsap.fromTo(card, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4 });
                } else {
                    card.style.display = 'none';
                }
            });
            
            // Refresh scroll trigger to account for new heights
            setTimeout(() => {
                ScrollTrigger.refresh();
            }, 500);
        });
    });

    // --- CLICK CARD TO UPDATE BEFORE/AFTER SLIDER ---
    const baSection = document.querySelector('.before-after-section');
    const baAfterImg = document.querySelector('.ba-after');
    const baBeforeImg = document.querySelector('.ba-before');

    if (baSection && baAfterImg && baBeforeImg) {
        portfolioCards.forEach(card => {
            card.addEventListener('click', () => {
                const cardImgSrc = card.querySelector('.portfolio-card-img').getAttribute('src');
                
                // Update images in slider
                baAfterImg.src = cardImgSrc;
                baBeforeImg.src = cardImgSrc;

                // Reset slider position to 50%
                const baBeforeWrapper = document.querySelector('.ba-before-wrapper');
                const baSliderBtn = document.querySelector('.ba-slider');
                if (baBeforeWrapper && baSliderBtn) {
                    baBeforeWrapper.style.width = '50%';
                    baSliderBtn.style.left = '50%';
                }
                
                // Smooth scroll to the before/after section
                const offsetTop = baSection.getBoundingClientRect().top + window.scrollY - 100;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            });
        });
    }
}

// --- PAGE TRANSITIONS ---
const pageTransition = document.getElementById('page-transition');
if (pageTransition) {
    document.querySelectorAll('a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetUrl = this.getAttribute('href');
            
            // Allow default behavior for external links, anchor links, phone numbers, emails, and target="_blank"
            if (!targetUrl || 
                targetUrl.startsWith('http') || 
                targetUrl.startsWith('#') || 
                targetUrl.startsWith('tel:') || 
                targetUrl.startsWith('mailto:') || 
                this.getAttribute('target') === '_blank') {
                return;
            }

            // Internal link -> Intercept and animate
            e.preventDefault();
            pageTransition.classList.add('active');
            
            setTimeout(() => {
                window.location.href = targetUrl;
            }, 400); // matches CSS transition duration
        });
    });
    
    // Page load reveal (if navigating via back/forward buttons, ensure overlay fades out)
    window.addEventListener('pageshow', (event) => {
        if (event.persisted) {
            pageTransition.classList.remove('active');
        }
    });
}

// --- BEFORE / AFTER SLIDER LOGIC ---
const baContainer = document.querySelector('.ba-container');
if (baContainer) {
    const baBeforeWrapper = baContainer.querySelector('.ba-before-wrapper');
    const baSlider = baContainer.querySelector('.ba-slider');
    let isDragging = false;

    const moveSlider = (e) => {
        if (!isDragging) return;
        
        const rect = baContainer.getBoundingClientRect();
        let x = (e.type.includes('mouse') ? e.clientX : e.touches[0].clientX) - rect.left;
        
        // Boundaries
        if (x < 0) x = 0;
        if (x > rect.width) x = rect.width;
        
        let percentage = (x / rect.width) * 100;
        
        baBeforeWrapper.style.width = `${percentage}%`;
        baSlider.style.left = `${percentage}%`;
    };

    baContainer.addEventListener('mousedown', () => isDragging = true);
    baContainer.addEventListener('touchstart', () => isDragging = true);
    
    window.addEventListener('mouseup', () => isDragging = false);
    window.addEventListener('touchend', () => isDragging = false);
    
    window.addEventListener('mousemove', moveSlider);
    window.addEventListener('touchmove', moveSlider);
}

// --- FAQ ACCORDION LOGIC ---
const faqQuestions = document.querySelectorAll('.faq-question');
faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
        const activeItem = document.querySelector('.faq-question.active');
        
        // Close currently active item if it's not the one clicked
        if (activeItem && activeItem !== question) {
            activeItem.classList.remove('active');
            activeItem.nextElementSibling.style.maxHeight = null;
        }

        // Toggle clicked item
        question.classList.toggle('active');
        const answer = question.nextElementSibling;
        
        if (question.classList.contains('active')) {
            answer.style.maxHeight = answer.scrollHeight + "px";
        } else {
            answer.style.maxHeight = null;
        }
        
        // Refresh scroll trigger to account for new heights
        setTimeout(() => {
            ScrollTrigger.refresh();
        }, 450);
    });
});

// Initialize menu and active links on load (Header is now loaded via PHP)
document.addEventListener("DOMContentLoaded", () => {
    initMobileMenu();
    highlightActiveLink();
});

function initMobileMenu() {
    const mobileMenuBtn = document.getElementById("mobile-menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");
    if (mobileMenuBtn && mobileMenu) {
        // Remove old listeners to prevent duplicates if called multiple times
        const newBtn = mobileMenuBtn.cloneNode(true);
        mobileMenuBtn.parentNode.replaceChild(newBtn, mobileMenuBtn);
        
        newBtn.addEventListener("click", () => {
            newBtn.classList.toggle("active");
            mobileMenu.classList.toggle("active");
            document.body.style.overflow = mobileMenu.classList.contains("active") ? "hidden" : "";
        });
    }
}


function highlightActiveLink() {
    const currentPath = window.location.pathname.split("/").pop() || "index.html";
    const navLinks = document.querySelectorAll(".nav-links .nav-link, .mobile-menu-inner .mobile-link");
    
    navLinks.forEach(link => {
        link.classList.remove("active");
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });
}

