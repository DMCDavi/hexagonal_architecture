"""
Restaurant Order System - Clean Hexagonal Architecture Demo

This application demonstrates the Clean Hexagonal Architecture pattern with:
- Domain Layer: Pure business logic (entities, value objects)
- Application Layer: Use cases and ports (interfaces)
- Infrastructure Layer: Adapters and external concerns

The architecture follows the dependency rule: dependencies point inward.
The core business logic is completely isolated from external concerns.
"""

# Infrastructure Layer - External adapters
from infrastructure.adapters.persistence.in_memory_product_repository import InMemoryProductRepository
from infrastructure.adapters.persistence.in_memory_order_repository import InMemoryOrderRepository  
from infrastructure.adapters.persistence.in_memory_customer_repository import InMemoryCustomerRepository
from infrastructure.adapters.external_services.mock_payment_gateway import MockPaymentGateway
from infrastructure.adapters.external_services.console_notification_service import ConsoleNotificationService
from infrastructure.adapters.external_services.mock_inventory_service import MockInventoryService
from infrastructure.adapters.presentation.console_interface import ConsoleInterface

# Application Layer - Use cases
from application.use_cases.product_service import ProductService
from application.use_cases.customer_service import CustomerService
from application.use_cases.order_service import OrderService


def setup_sample_data(product_service: ProductService):
    """Setup some sample products for demonstration"""
    print("🔄 Setting up sample data using domain factory methods...")
    
    # Define sample products data
    sample_products = [
        # Pizza category
        ("Margherita Pizza", "Classic pizza with tomato sauce, mozzarella, and fresh basil", 12.99, "Pizza"),
        ("Pepperoni Pizza", "Pizza with pepperoni, tomato sauce, and mozzarella cheese", 14.99, "Pizza"),
        
        # Burger category  
        ("Classic Burger", "Beef patty with lettuce, tomato, onion, and special sauce", 10.50, "Burger"),
        ("Chicken Burger", "Grilled chicken breast with lettuce and mayo", 9.99, "Burger"),
        
        # Drinks category
        ("Coca Cola", "Refreshing cola soft drink", 2.99, "Drinks"),
        ("Fresh Orange Juice", "Freshly squeezed orange juice", 4.50, "Drinks"),
        
        # Desserts category
        ("Chocolate Cake", "Rich chocolate cake with chocolate frosting", 6.99, "Desserts"),
        ("Ice Cream Sundae", "Vanilla ice cream with chocolate sauce and whipped cream", 5.50, "Desserts")
    ]
    
    # Create products using application service (which uses domain factory methods)
    for name, description, price, category in sample_products:
        try:
            product = product_service.add_product(name, description, price, category)
            print(f"   ✅ Created: {product.name} (${product.price:.2f}) with {product.get_default_inventory_level()} units")
        except ValueError as e:
            print(f"   ❌ Failed to create {name}: {e}")
    
    print("✅ Sample data loaded successfully with domain defaults!")


def main():
    """Main application entry point with dependency injection
    
    This function demonstrates the Clean Architecture dependency injection pattern:
    1. Create infrastructure adapters (outermost layer)
    2. Inject them into application services (middle layer) 
    3. Keep domain logic pure (innermost layer)
    """
    print("🚀 Starting Restaurant Order System...")
    print("📐 Using Clean Hexagonal Architecture")
    
    try:
        # ===== INFRASTRUCTURE LAYER =====
        # Initialize persistence adapters (easily replaceable with real databases)
        product_repository = InMemoryProductRepository()
        order_repository = InMemoryOrderRepository()
        customer_repository = InMemoryCustomerRepository()
        
        # Initialize external service adapters (easily replaceable with real services)
        payment_gateway = MockPaymentGateway()
        notification_service = ConsoleNotificationService()
        inventory_service = MockInventoryService()
        
        # ===== APPLICATION LAYER =====
        # Initialize use cases with injected dependencies (ports)
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
        
        # ===== PRESENTATION LAYER =====
        # Initialize presentation adapter
        console = ConsoleInterface(product_service, customer_service, order_service)
        
        # ===== BOOTSTRAP =====
        # Setup sample data for demonstration
        setup_sample_data(product_service)
        
        print("✅ System initialized successfully!")
        print("\n🏗️  Architecture Layers:")
        print("   🔷 Domain: Pure business logic")
        print("   ⚡ Application: Use cases and ports") 
        print("   🔧 Infrastructure: Adapters and external systems")
        print("\n🚀 Starting application...\n")
        
        # Start the application
        console.start()
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()