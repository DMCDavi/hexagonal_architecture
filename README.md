# Restaurant Order System - Clean Hexagonal Architecture

## 🏗️ Architecture Overview

This project demonstrates the **Clean Hexagonal Architecture** pattern for a restaurant ordering system. The architecture follows Uncle Bob's Clean Architecture principles with proper layer separation and dependency inversion.

### Core Principles

- **Dependency Rule**: Dependencies point inward toward the domain
- **Domain Independence**: Business logic is isolated from frameworks and external systems
- **Testability**: Easy to test by replacing adapters with test doubles  
- **Flexibility**: External systems can be changed without affecting the core
- **Single Responsibility**: Each class has a single, well-defined purpose

## 📁 Project Structure (Clean Architecture)

```
hexagonal_architecture/
├── domain/                           # 🔷 INNER LAYER - Business Logic
│   ├── entities/                     # Business entities with behavior
│   │   ├── __init__.py
│   │   ├── product.py               # Product entity
│   │   ├── customer.py              # Customer entity  
│   │   ├── order.py                 # Order aggregate root
│   │   └── order_item.py            # Order item entity
│   ├── value_objects/               # Immutable data structures
│   │   ├── __init__.py
│   │   ├── order_status.py          # Order status enumeration
│   │   └── payment_result.py        # Payment result data
│   └── __init__.py
├── application/                      # ⚡ MIDDLE LAYER - Use Cases
│   ├── ports/                       # Interfaces (contracts)
│   │   ├── repositories/            # Data access interfaces
│   │   │   ├── __init__.py
│   │   │   ├── product_repository.py
│   │   │   ├── order_repository.py
│   │   │   └── customer_repository.py
│   │   ├── services/                # External service interfaces
│   │   │   ├── __init__.py
│   │   │   ├── payment_gateway.py
│   │   │   ├── notification_service.py
│   │   │   └── inventory_service.py
│   │   └── __init__.py
│   ├── use_cases/                   # Business use cases
│   │   ├── __init__.py
│   │   ├── product_service.py       # Product management use cases
│   │   ├── customer_service.py      # Customer management use cases
│   │   └── order_service.py         # Order management use cases
│   └── __init__.py
├── infrastructure/                   # 🔧 OUTER LAYER - External Concerns
│   ├── adapters/                    # Implementations of ports
│   │   ├── persistence/             # Data storage implementations
│   │   │   ├── __init__.py
│   │   │   ├── in_memory_product_repository.py
│   │   │   ├── in_memory_order_repository.py
│   │   │   └── in_memory_customer_repository.py
│   │   ├── external_services/       # External service implementations
│   │   │   ├── __init__.py
│   │   │   ├── mock_payment_gateway.py
│   │   │   ├── console_notification_service.py
│   │   │   └── mock_inventory_service.py
│   │   ├── presentation/            # User interface implementations
│   │   │   ├── __init__.py
│   │   │   └── console_interface.py
│   │   └── __init__.py
│   └── __init__.py
├── main.py                          # 🚀 ENTRY POINT - Dependency injection
├── README.md                        # This file
└── ARCHITECTURE.md                  # Detailed architecture diagrams
```

## 🎯 Clean Architecture Layers

### 🔷 Domain Layer (Innermost - Enterprise Business Rules)
- **Entities**: Core business objects with behavior (`Product`, `Order`, `Customer`)
- **Value Objects**: Immutable data structures (`OrderStatus`, `PaymentResult`)
- **Business Rules**: Pure domain logic with no external dependencies

### ⚡ Application Layer (Application Business Rules)
- **Use Cases**: Application-specific business operations (`ProductService`, `OrderService`)
- **Ports**: Interfaces defining contracts with external systems
- **Orchestration**: Coordinates domain objects and external services

### 🔧 Infrastructure Layer (Outermost - Frameworks & Drivers)
- **Persistence Adapters**: Database implementations (in-memory, SQL, NoSQL)
- **External Service Adapters**: Third-party service integrations
- **Presentation Adapters**: User interfaces (console, web, mobile)
- **Configuration**: Framework and external system setup

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher

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
2. **Browse Menu** → View products by category (Pizza, Burgers, Drinks, Desserts)
3. **Create Order** → Select products and quantities
4. **Confirm Order** → Process payment simulation
5. **View Orders** → Check order status and history

### Admin Flow:
1. **Add Products** → Expand the menu with new items
2. **View All Orders** → Monitor system activity
3. **Update Order Status** → Manage order lifecycle (pending → confirmed → preparing → ready → delivered)

## 🧪 Architecture Benefits Demonstrated

### 1. **Complete Layer Isolation**
```python
# Domain entities have no external dependencies
class Order:
    def update_status(self, new_status: OrderStatus):
        if not self._is_valid_status_transition(self.status, new_status):
            raise ValueError("Invalid status transition")
        self.status = new_status
```

### 2. **Dependency Inversion**
```python
# Use cases depend on abstractions, not concretions
class OrderService:
    def __init__(self, order_repository: OrderRepository):  # ← Interface
        self._order_repository = order_repository
```

### 3. **Easy Adapter Replacement**
```python
# Infrastructure adapters can be easily swapped
# From: InMemoryProductRepository()
# To:   PostgreSQLProductRepository() or MongoProductRepository()
product_repository = InMemoryProductRepository()  # ← Easily replaceable
```

### 4. **Clean Dependency Injection**
```python
# Main.py wires everything together
def main():
    # Infrastructure layer
    product_repository = InMemoryProductRepository()
    payment_gateway = MockPaymentGateway()
    
    # Application layer  
    product_service = ProductService(product_repository)
    
    # Presentation layer
    console = ConsoleInterface(product_service)
```

## 🔄 Data Flow (Clean Architecture)

```
User Input → Presentation Adapter → Use Case → Domain Logic → Port → Infrastructure Adapter → External System
     ↑                                                                                              ↓
User Output ← Presentation Adapter ← Use Case ← Domain Logic ← Port ← Infrastructure Adapter ← External System
```

**Detailed Flow:**
1. **User** interacts with **Console Interface** (Infrastructure/Presentation)
2. **Console** calls **Use Case Service** (Application)
3. **Use Case** orchestrates **Domain Entities** (Domain)
4. **Use Case** calls **Port Interface** (Application)
5. **Infrastructure Adapter** implements **Port** (Infrastructure)
6. **Adapter** communicates with **External System** (Database, API, etc.)

## 🎨 Key Features

### Business Features:
- ✅ Product catalog management with categories
- ✅ Customer registration with validation
- ✅ Order creation with multiple items
- ✅ Payment processing simulation
- ✅ Order status tracking with business rules
- ✅ Inventory management simulation
- ✅ Multi-channel notifications
- ✅ Admin panel for system management

### Architecture Features:
- ✅ Complete separation of concerns across layers
- ✅ Framework and database independence
- ✅ Easy testing with dependency injection
- ✅ Flexible adapter replacement
- ✅ Clean dependency management
- ✅ Single Responsibility Principle
- ✅ Dependency Inversion Principle

## 🔧 Extending the System

### Adding New Payment Provider:
1. Implement `PaymentGateway` port in infrastructure layer
2. Inject new adapter in `main.py`
3. **No changes needed in domain or application layers**

### Adding Database:
1. Implement repository ports with database adapters
2. Replace in-memory repositories in `main.py`
3. **Core logic and use cases remain unchanged**

### Adding Web Interface:
1. Create web adapter in infrastructure/presentation
2. Use same application use cases
3. **No business logic duplication**

### Adding New Business Rules:
1. Add logic to domain entities
2. Update use cases if needed
3. **Infrastructure adapters remain unchanged**

## 📊 Sample Data

The system comes pre-loaded with sample data:
- **Pizza**: Margherita ($12.99), Pepperoni ($14.99)
- **Burgers**: Classic ($10.50), Chicken ($9.99)
- **Drinks**: Coca Cola ($2.99), Orange Juice ($4.50)
- **Desserts**: Chocolate Cake ($6.99), Ice Cream Sundae ($5.50)

## 🏆 Architecture Comparison

| Aspect | Traditional Layered | Hexagonal | Clean Hexagonal |
|--------|-------------------|-----------|----------------|
| **Dependency Direction** | Top-down | Inward to domain | Inward to domain |
| **Database Independence** | ❌ Coupled | ✅ Independent | ✅ Independent |
| **Framework Independence** | ❌ Coupled | ✅ Independent | ✅ Independent |
| **Testability** | ⚠️ Difficult | ✅ Easy | ✅ Very Easy |
| **Business Logic Purity** | ❌ Mixed concerns | ✅ Clean | ✅ Very Clean |
| **Single Responsibility** | ⚠️ Often violated | ✅ Enforced | ✅ Strictly Enforced |

## 🚦 Testing Strategy

### Unit Tests:
```python
# Test domain logic in isolation
def test_order_total_calculation():
    order = Order(...)
    assert order.total_amount == expected_total

# Test use cases with mock ports
def test_order_creation():
    mock_repo = Mock(spec=OrderRepository)
    service = OrderService(mock_repo, ...)
    # Test business logic without external dependencies
```

### Integration Tests:
```python
# Test with real infrastructure adapters
def test_database_integration():
    real_db_repo = PostgreSQLOrderRepository()
    service = OrderService(real_db_repo, ...)
    # Test actual database interactions
```

## 🤝 Contributing

This is a demonstration project for educational purposes. The architecture showcases how Clean Hexagonal Architecture principles create maintainable, testable, and flexible applications that can evolve with changing requirements while keeping the business logic stable and protected.

---

**Built with 💡 for learning Clean Hexagonal Architecture**