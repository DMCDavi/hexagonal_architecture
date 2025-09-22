"""Customer Repository Port

Interface for customer data persistence.
This is a port - defines the contract for data access.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.customer import Customer


class CustomerRepository(ABC):
    """Port for customer data persistence"""
    
    @abstractmethod
    def save(self, customer: Customer) -> None:
        """Save a customer to the repository"""
        pass
    
    @abstractmethod
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        """Find a customer by their ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Customer]:
        """Find all customers"""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Customer]:
        """Find a customer by their email address"""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Check if a customer exists with the given email"""
        pass
    
    @abstractmethod
    def delete(self, customer_id: str) -> None:
        """Delete a customer by their ID"""
        pass
