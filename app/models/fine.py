# In app/models/fine.py

from app import db
from . import FineStatusEnum, datetime
from decimal import Decimal

class Fine(db.Model):
    """Model for fines associated with a loan."""
    __tablename__ = "fine"

    # Standard fine amount for physical books (₹200)
    STANDARD_FINE_AMOUNT = Decimal('200.00')

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    paid_amount = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    status = db.Column(db.Enum(FineStatusEnum), default=FineStatusEnum.PENDING, nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # --- Foreign Key (The physical database link) ---
    # A fine must be linked to exactly one loan.
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), unique=True, nullable=False)

    # --- Relationship (The Python shortcut) ---
    loan = db.relationship('Loan', back_populates='fine')
    
    @classmethod
    def create_standard_fine(cls, loan_id):
        """
        Create a standard fine of ₹200 for a physical book loan.
        
        Args:
            loan_id: ID of the loan to create fine for
            
        Returns:
            Fine instance with standard amount
        """
        return cls(
            loan_id=loan_id,
            amount=cls.STANDARD_FINE_AMOUNT,
            status=FineStatusEnum.PENDING
        )

    @property
    def balance(self):
        """
        Calculated property to get the outstanding balance.
        This is NOT a database column.
        """
        return self.amount - self.paid_amount

    def __repr__(self):
        """Provides a developer-friendly representation of the fine object."""
        return f"<Fine id={self.id} loan_id={self.loan_id} amount={self.amount}>"