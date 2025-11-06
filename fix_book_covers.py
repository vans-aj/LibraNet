"""
Fix Physical Book Cover Images
===============================
Updates existing physical books with real book covers from Open Library API.
"""

from app import create_app, db
from app.models.physical_book import PhysicalBook
import requests # type: ignore
import time

def get_real_cover_from_openlibrary(title, author):
    """
    Fetch real book cover from Open Library API.
    
    Args:
        title: Book title
        author: Author name
        
    Returns:
        Cover image URL or None
    """
    try:
        # Search Open Library for the book
        search_url = "https://openlibrary.org/search.json"
        params = {
            'title': title,
            'author': author,
            'limit': 1
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        data = response.json()
        
        if data.get('docs') and len(data['docs']) > 0:
            book_data = data['docs'][0]
            
            # Try to get cover ID
            if 'cover_i' in book_data:
                cover_id = book_data['cover_i']
                return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            
            # Try ISBN
            if 'isbn' in book_data and len(book_data['isbn']) > 0:
                isbn = book_data['isbn'][0]
                return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        
        return None
        
    except Exception as e:
        print(f"   ⚠️  API error: {e}")
        return None


def fix_cover_images():
    """Update all physical books with real book covers from Open Library."""
    
    app = create_app()
    
    with app.app_context():
        books = PhysicalBook.query.all()
        
        print(f"\n📚 Found {len(books)} books to update")
        print("="*70)
        print("🔍 Fetching real book covers from Open Library...")
        print("   This may take a few minutes...\n")
        
        updated = 0
        not_found = 0
        
        for idx, book in enumerate(books, 1):
            try:
                print(f"[{idx}/{len(books)}] {book.title[:40]}...")
                
                # Get real cover from Open Library
                cover_url = get_real_cover_from_openlibrary(book.title, book.author)
                
                if cover_url:
                    book.image_url = cover_url
                    updated += 1
                    print(f"   ✅ Found cover!")
                else:
                    # Fallback to colorful placeholder
                    import hashlib
                    seed = hashlib.md5(book.title.encode()).hexdigest()[:10]
                    book.image_url = f"https://api.dicebear.com/7.x/shapes/svg?seed={seed}&size=400&backgroundColor=1e40af,3b82f6,60a5fa"
                    not_found += 1
                    print(f"   ⚠️  No cover found, using placeholder")
                
                # Rate limiting - be nice to Open Library API
                if idx % 5 == 0:
                    time.sleep(1)
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                not_found += 1
        
        # Commit all changes
        try:
            db.session.commit()
            print("\n" + "="*70)
            print(f"✅ Real covers found: {updated}")
            print(f"⚠️  Placeholders used: {not_found}")
            print(f"📚 Total updated: {len(books)}")
            print("="*70 + "\n")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error committing changes: {e}\n")


if __name__ == '__main__':
    print("\n⚠️  This will fetch REAL book covers from Open Library.")
    print("   📸 Real vintage covers for classic books!")
    print("   ⏱️  This will take 2-3 minutes (rate-limited API calls).")
    confirm = input("\nContinue? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        fix_cover_images()
        print("\n🎉 Done! Reload your browser to see the real book covers!")
        print("   Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)\n")
    else:
        print("\n❌ Cancelled.\n")
