from app import create_app, db
from seeds_book import seed_books_from_csv

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Database reset complete.")
    
    # Run your seeder
    seed_books_from_csv("books.csv")