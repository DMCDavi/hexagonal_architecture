"""Mock Inventory Service Adapter

Mock implementation of InventoryService for demonstration purposes.
This is an adapter - implements the port interface for external inventory systems.
"""

from typing import Dict

from application.ports.services.inventory_service import InventoryService


class MockInventoryService(InventoryService):
    """Mock inventory service for demonstration"""
    
    def __init__(self):
        # Simulate inventory levels
        self._inventory: Dict[str, int] = {}
    
    def check_product_availability(self, product_id: str, quantity: int) -> bool:
        """Check if a product is available in the requested quantity
        
        Args:
            product_id: The ID of the product to check
            quantity: The quantity needed
            
        Returns:
            True if product is available in requested quantity, False otherwise
        """
        # Use domain default if product not in inventory
        from domain.entities.product import Product
        default_level = Product.DEFAULT_INVENTORY_LEVEL
        available_quantity = self._inventory.get(product_id, default_level)
        print(f"[Inventory] Checking availability for product {product_id}: {available_quantity} units available")
        return available_quantity >= quantity
    
    def reserve_products(self, product_quantities: Dict[str, int]) -> bool:
        """Reserve products for an order
        
        Args:
            product_quantities: Dictionary mapping product IDs to quantities
            
        Returns:
            True if all products were successfully reserved, False otherwise
        """
        print("[Inventory] Reserving products:")
        
        # Use domain default for inventory levels
        from domain.entities.product import Product
        default_level = Product.DEFAULT_INVENTORY_LEVEL
        
        # First, check if all products can be reserved
        for product_id, quantity in product_quantities.items():
            current = self._inventory.get(product_id, default_level)
            if current < quantity:
                print(f"   - Failed to reserve {quantity} units of product {product_id} (only {current} available)")
                return False
        
        # If all can be reserved, do the reservation
        for product_id, quantity in product_quantities.items():
            current = self._inventory.get(product_id, default_level)
            self._inventory[product_id] = current - quantity
            print(f"   - Reserved {quantity} units of product {product_id}")
        
        return True
    
    def release_products(self, product_quantities: Dict[str, int]) -> bool:
        """Release previously reserved products
        
        Args:
            product_quantities: Dictionary mapping product IDs to quantities
            
        Returns:
            True if products were successfully released, False otherwise
        """
        print("[Inventory] Releasing reserved products:")
        # Use domain default for inventory levels
        from domain.entities.product import Product
        default_level = Product.DEFAULT_INVENTORY_LEVEL
        
        for product_id, quantity in product_quantities.items():
            current = self._inventory.get(product_id, default_level)
            self._inventory[product_id] = current + quantity
            print(f"   - Released {quantity} units of product {product_id}")
        return True
    
    def get_available_quantity(self, product_id: str) -> int:
        """Get the available quantity for a specific product
        
        Args:
            product_id: The ID of the product
            
        Returns:
            The available quantity for the product
        """
        # Use domain default for inventory levels
        from domain.entities.product import Product
        default_level = Product.DEFAULT_INVENTORY_LEVEL
        
        quantity = self._inventory.get(product_id, default_level)
        print(f"[Inventory] Available quantity for product {product_id}: {quantity}")
        return quantity
    
    def update_stock(self, product_id: str, quantity_change: int) -> bool:
        """Update stock levels for a product
        
        Args:
            product_id: The ID of the product
            quantity_change: The change in quantity (positive for restocking, negative for consumption)
            
        Returns:
            True if stock was successfully updated, False otherwise
        """
        # Use domain default for inventory levels
        from domain.entities.product import Product
        default_level = Product.DEFAULT_INVENTORY_LEVEL
        
        current = self._inventory.get(product_id, default_level)
        new_quantity = current + quantity_change
        
        if new_quantity < 0:
            print(f"[Inventory] Cannot update stock for product {product_id}: would result in negative stock")
            return False
        
        self._inventory[product_id] = new_quantity
        operation = "Restocked" if quantity_change > 0 else "Consumed"
        print(f"[Inventory] {operation} {abs(quantity_change)} units for product {product_id}. New stock: {new_quantity}")
        return True
