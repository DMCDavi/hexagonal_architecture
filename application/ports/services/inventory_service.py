"""Inventory Service Port

Interface for inventory management services.
This is a port - defines the contract for external inventory systems.
"""

from abc import ABC, abstractmethod
from typing import Dict


class InventoryService(ABC):
    """Port for inventory management"""
    
    @abstractmethod
    def check_product_availability(self, product_id: str, quantity: int) -> bool:
        """Check if a product is available in the requested quantity
        
        Args:
            product_id: The ID of the product to check
            quantity: The quantity needed
            
        Returns:
            True if product is available in requested quantity, False otherwise
        """
        pass
    
    @abstractmethod
    def reserve_products(self, product_quantities: Dict[str, int]) -> bool:
        """Reserve products for an order
        
        Args:
            product_quantities: Dictionary mapping product IDs to quantities
            
        Returns:
            True if all products were successfully reserved, False otherwise
        """
        pass
    
    @abstractmethod
    def release_products(self, product_quantities: Dict[str, int]) -> bool:
        """Release previously reserved products
        
        Args:
            product_quantities: Dictionary mapping product IDs to quantities
            
        Returns:
            True if products were successfully released, False otherwise
        """
        pass
    
    @abstractmethod
    def get_available_quantity(self, product_id: str) -> int:
        """Get the available quantity for a specific product
        
        Args:
            product_id: The ID of the product
            
        Returns:
            The available quantity for the product
        """
        pass
    
    @abstractmethod
    def update_stock(self, product_id: str, quantity_change: int) -> bool:
        """Update stock levels for a product
        
        Args:
            product_id: The ID of the product
            quantity_change: The change in quantity (positive for restocking, negative for consumption)
            
        Returns:
            True if stock was successfully updated, False otherwise
        """
        pass
