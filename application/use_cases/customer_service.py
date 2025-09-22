"""Customer Service Use Case

Handles all customer-related business operations.
This is an application service - orchestrates domain logic and external dependencies.
"""

from typing import List, Optional
import re

from domain.entities.customer import Customer
from application.ports.repositories.customer_repository import CustomerRepository


class CustomerService:
    """Application service for customer management"""
    
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository
    
    def register_customer(self, name: str, email: str, phone: str, address: str) -> Customer:
        """Register a new customer
        
        Args:
            name: Customer name
            email: Customer email address
            phone: Customer phone number
            address: Customer address
            
        Returns:
            The registered customer (existing or newly created)
            
        Raises:
            ValueError: If email format is invalid
        """
        # Validate email format
        if not self._is_valid_email(email):
            raise ValueError("Invalid email address format")
        
        # Validate required fields
        if not name.strip():
            raise ValueError("Customer name cannot be empty")
        
        if not phone.strip():
            raise ValueError("Phone number cannot be empty")
        
        if not address.strip():
            raise ValueError("Address cannot be empty")
        
        # Check if customer already exists
        existing = self._customer_repository.find_by_email(email.lower())
        if existing:
            return existing
        
        customer = Customer(
            id="",
            name=name.strip(),
            email=email.lower(),
            phone=phone.strip(),
            address=address.strip()
        )
        self._customer_repository.save(customer)
        return customer
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Find customer by email
        
        Args:
            email: The email address to search for
            
        Returns:
            The customer if found, None otherwise
        """
        return self._customer_repository.find_by_email(email.lower())
    
    def get_customer_by_id(self, customer_id: str) -> Optional[Customer]:
        """Find customer by ID
        
        Args:
            customer_id: The customer ID to search for
            
        Returns:
            The customer if found, None otherwise
        """
        return self._customer_repository.find_by_id(customer_id)
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers
        
        Returns:
            List of all customers
        """
        return self._customer_repository.find_all()
    
    def update_customer_contact(self, customer_id: str, phone: str = None, address: str = None) -> bool:
        """Update customer contact information
        
        Args:
            customer_id: The ID of the customer to update
            phone: New phone number (optional)
            address: New address (optional)
            
        Returns:
            True if update was successful, False otherwise
        """
        customer = self._customer_repository.find_by_id(customer_id)
        if not customer:
            return False
        
        try:
            customer.update_contact_info(phone, address)
            self._customer_repository.save(customer)
            return True
        except ValueError:
            return False
    
    def update_customer_email(self, customer_id: str, new_email: str) -> bool:
        """Update customer email address
        
        Args:
            customer_id: The ID of the customer to update
            new_email: The new email address
            
        Returns:
            True if update was successful, False otherwise
        """
        if not self._is_valid_email(new_email):
            return False
        
        # Check if email is already taken
        if self._customer_repository.exists_by_email(new_email.lower()):
            return False
        
        customer = self._customer_repository.find_by_id(customer_id)
        if not customer:
            return False
        
        try:
            customer.update_email(new_email.lower())
            self._customer_repository.save(customer)
            return True
        except ValueError:
            return False
    
    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer
        
        Args:
            customer_id: The ID of the customer to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        customer = self._customer_repository.find_by_id(customer_id)
        if not customer:
            return False
        
        self._customer_repository.delete(customer_id)
        return True
    
    def customer_exists(self, email: str) -> bool:
        """Check if a customer exists with the given email
        
        Args:
            email: The email address to check
            
        Returns:
            True if customer exists, False otherwise
        """
        return self._customer_repository.exists_by_email(email.lower())
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format
        
        Args:
            email: The email address to validate
            
        Returns:
            True if email format is valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))
