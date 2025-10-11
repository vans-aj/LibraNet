# In app/models/ebook.py

from app import db
from .publication import Publication

class Ebook(Publication):
    """Model for Ebooks in the library catalog."""
    __tablename__ = "ebook"

    id = db.Column(db.Integer, db.ForeignKey('publication.id'), primary_key=True)
    file_path = db.Column(db.String(255), nullable=False, unique=True) # Path on the server
    file_format = db.Column(db.String(10), nullable=False) # e.g., 'PDF', 'EPUB'
    file_size_mb = db.Column(db.Float, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'ebook',
    }
    
    def __repr__(self):
        return f"<Ebook id={self.id} title='{self.title}'>"