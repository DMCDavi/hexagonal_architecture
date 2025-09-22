"""
Simple demo script to test the hexagonal architecture implementation
This script demonstrates the core functionality without user interaction
"""

from domain.entities import OrderStatus
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


def run_demo():
    """Run a demonstration of the system functionality"""
    print("🧪 Testing Hexagonal Architecture Implementation")
    print("=" * 50)
    
    # Setup dependencies (Dependency Injection)
    product_repo = InMemoryProductRepository()
    order_repo = InMemoryOrderRepository()
    customer_repo = InMemoryCustomerRepository()
    
    payment_gateway = MockPaymentGateway()
    notification_service = ConsoleNotificationService()
    inventory_service = MockInventoryService()
    
    # Initialize services
    product_service = ProductService(product_repo)
    customer_service = CustomerService(customer_repo)
    order_service = OrderService(
        order_repo,
        product_repo, 
        customer_repo,
        payment_gateway,
        notification_service,
        inventory_service
    )
    
    print("\n1️⃣ Adding products to menu...")
    # Add products
    pizza = product_service.add_product(
        "Margherita Pizza",
        "Classic pizza with fresh basil",
        12.99,
        "Pizza"
    )
    
    burger = product_service.add_product(
        "Classic Burger", 
        "Beef burger with lettuce and tomato",
        10.50,
        "Burger"
    )
    
    print(f"✅ Added {pizza.name} (${pizza.price})")
    print(f"✅ Added {burger.name} (${burger.price})")
    
    print("\n2️⃣ Registering customer...")
    # Register customer
    customer = customer_service.register_customer(
        "John Doe",
        "john@example.com", 
        "+1234567890",
        "123 Main St, City, State"
    )
    print(f"✅ Registered customer: {customer.name}")
    
    print("\n3️⃣ Creating order...")
    # Create order
    order_items = [
        {'product_id': pizza.id, 'quantity': 2},
        {'product_id': burger.id, 'quantity': 1}
    ]
    
    order = order_service.create_order(
        customer.id,
        order_items,
        "Please deliver to front door"
    )
    
    if order:
        print(f"✅ Order created: {order.id}")
        print(f"   Total: ${order.total_amount:.2f}")
        print(f"   Status: {order.status.value}")
        
        print("\n4️⃣ Confirming order and processing payment...")
        # Confirm order (process payment)
        if order_service.confirm_order(order.id):
            print(f"✅ Order confirmed and payment processed!")
            
            print("\n5️⃣ Updating order status...")
            # Update order status
            order_service.update_order_status(order.id, OrderStatus.PREPARING)
            order_service.update_order_status(order.id, OrderStatus.READY)
            order_service.update_order_status(order.id, OrderStatus.DELIVERED)
            
            print("\n6️⃣ Final order details...")
            final_order = order_service.get_order_by_id(order.id)
            print(f"   Order ID: {final_order.id}")
            print(f"   Status: {final_order.status.value}")
            print(f"   Customer: {customer.name}")
            print(f"   Total: ${final_order.total_amount:.2f}")
            print(f"   Items:")
            for item in final_order.items:
                print(f"   - {item.product_name} x{item.quantity}")
        else:
            print("❌ Order confirmation failed")
    else:
        print("❌ Order creation failed")
    
    print("\n🎉 Demo completed successfully!")
    print("\n🏗️ Architecture Benefits Demonstrated:")
    print("   ✅ Domain logic isolated from infrastructure")
    print("   ✅ Easy to test with mock adapters") 
    print("   ✅ Clean separation of concerns")
    print("   ✅ Flexible adapter replacement")
    print("   ✅ Dependency injection pattern")
    

if __name__ == "__main__":
    run_demo()
