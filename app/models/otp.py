from app import db
from datetime import datetime, timedelta
import random
import string

class OTP(db.Model):
    """Model for storing OTPs for email verification."""
    __tablename__ = "otp"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, index=True)
    otp_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    attempts = db.Column(db.Integer, default=0, nullable=False)
    
    def __init__(self, email, expiry_minutes=10):
        self.email = email
        self.otp_code = self.generate_otp()
        self.expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    
    @staticmethod
    def generate_otp(length=6):
        """Generate a random 6-digit OTP."""
        return ''.join(random.choices(string.digits, k=length))
    
    def is_valid(self):
        """Check if OTP is still valid."""
        return not self.is_used and datetime.utcnow() < self.expires_at and self.attempts < 3
    
    def __repr__(self):
        return f"<OTP email={self.email} code={self.otp_code}>"