"""
Restaurant Order System - Hexagonal Architecture Demo

This application demonstrates the hexagonal architecture pattern with:
- Domain entities (business logic)
- Ports (interfaces)
- Adapters (implementations)
- Application services (use cases)
- Console interface (user adapter)

The core business logic is completely isolated from external concerns.
"""

from domain.entities import Product
from adapters.repositories import (
    InMemoryProductRepository,
    InMemoryOrderRepository,
    InMemoryCustomerRepository
)
from adapters.services import (
    MockPaymentGateway,
    ConsoleNotificationService,
    MockInventoryService
)
from application.services import ProductService, CustomerService, OrderService
from interface.console import ConsoleInterface


def setup_sample_data(product_service: ProductService):
    """Setup some sample products for demonstration"""
    print("🔄 Setting up sample data...")
    
    # Pizza category
    product_service.add_product(
        "Margherita Pizza",
        "Classic pizza with tomato sauce, mozzarella, and fresh basil",
        12.99,
        "Pizza"
    )
    
    product_service.add_product(
        "Pepperoni Pizza",
        "Pizza with pepperoni, tomato sauce, and mozzarella cheese",
        14.99,
        "Pizza"
    )
    
    # Burger category
    product_service.add_product(
        "Classic Burger",
        "Beef patty with lettuce, tomato, onion, and special sauce",
        10.50,
        "Burger"
    )
    
    product_service.add_product(
        "Chicken Burger",
        "Grilled chicken breast with lettuce and mayo",
        9.99,
        "Burger"
    )
    
    # Drinks category
    product_service.add_product(
        "Coca Cola",
        "Refreshing cola soft drink",
        2.99,
        "Drinks"
    )
    
    product_service.add_product(
        "Fresh Orange Juice",
        "Freshly squeezed orange juice",
        4.50,
        "Drinks"
    )
    
    # Desserts category
    product_service.add_product(
        "Chocolate Cake",
        "Rich chocolate cake with chocolate frosting",
        6.99,
        "Desserts"
    )
    
    product_service.add_product(
        "Ice Cream Sundae",
        "Vanilla ice cream with chocolate sauce and whipped cream",
        5.50,
        "Desserts"
    )
    
    print("✅ Sample data loaded successfully!")


def main():
    """Main application entry point with dependency injection"""
    print("🚀 Starting Restaurant Order System...")
    
    try:
        # Initialize adapters (implementations of ports)
        # These could easily be replaced with different implementations
        product_repository = InMemoryProductRepository()
        order_repository = InMemoryOrderRepository()
        customer_repository = InMemoryCustomerRepository()
        
        payment_gateway = MockPaymentGateway()
        notification_service = ConsoleNotificationService()
        inventory_service = MockInventoryService()
        
        # Initialize application services with injected dependencies
        product_service = ProductService(product_repository)
        customer_service = CustomerService(customer_repository)
        order_service = OrderService(
            order_repository,
            product_repository,
            customer_repository,
            payment_gateway,
            notification_service,
            inventory_service
        )
        
        # Setup sample data
        setup_sample_data(product_service)
        
        # Initialize and start the console interface
        console = ConsoleInterface(product_service, customer_service, order_service)
        
        print("✅ System initialized successfully!")
        console.start()
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
