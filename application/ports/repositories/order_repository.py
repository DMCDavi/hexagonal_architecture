"""Order Repository Port

Interface for order data persistence.
This is a port - defines the contract for data access.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.order import Order
from domain.value_objects.order_status import OrderStatus


class OrderRepository(ABC):
    """Port for order data persistence"""
    
    @abstractmethod
    def save(self, order: Order) -> None:
        """Save an order to the repository"""
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        """Find an order by its ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Order]:
        """Find all orders"""
        pass
    
    @abstractmethod
    def find_by_customer_id(self, customer_id: str) -> List[Order]:
        """Find all orders for a specific customer"""
        pass
    
    @abstractmethod
    def find_by_status(self, status: OrderStatus) -> List[Order]:
        """Find all orders with a specific status"""
        pass
    
    @abstractmethod
    def count_by_customer_id(self, customer_id: str) -> int:
        """Count orders for a specific customer"""
        pass
