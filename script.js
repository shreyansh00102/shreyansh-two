// ==========================================================================
// SHREYANSH YADAV PORTFOLIO INTERACTIVITY SCRIPT
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Footer Year
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // 2. Navbar Scroll Effect & Active Link Highlight
    const navbar = document.getElementById('navbar');
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Active link on scroll
        let currentSection = '';
        sections.forEach(sec => {
            const secTop = sec.offsetTop - 120;
            const secHeight = sec.offsetHeight;
            if (window.scrollY >= secTop && window.scrollY < secTop + secHeight) {
                currentSection = sec.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    });

    // 3. Mobile Navigation Menu Toggle
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const navLinksContainer = document.querySelector('.nav-links');
    const menuOverlay = document.getElementById('menuOverlay');

    function toggleMenu() {
        navLinksContainer.classList.toggle('active');
        menuOverlay.classList.toggle('active');
        const icon = hamburgerBtn.querySelector('i');
        if (navLinksContainer.classList.contains('active')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    }

    if (hamburgerBtn) hamburgerBtn.addEventListener('click', toggleMenu);
    if (menuOverlay) menuOverlay.addEventListener('click', toggleMenu);

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navLinksContainer.classList.contains('active')) {
                toggleMenu();
            }
        });
    });

    // 4. Custom Glowing Cursor
    const cursorDot = document.getElementById('cursorDot');
    const cursorOutline = document.getElementById('cursorOutline');

    if (cursorDot && cursorOutline && window.innerWidth > 992) {
        window.addEventListener('mousemove', (e) => {
            const posX = e.clientX;
            const posY = e.clientY;

            cursorDot.style.left = `${posX}px`;
            cursorDot.style.top = `${posY}px`;

            cursorOutline.animate({
                left: `${posX}px`,
                top: `${posY}px`
            }, { duration: 250, fill: "forwards" });
        });
    }

    // 5. Scroll Reveal Animation
    const revealElements = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.12 });

    revealElements.forEach(el => revealObserver.observe(el));

    // 6. Interactive Terminal CLI
    const terminalBody = document.getElementById('terminalBody');
    
    window.runCLICommand = function(command) {
        if (!terminalBody) return;

        let outputHtml = '';
        if (command === 'about') {
            outputHtml = `
                <div class="terminal-line"><span class="t-prompt">shreyansh@portfolio:~$</span> <span class="t-cmd">cat about.txt</span></div>
                <div class="terminal-line t-output">Shreyansh Yadav is a Full Stack Software Developer pursuing B.Tech CS at KNIPSS Sultanpur, UP. Passionate about MERN stack, clean architecture, and modern UX design.</div>
            `;
        } else if (command === 'contact') {
            outputHtml = `
                <div class="terminal-line"><span class="t-prompt">shreyansh@portfolio:~$</span> <span class="t-cmd">curl contact_info</span></div>
                <div class="terminal-line t-output">Email: shreyansh00102@gmail.com | Phone: +91 70077 06755 | Location: Sultanpur, UP</div>
            `;
        } else if (command === 'status') {
            outputHtml = `
                <div class="terminal-line"><span class="t-prompt">shreyansh@portfolio:~$</span> <span class="t-cmd">git status</span></div>
                <div class="terminal-line t-output"><span class="t-green">On branch main. Your portfolio is up to date and ready for new projects!</span></div>
            `;
        } else if (command === 'clear') {
            terminalBody.innerHTML = `
                <div class="terminal-line"><span class="t-prompt">shreyansh@portfolio:~$</span> <span class="t-accent">Terminal cleared. Type commands or click chips below:</span></div>
            `;
            return;
        }

        terminalBody.innerHTML += outputHtml;
        terminalBody.scrollTop = terminalBody.scrollHeight;
    };

    // 7. Skills Filter
    const filterBtns = document.querySelectorAll('.filter-btn');
    const skillCards = document.querySelectorAll('.skill-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');

            skillCards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-category') === filter) {
                    card.style.display = 'flex';
                    setTimeout(() => card.style.opacity = '1', 50);
                } else {
                    card.style.opacity = '0';
                    setTimeout(() => card.style.display = 'none', 300);
                }
            });
        });
    });

    // 8. Interactive Project Modal Specifications
    const projectModal = document.getElementById('projectModal');
    const modalBackdrop = document.getElementById('modalBackdrop');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const modalCloseBtn2 = document.getElementById('modalCloseBtn2');
    const viewSpecBtns = document.querySelectorAll('.view-spec-btn');

    const projectData = {
        phishing: {
            title: "Phishing URL Detection System",
            category: "Cybersecurity & Machine Learning",
            desc: "A machine learning solution developed in Python & Flask that extracts lexical and topological features from domain names to identify phishing threats in real time.",
            highlights: [
                "Achieved 89.2% model classification accuracy",
                "Built custom Flask REST API endpoint for URL verification",
                "Integrated interactive web dashboard with feature analysis breakdown"
            ]
        },
        finance: {
            title: "Smart Finance Tracker",
            category: "Web Application & Analytics",
            desc: "An intuitive web application for managing personal budgets, tracking daily expenses, and generating dynamic category visualizations using Chart.js.",
            highlights: [
                "Real-time expense calculation and budget threshold alerts",
                "Interactive donut & line charts for monthly cashflow",
                "Client-side persistent storage with LocalStorage API"
            ]
        },
        weather: {
            title: "Real-Time Weather App",
            category: "Frontend Web Application",
            desc: "A responsive weather widget application that fetches live meteorological data from OpenWeather APIs, displaying temperature, humidity, wind, and forecast conditions.",
            highlights: [
                "Asynchronous JS fetch architecture with automatic error recovery",
                "Geolocation support for instant local forecast retrieval",
                "Dynamic background themes reflecting live weather conditions"
            ]
        }
    };

    function openModal(projectId) {
        const data = projectData[projectId];
        if (!data) return;

        document.getElementById('modalTitle').textContent = data.title;
        document.getElementById('modalCategory').textContent = data.category;
        document.getElementById('modalDesc').textContent = data.desc;

        const highlightsContainer = document.getElementById('modalHighlights');
        highlightsContainer.innerHTML = data.highlights.map(h => `<li>${h}</li>`).join('');

        projectModal.classList.add('active');
    }

    function closeModal() {
        if (projectModal) projectModal.classList.remove('active');
    }

    viewSpecBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const pId = btn.getAttribute('data-project');
            openModal(pId);
        });
    });

    if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
    if (modalCloseBtn2) modalCloseBtn2.addEventListener('click', closeModal);
    if (modalBackdrop) modalBackdrop.addEventListener('click', closeModal);

    // 9. Toast Notification Handler
    window.showToast = function(message) {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `<i class="fas fa-info-circle" style="color: var(--accent-cyan);"></i> ${message}`;

        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    };

    // 10. Contact Form WhatsApp Submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = contactForm.querySelector('button');
            const originalContent = btn.innerHTML;

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;

            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Preparing WhatsApp...';
            btn.disabled = true;

            const phoneNumber = "917007706755";
            const waText = `*Portfolio Contact Inquiry*\n\n` +
                           `👤 *Name:* ${name}\n` +
                           `📧 *Email:* ${email}\n` +
                           `💬 *Message:* ${message}`;

            const waUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(waText)}`;

            setTimeout(() => {
                window.open(waUrl, '_blank');
                btn.innerHTML = '<i class="fas fa-check"></i> Redirected!';
                showToast("Opening WhatsApp with your message details...");
                contactForm.reset();

                setTimeout(() => {
                    btn.innerHTML = originalContent;
                    btn.disabled = false;
                }, 3000);
            }, 800);
        });
    }

    // 11. Quick Stat Counters
    const statElements = document.querySelectorAll('.quick-stat-num');
    let counted = false;

    const countObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !counted) {
                counted = true;
                statElements.forEach(el => {
                    const target = parseInt(el.getAttribute('data-target'));
                    let current = 0;
                    const increment = Math.ceil(target / 40);
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= target) {
                            current = target;
                            clearInterval(timer);
                        }
                        const span = el.querySelector('span')?.outerHTML || '';
                        el.innerHTML = `${current}${span}`;
                    }, 40);
                });
            }
        });
    }, { threshold: 0.5 });

    statElements.forEach(el => countObserver.observe(el));

    // 12. Back To Top Scroll Progress
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollTopBtn.classList.add('active');
            } else {
                scrollTopBtn.classList.remove('active');
            }
        });

        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // 13. Dynamic Particle Field Canvas
    const canvas = document.getElementById('particle-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        const particles = [];
        const particleCount = Math.min(Math.floor(width / 25), 45);

        class Particle {
            constructor() {
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.radius = Math.random() * 1.8 + 0.5;
                this.vx = (Math.random() - 0.5) * 0.4;
                this.vy = (Math.random() - 0.5) * 0.4;
                this.alpha = Math.random() * 0.5 + 0.2;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                if (this.x < 0 || this.x > width) this.vx *= -1;
                if (this.y < 0 || this.y > height) this.vy *= -1;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(139, 92, 246, ${this.alpha})`;
                ctx.fill();
            }
        }

        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function animateParticles() {
            ctx.clearRect(0, 0, width, height);

            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();

                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 110) {
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(6, 182, 212, ${0.15 - dist / 1100})`;
                        ctx.lineWidth = 0.6;
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animateParticles);
        }

        animateParticles();
    }
});
