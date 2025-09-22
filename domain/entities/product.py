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
    
    # Domain default values
    DEFAULT_INVENTORY_LEVEL = 100
    MIN_PRICE = 0.01
    
    def __post_init__(self):
        # Generate ID if not provided
        if not self.id:
            self.id = str(uuid.uuid4())
        
        # Apply business validation with defaults
        self._validate_and_normalize()
    
    def _validate_and_normalize(self):
        """Apply business rules and normalize data"""
        # Normalize strings
        if self.name:
            self.name = self.name.strip()
        if self.description:
            self.description = self.description.strip()
        if self.category:
            self.category = self.category.strip()
        
        # Business validation
        if not self.name:
            raise ValueError("Product name cannot be empty")
        
        if self.price <= 0:
            raise ValueError(f"Price must be greater than ${self.MIN_PRICE:.2f}")
        
        if not self.category:
            raise ValueError("Product category cannot be empty")
    
    @classmethod
    def create(cls, name: str, description: str, price: float, category: str) -> 'Product':
        """Factory method to create a new product with domain defaults"""
        return cls(
            id="",  # Will be auto-generated
            name=name,
            description=description,
            price=price,
            category=category,
            available=True  # Default availability
        )
    
    def make_unavailable(self):
        """Mark product as unavailable"""
        self.available = False
    
    def make_available(self):
        """Mark product as available"""
        self.available = True
    
    def update_price(self, new_price: float):
        """Update product price with validation"""
        if new_price <= 0:
            raise ValueError(f"Price must be greater than ${self.MIN_PRICE:.2f}")
        self.price = new_price
    
    def get_default_inventory_level(self) -> int:
        """Get the default inventory level for this product"""
        return self.DEFAULT_INVENTORY_LEVEL
