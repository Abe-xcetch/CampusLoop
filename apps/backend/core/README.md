# Django Clean Architecture & Domain-Driven Design (DDD)

This backend is organized using a **Feature-Based Modular** structure where each feature is represented as a self-contained Django application inside `core/`. Within each feature app, we apply **Clean Architecture** principles to separate business rule logic from the framework and database.

## Architecture Layers

For any feature app (e.g., `core/listings/`), the internal layout is structured as follows:

```
core/listings/
├── domain/                  # DOMAIN LAYER (Enterprise Business Rules)
│   ├── models.py            # Pure Python Entities and Value Objects (decoupled from ORM)
│   ├── exceptions.py        # Domain-specific validation errors
│   └── events.py            # Domain events (e.g. ListingFlaggedDomainEvent)
│
├── application/             # APPLICATION LAYER (Application Business Rules)
│   ├── use_cases.py         # Business operations orchestration (e.g. ApproveListingUseCase)
│   ├── services.py          # Application services coordinating transactions
│   └── tasks.py             # Celery background tasks (e.g. queue_listing_approval_notification)
│
├── infrastructure/          # INFRASTRUCTURE LAYER (Gateways, DB, Framework adapters)
│   ├── orm_models.py        # Django ORM models representing tables
│   ├── repositories.py      # Abstract repository implementations mapping ORM <-> Domain Entities
│   └── adapters/            # External services implementations (e.g. Firebase storage adapter)
│
└── presentation/            # PRESENTATION LAYER (API Entrypoints)
    ├── views.py             # DRF ViewSets / APIViews
    ├── serializers.py       # DRF serializers (mapping presentation inputs)
    ├── permissions.py       # DRF custom authorization rules (e.g. IsListingSeller)
    └── signals.py           # Django framework signal receivers
```

---

## Data Flow Pipeline

1. **HTTP Request** arrives at Django Router (`config/urls.py` -> `core/listings/presentation/views.py`).
2. **Presentation Layer** validates the request parameters using DRF **Serializers** and validates security permissions using **Permissions**.
3. The **View** calls the corresponding **Use Case** in the **Application Layer**.
4. The **Use Case** interacts with the database abstractly via a **Repository** interface.
5. The **Repository** retrieves Django ORM models from the database and maps them to pure Python **Domain Entities**.
6. The **Use Case** executes domain logic on the **Domain Entities** and saves updates back to the **Repository**.
7. If needed, the **Use Case** triggers a **Celery Task** in the background or publishes a **Domain Event**.
8. The **View** returns a JSON response to the client.
