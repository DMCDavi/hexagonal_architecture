"""In-Memory Product Repository Adapter

Concrete implementation of ProductRepository using in-memory storage.
This is an adapter - implements the port interface for external storage concerns.
"""

from typing import List, Optional, Dict

from domain.entities.product import Product
from application.ports.repositories.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    """In-memory implementation of product repository"""
    
    def __init__(self):
        self._products: Dict[str, Product] = {}
    
    def save(self, product: Product) -> None:
        """Save a product to the repository"""
        self._products[product.id] = product
    
    def find_by_id(self, product_id: str) -> Optional[Product]:
        """Find a product by its ID"""
        return self._products.get(product_id)
    
    def find_all(self) -> List[Product]:
        """Find all products"""
        return list(self._products.values())
    
    def find_by_category(self, category: str) -> List[Product]:
        """Find all products in a specific category"""
        return [p for p in self._products.values() if p.category == category]
    
    def delete(self, product_id: str) -> None:
        """Delete a product by its ID"""
        if product_id in self._products:
            del self._products[product_id]
    
    def find_available(self) -> List[Product]:
        """Find all available products"""
        return [p for p in self._products.values() if p.available]
