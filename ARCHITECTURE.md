# Hexagonal Architecture Diagram

## 🏗️ System Architecture Overview

```
                    🖥️ USER INTERFACES (Adapters)
                    ┌─────────────────────────────┐
                    │     Console Interface       │
                    │    (interface/console.py)   │
                    └─────────────┬───────────────┘
                                  │
                    ⚡ APPLICATION LAYER (Use Cases)
                    ┌─────────────────────────────┐
                    │    Application Services     │
                    │   - ProductService          │
                    │   - CustomerService         │
                    │   - OrderService            │
                    │  (application/services.py)  │
                    └─────────────┬───────────────┘
                                  │
    🔌 PORTS (Interfaces)         │         🔌 PORTS (Interfaces)
    ┌─────────────────┐          │          ┌─────────────────┐
    │  Repository     │          │          │    Service      │
    │    Ports        │          │          │     Ports       │
    │                 │          │          │                 │
    │ - Product       │◄─────────┼─────────►│ - Payment       │
    │ - Order         │          │          │ - Notification  │
    │ - Customer      │          │          │ - Inventory     │
    └─────┬───────────┘          │          └─────┬───────────┘
          │                      │                │
          │        🔷 DOMAIN CORE (Business Logic) │
          │        ┌─────────────────────────────┐ │
          │        │         Entities            │ │
          │        │       - Product             │ │
          │        │       - Order               │ │
          │        │       - Customer            │ │
          │        │       - OrderItem           │ │
          │        │                             │ │
          │        │       Value Objects         │ │
          │        │       - OrderStatus         │ │
          │        │       - PaymentResult       │ │
          │        │   (domain/entities.py)      │ │
          │        └─────────────────────────────┘ │
          │                                        │
    🔧 ADAPTERS (Implementations)         🔧 ADAPTERS (Implementations)
    ┌─────────────────┐                  ┌─────────────────┐
    │   Repository    │                  │    Service      │
    │    Adapters     │                  │    Adapters     │
    │                 │                  │                 │
    │ - InMemory      │                  │ - Mock Payment  │
    │   Product Repo  │                  │ - Console       │
    │ - InMemory      │                  │   Notifications │
    │   Order Repo    │                  │ - Mock          │
    │ - InMemory      │                  │   Inventory     │
    │   Customer Repo │                  │                 │
    └─────┬───────────┘                  └─────┬───────────┘
          │                                    │
          ▼                                    ▼
    💾 DATA STORAGE                    🌐 EXTERNAL SYSTEMS
    ┌─────────────────┐                ┌─────────────────┐
    │   In-Memory     │                │  Payment APIs   │
    │   Collections   │                │  Email Services │
    │                 │                │  SMS Services   │
    │ (Easily         │                │  Inventory      │
    │  replaceable    │                │  Management     │
    │  with real DB)  │                │                 │
    └─────────────────┘                └─────────────────┘
```

## 🔄 Data Flow Example: Creating an Order

```
1. 👤 User (Console) → "Create Order"
        ↓
2. 🖥️ Console Interface → calls OrderService.create_order()
        ↓  
3. ⚡ OrderService → validates products via ProductRepository (port)
        ↓
4. 🔧 InMemoryProductRepository (adapter) → returns product data
        ↓
5. ⚡ OrderService → creates Order entity (domain logic)
        ↓
6. ⚡ OrderService → reserves inventory via InventoryService (port)
        ↓
7. 🔧 MockInventoryService (adapter) → simulates reservation
        ↓
8. ⚡ OrderService → saves order via OrderRepository (port)
        ↓
9. 🔧 InMemoryOrderRepository (adapter) → persists order
        ↓
10. 🖥️ Console Interface ← returns order confirmation
        ↓
11. 👤 User receives confirmation
```

## 🎯 Key Architectural Decisions

### 1. **Ports (Interfaces) Design**
- **Repository Ports**: Abstract data access (save, find, delete)
- **Service Ports**: Abstract external services (payment, notifications)
- **Consistent Contracts**: Same interface regardless of implementation

### 2. **Adapter Implementations**  
- **In-Memory Repositories**: Simple for demo, easily replaceable
- **Mock External Services**: Simulate real services with console output
- **Console Interface**: Text-based UI that could be replaced with web/mobile

### 3. **Domain Layer Isolation**
- **Pure Business Logic**: No external dependencies
- **Rich Entities**: Order calculates total, manages status
- **Value Objects**: Immutable data structures (OrderStatus, PaymentResult)

### 4. **Application Services (Use Cases)**
- **Orchestration**: Coordinate between domain and infrastructure  
- **Transaction Boundaries**: Handle complete business operations
- **Validation**: Business rule enforcement

### 5. **Dependency Injection**
```python
# Easy to swap implementations
order_service = OrderService(
    InMemoryOrderRepository(),     # Could be: PostgreSQLOrderRepository()
    MockPaymentGateway(),          # Could be: StripePaymentGateway()
    ConsoleNotificationService(),  # Could be: EmailNotificationService()
    # ...
)
```

## 🧪 Testing Strategy

### Unit Tests (Inner Layers)
```python
# Test domain logic in isolation
def test_order_total_calculation():
    order = Order(...)
    assert order.total_amount == expected_total

# Test application services with mocks
def test_order_creation():
    mock_repo = MockOrderRepository()
    service = OrderService(mock_repo, ...)
    # Test business logic without external dependencies
```

### Integration Tests (Outer Layers)
```python
# Test with real adapters
def test_database_integration():
    real_db_repo = PostgreSQLOrderRepository()
    service = OrderService(real_db_repo, ...)
    # Test actual database interactions
```

## 🔄 Evolution Examples

### Replacing Payment System:
```python
# Before: Mock payment
payment_gateway = MockPaymentGateway()

# After: Real payment provider
payment_gateway = StripePaymentGateway(api_key="...")

# ✅ No changes needed in business logic!
```

### Adding Web Interface:
```python
# Current: Console interface
console = ConsoleInterface(product_service, ...)

# Future: Web interface  
web_app = FlaskWebInterface(product_service, ...)
api = FastAPIInterface(product_service, ...)

# ✅ Same services, different adapters!
```

### Database Migration:
```python
# Current: In-memory storage
repos = InMemoryRepositories()

# Future: Real database
repos = PostgreSQLRepositories(connection_string)

# ✅ Core logic unchanged!
```

## 🏆 Benefits Achieved

### ✅ **Testability**
- Easy unit testing with mocks
- Integration testing with real adapters
- Business logic tested in isolation

### ✅ **Maintainability**  
- Clear separation of concerns
- Changes in one layer don't affect others
- Easy to understand and modify

### ✅ **Flexibility**
- Swap implementations without code changes
- Add new interfaces (web, mobile) easily  
- Technology-agnostic core

### ✅ **Scalability**
- Core logic can handle increased complexity
- Infrastructure can be scaled independently
- Easy to add new features

---

This architecture demonstrates how the hexagonal pattern creates a robust, maintainable, and testable system that can evolve with changing requirements while keeping the business logic stable and protected.
