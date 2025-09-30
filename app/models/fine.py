from app import db
from . import FineStatusEnum, datetime

class Fine(db.Model):
    """Model for fines associated with a loan."""

    __tablename__ = "fine"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False) # e.g., can store up to 99999999.99
    paid_amount = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    status = db.Column(db.Enum(FineStatusEnum), default=FineStatusEnum.PENDING, nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # --- Foreign Key ---
    # A fine must be linked to exactly one loan. 'unique=True' enforces this.
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), unique=True, nullable=False)

    # --- Relationship ---
    loan = db.relationship('Loan', back_populates='fine')

    @property
    def balance(self):
        """Calculated property to get the outstanding balance."""
        return self.amount - self.paid_amount

    def __repr__(self) -> str:
        return f"<Fine id={self.id} loan_id={self.loan_id} amount={self.amount}>"