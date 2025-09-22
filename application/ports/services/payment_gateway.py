"""Payment Gateway Port

Interface for payment processing services.
This is a port - defines the contract for external payment systems.
"""

from abc import ABC, abstractmethod

from domain.entities.order import Order
from domain.entities.customer import Customer
from domain.value_objects.payment_result import PaymentResult


class PaymentGateway(ABC):
    """Port for payment processing"""
    
    @abstractmethod
    def process_payment(self, order: Order, customer: Customer) -> PaymentResult:
        """Process payment for an order
        
        Args:
            order: The order to process payment for
            customer: The customer making the payment
            
        Returns:
            PaymentResult indicating success/failure and transaction details
        """
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> PaymentResult:
        """Process a refund for a previous payment
        
        Args:
            transaction_id: The original transaction ID to refund
            amount: The amount to refund
            
        Returns:
            PaymentResult indicating refund success/failure
        """
        pass
    
    @abstractmethod
    def verify_payment(self, transaction_id: str) -> bool:
        """Verify if a payment transaction was successful
        
        Args:
            transaction_id: The transaction ID to verify
            
        Returns:
            True if payment is verified, False otherwise
        """
        pass
