/**
 * Search Functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initSearch();
});

/**
 * Initialize Search
 */
function initSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    
    if (!searchInput) return;
    
    // Auto-complete functionality
    let searchTimeout;
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        
        const query = e.target.value.trim();
        
        if (query.length < 2) {
            hideSearchSuggestions();
            return;
        }
        
        searchTimeout = setTimeout(() => {
            fetchSearchSuggestions(query);
        }, 300);
    });
    
    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-wrapper')) {
            hideSearchSuggestions();
        }
    });
    
    // Handle keyboard navigation
    searchInput.addEventListener('keydown', handleSearchKeyboard);
}

/**
 * Fetch Search Suggestions
 */
async function fetchSearchSuggestions(query) {
    try {
        const response = await fetch(`/api/search/suggestions?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) return;
        
        const data = await response.json();
        displaySearchSuggestions(data.suggestions);
    } catch (error) {
        console.error('Search suggestions error:', error);
    }
}

/**
 * Display Search Suggestions
 */
function displaySearchSuggestions(suggestions) {
    const searchWrapper = document.querySelector('.search-wrapper');
    
    // Remove existing suggestions
    let suggestionsBox = document.querySelector('.search-suggestions');
    if (suggestionsBox) {
        suggestionsBox.remove();
    }
    
    if (!suggestions || suggestions.length === 0) return;
    
    // Create suggestions box
    suggestionsBox = document.createElement('div');
    suggestionsBox.className = 'search-suggestions';
    
    suggestions.forEach(item => {
        const suggestionItem = document.createElement('a');
        suggestionItem.href = item.url;
        suggestionItem.className = 'search-suggestion-item';
        suggestionItem.innerHTML = `
            <div class="suggestion-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
            </div>
            <div class="suggestion-content">
                <div class="suggestion-title">${highlightMatch(item.title, query)}</div>
                <div class="suggestion-meta">${item.author}</div>
            </div>
        `;
        
        suggestionsBox.appendChild(suggestionItem);
    });
    
    searchWrapper.appendChild(suggestionsBox);
}

/**
 * Hide Search Suggestions
 */
function hideSearchSuggestions() {
    const suggestionsBox = document.querySelector('.search-suggestions');
    if (suggestionsBox) {
        suggestionsBox.remove();
    }
}

/**
 * Highlight Match in Text
 */
function highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

/**
 * Handle Keyboard Navigation
 */
function handleSearchKeyboard(e) {
    const suggestions = document.querySelectorAll('.search-suggestion-item');
    if (!suggestions.length) return;
    
    const currentIndex = Array.from(suggestions).findIndex(item => 
        item.classList.contains('active')
    );
    
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        const nextIndex = currentIndex < suggestions.length - 1 ? currentIndex + 1 : 0;
        setActiveSuggestion(suggestions, nextIndex);
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const prevIndex = currentIndex > 0 ? currentIndex - 1 : suggestions.length - 1;
        setActiveSuggestion(suggestions, prevIndex);
    } else if (e.key === 'Enter' && currentIndex >= 0) {
        e.preventDefault();
        suggestions[currentIndex].click();
    }
}

/**
 * Set Active Suggestion
 */
function setActiveSuggestion(suggestions, index) {
    suggestions.forEach(item => item.classList.remove('active'));
    suggestions[index].classList.add('active');
    suggestions[index].scrollIntoView({ block: 'nearest' });
}

/**
 * Search Suggestions Styles (add to CSS)
 */
const searchStyles = `
.search-suggestions {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-xl);
    max-height: 400px;
    overflow-y: auto;
    z-index: var(--z-dropdown);
}

.search-suggestion-item {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
    border-bottom: 1px solid var(--gray-100);
    transition: background var(--transition);
    cursor: pointer;
}

.search-suggestion-item:last-child {
    border-bottom: none;
}

.search-suggestion-item:hover,
.search-suggestion-item.active {
    background: var(--gray-50);
}

.suggestion-icon {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--gray-100);
    border-radius: var(--radius-md);
    color: var(--gray-600);
}

.suggestion-icon svg {
    width: 20px;
    height: 20px;
}

.suggestion-content {
    flex: 1;
}

.suggestion-title {
    font-size: var(--text-sm);
    font-weight: var(--font-semibold);
    color: var(--gray-900);
    margin-bottom: 2px;
}

.suggestion-title mark {
    background: var(--primary);
    color: var(--white);
    padding: 0 2px;
    border-radius: 2px;
}

.suggestion-meta {
    font-size: var(--text-xs);
    color: var(--gray-600);
}
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = searchStyles;
document.head.appendChild(styleSheet);