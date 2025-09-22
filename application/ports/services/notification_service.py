"""Notification Service Port

Interface for sending notifications to customers.
This is a port - defines the contract for external notification systems.
"""

from abc import ABC, abstractmethod

from domain.entities.order import Order
from domain.entities.customer import Customer


class NotificationService(ABC):
    """Port for sending notifications"""
    
    @abstractmethod
    def send_order_confirmation(self, order: Order, customer: Customer) -> bool:
        """Send order confirmation notification to customer
        
        Args:
            order: The confirmed order
            customer: The customer to notify
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def send_status_update(self, order: Order, customer: Customer) -> bool:
        """Send order status update notification to customer
        
        Args:
            order: The order with updated status
            customer: The customer to notify
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def send_delivery_notification(self, order: Order, customer: Customer) -> bool:
        """Send delivery notification to customer
        
        Args:
            order: The delivered order
            customer: The customer to notify
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def send_order_cancelled(self, order: Order, customer: Customer) -> bool:
        """Send order cancellation notification to customer
        
        Args:
            order: The cancelled order
            customer: The customer to notify
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        pass
