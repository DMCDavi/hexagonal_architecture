from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import uuid


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class Product:
    id: str
    name: str
    description: str
    price: float
    category: str
    available: bool = True
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class OrderItem:
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: str
    address: str
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class Order:
    id: str
    customer_id: str
    items: List[OrderItem]
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()
    
    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items)
    
    def update_status(self, new_status: OrderStatus):
        self.status = new_status
        self.updated_at = datetime.now()
    
    def add_item(self, product: Product, quantity: int):
        item = OrderItem(
            product_id=product.id,
            product_name=product.name,
            quantity=quantity,
            unit_price=product.price
        )
        self.items.append(item)
        self.updated_at = datetime.now()


@dataclass
class PaymentResult:
    success: bool
    transaction_id: Optional[str] = None
    error_message: Optional[str] = None
