"""In-Memory Order Repository Adapter

Concrete implementation of OrderRepository using in-memory storage.
This is an adapter - implements the port interface for external storage concerns.
"""

from typing import List, Optional, Dict

from domain.entities.order import Order
from domain.value_objects.order_status import OrderStatus
from application.ports.repositories.order_repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory implementation of order repository"""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
    
    def save(self, order: Order) -> None:
        """Save an order to the repository"""
        self._orders[order.id] = order
    
    def find_by_id(self, order_id: str) -> Optional[Order]:
        """Find an order by its ID"""
        return self._orders.get(order_id)
    
    def find_all(self) -> List[Order]:
        """Find all orders"""
        return list(self._orders.values())
    
    def find_by_customer_id(self, customer_id: str) -> List[Order]:
        """Find all orders for a specific customer"""
        return [o for o in self._orders.values() if o.customer_id == customer_id]
    
    def find_by_status(self, status: OrderStatus) -> List[Order]:
        """Find all orders with a specific status"""
        return [o for o in self._orders.values() if o.status == status]
    
    def count_by_customer_id(self, customer_id: str) -> int:
        """Count orders for a specific customer"""
        return len(self.find_by_customer_id(customer_id))
