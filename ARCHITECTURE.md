# Clean Hexagonal Architecture Diagram

## 🏗️ System Architecture Overview

```
                              🖥️ PRESENTATION LAYER
    ┌─────────────────────────────────────────────────────────────┐
    │                 Console Interface                           │
    │        (infrastructure/adapters/presentation/)              │
    └─────────────────┬───────────────────────────────────────────┘
                      │ Dependencies point INWARD
                      ▼
                              ⚡ APPLICATION LAYER
    ┌─────────────────────────────────────────────────────────────┐
    │                   USE CASES                                 │
    │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
    │  │   Product   │ │  Customer   │ │    Order    │           │
    │  │   Service   │ │   Service   │ │   Service   │           │
    │  └─────────────┘ └─────────────┘ └─────────────┘           │
    │         │              │              │                    │
    │         ▼              ▼              ▼                    │
    │                    PORTS (Interfaces)                      │
    │  ┌─────────────┐                    ┌─────────────┐        │
    │  │ Repository  │                    │   Service   │        │
    │  │    Ports    │                    │    Ports    │        │
    │  │             │                    │             │        │
    │  │ - Product   │                    │ - Payment   │        │
    │  │ - Order     │                    │ - Notify    │        │
    │  │ - Customer  │                    │ - Inventory │        │
    │  └─────────────┘                    └─────────────┘        │
    └─────────────────┬───────────────────────┬───────────────────┘
                      │ Dependencies point    │ Dependencies point
                      │ INWARD to domain      │ INWARD to domain
                      ▼                       ▼
                              🔷 DOMAIN LAYER (CORE)
    ┌─────────────────────────────────────────────────────────────┐
    │                    ENTITIES                                 │
    │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
    │  │   Product   │ │   Customer  │ │    Order    │           │
    │  │   Entity    │ │   Entity    │ │   Entity    │           │
    │  └─────────────┘ └─────────────┘ └─────────────┘           │
    │                                                             │
    │                 VALUE OBJECTS                               │
    │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
    │  │ OrderStatus │ │PaymentResult│ │  OrderItem  │           │
    │  │   (enum)    │ │ (dataclass) │ │   Entity    │           │
    │  └─────────────┘ └─────────────┘ └─────────────┘           │
    └─────────────────────────────────────────────────────────────┘
                      ▲                       ▲
                      │ Dependencies point    │ Dependencies point  
                      │ INWARD to domain      │ INWARD to domain
    ┌─────────────────┴───────────────────────┴───────────────────┐
    │                🔧 INFRASTRUCTURE LAYER                      │
    │                                                             │
    │  PERSISTENCE ADAPTERS          EXTERNAL SERVICE ADAPTERS   │
    │  ┌─────────────┐                ┌─────────────┐            │
    │  │ InMemory    │                │    Mock     │            │
    │  │ Product     │                │   Payment   │            │
    │  │ Repository  │                │   Gateway   │            │
    │  └─────────────┘                └─────────────┘            │
    │  ┌─────────────┐                ┌─────────────┐            │
    │  │ InMemory    │                │   Console   │            │
    │  │   Order     │                │Notification │            │
    │  │ Repository  │                │   Service   │            │
    │  └─────────────┘                └─────────────┘            │
    │  ┌─────────────┐                ┌─────────────┐            │
    │  │ InMemory    │                │    Mock     │            │
    │  │ Customer    │                │ Inventory   │            │
    │  │ Repository  │                │   Service   │            │
    │  └─────────────┘                └─────────────┘            │
    └─────┬───────────┘                └─────┬───────────────────┘
          │                                  │
          ▼                                  ▼
    💾 DATA STORAGE                    🌐 EXTERNAL SYSTEMS
    ┌─────────────────┐                ┌─────────────────┐
    │   In-Memory     │                │  Payment APIs   │
    │   Collections   │                │  Email/SMS      │
    │                 │                │  Inventory Mgmt │
    │ (Easily         │                │                 │
    │  replaceable    │                │ (Easily         │
    │  with real DB)  │                │  replaceable)   │
    └─────────────────┘                └─────────────────┘
```

## 🎯 Clean Architecture Principles Applied

### 1. **The Dependency Rule**
> Dependencies point inward. Source code dependencies can only point inward.

- **✅ Infrastructure → Application**: Adapters implement ports defined in application layer
- **✅ Application → Domain**: Use cases orchestrate domain entities
- **❌ Domain → Application**: Domain never depends on application layer
- **❌ Domain → Infrastructure**: Domain never depends on external concerns

### 2. **Layer Responsibilities**

#### 🔷 Domain Layer (Enterprise Business Rules)
```python
# Pure business logic - no external dependencies
class Order:
    def update_status(self, new_status: OrderStatus):
        if not self._is_valid_status_transition(self.status, new_status):
            raise ValueError("Invalid status transition")
        self.status = new_status
        self.updated_at = datetime.now()
```

#### ⚡ Application Layer (Application Business Rules)
```python
# Orchestrates domain + defines contracts for external systems
class OrderService:
    def __init__(self, order_repository: OrderRepository):  # ← Port (Interface)
        self._order_repository = order_repository
    
    def confirm_order(self, order_id: str) -> bool:
        order = self._order_repository.find_by_id(order_id)  # ← Use port
        # ... business logic using domain objects
```

#### 🔧 Infrastructure Layer (Frameworks & Drivers)
```python
# Implements ports defined in application layer
class InMemoryOrderRepository(OrderRepository):  # ← Implements port
    def find_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
```

## 🔄 Data Flow Example: Creating an Order

```
1. 👤 User Input → ConsoleInterface.create_order()
        ↓ (Infrastructure → Application)
2. 🖥️ ConsoleInterface → OrderService.create_order()
        ↓ (Application orchestrates)
3. ⚡ OrderService → validates via ProductRepository port
        ↓ (Application → Infrastructure via port)
4. 🔧 InMemoryProductRepository → returns product data
        ↓ (Infrastructure returns data)
5. ⚡ OrderService → creates Order entity (domain logic)
        ↓ (Application → Domain)
6. 🔷 Order.add_item() → pure domain behavior
        ↓ (Domain logic)
7. ⚡ OrderService → reserves via InventoryService port
        ↓ (Application → Infrastructure via port)
8. 🔧 MockInventoryService → simulates reservation
        ↓ (Infrastructure simulation)
9. ⚡ OrderService → saves via OrderRepository port
        ↓ (Application → Infrastructure via port)
10. 🔧 InMemoryOrderRepository → persists order
        ↓ (Infrastructure persistence)
11. 🖥️ ConsoleInterface ← returns success/failure
        ↓ (Infrastructure ← Application)
12. 👤 User receives confirmation
```

## 📁 File Organization by Layer

### 🔷 Domain Layer (Innermost)
```
domain/
├── entities/           # Objects with identity and behavior
│   ├── product.py     # Product business logic
│   ├── customer.py    # Customer business logic  
│   ├── order.py       # Order aggregate root
│   └── order_item.py  # Order item logic
└── value_objects/     # Immutable data structures
    ├── order_status.py    # Status enumeration
    └── payment_result.py  # Payment data
```

### ⚡ Application Layer (Middle)
```
application/
├── ports/             # Interfaces (contracts)
│   ├── repositories/  # Data access contracts
│   └── services/      # External service contracts
└── use_cases/         # Application-specific business rules
    ├── product_service.py   # Product use cases
    ├── customer_service.py  # Customer use cases
    └── order_service.py     # Order use cases
```

### 🔧 Infrastructure Layer (Outermost)
```
infrastructure/
└── adapters/          # Implementations of ports
    ├── persistence/   # Data storage implementations
    ├── external_services/  # Third-party service implementations
    └── presentation/  # User interface implementations
```

## 🧪 Testing Strategy by Layer

### Unit Tests (Domain Layer)
```python
def test_order_total_calculation():
    # Test pure domain logic
    items = [OrderItem("p1", "Pizza", 2, 10.0)]
    order = Order("o1", "c1", items, OrderStatus.PENDING, datetime.now(), datetime.now())
    assert order.total_amount == 20.0

def test_invalid_status_transition():
    order = Order(...)
    with pytest.raises(ValueError):
        order.update_status(OrderStatus.DELIVERED)  # Invalid from PENDING
```

### Integration Tests (Application Layer)
```python
def test_order_service_with_mocks():
    # Test use cases with mocked infrastructure
    mock_repo = Mock(spec=OrderRepository)
    mock_payment = Mock(spec=PaymentGateway)
    
    service = OrderService(mock_repo, ..., mock_payment, ...)
    result = service.create_order("customer_id", [{"product_id": "p1", "quantity": 1}])
    
    assert result is not None
    mock_repo.save.assert_called_once()
```

### End-to-End Tests (Infrastructure Layer)
```python
def test_complete_order_flow():
    # Test with real adapters
    real_repos = setup_real_repositories()
    real_services = setup_real_external_services()
    
    # Test complete flow from presentation to persistence
```

## 🔄 Architecture Evolution Examples

### Adding Real Database Support
```python
# 1. Create new infrastructure adapter
class PostgreSQLOrderRepository(OrderRepository):
    def save(self, order: Order) -> None:
        # SQL implementation
        pass

# 2. Update dependency injection in main.py
def main():
    order_repository = PostgreSQLOrderRepository(connection_string)  # ← Change here
    order_service = OrderService(order_repository, ...)
    
    # ✅ Domain and Application layers unchanged!
```

### Adding Web API Interface
```python
# 1. Create new presentation adapter
class FastAPIInterface:
    def __init__(self, order_service: OrderService):
        self._order_service = order_service
    
    @app.post("/orders")
    def create_order(self, request: CreateOrderRequest):
        return self._order_service.create_order(...)

# 2. Update main.py
def main():
    # Same use cases, different presentation
    web_interface = FastAPIInterface(order_service)  # ← New interface
    
    # ✅ Domain and Application layers unchanged!
```

### Adding New Payment Provider
```python
# 1. Create new external service adapter
class StripePaymentGateway(PaymentGateway):
    def process_payment(self, order: Order, customer: Customer) -> PaymentResult:
        # Stripe API integration
        pass

# 2. Update dependency injection
def main():
    payment_gateway = StripePaymentGateway(stripe_api_key)  # ← Change here
    order_service = OrderService(..., payment_gateway, ...)
    
    # ✅ Domain and Application layers unchanged!
```

## 🏆 Architecture Benefits Achieved

### ✅ **Independence**
- **Framework Independence**: Can change from Flask to FastAPI without touching business logic
- **Database Independence**: Can switch from PostgreSQL to MongoDB without changing use cases
- **UI Independence**: Can add web, mobile, CLI interfaces using same use cases

### ✅ **Testability**
- **Domain**: Test pure business logic in isolation
- **Application**: Test use cases with mocked infrastructure
- **Infrastructure**: Test adapters with real external systems

### ✅ **Maintainability**
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Dependency Inversion**: Depend on abstractions, not concretions

### ✅ **Flexibility**
- **Business Rules**: Centralized in domain layer
- **Use Cases**: Reusable across different interfaces
- **Infrastructure**: Swappable without affecting business logic

## 📏 Architecture Metrics

| Metric | Score | Description |
|--------|-------|-------------|
| **Coupling** | 🟢 Low | Layers communicate through well-defined interfaces |
| **Cohesion** | 🟢 High | Related functionality grouped together |
| **Complexity** | 🟡 Medium | More complex than simple layered, but manageable |
| **Testability** | 🟢 Very High | Easy to test at all levels with dependency injection |
| **Maintainability** | 🟢 Very High | Changes localized to specific layers |
| **Extensibility** | 🟢 Very High | New features added without modifying existing code |

---

This architecture demonstrates how proper separation of concerns and dependency management create a robust, maintainable, and testable system that can evolve with changing business requirements while keeping the core business logic stable and protected.