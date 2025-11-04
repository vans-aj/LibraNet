import os
import requests
from dotenv import load_dotenv
from app import create_app, db
from app.models.publication import Publication
from app.models.audiobook import Audiobook, AudiobookChapter
import urllib.parse 

# .env file ko load karein
load_dotenv()

# --- CONFIGURATION ---
LIBRIVOX_API_URL = os.environ.get("LIBRIVOX_API_URL")
OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
OPEN_LIBRARY_COVER_URL = "https://covers.openlibrary.org/b/id/"

# Popular audiobooks from LibriVox (100+ books)
BOOKS_TO_SEED = [
    # Classic Horror & Gothic
    "Dracula",
    "Frankenstein",
    "The Strange Case of Dr Jekyll and Mr Hyde",
    "The Picture of Dorian Gray",
    "The Turn of the Screw",
    "The Phantom of the Opera",
    
    # Jane Austen (Complete Works)
    "Pride and Prejudice",
    "Emma",
    "Sense and Sensibility",
    "Persuasion",
    "Northanger Abbey",
    "Mansfield Park",
    
    # Charles Dickens
    "A Tale of Two Cities",
    "Great Expectations",
    "Oliver Twist",
    "A Christmas Carol",
    "David Copperfield",
    "Bleak House",
    "Hard Times",
    "The Pickwick Papers",
    
    # Adventure & Action
    "Treasure Island",
    "The Adventures of Tom Sawyer",
    "The Adventures of Huckleberry Finn",
    "Robinson Crusoe",
    "The Count of Monte Cristo",
    "Around the World in Eighty Days",
    "The Three Musketeers",
    "The Man in the Iron Mask",
    "Kim",
    "Kidnapped",
    "The Thirty-Nine Steps",
    
    # Mystery & Detective
    "The Adventures of Sherlock Holmes",
    "The Hound of the Baskervilles",
    "The Sign of the Four",
    "A Study in Scarlet",
    "The Mysterious Affair at Styles",
    "The Murder of Roger Ackroyd",
    
    # American Literature
    "Moby Dick, or the Whale",
    "The Great Gatsby",
    "The Scarlet Letter",
    "Little Women",
    "The Call of the Wild",
    "White Fang",
    "The Red Badge of Courage",
    "Uncle Tom's Cabin",
    "The Awakening",
    "My Antonia",
    "O Pioneers!",
    
    # Russian Literature
    "Crime and Punishment",
    "The Brothers Karamazov",
    "Anna Karenina",
    "War and Peace",
    "The Idiot",
    "Fathers and Sons",
    
    # Science Fiction & Fantasy
    "The Time Machine",
    "The War of the Worlds",
    "Twenty Thousand Leagues Under the Sea",
    "Journey to the Center of the Earth",
    "The Invisible Man",
    "The Island of Doctor Moreau",
    "A Princess of Mars",
    
    # Philosophy & Social Commentary
    "The Prince",
    "The Republic",
    "Utopia",
    "Walden",
    "The Communist Manifesto",
    
    # Poetry & Drama
    "The Importance of Being Earnest",
    "Romeo and Juliet",
    "Hamlet",
    "Macbeth",
    "A Midsummer Night's Dream",
    "The Tempest",
    
    # British Classics
    "Wuthering Heights",
    "Jane Eyre",
    "Tess of the d'Urbervilles",
    "Far from the Madding Crowd",
    "Middlemarch",
    "Vanity Fair",
    "The Mill on the Floss",
    
    # Children's & Young Adult
    "The Jungle Book",
    "Alice's Adventures in Wonderland",
    "Through the Looking Glass",
    "The Wonderful Wizard of Oz",
    "Anne of Green Gables",
    "The Secret Garden",
    "Peter Pan",
    "The Wind in the Willows",
    "Black Beauty",
    "Heidi",
    
    # American Classics
    "The Legend of Sleepy Hollow",
    "Rip Van Winkle",
    "The Last of the Mohicans",
    "The House of the Seven Gables",
    
    # European Literature
    "Les Miserables",
    "The Hunchback of Notre Dame",
    "Candide",
    "Don Quixote",
    "The Metamorphosis",
    
    # Short Story Collections
    "Dubliners",
    "The Yellow Wallpaper",
    "The Gift of the Magi",
    
    # Historical & Biography
    "The Autobiography of Benjamin Franklin",
    "Narrative of the Life of Frederick Douglass",
]

def fetch_cover_url(title, author):
    """Open Library se cover photo ka URL fetch karta hai."""
    try:
        # Use separate title and author parameters for better results
        params = {'title': title, 'author': author, 'limit': 1}
        response = requests.get(OPEN_LIBRARY_SEARCH_URL, params=params)
        response.raise_for_status() 
        data = response.json()
        if data.get('docs') and data['docs'][0].get('cover_i'):
            cover_id = data['docs'][0]['cover_i']
            return f"{OPEN_LIBRARY_COVER_URL}{cover_id}-L.jpg"
    except Exception as e:
        print(f"  [Cover Error] Could not find cover for '{title}': {e}")
    return None

def seed_audiobook(title_query):
    """
    Ek single audiobook aur uske chapters ko LibriVox se fetch karke DB mein seed karta hai.
    """
    try:
        # Title se check karein (lekin 'like' use karein)
        existing_book = Audiobook.query.filter(Audiobook.title.ilike(f"%{title_query}%")).first()
        if existing_book:
            print(f"[Skipping] Book '{title_query}' already in database.")
            return

        print(f"[Fetching] '{title_query}' from LibriVox...")
        
        # URL-safe title
        safe_title = urllib.parse.quote_plus(title_query)
        
        api_url = f"{LIBRIVOX_API_URL}?title={safe_title}&format=json&extended=1"
        
        response = requests.get(api_url)
        response.raise_for_status() # 404 error check
        
        data = response.json()
        
        if not data.get('books'):
            print(f"  [Error] No book found with title '{title_query}'")
            return
            
        # === YEH HAI NAYA AUR SABSE IMPORTANT LOGIC ===
        # Hum 0 chapters waali galat entry ko filter karenge
        
        best_book = None
        max_chapters = 0 # Hum sirf 0 se zyada chapter waali book accept karenge

        for book in data.get('books', []):
            # Check 1: Must be English
            if book.get('language') != 'English':
                continue # Skip this book
            
            # Check 2: Must have chapters
            num_chapters = len(book.get('sections', []))
            if num_chapters == 0:
                continue # Skip this 0-chapter book
                    
            # Check 3: Is it the best one so far?
            if num_chapters > max_chapters:
                max_chapters = num_chapters
                best_book = book
        
        if not best_book:
            # Agar koi achhi book nahi mili
            print(f"  [Error] Found '{title_query}' but no suitable English version with chapters.")
            return

        book_data = best_book # Ab hum sabse achhi waali book use kar rahe hain
        # === NAYA LOGIC KHATAM ===

        librivox_id = book_data.get('id')
        title = book_data.get('title', 'Untitled')
        summary = book_data.get('description', 'No summary available.')
        
        # === YEH 'TYPE' KEYERROR KA FIX HAI ===
        # Authors don't have 'type' field - they're all authors by default
        authors = [
            f"{a.get('first_name', '')} {a.get('last_name', '')}".strip() 
            for a in book_data.get('authors', [])
        ]
        author_str = ", ".join(filter(None, authors)) or "Unknown Author" 
        
        # Get narrators from the first section's readers
        narrators = []
        if book_data.get('sections') and book_data['sections']:
            first_section = book_data['sections'][0]
            narrators = [
                reader.get('display_name', '').strip()
                for reader in first_section.get('readers', [])
            ]
        narrator_str = ", ".join(filter(None, narrators)) or author_str

        print(f"  [Found] '{title}' by {author_str} (ID: {librivox_id})")
        
        print("  [Fetching] Cover image from Open Library...")
        cover_url = fetch_cover_url(title, author_str)
        
        new_audiobook = Audiobook(
            librivox_id=librivox_id, 
            narrator=narrator_str,
            title=title,
            author=author_str,
            summary=summary,
            image_url=cover_url
        )
        
        db.session.add(new_audiobook)
        
        chapters_added = 0
        for section in book_data.get('sections', []):
            # Use listen_url instead of file_name
            audio_url = section.get('listen_url') or section.get('file_name')
            if not audio_url:
                continue
                
            new_chapter = AudiobookChapter(
                content_url=audio_url, 
                chapter_title=section.get('title', 'Chapter'),
                chapter_number=int(section.get('section_number', 0)),
                duration_seconds=float(section.get('playtime', 0.0)),
                audiobook=new_audiobook
            )
            db.session.add(new_chapter)
            chapters_added += 1
            
        db.session.commit()
        print(f"  [Success] Added '{title}' (ID: {librivox_id}) with {chapters_added} chapters to database.\n")

    except Exception as e:
        db.session.rollback() 
        print(f"  [FAILED] Could not seed book '{title_query}': {e}\n")


def run_seeder():
    if not LIBRIVOX_API_URL:
        print("Error: LIBRIVOX_API_URL environment variable not set.")
        return

    # Pehle puraana saara data delete karein
    try:
        print("--- Deleting all existing audiobook data... ---")
        chapters_deleted = db.session.query(AudiobookChapter).delete()
        books_deleted = db.session.query(Audiobook).delete()
        
        db.session.commit()
        print(f"--- Deleted {books_deleted} books and {chapters_deleted} chapters. ---")
    except Exception as e:
        print(f"  [Error deleting data] {e}")
        db.session.rollback()
        return

    print("--- Starting new audiobook seed... ---")
    
    for book_title in BOOKS_TO_SEED: 
        seed_audiobook(book_title)
        
    print("--- Seeding Complete ---")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run_seeder()