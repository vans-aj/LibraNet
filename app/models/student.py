# In app/models/student.py

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from flask_login import UserMixin
# The RoleEnum import has been removed

class Student(UserMixin, db.Model):
    """Model ONLY for student users."""
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # --- Relationships ---
    # A student can have many loans.
    loans = db.relationship('Loan', back_populates='student', lazy=True, cascade="all, delete-orphan")

    # --- Password helpers ---
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<Student id={self.id} email={self.email}>"


# This user loader function remains the same.
# It will now ONLY load students.
@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))