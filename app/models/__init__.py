from enum import Enum
from datetime import datetime, timedelta

class RoleEnum(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    GUEST = "guest"

class BookFormatEnum(Enum):
    PHYSICAL = "physical"
    EBOOK = "ebook"
    AUDIO = "audio"

class LoanStatusEnum(Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"
    LOST = "lost"

# Added FineStatusEnum used by app/models/fine.py
class FineStatusEnum(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

class PaymentStatusEnum(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

# for wild card import
__all__ = [ 
    "RoleEnum",
    "BookFormatEnum",
    "LoanStatusEnum",
    "FineStatusEnum",
    "PaymentStatusEnum",
    "datetime",
    "timedelta",
]