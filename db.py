# db.py
from app import create_app, db
from sqlalchemy import text
from seeds_book import seed_books_from_csv

app = create_app()

with app.app_context():
    # drop dependent table(s) explicitly first
    # import your model classes if needed:
    # from models import Payment, Student
    # Payment.__table__.drop(db.engine)   # drop only payment table

    # If you don't want to import models, drop_all after removing dependents:
    db.session.execute(text("DROP TABLE IF EXISTS payment"))
    db.session.commit()

    # now safe to drop the rest
    db.drop_all()
    db.create_all()
    print("✅ Database reset complete.")

    seed_books_from_csv("books.csv")