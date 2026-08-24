from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class FailureReason(str, Enum):
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    GATEWAY_TIMEOUT = "GATEWAY_TIMEOUT"
    CARD_EXPIRED = "CARD_EXPIRED"
    MANDATE_DECLINED = "MANDATE_DECLINED"

class TransactionState(BaseModel):
    payment_id: str
    customer_id: str
    amount: float
    failure_reason: FailureReason
    contact_attempts: int = 0
    max_attempts: int = Field(default=3, description="Hard compliance limit")
    retry_scheduled_at: Optional[str] = None
    applied_discount_percent: float = 0.0
    status: str = "PENDING"
    audit_trail: List[str] = []
    