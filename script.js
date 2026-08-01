// Initialize Current Year in Footer
document.getElementById('year').textContent = new Date().getFullYear();

// Navbar Scroll Effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile Menu Toggle (Advanced)
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const menuOverlay = document.getElementById('menuOverlay');

function openMenu() {
    navLinks.classList.add('active');
    menuOverlay.classList.add('active');
    hamburger.classList.add('menu-open');
    document.body.classList.add('menu-open');
    const icon = hamburger.querySelector('i');
    icon.classList.remove('fa-bars');
    icon.classList.add('fa-times');
}

function closeMenu() {
    navLinks.classList.remove('active');
    menuOverlay.classList.remove('active');
    hamburger.classList.remove('menu-open');
    document.body.classList.remove('menu-open');
    const icon = hamburger.querySelector('i');
    icon.classList.remove('fa-times');
    icon.classList.add('fa-bars');
}

hamburger.addEventListener('click', () => {
    if (navLinks.classList.contains('active')) {
        closeMenu();
    } else {
        openMenu();
    }
});

// Close on overlay click
menuOverlay.addEventListener('click', closeMenu);

// Close mobile menu on link click
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', closeMenu);
});

// Scroll Reveal Animation (Intersection Observer)
const revealElements = document.querySelectorAll('.reveal');

const revealOptions = {
    threshold: 0.15,
    rootMargin: "0px 0px -50px 0px"
};

const revealOnScroll = new IntersectionObserver(function(entries, observer) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            return;
        }
        
        // Add active class to trigger CSS transitions
        entry.target.classList.add('active');
        
        // Optional: stop observing once revealed
        // observer.unobserve(entry.target);
    });
}, revealOptions);

revealElements.forEach(el => {
    revealOnScroll.observe(el);
});

// Form Submission with WhatsApp Redirection
document.getElementById('contactForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    const originalText = btn.innerHTML;
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Opening WhatsApp...';
    btn.disabled = true;
    
    // WhatsApp Number (917007706755)
    const phoneNumber = "917007706755";
    
    // Formatting the WhatsApp Message with bold styling
    const waMessage = `*New Portfolio Inquiry*\n\n` +
                      `👤 *Name:* ${name}\n` +
                      `📧 *Email:* ${email}\n` +
                      `💬 *Message:* ${message}`;
                      
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(waMessage)}`;
    
    setTimeout(() => {
        // Open WhatsApp in a new tab
        window.open(whatsappUrl, '_blank');
        
        btn.innerHTML = '<i class="fas fa-check"></i> Connected!';
        btn.style.background = '#10b981'; // Green color for success
        e.target.reset();
        
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
            btn.disabled = false;
        }, 3000);
    }, 1000);
});

// --- Dynamic Typewriter Animation ---
const words = ["Developer", "Designer", "Problem Solver", "Creator"];
let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;
const dynamicText = document.getElementById('dynamic-text');

function typeEffect() {
    const currentWord = words[wordIndex];
    if (isDeleting) {
        dynamicText.textContent = currentWord.substring(0, charIndex - 1);
        charIndex--;
    } else {
        dynamicText.textContent = currentWord.substring(0, charIndex + 1);
        charIndex++;
    }

    let typeSpeed = isDeleting ? 75 : 150;

    if (!isDeleting && charIndex === currentWord.length) {
        typeSpeed = 2000; // Pause at full word
        isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        wordIndex = (wordIndex + 1) % words.length;
        typeSpeed = 800; // Pause before typing next word
    }

    setTimeout(typeEffect, typeSpeed);
}

// Start typewriter effect if the element exists
if (dynamicText) {
    typeEffect();
}

// --- 1. Custom Glowing Cursor Follower ---
const cursorDot = document.getElementById('cursorDot');
const cursorOutline = document.getElementById('cursorOutline');

if (cursorDot && cursorOutline && window.innerWidth > 992) {
    let mouseX = 0, mouseY = 0;
    let outlineX = 0, outlineY = 0;

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        cursorDot.style.left = `${mouseX}px`;
        cursorDot.style.top = `${mouseY}px`;
    });

    function animateCursor() {
        outlineX += (mouseX - outlineX) * 0.15;
        outlineY += (mouseY - outlineY) * 0.15;
        cursorOutline.style.left = `${outlineX}px`;
        cursorOutline.style.top = `${outlineY}px`;
        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    const hoverTargets = document.querySelectorAll('a, button, .btn, .glass-card, .skill-card-v2, .project-card, .skill-filter-btn');
    hoverTargets.forEach(target => {
        target.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
        target.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
    });
}

// --- 2. 3D Tilt Effect on Cards ---
const tiltCards = document.querySelectorAll('[data-tilt]');
tiltCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = ((y - centerY) / centerY) * -8;
        const rotateY = ((x - centerX) / centerX) * 8;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    });
});

// --- 3. Animated Statistics Counter ---
const counters = document.querySelectorAll('.counter');
let countersTriggered = false;

const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !countersTriggered) {
            countersTriggered = true;
            counters.forEach(counter => {
                const target = +counter.getAttribute('data-target');
                const duration = 2000;
                const increment = target / (duration / 16);
                let current = 0;

                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        counter.textContent = Math.ceil(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target;
                    }
                };
                updateCounter();
            });
        }
    });
}, { threshold: 0.3 });

const statsSection = document.getElementById('stats');
if (statsSection) {
    statsObserver.observe(statsSection);
}

// --- 4. Interactive Skill Category Filters ---
const filterBtns = document.querySelectorAll('.skill-filter-btn');
const skillCards = document.querySelectorAll('.skill-card-v2');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filterValue = btn.getAttribute('data-filter');

        skillCards.forEach(card => {
            const category = card.getAttribute('data-category');
            if (filterValue === 'all' || category === filterValue) {
                card.classList.remove('hidden');
                card.style.animation = 'fadeInUp 0.4s ease forwards';
            } else {
                card.classList.add('hidden');
            }
        });
    });
});

// --- 5. Toast Notification System & Copy-to-Clipboard ---
const toastContainer = document.getElementById('toastContainer');

function showToast(message, iconClass = 'fa-check-circle') {
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fas ${iconClass} toast-icon"></i> <span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

// Attach Toast to email & phone links
document.querySelectorAll('a[href^="mailto:"], a[href^="tel:"]').forEach(link => {
    link.addEventListener('click', (e) => {
        const text = link.textContent.trim();
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showToast(`Copied to clipboard: ${text}`, 'fa-copy');
            });
        }
    });
});

// --- 6. Interactive Project Modal Drawer ---
const projectsData = {
    phishing: {
        title: "Phishing URL Detection System",
        category: "Cybersecurity & Machine Learning",
        banner: '<i class="fas fa-shield-alt" style="color: #00d4ff;"></i>',
        desc: "An intelligent security system built using Flask and Machine Learning algorithms that analyzes URLs in real-time to protect users against malicious phishing attempts with an impressive 89.2% accuracy rate.",
        highlights: [
            "Real-time heuristic & ML URL feature extraction.",
            "Ensemble Classification algorithm trained on 50,000+ verified URLs.",
            "Clean Web Interface with threat scoring visualization.",
            "REST API endpoint for third-party integration."
        ],
        tags: ["Python", "Flask", "Scikit-Learn", "Machine Learning", "JavaScript", "CSS3"],
        liveLink: "Phishing URL Detection System/index.html"
    },
    finance: {
        title: "Personal Finance & Expense Tracker",
        category: "FinTech & Data Analytics",
        banner: '<i class="fas fa-chart-line" style="color: #ec4899;"></i>',
        desc: "A feature-rich financial management dashboard empowering users to monitor budgets, categorize expenses, track income streams, and visualize spending habits through interactive Chart.js analytics.",
        highlights: [
            "Dynamic budget breakdown & category management.",
            "Real-time expense charting and monthly financial reports.",
            "Local storage data persistence with instant export capabilities.",
            "Responsive glassmorphic UI designed for mobile and desktop."
        ],
        tags: ["JavaScript", "Chart.js", "HTML5", "CSS3", "Local Storage"],
        liveLink: "#"
    },
    weather: {
        title: "Global Weather Forecast App",
        category: "Web Application & API",
        banner: '<i class="fas fa-cloud-sun" style="color: #10b981;"></i>',
        desc: "An asynchronous weather application fetching live meteorological data from OpenWeatherMap API to display temperature, humidity, wind velocity, UV index, and 5-day weather forecasts for cities worldwide.",
        highlights: [
            "Automatic geolocation detection & city search auto-complete.",
            "Dynamic background transitions corresponding to live weather conditions.",
            "Detailed hourly forecast breakdown & environmental metrics.",
            "Optimized asynchronous JavaScript API fetching with fallback error handling."
        ],
        tags: ["Async JavaScript", "OpenWeatherMap API", "HTML5", "CSS3", "Flexbox"],
        liveLink: "#"
    }
};

const projectModal = document.getElementById('projectModal');
const modalCloseBtn = document.getElementById('modalCloseBtn');
const modalBackdrop = document.getElementById('modalBackdrop');

function openProjectModal(projectId) {
    const data = projectsData[projectId];
    if (!data || !projectModal) return;

    document.getElementById('modalTitle').textContent = data.title;
    document.getElementById('modalCategory').textContent = data.category;
    document.getElementById('modalBanner').innerHTML = data.banner;
    document.getElementById('modalDesc').textContent = data.desc;

    const highlightsList = document.getElementById('modalHighlights');
    highlightsList.innerHTML = data.highlights.map(h => `<li>${h}</li>`).join('');

    const tagsBox = document.getElementById('modalTags');
    tagsBox.innerHTML = data.tags.map(t => `<span>${t}</span>`).join('');

    document.getElementById('modalLiveLink').href = data.liveLink;

    projectModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeProjectModal() {
    if (!projectModal) return;
    projectModal.classList.remove('active');
    document.body.style.overflow = '';
}

document.querySelectorAll('.view-project-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const projId = btn.getAttribute('data-project');
        openProjectModal(projId);
    });
});

if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeProjectModal);
if (modalBackdrop) modalBackdrop.addEventListener('click', closeProjectModal);

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && projectModal && projectModal.classList.contains('active')) {
        closeProjectModal();
    }
});

// --- 7. Scroll Progress Circle & Back To Top ---
const scrollProgressWrap = document.getElementById('scrollProgressWrap');
const progressPath = document.querySelector('.scroll-progress-svg path');

if (scrollProgressWrap && progressPath) {
    const pathLength = progressPath.getTotalLength();
    progressPath.style.transition = progressPath.style.WebkitTransition = 'none';
    progressPath.style.strokeDasharray = `${pathLength} ${pathLength}`;
    progressPath.style.strokeDashoffset = pathLength;
    progressPath.getBoundingClientRect();
    progressPath.style.transition = progressPath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';

    const updateScrollProgress = () => {
        const scroll = window.scrollY;
        const height = document.documentElement.scrollHeight - window.innerHeight;
        const progress = pathLength - (scroll * pathLength / height);
        progressPath.style.strokeDashoffset = progress;

        if (scroll > 300) {
            scrollProgressWrap.classList.add('active-progress');
        } else {
            scrollProgressWrap.classList.remove('active-progress');
        }
    };

    window.addEventListener('scroll', updateScrollProgress);

    scrollProgressWrap.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

