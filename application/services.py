from typing import List, Optional
from datetime import datetime
from domain.entities import Product, Order, Customer, OrderStatus, OrderItem
from ports.repositories import ProductRepository, OrderRepository, CustomerRepository
from ports.services import PaymentGateway, NotificationService, InventoryService


class ProductService:
    """Application service for product management"""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    def add_product(self, name: str, description: str, price: float, category: str) -> Product:
        """Add a new product to the menu"""
        product = Product(
            id="",
            name=name,
            description=description,
            price=price,
            category=category
        )
        self._product_repository.save(product)
        return product
    
    def get_all_products(self) -> List[Product]:
        """Get all available products"""
        return [p for p in self._product_repository.find_all() if p.available]
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        return [p for p in self._product_repository.find_by_category(category) if p.available]
    
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a specific product by ID"""
        return self._product_repository.find_by_id(product_id)


class CustomerService:
    """Application service for customer management"""
    
    def __init__(self, customer_repository: CustomerRepository):
        self._customer_repository = customer_repository
    
    def register_customer(self, name: str, email: str, phone: str, address: str) -> Customer:
        """Register a new customer"""
        # Check if customer already exists
        existing = self._customer_repository.find_by_email(email)
        if existing:
            return existing
        
        customer = Customer(
            id="",
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        self._customer_repository.save(customer)
        return customer
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Find customer by email"""
        return self._customer_repository.find_by_email(email)
    
    def get_customer_by_id(self, customer_id: str) -> Optional[Customer]:
        """Find customer by ID"""
        return self._customer_repository.find_by_id(customer_id)


class OrderService:
    """Application service for order management"""
    
    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        customer_repository: CustomerRepository,
        payment_gateway: PaymentGateway,
        notification_service: NotificationService,
        inventory_service: InventoryService
    ):
        self._order_repository = order_repository
        self._product_repository = product_repository
        self._customer_repository = customer_repository
        self._payment_gateway = payment_gateway
        self._notification_service = notification_service
        self._inventory_service = inventory_service
    
    def create_order(self, customer_id: str, items: List[dict], notes: Optional[str] = None) -> Optional[Order]:
        """Create a new order
        
        Args:
            customer_id: ID of the customer
            items: List of dicts with 'product_id' and 'quantity'
            notes: Optional order notes
        
        Returns:
            Created order or None if creation failed
        """
        customer = self._customer_repository.find_by_id(customer_id)
        if not customer:
            print(f"Customer with ID {customer_id} not found")
            return None
        
        # Validate and prepare order items
        order_items = []
        product_quantities = {}
        
        for item_data in items:
            product = self._product_repository.find_by_id(item_data['product_id'])
            if not product or not product.available:
                print(f"Product {item_data['product_id']} not available")
                return None
            
            quantity = item_data['quantity']
            if not self._inventory_service.check_product_availability(product.id, quantity):
                print(f"Insufficient inventory for product {product.name}")
                return None
            
            order_items.append(OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                unit_price=product.price
            ))
            product_quantities[product.id] = quantity
        
        # Reserve inventory
        if not self._inventory_service.reserve_products(product_quantities):
            print("Failed to reserve inventory")
            return None
        
        # Create order
        order = Order(
            id="",
            customer_id=customer_id,
            items=order_items,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            notes=notes
        )
        
        self._order_repository.save(order)
        print(f"Order {order.id} created successfully")
        return order
    
    def confirm_order(self, order_id: str) -> bool:
        """Confirm an order by processing payment"""
        order = self._order_repository.find_by_id(order_id)
        if not order:
            print(f"Order {order_id} not found")
            return False
        
        if order.status != OrderStatus.PENDING:
            print(f"Order {order_id} is not in pending status")
            return False
        
        customer = self._customer_repository.find_by_id(order.customer_id)
        if not customer:
            print(f"Customer {order.customer_id} not found")
            return False
        
        # Process payment
        payment_result = self._payment_gateway.process_payment(order, customer)
        if not payment_result.success:
            print(f"Payment failed: {payment_result.error_message}")
            # Release reserved inventory
            product_quantities = {item.product_id: item.quantity for item in order.items}
            self._inventory_service.release_products(product_quantities)
            return False
        
        # Update order status
        order.update_status(OrderStatus.CONFIRMED)
        self._order_repository.save(order)
        
        # Send confirmation notification
        self._notification_service.send_order_confirmation(order, customer)
        
        print(f"Order {order_id} confirmed successfully")
        return True
    
    def update_order_status(self, order_id: str, new_status: OrderStatus) -> bool:
        """Update order status and send notification"""
        order = self._order_repository.find_by_id(order_id)
        if not order:
            print(f"Order {order_id} not found")
            return False
        
        customer = self._customer_repository.find_by_id(order.customer_id)
        if not customer:
            print(f"Customer {order.customer_id} not found")
            return False
        
        old_status = order.status
        order.update_status(new_status)
        self._order_repository.save(order)
        
        # Send status update notification
        self._notification_service.send_status_update(order, customer)
        
        # Special handling for delivery
        if new_status == OrderStatus.DELIVERED:
            self._notification_service.send_delivery_notification(order, customer)
        
        print(f"Order {order_id} status updated from {old_status.value} to {new_status.value}")
        return True
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        return self._order_repository.find_by_id(order_id)
    
    def get_orders_by_customer(self, customer_id: str) -> List[Order]:
        """Get all orders for a customer"""
        return self._order_repository.find_by_customer_id(customer_id)
    
    def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        return self._order_repository.find_all()
