from abc import ABC, abstractmethod
from domain.entities import Order, Customer, PaymentResult


class PaymentGateway(ABC):
    """Port for payment processing"""
    
    @abstractmethod
    def process_payment(self, order: Order, customer: Customer) -> PaymentResult:
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> PaymentResult:
        pass


class NotificationService(ABC):
    """Port for sending notifications"""
    
    @abstractmethod
    def send_order_confirmation(self, order: Order, customer: Customer) -> bool:
        pass
    
    @abstractmethod
    def send_status_update(self, order: Order, customer: Customer) -> bool:
        pass
    
    @abstractmethod
    def send_delivery_notification(self, order: Order, customer: Customer) -> bool:
        pass


class InventoryService(ABC):
    """Port for inventory management"""
    
    @abstractmethod
    def check_product_availability(self, product_id: str, quantity: int) -> bool:
        pass
    
    @abstractmethod
    def reserve_products(self, product_quantities: dict) -> bool:
        pass
    
    @abstractmethod
    def release_products(self, product_quantities: dict) -> bool:
        pass
