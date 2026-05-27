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
