"""Console Notification Service Adapter

Console-based implementation of NotificationService for demonstration purposes.
This is an adapter - implements the port interface for external notification systems.
"""

from domain.entities.order import Order
from domain.entities.customer import Customer
from application.ports.services.notification_service import NotificationService


class ConsoleNotificationService(NotificationService):
    """Console-based notification service for demonstration"""
    
    def send_order_confirmation(self, order: Order, customer: Customer) -> bool:
        """Send order confirmation notification to customer
        
        Args:
            order: The confirmed order
            customer: The customer to notify
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        print(f"\n📧 [Notification] Order Confirmation sent to {customer.email}")
        print(f"   Dear {customer.name}, your order #{order.id} has been confirmed!")
        print(f"   Total: ${order.total_amount:.2f}")
        print(f"   Items:")
        for item in order.items:
            print(f"   - {item.product_name} x{item.quantity} @ ${item.unit_price:.2f}")
        if order.notes:
            print(f"   Notes: {order.notes}")
        return True
    
    def send_status_update(self, order: Order, customer: Customer) -> bool:
        """Send order status update notification to customer
        
        Args:
            order: The order with updated status
            customer: The customer to notify
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        print(f"\n📱 [Notification] Status update sent to {customer.phone}")
        print(f"   Order #{order.id} status: {order.status.value.upper()}")
        return True
    
    def send_delivery_notification(self, order: Order, customer: Customer) -> bool:
        """Send delivery notification to customer
        
        Args:
            order: The delivered order
            customer: The customer to notify
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        print(f"\n🚚 [Notification] Delivery notification sent to {customer.email}")
        print(f"   Your order #{order.id} has been delivered to {customer.address}")
        print(f"   Thank you for choosing our restaurant!")
        return True
    
    def send_order_cancelled(self, order: Order, customer: Customer) -> bool:
        """Send order cancellation notification to customer
        
        Args:
            order: The cancelled order
            customer: The customer to notify
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        print(f"\n❌ [Notification] Order cancellation sent to {customer.email}")
        print(f"   Dear {customer.name}, your order #{order.id} has been cancelled.")
        print(f"   If you paid for this order, a refund will be processed.")
        return True
