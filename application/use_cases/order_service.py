"""Order Service Use Case

Handles all order-related business operations.
This is an application service - orchestrates domain logic and external dependencies.
"""

from typing import List, Optional, Dict
from datetime import datetime

from domain.entities.order import Order
from domain.entities.order_item import OrderItem
from domain.value_objects.order_status import OrderStatus
from application.ports.repositories.order_repository import OrderRepository
from application.ports.repositories.product_repository import ProductRepository
from application.ports.repositories.customer_repository import CustomerRepository
from application.ports.services.payment_gateway import PaymentGateway
from application.ports.services.notification_service import NotificationService
from application.ports.services.inventory_service import InventoryService


class OrderService:
    """Application service for order management"""
    
    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        customer_repository: CustomerRepository,
        payment_gateway: PaymentGateway,
        notification_service: NotificationService,
        inventory_service: InventoryService
    ):
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._customer_repository = customer_repository
        self._payment_gateway = payment_gateway
        self._notification_service = notification_service
        self._inventory_service = inventory_service
    
    def create_order(self, customer_id: str, items: List[Dict], notes: Optional[str] = None) -> Optional[Order]:
        """Create a new order
        
        Args:
            customer_id: ID of the customer
            items: List of dicts with 'product_id' and 'quantity'
            notes: Optional order notes
        
        Returns:
            Created order or None if creation failed
        
        Raises:
            ValueError: If customer not found or invalid items
        """
        customer = self._customer_repository.find_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} not found")
        
        if not items:
            raise ValueError("Order must have at least one item")
        
        # Validate and prepare order items
        order_items = []
        product_quantities = {}
        
        for item_data in items:
            if 'product_id' not in item_data or 'quantity' not in item_data:
                raise ValueError("Each item must have product_id and quantity")
            
            product = self._product_repository.find_by_id(item_data['product_id'])
            if not product or not product.available:
                raise ValueError(f"Product {item_data['product_id']} not available")
            
            quantity = item_data['quantity']
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            
            if not self._inventory_service.check_product_availability(product.id, quantity):
                raise ValueError(f"Insufficient inventory for product {product.name}")
            
            order_items.append(OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                unit_price=product.price
            ))
            product_quantities[product.id] = quantity
        
        # Reserve inventory
        if not self._inventory_service.reserve_products(product_quantities):
            raise ValueError("Failed to reserve inventory")
        
        try:
            # Create order
            order = Order(
                id="",
                customer_id=customer_id,
                items=order_items,
                status=OrderStatus.PENDING,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                notes=notes
            )
            
            self._order_repository.save(order)
            return order
            
        except Exception:
            # Release inventory if order creation fails
            self._inventory_service.release_products(product_quantities)
            raise
    
    def confirm_order(self, order_id: str) -> bool:
        """Confirm an order by processing payment
        
        Args:
            order_id: The ID of the order to confirm
            
        Returns:
            True if order was confirmed successfully, False otherwise
        
        Raises:
            ValueError: If order not found or not in pending status
        """
        order = self._order_repository.find_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        if order.status != OrderStatus.PENDING:
            raise ValueError(f"Order {order_id} is not in pending status")
        
        customer = self._customer_repository.find_by_id(order.customer_id)
        if not customer:
            raise ValueError(f"Customer {order.customer_id} not found")
        
        # Process payment
        payment_result = self._payment_gateway.process_payment(order, customer)
        if not payment_result.success:
            # Release reserved inventory on payment failure
            product_quantities = {item.product_id: item.quantity for item in order.items}
            self._inventory_service.release_products(product_quantities)
            return False
        
        # Update order status
        order.update_status(OrderStatus.CONFIRMED)
        self._order_repository.save(order)
        
        # Send confirmation notification
        self._notification_service.send_order_confirmation(order, customer)
        
        return True
    
    def update_order_status(self, order_id: str, new_status: OrderStatus) -> bool:
        """Update order status and send notification
        
        Args:
            order_id: The ID of the order to update
            new_status: The new status to set
            
        Returns:
            True if status was updated successfully, False otherwise
            
        Raises:
            ValueError: If order not found or invalid status transition
        """
        order = self._order_repository.find_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        customer = self._customer_repository.find_by_id(order.customer_id)
        if not customer:
            raise ValueError(f"Customer {order.customer_id} not found")
        
        try:
            old_status = order.status
            order.update_status(new_status)
            self._order_repository.save(order)
            
            # Send status update notification
            self._notification_service.send_status_update(order, customer)
            
            # Special handling for delivery
            if new_status == OrderStatus.DELIVERED:
                self._notification_service.send_delivery_notification(order, customer)
            
            # Special handling for cancellation
            if new_status == OrderStatus.CANCELLED:
                self._notification_service.send_order_cancelled(order, customer)
                # Release inventory for cancelled orders
                if old_status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
                    product_quantities = {item.product_id: item.quantity for item in order.items}
                    self._inventory_service.release_products(product_quantities)
            
            return True
            
        except ValueError as e:
            raise ValueError(f"Failed to update order status: {str(e)}")
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order
        
        Args:
            order_id: The ID of the order to cancel
            
        Returns:
            True if order was cancelled successfully, False otherwise
        """
        order = self._order_repository.find_by_id(order_id)
        if not order:
            return False
        
        try:
            if not order.can_be_cancelled():
                return False
            
            order.cancel()
            self._order_repository.save(order)
            
            # Release inventory and notify customer
            return self.update_order_status(order_id, OrderStatus.CANCELLED)
            
        except Exception:
            return False
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID
        
        Args:
            order_id: The ID of the order to find
            
        Returns:
            The order if found, None otherwise
        """
        return self._order_repository.find_by_id(order_id)
    
    def get_orders_by_customer(self, customer_id: str) -> List[Order]:
        """Get all orders for a customer
        
        Args:
            customer_id: The ID of the customer
            
        Returns:
            List of orders for the customer
        """
        return self._order_repository.find_by_customer_id(customer_id)
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders
        
        Returns:
            List of all orders in the system
        """
        return self._order_repository.find_all()
    
    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Get all orders with a specific status
        
        Args:
            status: The order status to filter by
            
        Returns:
            List of orders with the specified status
        """
        return self._order_repository.find_by_status(status)
    
    def get_customer_order_count(self, customer_id: str) -> int:
        """Get the number of orders for a customer
        
        Args:
            customer_id: The ID of the customer
            
        Returns:
            Number of orders for the customer
        """
        return self._order_repository.count_by_customer_id(customer_id)
    
    def add_item_to_order(self, order_id: str, product_id: str, quantity: int) -> bool:
        """Add an item to an existing order
        
        Args:
            order_id: The ID of the order
            product_id: The ID of the product to add
            quantity: The quantity to add
            
        Returns:
            True if item was added successfully, False otherwise
        """
        order = self._order_repository.find_by_id(order_id)
        if not order:
            return False
        
        product = self._product_repository.find_by_id(product_id)
        if not product:
            return False
        
        try:
            # Check inventory availability
            if not self._inventory_service.check_product_availability(product_id, quantity):
                return False
            
            # Reserve additional inventory
            if not self._inventory_service.reserve_products({product_id: quantity}):
                return False
            
            order.add_item(product, quantity)
            self._order_repository.save(order)
            return True
            
        except Exception:
            return False
    
    def remove_item_from_order(self, order_id: str, product_id: str) -> bool:
        """Remove an item from an order
        
        Args:
            order_id: The ID of the order
            product_id: The ID of the product to remove
            
        Returns:
            True if item was removed successfully, False otherwise
        """
        order = self._order_repository.find_by_id(order_id)
        if not order:
            return False
        
        try:
            # Find the item to get quantity for inventory release
            item_to_remove = None
            for item in order.items:
                if item.product_id == product_id:
                    item_to_remove = item
                    break
            
            if not item_to_remove:
                return False
            
            order.remove_item(product_id)
            self._order_repository.save(order)
            
            # Release inventory
            self._inventory_service.release_products({product_id: item_to_remove.quantity})
            return True
            
        except Exception:
            return False
