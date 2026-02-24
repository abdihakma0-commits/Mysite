// ========================================
// Premium Portfolio JavaScript - Hakimu
// Loading Screen, Cursor Effects, Animations
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initLoadingScreen();
    initGlowCursor();
    initRevealAnimations();
    initExpandableCards();
    initTextSwitch();
    initHoverEffects();
});

// ===== Loading Screen =====
function initLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    const welcomeButton = document.getElementById('welcome-button');
    const mainContent = document.getElementById('main-content');
    const progressBar = document.getElementById('progress-bar');
    const percentage = document.getElementById('percentage');
    
    let progress = 0;
    
    const interval = setInterval(() => {
        progress += 1;
        progressBar.style.width = progress + '%';
        percentage.textContent = progress + '%';
        
        if (progress >= 100) {
            clearInterval(interval);
            
            setTimeout(() => {
                loadingScreen.style.opacity = '0';
                setTimeout(() => {
                    loadingScreen.classList.add('hidden');
                    welcomeButton.classList.remove('hidden');
                }, 500);
            }, 500);
        }
    }, 30);
    
    // Welcome button click
    const welcomeBtn = document.querySelector('.welcome-btn');
    welcomeBtn.addEventListener('click', () => {
        welcomeButton.style.opacity = '0';
        setTimeout(() => {
            welcomeButton.classList.add('hidden');
            mainContent.classList.remove('hidden');
            // Trigger initial animations
            initSectionTitles();
        }, 500);
    });
}

// ===== Glow Cursor =====
function initGlowCursor() {
    const cursorGlow = document.getElementById('cursor-glow');
    const cursorDot = document.getElementById('cursor-dot');
    
    document.addEventListener('mousemove', (e) => {
        const x = e.clientX;
        const y = e.clientY;
        
        cursorGlow.style.left = x + 'px';
        cursorGlow.style.top = y + 'px';
        cursorDot.style.left = x + 'px';
        cursorDot.style.top = y + 'px';
    });
    
    // Scale cursor on hoverable elements
    const hoverables = document.querySelectorAll('a, button, .project-card, .expandable-card, .timeline-node-wrapper');
    
    hoverables.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursorGlow.style.width = '400px';
            cursorGlow.style.height = '400px';
            cursorDot.style.width = '12px';
            cursorDot.style.height = '12px';
        });
        
        el.addEventListener('mouseleave', () => {
            cursorGlow.style.width = '300px';
            cursorGlow.style.height = '300px';
            cursorDot.style.width = '8px';
            cursorDot.style.height = '8px';
        });
    });
}

// ===== Scroll Reveal Animations =====
function initRevealAnimations() {
    const reveals = document.querySelectorAll('.reveal, .section-title, .project-card, .expandable-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px'
    });
    
    reveals.forEach(el => observer.observe(el));
}

// ===== Section Titles Animation =====
function initSectionTitles() {
    const titles = document.querySelectorAll('.section-title');
    titles.forEach((title, index) => {
        setTimeout(() => {
            title.classList.add('visible');
        }, index * 200);
    });
}

// ===== Expandable Cards =====
function initExpandableCards() {
    const cards = document.querySelectorAll('.expandable-card');
    
    cards.forEach(card => {
        card.addEventListener('click', () => {
            // Close other cards
            cards.forEach(c => {
                if (c !== card) {
                    c.classList.remove('expanded');
                }
            });
            
            // Toggle current card
            card.classList.toggle('expanded');
        });
        
        // Pre-expand on hover
        card.addEventListener('mouseenter', () => {
            if (!card.classList.contains('expanded')) {
                const stack = card.querySelector('.tech-stack');
                stack.style.maxHeight = '300px';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            if (!card.classList.contains('expanded')) {
                const stack = card.querySelector('.tech-stack');
                stack.style.maxHeight = '0';
            }
        });
    });
}

// ===== Text Switch Animation =====
function initTextSwitch() {
    const textSwitch = document.getElementById('text-switch');
    if (!textSwitch) return;
    
    setInterval(() => {
        textSwitch.style.transform = 'translateY(-100px)';
        setTimeout(() => {
            textSwitch.style.transform = 'translateY(-200px)';
        }, 3000);
        setTimeout(() => {
            textSwitch.style.transform = 'translateY(0)';
        }, 6000);
    }, 9000);
}

// ===== Hover Effects =====
function initHoverEffects() {
    // Project cards
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            const button = card.querySelector('.project-button');
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        });
        
        card.addEventListener('mouseleave', () => {
            const button = card.querySelector('.project-button');
            button.style.opacity = '0';
            button.style.transform = 'translateY(10px)';
        });
    });
    
    // Timeline nodes
    const timelineNodes = document.querySelectorAll('.timeline-node-wrapper');
    timelineNodes.forEach(node => {
        const card = node.querySelector('.timeline-card');
        
        node.addEventListener('mouseenter', () => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1.05)';
        });
        
        node.addEventListener('mouseleave', () => {
            card.style.opacity = '0.7';
            card.style.transform = 'scale(1)';
        });
    });
}

// ===== Smooth Scroll =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== Parallax Effect =====
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroCanvas = document.querySelector('.hero-canvas');
    const heroTitle = document.querySelector('.hero-title');
    
    if (heroCanvas) {
        heroCanvas.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
    
    if (heroTitle) {
        heroTitle.style.transform = `translateY(${scrolled * 0.5}px)`;
        heroTitle.style.opacity = 1 - (scrolled * 0.002);
    }
});