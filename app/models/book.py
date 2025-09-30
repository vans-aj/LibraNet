from app import db
from . import BookFormatEnum

class Book(db.Model):
    """Model for books in the library catalog."""

    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(150), nullable=False, index=True)
    isbn = db.Column(db.String(20), unique=True, nullable=True) # ISBN can be unique
    format = db.Column(db.Enum(BookFormatEnum), default=BookFormatEnum.PHYSICAL, nullable=False)
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)

    # --- Relationships ---
    # A book can be involved in many loans.
    loans = db.relationship('Loan', back_populates='book', lazy=True)

    def __repr__(self) -> str:
        return f"<Book id={self.id} title='{self.title}'>"