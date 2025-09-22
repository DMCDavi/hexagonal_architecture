"""Order Entity

Represents a customer order in the system.
This is an aggregate root - controls access to its OrderItems.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import uuid

from ..value_objects.order_status import OrderStatus
from .order_item import OrderItem
from .product import Product


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
        if not self.items:
            self.items = []
    
    @property
    def total_amount(self) -> float:
        """Calculate total order amount"""
        return sum(item.total_price for item in self.items)
    
    @property
    def total_items(self) -> int:
        """Get total number of items in the order"""
        return sum(item.quantity for item in self.items)
    
    def update_status(self, new_status: OrderStatus):
        """Update order status with business rules"""
        if not self._is_valid_status_transition(self.status, new_status):
            raise ValueError(f"Invalid status transition from {self.status.value} to {new_status.value}")
        
        self.status = new_status
        self.updated_at = datetime.now()
    
    def add_item(self, product: Product, quantity: int):
        """Add an item to the order"""
        if self.status != OrderStatus.PENDING:
            raise ValueError("Cannot modify order that is not pending")
        
        if not product.available:
            raise ValueError("Product is not available")
        
        # Check if product already exists in order
        existing_item = self._find_item_by_product_id(product.id)
        if existing_item:
            existing_item.update_quantity(existing_item.quantity + quantity)
        else:
            item = OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                unit_price=product.price
            )
            self.items.append(item)
        
        self.updated_at = datetime.now()
    
    def remove_item(self, product_id: str):
        """Remove an item from the order"""
        if self.status != OrderStatus.PENDING:
            raise ValueError("Cannot modify order that is not pending")
        
        self.items = [item for item in self.items if item.product_id != product_id]
        self.updated_at = datetime.now()
    
    def update_item_quantity(self, product_id: str, new_quantity: int):
        """Update quantity of a specific item"""
        if self.status != OrderStatus.PENDING:
            raise ValueError("Cannot modify order that is not pending")
        
        item = self._find_item_by_product_id(product_id)
        if not item:
            raise ValueError("Item not found in order")
        
        if new_quantity <= 0:
            self.remove_item(product_id)
        else:
            item.update_quantity(new_quantity)
        
        self.updated_at = datetime.now()
    
    def add_notes(self, notes: str):
        """Add or update order notes"""
        self.notes = notes
        self.updated_at = datetime.now()
    
    def can_be_cancelled(self) -> bool:
        """Check if order can be cancelled"""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    def cancel(self):
        """Cancel the order"""
        if not self.can_be_cancelled():
            raise ValueError("Order cannot be cancelled in current status")
        
        self.update_status(OrderStatus.CANCELLED)
    
    def _find_item_by_product_id(self, product_id: str) -> Optional[OrderItem]:
        """Find an item in the order by product ID"""
        for item in self.items:
            if item.product_id == product_id:
                return item
        return None
    
    def _is_valid_status_transition(self, current: OrderStatus, new: OrderStatus) -> bool:
        """Validate if status transition is allowed"""
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
            OrderStatus.PREPARING: [OrderStatus.READY, OrderStatus.CANCELLED],
            OrderStatus.READY: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],  # Final state
            OrderStatus.CANCELLED: []   # Final state
        }
        
        return new in valid_transitions.get(current, [])
