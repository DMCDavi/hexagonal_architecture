"""In-Memory Customer Repository Adapter

Concrete implementation of CustomerRepository using in-memory storage.
This is an adapter - implements the port interface for external storage concerns.
"""

from typing import List, Optional, Dict

from domain.entities.customer import Customer
from application.ports.repositories.customer_repository import CustomerRepository


class InMemoryCustomerRepository(CustomerRepository):
    """In-memory implementation of customer repository"""
    
    def __init__(self):
        self._customers: Dict[str, Customer] = {}
    
    def save(self, customer: Customer) -> None:
        """Save a customer to the repository"""
        self._customers[customer.id] = customer
    
    def find_by_id(self, customer_id: str) -> Optional[Customer]:
        """Find a customer by their ID"""
        return self._customers.get(customer_id)
    
    def find_all(self) -> List[Customer]:
        """Find all customers"""
        return list(self._customers.values())
    
    def find_by_email(self, email: str) -> Optional[Customer]:
        """Find a customer by their email address"""
        for customer in self._customers.values():
            if customer.email.lower() == email.lower():
                return customer
        return None
    
    def exists_by_email(self, email: str) -> bool:
        """Check if a customer exists with the given email"""
        return self.find_by_email(email) is not None
    
    def delete(self, customer_id: str) -> None:
        """Delete a customer by their ID"""
        if customer_id in self._customers:
            del self._customers[customer_id]
