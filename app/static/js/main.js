/**
 * LibraNet Main JavaScript
 * Global functionality and utilities
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all components
    initFlashMessages();
    initTooltips();
    initSearchShortcut();
    
});

/**
 * Flash Messages
 */
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(flash => {
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            dismissFlash(flash);
        }, 5000);
        
        // Close button
        const closeBtn = flash.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissFlash(flash);
            });
        }
    });
}

function dismissFlash(element) {
    element.style.animation = 'slideOutRight 0.3s ease-out';
    setTimeout(() => {
        element.remove();
    }, 300);
}

/**
 * Tooltips
 */
function initTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', showTooltip);
        trigger.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const text = e.target.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.id = 'active-tooltip';
    
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
}

function hideTooltip() {
    const tooltip = document.getElementById('active-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

/**
 * Search Keyboard Shortcut (/)
 */
function initSearchShortcut() {
    const searchInput = document.querySelector('.search-input');
    
    if (searchInput) {
        document.addEventListener('keydown', (e) => {
            if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }
}

/**
 * Utility Functions
 */

// Format date
function formatDate(date) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show loading spinner
function showLoading(button) {
    const originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.innerHTML = '<span class="spinner"></span>';
    button.disabled = true;
}

// Hide loading spinner
function hideLoading(button) {
    const originalText = button.getAttribute('data-original-text');
    button.innerHTML = originalText;
    button.disabled = false;
}

// API request helper
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Export utilities
window.LibraNet = {
    formatDate,
    debounce,
    showLoading,
    hideLoading,
    apiRequest
};