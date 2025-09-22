"""Order Item Entity

Represents an item within an order.
This is an entity - has business logic and behavior.
"""

from dataclasses import dataclass


@dataclass
class OrderItem:
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")
    
    @property
    def total_price(self) -> float:
        """Calculate total price for this item"""
        return self.quantity * self.unit_price
    
    def update_quantity(self, new_quantity: int):
        """Update the quantity of this item"""
        if new_quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.quantity = new_quantity
    
    def apply_discount(self, discount_percentage: float):
        """Apply a discount to the unit price"""
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        discount_amount = self.unit_price * (discount_percentage / 100)
        self.unit_price -= discount_amount
