// Portfolio Interactive JavaScript

// Theme Toggle
const themeToggle = document.querySelector('.theme-toggle');
let isDarkMode = true;

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        isDarkMode = !isDarkMode;
        
        if (!isDarkMode) {
            // Light mode colors
            document.documentElement.style.setProperty('--bg-primary', '#ffffff');
            document.documentElement.style.setProperty('--bg-secondary', '#f9f9f9');
            document.documentElement.style.setProperty('--bg-card', '#f5f5f5');
            document.documentElement.style.setProperty('--bg-card-hover', '#eeeeee');
            document.documentElement.style.setProperty('--text-primary', '#0a0a0a');
            document.documentElement.style.setProperty('--text-secondary', '#666666');
            document.documentElement.style.setProperty('--text-muted', '#999999');
            document.documentElement.style.setProperty('--border-color', '#e5e5e5');
            document.documentElement.style.setProperty('--border-light', '#d0d0d0');
        } else {
            // Dark mode colors (default)
            document.documentElement.style.setProperty('--bg-primary', '#0a0a0a');
            document.documentElement.style.setProperty('--bg-secondary', '#111111');
            document.documentElement.style.setProperty('--bg-card', '#161616');
            document.documentElement.style.setProperty('--bg-card-hover', '#1a1a1a');
            document.documentElement.style.setProperty('--text-primary', '#ffffff');
            document.documentElement.style.setProperty('--text-secondary', '#888888');
            document.documentElement.style.setProperty('--text-muted', '#666666');
            document.documentElement.style.setProperty('--border-color', '#262626');
            document.documentElement.style.setProperty('--border-light', '#333333');
        }
        
        // Store preference
        localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    });
    
    // Load saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        themeToggle.click();
    }
}

// Chat Toggle (placeholder functionality)
const chatToggle = document.querySelector('.chat-toggle');
if (chatToggle) {
    chatToggle.addEventListener('click', () => {
        alert('Chat feature coming soon!');
    });
}

// Smooth scroll for anchor links
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

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all sections
document.querySelectorAll('section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(20px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(section);
});

// Project cards hover effect
const projectCards = document.querySelectorAll('.project-card');
projectCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-8px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
    
    // Add click functionality
    card.addEventListener('click', function() {
        // Placeholder for project navigation
        console.log('Project clicked:', this.querySelector('h3').textContent);
    });
});

// Email link copy functionality (removed - no email link)

// Social links hover effect
const socialLinks = document.querySelectorAll('.social-link');
socialLinks.forEach(link => {
    link.style.cursor = 'pointer';
    link.addEventListener('click', function() {
        const platform = this.querySelector('h4').textContent;
        const username = this.querySelector('p').textContent;
        
        // Map social platforms to URLs
        const socialUrls = {
            'GitHub': `https://github.com/mochitoChef`,
            'LinkedIn': `https://www.linkedin.com/in/mochito-chef-14397a382/`,
            'HubSpot Community': `https://community.hubspot.com/t5/user/viewprofilepage/user-id/${username.replace('@', '')}`
        };
        
        if (socialUrls[platform]) {
            window.open(socialUrls[platform], '_blank');
        }
    });
});

// Parallax effect for hero section
let ticking = false;
function updateParallax() {
    const scrolled = window.pageYOffset;
    const heroTitle = document.querySelector('.hero-title');
    const heroDescription = document.querySelector('.hero-description');
    
    if (heroTitle && scrolled < window.innerHeight) {
        heroTitle.style.transform = `translateY(${scrolled * 0.3}px)`;
        heroTitle.style.opacity = 1 - (scrolled / 800);
    }
    
    if (heroDescription && scrolled < window.innerHeight) {
        heroDescription.style.transform = `translateY(${scrolled * 0.15}px)`;
    }
    
    ticking = false;
}

function requestTick() {
    if (!ticking) {
        window.requestAnimationFrame(updateParallax);
        ticking = true;
    }
}

window.addEventListener('scroll', requestTick);

// Dynamic year update
const yearElements = document.querySelectorAll('.current-year');
yearElements.forEach(element => {
    element.textContent = new Date().getFullYear();
});

// Loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    // Press 'T' to toggle theme
    if (e.key === 't' || e.key === 'T') {
        if (themeToggle) themeToggle.click();
    }
    
    // Press 'ESC' to close any modals (future implementation)
    if (e.key === 'Escape') {
        // Close modals
    }
});

// Mobile menu toggle (if needed in future)
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        document.body.classList.toggle('menu-open');
    });
}

// Console Easter egg
console.log('%c👋 Hey there, fellow developer!', 'font-size: 20px; font-weight: bold; color: #10b981;');
console.log('%cInterested in the code? Let\'s connect!', 'font-size: 14px; color: #888;');
console.log('%cBuilt with ❤️ by Mochito', 'font-size: 12px; color: #666;');
