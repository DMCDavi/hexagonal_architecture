"""Customer Entity

Represents a customer in the system.
This is an entity - has identity and business logic.
"""

from dataclasses import dataclass
import uuid
import re


@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: str
    address: str
    
    def __post_init__(self):
        # Generate ID if not provided
        if not self.id:
            self.id = str(uuid.uuid4())
        
        # Apply domain validation and normalization
        self._validate_and_normalize()
    
    @classmethod
    def create(cls, name: str, email: str, phone: str, address: str) -> 'Customer':
        """Factory method to create a new customer with domain defaults"""
        return cls(
            id="",  # Will be auto-generated
            name=name,
            email=email,
            phone=phone,
            address=address
        )
    
    def _validate_and_normalize(self):
        """Apply business rules validation and normalize data"""
        # Normalize strings
        if self.name:
            self.name = self.name.strip()
        if self.email:
            self.email = self.email.strip().lower()
        if self.phone:
            self.phone = self.phone.strip()
        if self.address:
            self.address = self.address.strip()
        
        # Business validation
        if not self.name:
            raise ValueError("Customer name cannot be empty")
        
        if not self._is_valid_email(self.email):
            raise ValueError("Invalid email address format")
        
        if not self.phone:
            raise ValueError("Phone number cannot be empty")
        
        if not self.address:
            raise ValueError("Address cannot be empty")
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format using domain business rules"""
        if not email:
            return False
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    def update_contact_info(self, phone: str = None, address: str = None):
        """Update customer contact information with validation"""
        if phone:
            phone = phone.strip()
            if not phone:
                raise ValueError("Phone number cannot be empty")
            self.phone = phone
        
        if address:
            address = address.strip()
            if not address:
                raise ValueError("Address cannot be empty")
            self.address = address
    
    def update_email(self, new_email: str):
        """Update customer email with validation"""
        if not new_email:
            raise ValueError("Email cannot be empty")
        
        new_email = new_email.strip().lower()
        if not self._is_valid_email(new_email):
            raise ValueError("Invalid email address format")
        
        self.email = new_email
