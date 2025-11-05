// Theme Management
(function() {
    'use strict';

    // Get theme from localStorage or system preference
    function getPreferredTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        
        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        
        return 'light';
    }

    // Set theme on document
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update toggle button if it exists
        updateToggleButton(theme);
    }

    // Update toggle button appearance
    function updateToggleButton(theme) {
        const toggleBtn = document.getElementById('theme-toggle');
        if (!toggleBtn) return;

        const sunIcon = toggleBtn.querySelector('.sun-icon');
        const moonIcon = toggleBtn.querySelector('.moon-icon');

        if (theme === 'dark') {
            if (sunIcon) sunIcon.style.display = 'none';
            if (moonIcon) moonIcon.style.display = 'block';
        } else {
            if (sunIcon) sunIcon.style.display = 'block';
            if (moonIcon) moonIcon.style.display = 'none';
        }
    }

    // Toggle theme
    function toggleTheme(event) {
        // Prevent event bubbling and default behavior
        if (event) {
            event.stopPropagation();
            event.preventDefault();
            event.stopImmediatePropagation();
        }
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        return false;
    }

    // Initialize theme on page load
    document.addEventListener('DOMContentLoaded', function() {
        const preferredTheme = getPreferredTheme();
        setTheme(preferredTheme);

        // Add event listener to toggle button with capture phase
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                e.preventDefault();
                toggleTheme(e);
            }, true);
            
            // Prevent clicks on child elements from bubbling
            const slider = toggleBtn.querySelector('.theme-toggle-slider');
            if (slider) {
                slider.addEventListener('click', function(e) {
                    e.stopPropagation();
                    e.preventDefault();
                }, true);
            }
        }
    });

    // Listen for system theme changes
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
            // Only auto-switch if user hasn't manually set a preference
            if (!localStorage.getItem('theme')) {
                setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    // Expose theme functions globally
    window.themeManager = {
        setTheme: setTheme,
        toggleTheme: toggleTheme,
        getTheme: function() {
            return document.documentElement.getAttribute('data-theme') || 'light';
        }
    };
})();
