from app import db
from . import LoanStatusEnum, datetime, timedelta

class Loan(db.Model):
    """Model for tracking a book loan (a transaction)."""

    __tablename__ = "loan"

    id = db.Column(db.Integer, primary_key=True)
    borrowed_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=14))
    returned_date = db.Column(db.DateTime, nullable=True) # Null until the book is returned
    status = db.Column(db.Enum(LoanStatusEnum), default=LoanStatusEnum.BORROWED, nullable=False)

    # --- Foreign Keys ---
    # These create the database-level link to the other tables.
    # 'student.id' refers to the 'student' table and its 'id' column.
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    # --- Relationships ---
    # These create the Python-level link for easy access.
    student = db.relationship('Student', back_populates='loans')
    book = db.relationship('Book', back_populates='loans')

    # A loan can result in one fine. 'uselist=False' makes this a one-to-one relationship.
    fine = db.relationship('Fine', back_populates='loan', lazy=True, uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Loan id={self.id} student_id={self.student_id} book_id={self.book_id}>"