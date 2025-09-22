"""Mock Payment Gateway Adapter

Mock implementation of PaymentGateway for demonstration purposes.
This is an adapter - implements the port interface for external payment systems.
"""

import random
import uuid

from domain.entities.order import Order
from domain.entities.customer import Customer
from domain.value_objects.payment_result import PaymentResult
from application.ports.services.payment_gateway import PaymentGateway


class MockPaymentGateway(PaymentGateway):
    """Mock implementation of payment gateway for demonstration"""
    
    def process_payment(self, order: Order, customer: Customer) -> PaymentResult:
        """Process payment for an order
        
        Args:
            order: The order to process payment for
            customer: The customer making the payment
            
        Returns:
            PaymentResult indicating success/failure and transaction details
        """
        # Simulate payment processing
        print(f"[Payment Gateway] Processing payment for Order {order.id}")
        print(f"[Payment Gateway] Amount: ${order.total_amount:.2f}")
        print(f"[Payment Gateway] Customer: {customer.name}")
        
        # Simulate 90% success rate
        if random.random() > 0.1:
            transaction_id = str(uuid.uuid4())
            print(f"[Payment Gateway] Payment successful! Transaction ID: {transaction_id}")
            return PaymentResult(success=True, transaction_id=transaction_id)
        else:
            print("[Payment Gateway] Payment failed: Insufficient funds")
            return PaymentResult(success=False, error_message="Insufficient funds")
    
    def refund_payment(self, transaction_id: str, amount: float) -> PaymentResult:
        """Process a refund for a previous payment
        
        Args:
            transaction_id: The original transaction ID to refund
            amount: The amount to refund
            
        Returns:
            PaymentResult indicating refund success/failure
        """
        print(f"[Payment Gateway] Processing refund for transaction {transaction_id}")
        print(f"[Payment Gateway] Refund amount: ${amount:.2f}")
        
        # Simulate successful refund
        refund_id = str(uuid.uuid4())
        print(f"[Payment Gateway] Refund successful! Refund ID: {refund_id}")
        return PaymentResult(success=True, transaction_id=refund_id)
    
    def verify_payment(self, transaction_id: str) -> bool:
        """Verify if a payment transaction was successful
        
        Args:
            transaction_id: The transaction ID to verify
            
        Returns:
            True if payment is verified, False otherwise
        """
        print(f"[Payment Gateway] Verifying transaction {transaction_id}")
        # Simulate verification (90% success rate)
        is_verified = random.random() > 0.1
        print(f"[Payment Gateway] Transaction verification: {'Success' if is_verified else 'Failed'}")
        return is_verified
