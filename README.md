# Restaurant Order System - Hexagonal Architecture Demo

## 🏗️ Architecture Overview

This project demonstrates the **Hexagonal Architecture** (Ports & Adapters) pattern for a restaurant ordering system. The architecture ensures complete separation between business logic and external concerns.

### Core Principles

- **Domain Independence**: Business logic is isolated from frameworks and external systems
- **Testability**: Easy to test by replacing adapters with test doubles  
- **Flexibility**: External systems can be changed without affecting the core
- **Dependency Inversion**: Core depends on abstractions (ports), not implementations

## 📁 Project Structure

```
restaurant-order-system/
├── domain/                    # 🔷 CORE - Business entities
│   └── entities.py           
├── ports/                     # 🔌 INTERFACES - Contracts
│   ├── repositories.py       
│   └── services.py           
├── adapters/                  # 🔧 IMPLEMENTATIONS - External concerns
│   ├── repositories.py       
│   └── services.py           
├── application/               # ⚡ USE CASES - Application services
│   └── services.py           
├── interface/                 # 🖥️ USER INTERFACE - Console adapter
│   └── console.py            
└── main.py                   # 🚀 ENTRY POINT - Dependency injection
```

## 🎯 Hexagonal Architecture Components

### 🔷 Domain (Core)
- **Entities**: `Product`, `Order`, `Customer`, `OrderItem`
- **Value Objects**: `OrderStatus`, `PaymentResult`
- **Business Rules**: Order validation, status transitions, calculations

### 🔌 Ports (Interfaces)
- **Repository Ports**: Data persistence contracts
  - `ProductRepository`, `OrderRepository`, `CustomerRepository`
- **Service Ports**: External service contracts  
  - `PaymentGateway`, `NotificationService`, `InventoryService`

### 🔧 Adapters (Implementations)
- **Repository Adapters**: In-memory implementations (easily replaceable)
- **Service Adapters**: Mock external services (payment, notifications)
- **Interface Adapter**: Console-based user interface

### ⚡ Application Services
- **ProductService**: Menu management
- **CustomerService**: Customer registration/management  
- **OrderService**: Order creation, confirmation, status updates

## 🚀 How to Run

### Prerequisites
- Python 3.7 or higher

### Running the Application

1. **Navigate to the project directory:**
   ```bash
   cd hexagonal_architecture
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Follow the console prompts to:**
   - Register/Login as a customer
   - Browse the restaurant menu
   - Create orders
   - View order history
   - Access admin features

## 🎮 Usage Example

### Customer Flow:
1. **Register/Login** → Enter email and personal details
2. **Browse Menu** → View products by category
3. **Create Order** → Select products and quantities
4. **Confirm Order** → Process payment
5. **View Orders** → Check order status and history

### Admin Flow:
1. **Add Products** → Expand the menu
2. **View All Orders** → Monitor system activity
3. **Update Order Status** → Manage order lifecycle

## 🧪 Architecture Benefits Demonstrated

### 1. **Isolation of Business Logic**
```python
# Core business logic is independent of external concerns
class Order:
    def update_status(self, new_status: OrderStatus):
        self.status = new_status
        self.updated_at = datetime.now()
```

### 2. **Easy Adapter Replacement**
```python
# Payment adapter can be easily swapped
# From: MockPaymentGateway()
# To:   StripePaymentGateway() or PayPalGateway()
payment_gateway = MockPaymentGateway()  # ← Easily replaceable
```

### 3. **Testability**
```python
# Services can be tested with mock adapters
def test_order_creation():
    mock_repo = MockOrderRepository()
    mock_payment = MockPaymentGateway() 
    order_service = OrderService(mock_repo, mock_payment, ...)
    # Test business logic in isolation
```

### 4. **Dependency Injection**
```python
# Dependencies are injected, not hard-coded
order_service = OrderService(
    order_repository,      # ← Injected
    payment_gateway,       # ← Injected  
    notification_service   # ← Injected
)
```

## 🔄 Data Flow

1. **User Input** → Console Interface (Adapter)
2. **Interface** → Application Service (Use Case)  
3. **Service** → Domain Logic (Core)
4. **Service** → Repository/External Service (through Ports)
5. **Adapters** → External Systems (Database, APIs, etc.)

## 🎨 Key Features

### Business Features:
- ✅ Product catalog management
- ✅ Customer registration  
- ✅ Order creation and management
- ✅ Payment processing simulation
- ✅ Order status tracking
- ✅ Notification system

### Architecture Features:
- ✅ Complete separation of concerns
- ✅ Framework independence
- ✅ Database independence  
- ✅ Easy testing with mocks
- ✅ Flexible adapter replacement
- ✅ Clean dependency injection

## 🔧 Extending the System

### Adding New Payment Provider:
1. Implement `PaymentGateway` port
2. Inject new adapter in `main.py`
3. No changes needed in business logic

### Adding Database:
1. Implement repository ports with database adapters
2. Replace in-memory repositories in `main.py`
3. Core logic remains unchanged

### Adding Web Interface:
1. Create web adapter implementing same interface
2. Use same application services
3. No business logic duplication

## 📊 Sample Data

The system comes pre-loaded with sample data:
- **Pizza**: Margherita, Pepperoni
- **Burgers**: Classic, Chicken
- **Drinks**: Coca Cola, Orange Juice  
- **Desserts**: Chocolate Cake, Ice Cream Sundae

## 🏆 Architecture Trade-offs

### ✅ Benefits:
- High testability and maintainability
- Framework and database independence
- Easy to extend and modify
- Clear separation of concerns
- Scalable architecture

### ⚠️ Considerations:
- Initial complexity for simple applications
- More files and interfaces to manage
- Learning curve for team members
- Potential over-engineering for small projects

## 🤝 Contributing

This is a demonstration project for educational purposes. The architecture showcases how hexagonal architecture principles can be applied to create maintainable, testable, and flexible applications.

---

**Made with ❤️ for learning Hexagonal Architecture**