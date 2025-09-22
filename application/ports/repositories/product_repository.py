"""Product Repository Port

Interface for product data persistence.
This is a port - defines the contract for data access.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.product import Product


class ProductRepository(ABC):
    """Port for product data persistence"""
    
    @abstractmethod
    def save(self, product: Product) -> None:
        """Save a product to the repository"""
        pass
    
    @abstractmethod
    def find_by_id(self, product_id: str) -> Optional[Product]:
        """Find a product by its ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Product]:
        """Find all products"""
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[Product]:
        """Find all products in a specific category"""
        pass
    
    @abstractmethod
    def delete(self, product_id: str) -> None:
        """Delete a product by its ID"""
        pass
    
    @abstractmethod
    def find_available(self) -> List[Product]:
        """Find all available products"""
        pass
