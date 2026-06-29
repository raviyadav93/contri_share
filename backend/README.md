# contri_share Backend API

FastAPI-based backend service for the contri_share expense sharing application.

## Architecture

### Modular Structure
- **core/**: Configuration, database setup, security utilities
- **models/**: SQLModel data models with type hints
- **schemas/**: Pydantic v2 request/response validation
- **services/**: Business logic layer (CRUD, calculations)
- **api/v1/endpoints/**: REST API route handlers

### Key Features
- Async SQLAlchemy queries with SQLModel ORM
- Pydantic v2 data validation with strict type checking
- JWT-based authentication (bcrypt password hashing)
- CORS middleware for frontend integration
- Global exception handlers with structured error responses
- SQLite development / PostgreSQL production support

## Database Models

### User
- id, email, username, hashed_password, full_name, is_active
- Timestamps: created_at, updated_at

### Group
- id, name, description, owner_id, currency
- Timestamps: created_at, updated_at

### Expense
- id, group_id, paid_by_id, description, amount, category, expense_date
- Timestamps: created_at, updated_at

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
python main.py
```

## API Documentation

Auto-generated docs available at `/api/v1/docs` (Swagger UI)
