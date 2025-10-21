# In app/models/loan.py

from app import db
from . import LoanStatusEnum, datetime, timedelta

class Loan(db.Model):
    """Model for tracking a book loan (a transaction)."""
    __tablename__ = "loan"

    id = db.Column(db.Integer, primary_key=True)
    borrowed_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # --- CHANGED: Default due date is now 182 days (6 months) ---
    due_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=182))
    returned_date = db.Column(db.DateTime, nullable=True) # Is NULL until the book is returned
    status = db.Column(db.Enum(LoanStatusEnum), default=LoanStatusEnum.BORROWED, nullable=False)

    # --- Foreign Keys (The physical database links) ---
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('physical_book.id'), nullable=False)

    # --- Relationships (The Python shortcuts) ---
    student = db.relationship('Student', back_populates='loans')
    book = db.relationship('PhysicalBook', back_populates='loans')

    # A loan can result in one fine. We will build this out later.
    fine = db.relationship('Fine', back_populates='loan', lazy=True, uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        """Provides a developer-friendly representation of the loan object."""
        return f"<Loan id={self.id} student_id={self.student_id} book_id={self.book_id}>"