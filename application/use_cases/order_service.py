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
    
    def create_order_item(self, product_id: str, quantity: int) -> Optional[OrderItem]:
        """Create a new order item
        
        Args:
            product_id: ID of the product
            quantity: quantity of the product
        
        Returns:
            Created order item or None if creation failed
        """
        product = self._product_repository.find_by_id(product_id)
        if not product or not product.available:
            print(f"Product {product_id} not available")
            return None
        
        if not self._inventory_service.check_product_availability(product.id, quantity):
            print(f"Insufficient inventory for product {product.name}")
            return None
        
        # Use domain factory method that handles validation and defaults
        try:
            return OrderItem.create(
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                unit_price=product.price
            )
        except ValueError as e:
            print(f"Failed to create order item: {e}")
            return None
    
    def create_order(self, customer_id: str, items: List[dict], notes: Optional[str] = None) -> Optional[Order]:
        """Create a new order
        
        Args:
            customer_id: ID of the customer
            items: List of dicts with 'product_id' and 'quantity'
            notes: Optional order notes
        
        Returns:
            Created order or None if creation failed
        """
        customer = self._customer_repository.find_by_id(customer_id)
        if not customer:
            print(f"Customer with ID {customer_id} not found")
            return None
        
        # Validate and prepare order items
        order_items = []
        product_quantities = {}
        
        for item_data in items:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            order_items.append(self.create_order_item(product_id, quantity))
        
        # Reserve inventory
        if not self._inventory_service.reserve_products(product_quantities):
            print("Failed to reserve inventory")
            return None
        
        # Use domain factory method that handles defaults and validation
        order = Order.create_new(customer_id, notes)
        
        # Add items to the order
        order.items = [item for item in order_items if item is not None]
        
        self._order_repository.save(order)
        print(f"Order {order.id} created successfully")
        return order
    
    def confirm_order(self, order_id: str) -> bool:
        """Confirm an order by processing payment"""
        order = self._order_repository.find_by_id(order_id)
        if not order:
            print(f"Order {order_id} not found")
            return False
        
        if order.status != OrderStatus.PENDING:
            print(f"Order {order_id} is not in pending status")
            return False
        
        customer = self._customer_repository.find_by_id(order.customer_id)
        if not customer:
            print(f"Customer {order.customer_id} not found")
            return False
        
        # Process payment
        payment_result = self._payment_gateway.process_payment(order, customer)
        if not payment_result.success:
            print(f"Payment failed: {payment_result.error_message}")
            # Release reserved inventory
            product_quantities = {item.product_id: item.quantity for item in order.items}
            self._inventory_service.release_products(product_quantities)
            return False
        
        # Update order status
        order.update_status(OrderStatus.CONFIRMED)
        self._order_repository.save(order)
        
        # Send confirmation notification
        self._notification_service.send_order_confirmation(order, customer)
        
        print(f"Order {order_id} confirmed successfully")
        return True
    
    def update_order_status(self, order_id: str, new_status: OrderStatus) -> bool:
        """Update order status and send notification"""
        order = self._order_repository.find_by_id(order_id)
        if not order:
            print(f"Order {order_id} not found")
            return False
        
        customer = self._customer_repository.find_by_id(order.customer_id)
        if not customer:
            print(f"Customer {order.customer_id} not found")
            return False
        
        old_status = order.status
        order.update_status(new_status)
        self._order_repository.save(order)
        
        # Send status update notification
        self._notification_service.send_status_update(order, customer)
        
        # Special handling for delivery
        if new_status == OrderStatus.DELIVERED:
            self._notification_service.send_delivery_notification(order, customer)
        
        print(f"Order {order_id} status updated from {old_status.value} to {new_status.value}")
        return True
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        return self._order_repository.find_by_id(order_id)
    
    def get_orders_by_customer(self, customer_id: str) -> List[Order]:
        """Get all orders for a customer"""
        return self._order_repository.find_by_customer_id(customer_id)
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        return self._order_repository.find_all()
