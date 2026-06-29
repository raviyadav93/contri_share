# Architecture Guide

This document outlines the architectural patterns used in contri_share.

## Backend Architecture

### Layered Architecture

```
HTTP Request
    ↓
[API Layer] - Route handlers, request validation, response formatting
    ↓
[Service Layer] - Business logic, calculations, transactions
    ↓
[Data Layer] - ORM queries, database operations
    ↓
[Database] - PostgreSQL/SQLite
```

### Dependency Injection

FastAPI's `Depends` pattern is used for dependency injection:

```python
# core/database.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# api/v1/endpoints/users.py
@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)  # Injected dependency
) -> UserResponse:
    user = await UserService.get_user_by_id(db, user_id)
    return user
```

### Error Handling

Custom exception hierarchy with global exception handlers:

```python
# exceptions.py
class AppException(Exception):
    def __init__(self, message: str, status_code: int, error_code: str):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

# main.py
app.add_exception_handler(AppException, app_exception_handler)
```

### Data Validation

Pydantic v2 schemas at API boundary:

```python
# schemas/user.py
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Route handler validates automatically
@router.post("")
async def create_user(user_create: UserCreate) -> UserResponse:
    # user_create is guaranteed valid here
    user = await UserService.create_user(db, user_create)
    return user
```

## Frontend Architecture

### Component Organization

**Feature-Sliced Design Pattern:**

```
features/
  ├── dashboard/
  │   └── Dashboard.jsx          # Feature root
  ├── groups/
  │   ├── GroupList.jsx          # Public component
  │   └── GroupCard.jsx          # Private component
  └── expenses/
      ├── ExpenseForm.jsx
      └── ExpenseList.jsx

components/                       # Shared components
hooks/                           # Shared hooks
services/                        # Shared services
```

### Custom Hooks Pattern

Extract data fetching and state logic into custom hooks:

```jsx
// hooks/useApi.js
function useApi() {
  const get = async (url) => apiClient.get(url)
  const post = async (url, data) => apiClient.post(url, data)
  return { get, post }
}

// features/groups/GroupList.jsx
function GroupList() {
  const [groups, setGroups] = useState([])
  const { get } = useApi()
  
  useEffect(() => {
    get('/api/v1/groups').then(res => setGroups(res.data))
  }, [])
}
```

### Service Layer

Centralized API client with interceptors:

```jsx
// services/api.js
const apiClient = axios.create({ baseURL: API_BASE_URL })

// Request interceptor - add auth token
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor - handle 401
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

## Database Design

### Entity Relationships

```
User (1) ──→ (Many) Group
     └──→ (Many) Expense (as paid_by)

Group (1) ──→ (Many) Expense
```

### Timestamp Tracking

All entities include `created_at` and `updated_at`:

```python
class TimestampMixin:
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, TimestampMixin, table=True):
    # ...
```

## API Design

### Versioning

API routes grouped by version:

```
/api/v1/
  /health
  /users
  /groups
  /expenses
```

### Response Format

Consistent response format with proper HTTP status codes:

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "is_active": true
}
```

### Error Responses

Structured error format:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with id 999 not found",
    "path": "/api/v1/users/999"
  }
}
```

## Security Architecture

### Authentication (Future)

JWT-based authentication with refresh tokens:

```
Login Request
    ↓
Validate credentials
    ↓
Issue access token (short-lived) + refresh token (long-lived)
    ↓
Client stores tokens
    ↓
Send access token with each request
    ↓
Token expires → use refresh token to get new access token
```

### Authorization

Role-based access control (RBAC) - future enhancement:

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    # Validate JWT
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    # ...

@router.get("/groups/{group_id}")
async def get_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> GroupResponse:
    # Only group members can access
    # ...
```

## Performance Considerations

### Backend

1. **Async Operations:** All I/O operations are non-blocking
2. **Connection Pooling:** SQLAlchemy handles connection pool
3. **Query Optimization:** Use `.select()` instead of `.query()`
4. **Indexing:** Create indexes on frequently queried columns

```python
class User(SQLModel, table=True):
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
```

### Frontend

1. **Code Splitting:** Vite automatically splits by route
2. **Lazy Loading:** React Router supports lazy component loading
3. **Caching:** Service Worker caches static assets
4. **CSS Variables:** Minimal CSS bundle size

## Testing Strategy

### Backend (Pyramid)

```
        /\
       /  \ E2E Tests (API integration)
      /    \
     /______\
    /\      /\
   /  \    /  \ Integration Tests (DB queries)
  /____\  /____\
 /\    /\/\    /\
/  \  /    \  /  \ Unit Tests (Services, utils)
\____/______\/____/
```

### Frontend

```
        /\
       /  \ E2E Tests (Cypress, Playwright)
      /    \
     /______\
    /\      /\
   /  \    /  \ Integration Tests (Component + hooks)
  /____\  /____\
 /\    /\/\    /\
/  \  /    \  /  \ Unit Tests (Utils, hooks)
\____/______\/____/
```

## Monitoring & Observability

### Logging

```python
import logging
logger = logging.getLogger(__name__)

logger.info("User created", extra={"user_id": user.id})
logger.error("Database error", exc_info=True)
```

### Metrics (Future)

- API response times
- Database query latencies
- Error rates
- Cache hit rates

### Health Checks

```python
@router.get("/health")
async def health_check() -> dict:
    return {
        "status": "healthy",
        "service": "contri_share-api",
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Deployment Strategy

### Environment Parity

- Development: SQLite, live reload, verbose logging
- Staging: PostgreSQL, read-only replicas, monitoring enabled
- Production: PostgreSQL with backups, load balancing, CDN

### Rolling Deployments

```yaml
# Kubernetes deployment strategy
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

## Scaling Considerations

1. **Horizontal Scaling:** Multiple API replicas with load balancer
2. **Database Scaling:** Read replicas for read-heavy workloads
3. **Caching Layer:** Redis for session/cache management
4. **CDN:** CloudFront for static assets
5. **Background Jobs:** Celery for long-running tasks
