/**
 * Shopping Cart/Bag Functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initCart();
});

/**
 * Initialize Cart
 */
function initCart() {
    // Handle remove from cart buttons
    const removeButtons = document.querySelectorAll('.remove-btn');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', handleRemoveFromCart);
    });
    
    // Update cart count
    updateCartCount();
}

/**
 * Handle Remove from Cart
 */
function handleRemoveFromCart(e) {
    e.preventDefault();
    
    const form = e.target.closest('form');
    const bookItem = e.target.closest('.bag-item');
    
    if (!form || !bookItem) return;
    
    // Show confirmation
    if (!confirm('Are you sure you want to remove this book from your bag?')) {
        return;
    }
    
    // Animate removal
    bookItem.style.transition = 'all 0.3s ease-out';
    bookItem.style.opacity = '0';
    bookItem.style.transform = 'translateX(-20px)';
    
    setTimeout(() => {
        form.submit();
    }, 300);
}

/**
 * Add to Cart Animation
 */
function animateAddToCart(button, bookId) {
    const originalText = button.innerHTML;
    
    // Show loading
    button.innerHTML = `
        <svg class="spinner" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        <span>Adding...</span>
    `;
    button.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        button.innerHTML = `
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            <span>Added to Bag</span>
        `;
        button.classList.add('success');
        
        // Update cart count
        updateCartCount();
        
        // Reset after 2 seconds
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
            button.classList.remove('success');
        }, 2000);
    }, 1000);
}

/**
 * Update Cart Count
 */
function updateCartCount() {
    const cartCountElement = document.querySelector('.cart-count');
    
    if (cartCountElement) {
        // Fetch current cart count from server
        fetch('/api/cart/count')
            .then(response => response.json())
            .then(data => {
                if (data.count > 0) {
                    cartCountElement.textContent = data.count;
                    cartCountElement.style.display = 'flex';
                } else {
                    cartCountElement.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error updating cart count:', error);
            });
    }
}

/**
 * Calculate Cart Total
 */
function calculateCartTotal() {
    const items = document.querySelectorAll('.bag-item');
    const depositPerBook = 100;
    const total = items.length * depositPerBook;
    
    const totalElement = document.querySelector('.summary-value');
    if (totalElement) {
        totalElement.textContent = `₹${total}`;
    }
}

// Export functions
window.CartUtils = {
    animateAddToCart,
    updateCartCount,
    calculateCartTotal
};