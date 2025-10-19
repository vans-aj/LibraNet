from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from flask_login import UserMixin
from . import SubscriptionTierEnum

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

    # Relationships
    loans = db.relationship('Loan', back_populates='student', lazy=True, cascade="all, delete-orphan")
    subscriptions = db.relationship('Subscription', back_populates='student', lazy=True, cascade="all, delete-orphan")

    # Password helpers
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    @property
    def current_subscription(self):
        """Get the current active subscription."""
        active_sub = [s for s in self.subscriptions if s.is_active and not s.is_expired]
        if active_sub:
            return sorted(active_sub, key=lambda x: x.start_date, reverse=True)[0]
        
        # If no active subscription, create a FREE one
        from .subscription import Subscription
        free_sub = Subscription(
            student_id=self.id,
            tier=SubscriptionTierEnum.FREE,
            is_active=True
        )
        db.session.add(free_sub)
        db.session.commit()
        return free_sub
    
    @property
    def subscription_tier(self):
        """Get current subscription tier."""
        return self.current_subscription.tier
    
    def has_access_to_ebooks(self):
        """Check if user can access ebooks (PRO or MAX)."""
        tier = self.subscription_tier
        return tier in [SubscriptionTierEnum.PRO, SubscriptionTierEnum.MAX]
    
    def has_access_to_audiobooks(self):
        """Check if user can access audiobooks (MAX only)."""
        tier = self.subscription_tier
        return tier == SubscriptionTierEnum.MAX
    
    def has_access_to_physical_books(self):
        """Check if user can access physical books (BASIC, PRO, MAX)."""
        tier = self.subscription_tier
        return tier in [SubscriptionTierEnum.BASIC, SubscriptionTierEnum.PRO, SubscriptionTierEnum.MAX]

    def __repr__(self) -> str:
        return f"<Student id={self.id} email={self.email}>"


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))