from app import db
from . import SubscriptionTierEnum, datetime
from datetime import timedelta

class Subscription(db.Model):
    """Model for user subscriptions."""
    __tablename__ = "subscription"

    id = db.Column(db.Integer, primary_key=True)
    tier = db.Column(db.Enum(SubscriptionTierEnum), default=SubscriptionTierEnum.FREE, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    auto_renew = db.Column(db.Boolean, default=False, nullable=False)
    price_paid = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    
    # Foreign Key
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    
    # Relationship
    student = db.relationship('Student', back_populates='subscriptions')
    
    @property
    def is_expired(self):
        """Check if subscription has expired."""
        if self.tier == SubscriptionTierEnum.FREE:
            return False
        if self.end_date is None:
            return False
        return datetime.utcnow() > self.end_date
    
    @property
    def days_remaining(self):
        """Calculate days remaining in subscription."""
        if self.tier == SubscriptionTierEnum.FREE:
            return None
        if self.end_date is None:
            return None
        delta = self.end_date - datetime.utcnow()
        return max(0, delta.days)
    
    def __repr__(self):
        return f"<Subscription id={self.id} tier={self.tier.value} student_id={self.student_id}>"