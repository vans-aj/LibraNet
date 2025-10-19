from app import db
from .publication import Publication

class Audiobook(Publication):
    """Model for Audiobooks in the library catalog."""
    __tablename__ = "audiobook"

    id = db.Column(db.Integer, db.ForeignKey('publication.id'), primary_key=True)
    file_path = db.Column(db.String(255), nullable=False, unique=True)
    duration_minutes = db.Column(db.Integer, nullable=True)  # Duration in minutes
    narrator = db.Column(db.String(150), nullable=True)
    file_format = db.Column(db.String(10), nullable=False)  # e.g., 'MP3', 'M4B'
    file_size_mb = db.Column(db.Float, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'audiobook',
    }
    
    def __repr__(self):
        return f"<Audiobook id={self.id} title='{self.title}'>"
