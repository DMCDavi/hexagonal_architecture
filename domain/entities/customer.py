"""Customer Entity

Represents a customer in the system.
This is an entity - has identity and business logic.
"""

from dataclasses import dataclass
import uuid


@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: str
    address: str
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def update_contact_info(self, phone: str = None, address: str = None):
        """Update customer contact information"""
        if phone:
            self.phone = phone
        if address:
            self.address = address
    
    def update_email(self, new_email: str):
        """Update customer email"""
        if not new_email or '@' not in new_email:
            raise ValueError("Invalid email address")
        self.email = new_email
