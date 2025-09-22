"""Product Entity

Represents a restaurant menu item.
This is an entity - has identity and business logic.
"""

from dataclasses import dataclass
import uuid


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
    
    def make_unavailable(self):
        """Mark product as unavailable"""
        self.available = False
    
    def make_available(self):
        """Mark product as available"""
        self.available = True
    
    def update_price(self, new_price: float):
        """Update product price"""
        if new_price <= 0:
            raise ValueError("Price must be positive")
        self.price = new_price
