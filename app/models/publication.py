# In app/models/publication.py

from app import db

class Publication(db.Model):
    """Base model for all library items (books, ebooks, etc.)."""
    __tablename__ = "publication"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(150), nullable=False, index=True)
    summary = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    
    # This 'type' column is the key to our inheritance pattern.
    # It tells SQLAlchemy whether a row is a PhysicalBook or an Ebook.
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'publication',
        'polymorphic_on': type
    }

    def __repr__(self):
        return f"<Publication id={self.id} title='{self.title}'>"