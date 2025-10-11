# In app/models/physical_book.py

from app import db
from .publication import Publication

class PhysicalBook(Publication):
    """Model for PHYSICAL books in the library catalog."""
    __tablename__ = "physical_book"

    id = db.Column(db.Integer, db.ForeignKey('publication.id'), primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)

    # --- Relationships ---
    # The 'loans' relationship now belongs here, as only physical books can be loaned.
    loans = db.relationship('Loan', back_populates='book', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'physical_book',
    }

    def __repr__(self):
        return f"<PhysicalBook id={self.id} title='{self.title}'>"