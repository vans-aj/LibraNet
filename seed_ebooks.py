import os
import requests # type: ignore
from dotenv import load_dotenv
from app import create_app, db
from app.models.publication import Publication
from app.models.ebook import Ebook, EbookFormat
import time

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
GUTENBERG_API_URL = "https://gutendex.com/books"
OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
OPEN_LIBRARY_COVER_URL = "https://covers.openlibrary.org/b/id/"

# Popular ebooks from Project Gutenberg (100+ books)
BOOKS_TO_SEED = [
    # Classic Horror & Gothic
    {"title": "Dracula", "author": "Stoker"},
    {"title": "Frankenstein", "author": "Shelley"},
    {"title": "The Strange Case of Dr. Jekyll and Mr. Hyde", "author": "Stevenson"},
    {"title": "The Picture of Dorian Gray", "author": "Wilde"},
    {"title": "The Turn of the Screw", "author": "James"},
    
    # Jane Austen (Complete Works)
    {"title": "Pride and Prejudice", "author": "Austen"},
    {"title": "Emma", "author": "Austen"},
    {"title": "Sense and Sensibility", "author": "Austen"},
    {"title": "Persuasion", "author": "Austen"},
    {"title": "Northanger Abbey", "author": "Austen"},
    {"title": "Mansfield Park", "author": "Austen"},
    
    # Charles Dickens
    {"title": "A Tale of Two Cities", "author": "Dickens"},
    {"title": "Great Expectations", "author": "Dickens"},
    {"title": "Oliver Twist", "author": "Dickens"},
    {"title": "A Christmas Carol", "author": "Dickens"},
    {"title": "David Copperfield", "author": "Dickens"},
    {"title": "Bleak House", "author": "Dickens"},
    
    # Adventure & Action
    {"title": "Treasure Island", "author": "Stevenson"},
    {"title": "The Adventures of Tom Sawyer", "author": "Twain"},
    {"title": "Adventures of Huckleberry Finn", "author": "Twain"},
    {"title": "Robinson Crusoe", "author": "Defoe"},
    {"title": "The Count of Monte Cristo", "author": "Dumas"},
    {"title": "Around the World in Eighty Days", "author": "Verne"},
    {"title": "The Three Musketeers", "author": "Dumas"},
    {"title": "Kim", "author": "Kipling"},
    {"title": "Kidnapped", "author": "Stevenson"},
    
    # Mystery & Detective
    {"title": "The Adventures of Sherlock Holmes", "author": "Doyle"},
    {"title": "The Hound of the Baskervilles", "author": "Doyle"},
    {"title": "The Sign of the Four", "author": "Doyle"},
    {"title": "A Study in Scarlet", "author": "Doyle"},
    
    # American Literature
    {"title": "Moby Dick", "author": "Melville"},
    {"title": "The Scarlet Letter", "author": "Hawthorne"},
    {"title": "Little Women", "author": "Alcott"},
    {"title": "The Call of the Wild", "author": "London"},
    {"title": "White Fang", "author": "London"},
    {"title": "The Red Badge of Courage", "author": "Crane"},
    {"title": "Uncle Tom's Cabin", "author": "Stowe"},
    {"title": "The Awakening", "author": "Chopin"},
    
    # Russian Literature
    {"title": "Crime and Punishment", "author": "Dostoevsky"},
    {"title": "The Brothers Karamazov", "author": "Dostoevsky"},
    {"title": "Anna Karenina", "author": "Tolstoy"},
    {"title": "War and Peace", "author": "Tolstoy"},
    {"title": "The Idiot", "author": "Dostoevsky"},
    
    # Science Fiction & Fantasy
    {"title": "The Time Machine", "author": "Wells"},
    {"title": "The War of the Worlds", "author": "Wells"},
    {"title": "Twenty Thousand Leagues under the Sea", "author": "Verne"},
    {"title": "Journey to the Center of the Earth", "author": "Verne"},
    {"title": "The Invisible Man", "author": "Wells"},
    {"title": "A Princess of Mars", "author": "Burroughs"},
    
    # Philosophy & Social Commentary
    {"title": "The Prince", "author": "Machiavelli"},
    {"title": "The Republic", "author": "Plato"},
    {"title": "Utopia", "author": "More"},
    {"title": "Walden", "author": "Thoreau"},
    {"title": "The Communist Manifesto", "author": "Marx"},
    
    # Poetry & Drama
    {"title": "The Importance of Being Earnest", "author": "Wilde"},
    {"title": "Romeo and Juliet", "author": "Shakespeare"},
    {"title": "Hamlet", "author": "Shakespeare"},
    {"title": "Macbeth", "author": "Shakespeare"},
    {"title": "A Midsummer Night's Dream", "author": "Shakespeare"},
    
    # British Classics
    {"title": "Wuthering Heights", "author": "Brontë"},
    {"title": "Jane Eyre", "author": "Brontë"},
    {"title": "Middlemarch", "author": "Eliot"},
    {"title": "Vanity Fair", "author": "Thackeray"},
    
    # Children's & Young Adult
    {"title": "The Jungle Book", "author": "Kipling"},
    {"title": "Alice's Adventures in Wonderland", "author": "Carroll"},
    {"title": "Through the Looking-Glass", "author": "Carroll"},
    {"title": "The Wonderful Wizard of Oz", "author": "Baum"},
    {"title": "Anne of Green Gables", "author": "Montgomery"},
    {"title": "The Secret Garden", "author": "Burnett"},
    {"title": "Peter Pan", "author": "Barrie"},
    {"title": "The Wind in the Willows", "author": "Grahame"},
    {"title": "Black Beauty", "author": "Sewell"},
    {"title": "Heidi", "author": "Spyri"},
    
    # European Literature
    {"title": "Les Misérables", "author": "Hugo"},
    {"title": "The Hunchback of Notre-Dame", "author": "Hugo"},
    {"title": "Candide", "author": "Voltaire"},
    {"title": "Don Quixote", "author": "Cervantes"},
    {"title": "The Metamorphosis", "author": "Kafka"},
    
    # Short Story Collections
    {"title": "Dubliners", "author": "Joyce"},
    {"title": "The Yellow Wallpaper", "author": "Gilman"},
]


def fetch_cover_url(title, author):
    """Fetch cover image URL from Open Library."""
    try:
        params = {'title': title, 'author': author, 'limit': 1}
        response = requests.get(OPEN_LIBRARY_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('docs') and data['docs'][0].get('cover_i'):
            cover_id = data['docs'][0]['cover_i']
            return f"{OPEN_LIBRARY_COVER_URL}{cover_id}-L.jpg"
    except Exception as e:
        print(f"  [Cover Error] Could not find cover for '{title}': {e}")
    return None


def seed_ebook(title, author):
    """
    Fetch a single ebook from Project Gutenberg and seed it to the database.
    """
    try:
        # Check if book already exists
        existing_book = Ebook.query.filter(Ebook.title.ilike(f"%{title}%")).first()
        if existing_book:
            print(f"[Skipping] Book '{title}' already in database.")
            return

        print(f"[Fetching] '{title}' by {author} from Project Gutenberg...")
        
        # Search Gutenberg API
        params = {
            'search': f"{title} {author}",
            'languages': 'en'
        }
        
        response = requests.get(GUTENBERG_API_URL, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('results'):
            print(f"  [Error] No book found with title '{title}' by {author}")
            return
            
        # Get the first result
        book_data = data['results'][0]
        
        gutenberg_id = book_data.get('id')
        full_title = book_data.get('title', title)
        
        # Get authors
        authors = book_data.get('authors', [])
        author_str = ", ".join([a.get('name', '') for a in authors]) or "Unknown Author"
        
        # Get description
        summary = None
        if book_data.get('subjects'):
            summary = "; ".join(book_data['subjects'][:3])

        print(f"  [Found] '{full_title}' by {author_str} (ID: {gutenberg_id})")
        
        print("  [Fetching] Cover image from Open Library...")
        cover_url = fetch_cover_url(full_title, author_str)
        
        new_ebook = Ebook(
            external_id=str(gutenberg_id),
            title=full_title,
            author=author_str,
            summary=summary,
            image_url=cover_url
        )
        
        db.session.add(new_ebook)
        
        # Add formats
        formats_added = 0
        formats_data = book_data.get('formats', {})
        
        # Map of format types to their URLs
        format_mapping = {
            'EPUB': ['application/epub+zip'],
            'HTML': ['text/html', 'text/html; charset=utf-8'],
            'TXT': ['text/plain', 'text/plain; charset=utf-8', 'text/plain; charset=us-ascii'],
            'PDF': ['application/pdf']
        }
        
        for format_name, mime_types in format_mapping.items():
            for mime_type in mime_types:
                if mime_type in formats_data:
                    url = formats_data[mime_type]
                    new_format = EbookFormat(
                        file_format=format_name,
                        content_url=url,
                        ebook=new_ebook
                    )
                    db.session.add(new_format)
                    formats_added += 1
                    break
            
        db.session.commit()
        print(f"  [Success] Added '{full_title}' with {formats_added} formats to database.\n")
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)

    except Exception as e:
        db.session.rollback()
        print(f"  [FAILED] Could not seed book '{title}': {e}\n")


def run_seeder():
    # Delete existing ebook data
    try:
        print("--- Deleting all existing ebook data... ---")
        formats_deleted = db.session.query(EbookFormat).delete()
        books_deleted = db.session.query(Ebook).delete()
        
        db.session.commit()
        print(f"--- Deleted {books_deleted} books and {formats_deleted} formats. ---")
    except Exception as e:
        print(f"  [Error deleting data] {e}")
        db.session.rollback()
        return

    print("--- Starting new ebook seed... ---")
    
    for book in BOOKS_TO_SEED:
        seed_ebook(book['title'], book['author'])
        
    print("--- Seeding Complete ---")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run_seeder()
