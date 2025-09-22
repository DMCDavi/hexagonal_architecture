import random
import uuid
from domain.entities import Order, Customer, PaymentResult
from ports.services import PaymentGateway, NotificationService, InventoryService


class MockPaymentGateway(PaymentGateway):
    """Mock implementation of payment gateway for demonstration"""
    
    def process_payment(self, order: Order, customer: Customer) -> PaymentResult:
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
        print(f"[Payment Gateway] Processing refund for transaction {transaction_id}")
        print(f"[Payment Gateway] Refund amount: ${amount:.2f}")
        
        # Simulate successful refund
        refund_id = str(uuid.uuid4())
        print(f"[Payment Gateway] Refund successful! Refund ID: {refund_id}")
        return PaymentResult(success=True, transaction_id=refund_id)


class ConsoleNotificationService(NotificationService):
    """Console-based notification service for demonstration"""
    
    def send_order_confirmation(self, order: Order, customer: Customer) -> bool:
        print(f"\n📧 [Notification] Order Confirmation sent to {customer.email}")
        print(f"   Dear {customer.name}, your order #{order.id} has been confirmed!")
        print(f"   Total: ${order.total_amount:.2f}")
        print(f"   Items:")
        for item in order.items:
            print(f"   - {item.product_name} x{item.quantity} @ ${item.unit_price:.2f}")
        return True
    
    def send_status_update(self, order: Order, customer: Customer) -> bool:
        print(f"\n📱 [Notification] Status update sent to {customer.phone}")
        print(f"   Order #{order.id} status: {order.status.value.upper()}")
        return True
    
    def send_delivery_notification(self, order: Order, customer: Customer) -> bool:
        print(f"\n🚚 [Notification] Delivery notification sent to {customer.email}")
        print(f"   Your order #{order.id} has been delivered to {customer.address}")
        return True


class MockInventoryService(InventoryService):
    """Mock inventory service for demonstration"""
    
    def __init__(self):
        # Simulate inventory levels
        self._inventory = {}
    
    def check_product_availability(self, product_id: str, quantity: int) -> bool:
        # Simulate inventory check
        available_quantity = self._inventory.get(product_id, 100)  # Default 100 units
        print(f"[Inventory] Checking availability for product {product_id}: {available_quantity} units available")
        return available_quantity >= quantity
    
    def reserve_products(self, product_quantities: dict) -> bool:
        print("[Inventory] Reserving products:")
        for product_id, quantity in product_quantities.items():
            current = self._inventory.get(product_id, 100)
            if current >= quantity:
                self._inventory[product_id] = current - quantity
                print(f"   - Reserved {quantity} units of product {product_id}")
            else:
                print(f"   - Failed to reserve {quantity} units of product {product_id} (only {current} available)")
                return False
        return True
    
    def release_products(self, product_quantities: dict) -> bool:
        print("[Inventory] Releasing reserved products:")
        for product_id, quantity in product_quantities.items():
            current = self._inventory.get(product_id, 100)
            self._inventory[product_id] = current + quantity
            print(f"   - Released {quantity} units of product {product_id}")
        return True
