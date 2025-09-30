from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from . import RoleEnum

class Student(db.Model):
    """Model for library users (students, librarians, etc.)."""

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.STUDENT, nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # --- Relationships ---
    # This creates a link to the Loan model. A single student can have many loans.
    # 'back_populates' links it to the 'student' attribute in the Loan model.
    # 'lazy=True' means SQLAlchemy will load the loans only when you ask for them.
    loans = db.relationship('Loan', back_populates='student', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """Hash and store password securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<Student id={self.id} email={self.email}>"