/**
 * Books Page Functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initBooksPage();
});

/**
 * Initialize Books Page
 */
function initBooksPage() {
    initViewToggle();
    initFilters();
    initInfiniteScroll();
}

/**
 * View Toggle (Grid/List)
 */
function initViewToggle() {
    const gridViewBtn = document.getElementById('gridView');
    const listViewBtn = document.getElementById('listView');
    const booksContainer = document.getElementById('booksContainer');
    
    if (!gridViewBtn || !listViewBtn || !booksContainer) return;
    
    gridViewBtn.addEventListener('click', () => {
        booksContainer.className = 'books-grid';
        gridViewBtn.classList.add('active');
        listViewBtn.classList.remove('active');
        localStorage.setItem('bookView', 'grid');
    });
    
    listViewBtn.addEventListener('click', () => {
        booksContainer.className = 'books-list';
        listViewBtn.classList.add('active');
        gridViewBtn.classList.remove('active');
        localStorage.setItem('bookView', 'list');
    });
    
    // Restore saved view
    const savedView = localStorage.getItem('bookView');
    if (savedView === 'list') {
        listViewBtn.click();
    }
}

/**
 * Initialize Filters
 */
function initFilters() {
    const filterSelects = document.querySelectorAll('.filter-select');
    
    filterSelects.forEach(select => {
        select.addEventListener('change', () => {
            // Auto-submit form when filter changes
            const form = select.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
    
    // Restore filter values from URL
    const urlParams = new URLSearchParams(window.location.search);
    filterSelects.forEach(select => {
        const value = urlParams.get(select.name);
        if (value) {
            select.value = value;
        }
    });
}

/**
 * Infinite Scroll
 */
let isLoading = false;
let currentPage = 1;
let hasMorePages = true;

function initInfiniteScroll() {
    // Only enable on books page with grid view
    const booksContainer = document.getElementById('booksContainer');
    if (!booksContainer || !booksContainer.classList.contains('books-grid')) return;
    
    window.addEventListener('scroll', LibraNet.debounce(handleScroll, 200));
}

function handleScroll() {
    const scrollPosition = window.innerHeight + window.scrollY;
    const documentHeight = document.documentElement.scrollHeight;
    
    // Load more when 200px from bottom
    if (scrollPosition >= documentHeight - 200 && !isLoading && hasMorePages) {
        loadMoreBooks();
    }
}

async function loadMoreBooks() {
    isLoading = true;
    currentPage++;
    
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('page', currentPage);
    
    try {
        const response = await fetch(`/api/books?${urlParams.toString()}`);
        const data = await response.json();
        
        if (data.books && data.books.length > 0) {
            appendBooks(data.books);
        } else {
            hasMorePages = false;
        }
    } catch (error) {
        console.error('Error loading more books:', error);
    } finally {
        isLoading = false;
    }
}

function appendBooks(books) {
    const booksContainer = document.getElementById('booksContainer');
    
    books.forEach(book => {
        const bookCard = createBookCard(book);
        booksContainer.appendChild(bookCard);
    });
}

function createBookCard(book) {
    const card = document.createElement('a');
    card.href = `/books/${book.id}`;
    card.className = 'book-card';
    
    card.innerHTML = `
        <div class="book-card-image">
            <img src="${book.image_url || '/static/images/default-book.jpg'}" alt="${book.title}" loading="lazy">
            <div class="book-card-overlay">
                <span class="quick-view-btn">View Details</span>
            </div>
            <span class="book-card-badge ${book.available_copies > 0 ? 'available' : 'unavailable'}">
                ${book.available_copies > 0 ? 'Available' : 'Checked Out'}
            </span>
        </div>
        <div class="book-card-content">
            <h3 class="book-card-title">${book.title}</h3>
            <p class="book-card-author">${book.author}</p>
            <div class="book-card-meta">
                <span class="book-card-copies">
                    ${book.available_copies} / ${book.total_copies} available
                </span>
                <svg class="book-card-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
            </div>
        </div>
    `;
    
    return card;
}

/**
 * Book Card Hover Effects
 */
document.addEventListener('mouseover', function(e) {
    const bookCard = e.target.closest('.book-card');
    if (bookCard) {
        bookCard.style.transform = 'translateY(-8px)';
    }
});

document.addEventListener('mouseout', function(e) {
    const bookCard = e.target.closest('.book-card');
    if (bookCard) {
        bookCard.style.transform = 'translateY(0)';
    }
});