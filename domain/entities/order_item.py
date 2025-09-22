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
    
    # Domain default values and constants
    MIN_QUANTITY = 1
    MAX_QUANTITY = 99
    MIN_UNIT_PRICE = 0.01
    MAX_DISCOUNT_PERCENTAGE = 50.0
    
    def __post_init__(self):
        # Apply domain validation
        self._validate_order_item()
        
        # Normalize data
        self._normalize_data()
    
    @classmethod
    def create(cls, product_id: str, product_name: str, quantity: int, unit_price: float) -> 'OrderItem':
        """Factory method to create a new order item with domain defaults"""
        return cls(
            product_id=product_id,
            product_name=product_name,
            quantity=max(quantity, cls.MIN_QUANTITY),  # Ensure minimum quantity
            unit_price=max(unit_price, cls.MIN_UNIT_PRICE)  # Ensure minimum price
        )
    
    def _validate_order_item(self):
        """Apply domain business rules validation"""
        if not self.product_id:
            raise ValueError("Product ID cannot be empty")
        
        if not self.product_name:
            raise ValueError("Product name cannot be empty")
        
        if self.quantity < self.MIN_QUANTITY:
            raise ValueError(f"Quantity must be at least {self.MIN_QUANTITY}")
        
        if self.quantity > self.MAX_QUANTITY:
            raise ValueError(f"Quantity cannot exceed {self.MAX_QUANTITY}")
        
        if self.unit_price < self.MIN_UNIT_PRICE:
            raise ValueError(f"Unit price must be at least ${self.MIN_UNIT_PRICE:.2f}")
    
    def _normalize_data(self):
        """Normalize data according to domain rules"""
        if self.product_name:
            self.product_name = self.product_name.strip()
    
    @property
    def total_price(self) -> float:
        """Calculate total price for this item"""
        return round(self.quantity * self.unit_price, 2)
    
    def update_quantity(self, new_quantity: int):
        """Update the quantity of this item with validation"""
        if new_quantity < self.MIN_QUANTITY:
            raise ValueError(f"Quantity must be at least {self.MIN_QUANTITY}")
        
        if new_quantity > self.MAX_QUANTITY:
            raise ValueError(f"Quantity cannot exceed {self.MAX_QUANTITY}")
        
        self.quantity = new_quantity
    
    def apply_discount(self, discount_percentage: float):
        """Apply a discount to the unit price with business rules"""
        if discount_percentage < 0:
            raise ValueError("Discount percentage cannot be negative")
        
        if discount_percentage > self.MAX_DISCOUNT_PERCENTAGE:
            raise ValueError(f"Discount percentage cannot exceed {self.MAX_DISCOUNT_PERCENTAGE}%")
        
        discount_amount = self.unit_price * (discount_percentage / 100)
        new_price = self.unit_price - discount_amount
        
        # Ensure discounted price doesn't go below minimum
        if new_price < self.MIN_UNIT_PRICE:
            new_price = self.MIN_UNIT_PRICE
        
        self.unit_price = round(new_price, 2)
    
    def can_apply_discount(self, discount_percentage: float) -> bool:
        """Check if a discount can be applied without violating business rules"""
        if discount_percentage < 0 or discount_percentage > self.MAX_DISCOUNT_PERCENTAGE:
            return False
        
        discount_amount = self.unit_price * (discount_percentage / 100)
        new_price = self.unit_price - discount_amount
        
        return new_price >= self.MIN_UNIT_PRICE
