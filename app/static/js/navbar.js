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
