from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Product, Order, Customer


class ProductRepository(ABC):
    """Port for product data persistence"""
    
    @abstractmethod
    def save(self, product: Product) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, product_id: str) -> Optional[Product]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Product]:
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[Product]:
        pass
    
    @abstractmethod
    def delete(self, product_id: str) -> None:
        pass


class OrderRepository(ABC):
    """Port for order data persistence"""
    
    @abstractmethod
    def save(self, order: Order) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Order]:
        pass
    
    @abstractmethod
    def find_by_customer_id(self, customer_id: str) -> List[Order]:
        pass


class CustomerRepository(ABC):
    """Port for customer data persistence"""
    
    @abstractmethod
    def save(self, customer: Customer) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[Customer]:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Customer]:
        pass
