/**
 * Navigation Bar Functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initUserMenu();
    initMobileMenu();
});

/**
 * User Dropdown Menu
 */
function initUserMenu() {
    const userButton = document.getElementById('userMenuButton');
    const userMenu = document.querySelector('.user-menu');
    const dropdown = document.getElementById('userDropdown');
    
    if (userButton && userMenu) {
        userButton.addEventListener('click', (e) => {
            e.stopPropagation();
            userMenu.classList.toggle('active');
        });
        
        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!userMenu.contains(e.target)) {
                userMenu.classList.remove('active');
            }
        });
        
        // Close when pressing Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                userMenu.classList.remove('active');
            }
        });
    }
}

/**
 * Mobile Menu
 */
function initMobileMenu() {
    const mobileToggle = document.getElementById('mobileToggle');
    const navMenu = document.querySelector('.navbar-nav');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            mobileToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            document.body.classList.toggle('menu-open');
        });

        // Close menu when clicking on nav links (except theme toggle)
        const navLinks = navMenu.querySelectorAll('.nav-link:not(.theme-toggle-mobile)');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.classList.remove('menu-open');
            });
        });
    }

    // Mobile theme toggle
    const mobileThemeToggle = document.getElementById('theme-toggle-mobile');
    if (mobileThemeToggle) {
        mobileThemeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Toggle theme
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Update mobile toggle UI
            const sunIcon = this.querySelector('.sun-icon-mobile');
            const moonIcon = this.querySelector('.moon-icon-mobile');
            const themeLabel = this.querySelector('.theme-label');
            
            if (newTheme === 'dark') {
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'block';
                themeLabel.textContent = 'Light Mode';
            } else {
                sunIcon.style.display = 'block';
                moonIcon.style.display = 'none';
                themeLabel.textContent = 'Dark Mode';
            }
            
            // Also update desktop theme toggle if it exists
            const desktopToggle = document.querySelector('.theme-toggle:not(#theme-toggle-mobile)');
            if (desktopToggle) {
                const desktopSun = desktopToggle.querySelector('.sun-icon');
                const desktopMoon = desktopToggle.querySelector('.moon-icon');
                if (desktopSun && desktopMoon) {
                    if (newTheme === 'dark') {
                        desktopSun.style.display = 'none';
                        desktopMoon.style.display = 'block';
                    } else {
                        desktopSun.style.display = 'block';
                        desktopMoon.style.display = 'none';
                    }
                }
            }
        });

        // Initialize mobile theme toggle state
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const sunIcon = mobileThemeToggle.querySelector('.sun-icon-mobile');
        const moonIcon = mobileThemeToggle.querySelector('.moon-icon-mobile');
        const themeLabel = mobileThemeToggle.querySelector('.theme-label');
        
        if (currentTheme === 'dark') {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
            themeLabel.textContent = 'Light Mode';
        } else {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
            themeLabel.textContent = 'Dark Mode';
        }
    }
}

/**
 * Sticky Navbar
 */
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > lastScroll && currentScroll > 100) {
        // Scrolling down
        header.style.transform = 'translateY(-100%)';
    } else {
        // Scrolling up
        header.style.transform = 'translateY(0)';
    }
    
    lastScroll = currentScroll;
});
