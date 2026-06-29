# contri_share - Production-Ready Boilerplate

## 1. Architectural Overview

**Monorepo Structure:** Isolated `/backend` (FastAPI) and `/frontend` (React + Vite) with decoupled deployments.

**Purpose:** Production-grade expense sharing platform demonstrating clean architecture, type safety, async patterns, and PWA capabilities.

---

## 2. Tech Stack

### Backend (`/backend`)
- **Framework:** FastAPI 0.136+ (async/await, dependency injection)
- **ORM:** SQLModel 0.0.18 + SQLAlchemy 2.0 (type-safe ORM)
- **Validation:** Pydantic v2 (strict schemas)
- **Auth:** JWT (python-jose) + bcrypt password hashing
- **Server:** Uvicorn ASGI
- **Database:** SQLite (dev) / PostgreSQL (production)

**Core Modules:**
- `core/config.py` - Settings management with environment variables
- `core/database.py` - Async session factory and dependency injection
- `core/security.py` - JWT creation, password verification
- `models/` - SQLModel entities (User, Group, Expense) with timestamps
- `schemas/` - Pydantic v2 request/response validation
- `services/` - Business logic layer (CRUD operations)
- `api/v1/endpoints/` - Route handlers (health, users, groups, expenses)
- `exceptions.py` - Centralized error handling

### Frontend (`/frontend`)
- **Framework:** React 18.3+ (functional components, hooks)
- **Build Tool:** Vite 5.0+ (fast HMR, optimized builds)
- **PWA:** vite-plugin-pwa (service workers, manifest, offline)
- **HTTP:** Axios (interceptors for auth tokens)
- **Routing:** React Router v6
- **Styling:** CSS3 with CSS variables for theming

**Architecture:**
- `components/` - Reusable UI components (Layout, Navbar)
- `features/` - Feature-sliced modules (dashboard, groups, expenses)
- `hooks/` - Custom hooks (useApi for data fetching)
- `services/` - Axios client with request/response interceptors
- `App.jsx` - Root component with health check
- `App.css` - Global styles with semantic color/spacing variables

---

## 3. Project Structure

```
contri_share/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py       # Settings, environment
│   │   │   ├── database.py     # Async SQLAlchemy setup
│   │   │   └── security.py     # JWT, password hashing
│   │   ├── models/
│   │   │   ├── base.py         # TimestampMixin
│   │   │   ├── user.py         # User SQLModel
│   │   │   ├── group.py        # Group SQLModel
│   │   │   └── expense.py      # Expense SQLModel
│   │   ├── schemas/
│   │   │   ├── user.py         # User Pydantic schemas
│   │   │   ├── group.py        # Group Pydantic schemas
│   │   │   └── expense.py      # Expense Pydantic schemas
│   │   ├── services/
│   │   │   ├── user_service.py    # User CRUD
│   │   │   ├── group_service.py   # Group CRUD
│   │   │   └── expense_service.py # Expense CRUD
│   │   ├── api/v1/endpoints/
│   │   │   ├── health.py       # /api/v1/health
│   │   │   ├── users.py        # /api/v1/users/*
│   │   │   ├── groups.py       # /api/v1/groups/*
│   │   │   └── expenses.py     # /api/v1/expenses/*
│   │   └── exceptions.py       # Custom exceptions & handlers
│   ├── main.py                 # FastAPI app, CORS, routes
│   ├── pyproject.toml          # Python dependencies (uv/pip)
│   ├── .env.example            # Environment template
│   └── README.md               # Backend docs
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.jsx      # Main layout wrapper
│   │   ├── features/
│   │   │   ├── dashboard/
│   │   │   │   └── Dashboard.jsx
│   │   │   ├── groups/
│   │   │   │   └── GroupList.jsx
│   │   │   └── expenses/
│   │   ├── hooks/
│   │   │   └── useApi.js       # Data fetching hook
│   │   ├── services/
│   │   │   └── api.js          # Axios client
│   │   ├── App.jsx             # Root component
│   │   ├── App.css             # Global styles
│   │   └── main.jsx            # React entry
│   ├── public/
│   │   └── manifest.json       # PWA manifest
│   ├── vite.config.js          # Vite + PWA config
│   ├── package.json            # Node dependencies
│   ├── tsconfig.json           # TypeScript config
│   ├── .env.example            # Environment template
│   └── README.md               # Frontend docs
│
├── .gitignore
├── README.md                   # Root documentation
└── context.md                  # This file
```

---

## 4. API Specification

### Health Check
```http
GET /api/v1/health
Response: { "status": "healthy", "service": "contri_share-api" }
```

### Users
```http
POST   /api/v1/users              # Create user
GET    /api/v1/users/{user_id}    # Get user
PATCH  /api/v1/users/{user_id}    # Update user
```

### Groups
```http
POST   /api/v1/groups             # Create group
GET    /api/v1/groups             # List user groups
GET    /api/v1/groups/{group_id}  # Get group
PATCH  /api/v1/groups/{group_id}  # Update group
DELETE /api/v1/groups/{group_id}  # Delete group
```

### Expenses
```http
POST   /api/v1/expenses                    # Create expense
GET    /api/v1/expenses/{expense_id}       # Get expense
GET    /api/v1/expenses/group/{group_id}   # List group expenses
PATCH  /api/v1/expenses/{expense_id}       # Update expense
DELETE /api/v1/expenses/{expense_id}       # Delete expense
```

---

## 5. Database Models

### User
```python
id (PK), email (UNIQUE), username (UNIQUE), hashed_password, 
full_name, is_active, created_at, updated_at
```

### Group
```python
id (PK), name, description, owner_id (FK→User), currency, 
created_at, updated_at
```

### Expense
```python
id (PK), group_id (FK→Group), paid_by_id (FK→User), 
description, amount, category, expense_date, created_at, updated_at
```

---

## 6. Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e .
cp .env.example .env
python main.py
```
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/api/v1/docs`

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
- App: `http://localhost:5173`

---

## 7. Configuration

### Backend (.env)
```
DATABASE_URL=sqlite:///./contri_share.db
DEBUG=True
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
SECRET_KEY=your-secret-key-change-in-production
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000
```

---

## 8. Coding Standards

1. **Type Hinting:** All Python functions use explicit type hints
2. **Separation of Concerns:** 
   - Routes handle HTTP only
   - Services contain business logic
   - Models define data structures
3. **Async-First:** All I/O operations are async
4. **Error Handling:** Centralized exception handlers with structured responses
5. **React Patterns:**
   - Functional components with hooks
   - Custom hooks for reusable logic
   - Feature-sliced organization
6. **Validation:** Pydantic schemas at API boundary

---

## 9. Key Design Decisions

- **Async SQLAlchemy:** Supports high concurrency
- **SQLModel:** Single source of truth for DB and validation
- **Pydantic v2:** Strict validation with better performance
- **Feature-Sliced Frontend:** Scalable, modular component organization
- **PWA Support:** Offline capability and app-like experience
- **CSS Variables:** Easy theming and design token management
- **Custom useApi Hook:** Centralized data fetching with consistent error handling

---

## 10. Next Steps (Future Enhancements)

- [ ] JWT refresh token mechanism
- [ ] User authentication (login/signup)
- [ ] Expense split algorithms (equal, percentage, exact)
- [ ] Settlement calculation (minimize payment transfers)
- [ ] Group membership management
- [ ] Notification system (email/push)
- [ ] Database migrations (Alembic)
- [ ] Comprehensive test suites (pytest, vitest)
- [ ] CI/CD pipelines (GitHub Actions)
- [ ] Mobile-first responsive optimization
- [ ] API request logging and monitoring
- [ ] Rate limiting and DDoS protection

---

## 11. Production Deployment

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports: ['8000:8000']
    environment:
      DATABASE_URL: postgresql://user:pass@db/contri_share
      SECRET_KEY: ${SECRET_KEY}
  
  frontend:
    build: ./frontend
    ports: ['80:80']
    depends_on: [backend]
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: contri_share
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

### Environment-Specific Configs
- **Development:** SQLite, DEBUG=True, CORS open
- **Staging:** PostgreSQL, DEBUG=False, limited CORS
- **Production:** PostgreSQL, DEBUG=False, strict CORS, HTTPS only

---

## 12. Testing

### Backend
```bash
cd backend
pytest tests/
pytest --cov=app tests/
```

### Frontend
```bash
cd frontend
npm test
npm run type-check
```

---

## 13. Performance Optimization

- Async database queries with connection pooling
- Service worker caching for static assets
- API response caching via Workbox
- Database indexing on frequently queried columns
- Code splitting in Vite build
- CSS variable reuse for efficient styling

---

## 14. Security Considerations

- CORS properly configured per environment
- JWT tokens with short expiration
- Password hashing with bcrypt
- SQL injection prevention via SQLModel ORM
- Request validation with Pydantic
- HTTPS enforced in production
- Secrets managed via environment variables
- Rate limiting for API endpoints (TODO)

---

## References

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com)
- [React 18 Hooks](https://react.dev/reference/react/hooks)
- [Vite Guide](https://vitejs.dev/guide)
- [PWA Workbox](https://developers.google.com/web/tools/workbox)