from enum import Enum
from datetime import datetime, timedelta

from enum import Enum
from datetime import datetime, timedelta

class LoanStatusEnum(Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"
    LOST = "lost"

class FineStatusEnum(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

class PaymentStatusEnum(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class SubscriptionTierEnum(Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    MAX = "max"