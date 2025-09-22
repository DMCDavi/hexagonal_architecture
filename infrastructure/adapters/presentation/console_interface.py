"""Console Interface Adapter

Console-based user interface for the restaurant ordering system.
This is a presentation adapter - implements the user interface concerns.
"""

from typing import Optional

from domain.entities.product import Product
from domain.value_objects.order_status import OrderStatus
from application.use_cases.product_service import ProductService
from application.use_cases.customer_service import CustomerService
from application.use_cases.order_service import OrderService


class ConsoleInterface:
    """Console-based user interface (adapter)"""
    
    def __init__(
        self,
        product_service: ProductService,
        customer_service: CustomerService,
        order_service: OrderService
    ):
        self._product_service = product_service
        self._customer_service = customer_service
        self._order_service = order_service
        self._current_customer = None
    
    def start(self):
        """Start the console application"""
        print("🍽️  Welcome to Restaurant Order System!")
        print("=====================================")
        
        while True:
            try:
                self._show_main_menu()
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '1':
                    self._register_or_login()
                elif choice == '2':
                    self._browse_menu()
                elif choice == '3':
                    self._create_order()
                elif choice == '4':
                    self._view_orders()
                elif choice == '5':
                    self._admin_menu()
                elif choice == '0':
                    print("Thank you for using Restaurant Order System! 👋")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                
                input("\nPress Enter to continue...")
                print("\n" + "="*50)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")
    
    def _show_main_menu(self):
        """Display the main menu"""
        customer_info = f" (Logged in as: {self._current_customer.name})" if self._current_customer else ""
        print(f"\n📋 Main Menu{customer_info}")
        print("-" * 30)
        print("1. Register/Login")
        print("2. Browse Menu")
        print("3. Create Order")
        print("4. View My Orders")
        print("5. Admin Panel")
        print("0. Exit")
    
    def _register_or_login(self):
        """Register or login a customer"""
        print("\n👤 Customer Registration/Login")
        print("-" * 30)
        email = input("Enter your email: ").strip()
        
        if not email:
            print("❌ Email cannot be empty")
            return
        
        try:
            customer = self._customer_service.get_customer_by_email(email)
            
            if customer:
                print(f"✅ Welcome back, {customer.name}!")
                self._current_customer = customer
            else:
                print("📝 New customer registration:")
                name = input("Enter your name: ").strip()
                phone = input("Enter your phone: ").strip()
                address = input("Enter your address: ").strip()
                
                if not all([name, phone, address]):
                    print("❌ All fields are required")
                    return
                
                customer = self._customer_service.register_customer(name, email, phone, address)
                print(f"✅ Registration successful! Welcome, {customer.name}!")
                self._current_customer = customer
        except ValueError as e:
            print(f"❌ Registration failed: {e}")
    
    def _browse_menu(self):
        """Browse the restaurant menu"""
        print("\n🍽️  Restaurant Menu")
        print("-" * 30)
        
        products = self._product_service.get_all_products()
        if not products:
            print("❌ No products available")
            return
        
        # Group by category
        categories = {}
        for product in products:
            if product.category not in categories:
                categories[product.category] = []
            categories[product.category].append(product)
        
        for category, category_products in categories.items():
            print(f"\n📂 {category.upper()}")
            print("-" * 20)
            for product in category_products:
                print(f"🍴 {product.name} - ${product.price:.2f}")
                print(f"   {product.description}")
                print(f"   ID: {product.id}")
                print()
    
    def _create_order(self):
        """Create a new order"""
        if not self._current_customer:
            print("❌ Please register or login first")
            return
        
        print(f"\n🛒 Create Order for {self._current_customer.name}")
        print("-" * 30)
        
        products = self._product_service.get_all_products()
        if not products:
            print("❌ No products available")
            return
        
        items = []
        
        while True:
            print("\nAvailable products:")
            for i, product in enumerate(products, 1):
                print(f"{i}. {product.name} - ${product.price:.2f}")
            
            try:
                choice = input("\nSelect product number (0 to finish): ").strip()
                if choice == '0':
                    break
                
                product_index = int(choice) - 1
                if 0 <= product_index < len(products):
                    product = products[product_index]
                    quantity = int(input(f"Enter quantity for {product.name}: "))
                    
                    if quantity > 0:
                        items.append({
                            'product_id': product.id,
                            'quantity': quantity
                        })
                        print(f"✅ Added {quantity}x {product.name} to order")
                    else:
                        print("❌ Quantity must be greater than 0")
                else:
                    print("❌ Invalid product selection")
                    
            except ValueError:
                print("❌ Please enter valid numbers")
        
        if not items:
            print("❌ No items selected for order")
            return
        
        notes = input("Enter order notes (optional): ").strip()
        notes = notes if notes else None
        
        try:
            # Create order
            order = self._order_service.create_order(
                customer_id=self._current_customer.id,
                items=items,
                notes=notes
            )
            
            if order:
                print(f"✅ Order {order.id} created successfully!")
                print(f"💰 Total amount: ${order.total_amount:.2f}")
                
                # Ask to confirm order
                confirm = input("\nConfirm and process payment? (y/n): ").strip().lower()
                if confirm == 'y':
                    if self._order_service.confirm_order(order.id):
                        print("✅ Order confirmed and payment processed!")
                    else:
                        print("❌ Order confirmation failed")
            else:
                print("❌ Failed to create order")
        except ValueError as e:
            print(f"❌ Failed to create order: {e}")
    
    def _view_orders(self):
        """View customer orders"""
        if not self._current_customer:
            print("❌ Please register or login first")
            return
        
        print(f"\n📋 Orders for {self._current_customer.name}")
        print("-" * 30)
        
        orders = self._order_service.get_orders_by_customer(self._current_customer.id)
        
        if not orders:
            print("📭 No orders found")
            return
        
        for order in orders:
            print(f"\n🧾 Order #{order.id}")
            print(f"   Status: {order.status.value.upper()}")
            print(f"   Created: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Total: ${order.total_amount:.2f}")
            print("   Items:")
            for item in order.items:
                print(f"   - {item.product_name} x{item.quantity} @ ${item.unit_price:.2f}")
            if order.notes:
                print(f"   Notes: {order.notes}")
            print("-" * 40)
    
    def _admin_menu(self):
        """Admin panel for managing system"""
        print("\n🔧 Admin Panel")
        print("-" * 30)
        print("1. Add Product")
        print("2. View All Orders")
        print("3. Update Order Status")
        print("0. Back to Main Menu")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            self._add_product()
        elif choice == '2':
            self._view_all_orders()
        elif choice == '3':
            self._update_order_status()
    
    def _add_product(self):
        """Add a new product to the menu"""
        print("\n➕ Add New Product")
        print("-" * 20)
        
        try:
            name = input("Product name: ").strip()
            description = input("Description: ").strip()
            price = float(input("Price: $"))
            category = input("Category: ").strip()
            
            if not all([name, description, category]) or price <= 0:
                print("❌ All fields are required and price must be positive")
                return
            
            product = self._product_service.add_product(name, description, price, category)
            print(f"✅ Product '{product.name}' added successfully! ID: {product.id}")
            
        except ValueError as e:
            print(f"❌ Failed to add product: {e}")
    
    def _view_all_orders(self):
        """View all orders in the system"""
        print("\n📋 All Orders")
        print("-" * 20)
        
        orders = self._order_service.get_all_orders()
        
        if not orders:
            print("📭 No orders found")
            return
        
        for order in orders:
            customer = self._customer_service.get_customer_by_id(order.customer_id)
            customer_name = customer.name if customer else "Unknown"
            
            print(f"\n🧾 Order #{order.id}")
            print(f"   Customer: {customer_name}")
            print(f"   Status: {order.status.value.upper()}")
            print(f"   Total: ${order.total_amount:.2f}")
            print(f"   Created: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 40)
    
    def _update_order_status(self):
        """Update order status"""
        print("\n📊 Update Order Status")
        print("-" * 25)
        
        order_id = input("Enter Order ID: ").strip()
        
        try:
            order = self._order_service.get_order_by_id(order_id)
            
            if not order:
                print("❌ Order not found")
                return
            
            print(f"\nCurrent status: {order.status.value.upper()}")
            print("\nAvailable statuses:")
            statuses = list(OrderStatus)
            for i, status in enumerate(statuses, 1):
                print(f"{i}. {status.value.upper()}")
            
            choice = int(input("Select new status: "))
            if 1 <= choice <= len(statuses):
                new_status = statuses[choice - 1]
                if self._order_service.update_order_status(order_id, new_status):
                    print("✅ Order status updated successfully!")
                else:
                    print("❌ Failed to update order status")
            else:
                print("❌ Invalid status selection")
        except ValueError as e:
            print(f"❌ Error updating order status: {e}")
        except Exception:
            print("❌ Please enter a valid number")
