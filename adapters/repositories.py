from typing import List, Optional, Dict
from domain.entities import Product, Order, Customer
from ports.repositories import ProductRepository, OrderRepository, CustomerRepository


class InMemoryProductRepository(ProductRepository):
    """In-memory implementation of product repository"""
    
    def __init__(self):
        self._products: Dict[str, Product] = {}
    
    def save(self, product: Product) -> None:
        self._products[product.id] = product
    
    def find_by_id(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)
    
    def find_all(self) -> List[Product]:
        return list(self._products.values())
    
    def find_by_category(self, category: str) -> List[Product]:
        return [p for p in self._products.values() if p.category == category]
    
    def delete(self, product_id: str) -> None:
        if product_id in self._products:
            del self._products[product_id]


class InMemoryOrderRepository(OrderRepository):
    """In-memory implementation of order repository"""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
    
    def save(self, order: Order) -> None:
        self._orders[order.id] = order
    
    def find_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
    
    def find_all(self) -> List[Order]:
        return list(self._orders.values())
    
    def find_by_customer_id(self, customer_id: str) -> List[Order]:
        return [o for o in self._orders.values() if o.customer_id == customer_id]


class InMemoryCustomerRepository(CustomerRepository):
    """In-memory implementation of customer repository"""
    
    def __init__(self):
        self._customers: Dict[str, Customer] = {}
    
    def save(self, customer: Customer) -> None:
        self._customers[customer.id] = customer
    
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        return self._customers.get(customer_id)
    
    def find_all(self) -> List[Customer]:
        return list(self._customers.values())
    
    def find_by_email(self, email: str) -> Optional[Customer]:
        for customer in self._customers.values():
            if customer.email == email:
                return customer
        return None
