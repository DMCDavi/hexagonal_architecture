"""Product Service Use Case

Handles all product-related business operations.
This is an application service - orchestrates domain logic and external dependencies.
"""

from typing import List, Optional

from domain.entities.product import Product
from application.ports.repositories.product_repository import ProductRepository


class ProductService:
    """Application service for product management"""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    def add_product(self, name: str, description: str, price: float, category: str) -> Product:
        """Add a new product to the menu
        
        Args:
            name: Product name
            description: Product description
            price: Product price
            category: Product category
            
        Returns:
            The created product
            
        Raises:
            ValueError: If validation fails (handled by domain entity)
        """
        # Use domain factory method that handles validation and defaults
        product = Product.create(name, description, price, category)
        self._product_repository.save(product)
        return product
    
    def get_all_products(self) -> List[Product]:
        """Get all available products
        
        Returns:
            List of all available products
        """
        return self._product_repository.find_available()
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category
        
        Args:
            category: The category to filter by
            
        Returns:
            List of available products in the specified category
        """
        products = self._product_repository.find_by_category(category)
        return [p for p in products if p.available]
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a specific product by ID
        
        Args:
            product_id: The ID of the product to find
            
        Returns:
            The product if found, None otherwise
        """
        return self._product_repository.find_by_id(product_id)
    
    def update_product_price(self, product_id: str, new_price: float) -> bool:
        """Update product price
        
        Args:
            product_id: The ID of the product to update
            new_price: The new price
            
        Returns:
            True if update was successful, False otherwise
        """
        product = self._product_repository.find_by_id(product_id)
        if not product:
            return False
        
        try:
            product.update_price(new_price)
            self._product_repository.save(product)
            return True
        except ValueError:
            return False
    
    def make_product_unavailable(self, product_id: str) -> bool:
        """Make a product unavailable
        
        Args:
            product_id: The ID of the product to make unavailable
            
        Returns:
            True if update was successful, False otherwise
        """
        product = self._product_repository.find_by_id(product_id)
        if not product:
            return False
        
        product.make_unavailable()
        self._product_repository.save(product)
        return True
    
    def make_product_available(self, product_id: str) -> bool:
        """Make a product available
        
        Args:
            product_id: The ID of the product to make available
            
        Returns:
            True if update was successful, False otherwise
        """
        product = self._product_repository.find_by_id(product_id)
        if not product:
            return False
        
        product.make_available()
        self._product_repository.save(product)
        return True
    
    def delete_product(self, product_id: str) -> bool:
        """Delete a product
        
        Args:
            product_id: The ID of the product to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        product = self._product_repository.find_by_id(product_id)
        if not product:
            return False
        
        self._product_repository.delete(product_id)
        return True
    
    def get_categories(self) -> List[str]:
        """Get all unique product categories
        
        Returns:
            List of all unique categories
        """
        all_products = self._product_repository.find_all()
        categories = set(product.category for product in all_products)
        return sorted(list(categories))
