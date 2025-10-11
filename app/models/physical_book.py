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
    related_courses = db.Column(db.Text, nullable=True)

    # --- Relationships ---
    # The 'loans' relationship now belongs here, as only physical books can be loaned.
    loans = db.relationship('Loan', back_populates='book', lazy=True)
    def __init__(self, **kwargs):
        """
        Custom constructor to set available_copies equal to total_copies
        if it's not specified.
        """
        super(PhysicalBook, self).__init__(**kwargs)
        if self.available_copies is None:
            self.available_copies = self.total_copies

    __mapper_args__ = {
        'polymorphic_identity': 'physical_book',
    }

    def __repr__(self):
        return f"<PhysicalBook id={self.id} title='{self.title}'>"
    @property
    def is_available(self):
        """
        A property that returns True if at least one copy of the book is available.
        """
        return self.available_copies > 0