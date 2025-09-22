"""Payment Result Value Object

Represents the result of a payment operation.
This is a value object - immutable and defined by its value.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentResult:
    success: bool
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None
