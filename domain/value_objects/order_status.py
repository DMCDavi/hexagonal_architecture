"""Order Status Value Object

Represents the different states an order can be in.
This is a value object - immutable and defined by its value.
"""

from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
