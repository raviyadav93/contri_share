# contri_share - A Splitwise Clone

A production-ready monorepo for expense sharing built with FastAPI and React.

## Project Structure

```
contri_share/
├── backend/                  # FastAPI backend service
│   ├── app/
│   │   ├── core/            # Core config, database, security
│   │   ├── models/          # SQLModel data models
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── services/        # Business logic layer
│   │   └── api/
│   │       └── v1/
│   │           └── endpoints/  # Route handlers
│   ├── main.py              # FastAPI application entry point
│   ├── pyproject.toml       # Python dependencies
│   └── .env.example         # Environment variables template
│
└── frontend/                # React + Vite frontend application
    ├── src/
    │   ├── components/      # Reusable UI components
    │   ├── features/        # Feature-sliced modules
    │   │   ├── dashboard/   # Dashboard feature
    │   │   ├── groups/      # Groups feature
    │   │   └── expenses/    # Expenses feature
    │   ├── hooks/           # Custom React hooks
    │   ├── services/        # API integration
    │   ├── App.jsx          # Root component
    │   ├── App.css          # Global styles
    │   └── main.jsx         # Entry point
    ├── public/              # Static assets & manifest
    ├── vite.config.js       # Vite + PWA configuration
    ├── package.json         # Node dependencies
    ├── tsconfig.json        # TypeScript config
    └── .env.example         # Environment variables template
```

## Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment (Python 3.11+)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Create .env file
cp .env.example .env

# Run development server
python main.py
```

API will be available at `http://localhost:8000`  
Interactive docs: `http://localhost:8000/api/v1/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run development server
npm run dev
```

App will be available at `http://localhost:5173`

## API Endpoints

### Health Check
- `GET /api/v1/health` - Service health status

### Users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{user_id}` - Get user
- `PATCH /api/v1/users/{user_id}` - Update user

### Groups
- `POST /api/v1/groups` - Create group
- `GET /api/v1/groups` - List user groups
- `GET /api/v1/groups/{group_id}` - Get group
- `PATCH /api/v1/groups/{group_id}` - Update group
- `DELETE /api/v1/groups/{group_id}` - Delete group

### Expenses
- `POST /api/v1/expenses` - Create expense
- `GET /api/v1/expenses/{expense_id}` - Get expense
- `GET /api/v1/expenses/group/{group_id}` - List group expenses
- `PATCH /api/v1/expenses/{expense_id}` - Update expense
- `DELETE /api/v1/expenses/{expense_id}` - Delete expense

## Technology Stack

### Backend
- **Framework**: FastAPI 0.136+
- **ORM**: SQLModel + SQLAlchemy 2.0
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Validation**: Pydantic v2
- **Auth**: JWT + bcrypt
- **Server**: Uvicorn ASGI

### Frontend
- **Framework**: React 18.3+
- **Build Tool**: Vite 5.0+
- **PWA**: vite-plugin-pwa
- **HTTP Client**: Axios
- **Router**: React Router v6
- **Styling**: CSS3 with CSS variables

## Environment Configuration

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
VITE_APP_NAME=contri_share
```

## Production Deployment

### Backend
```bash
# Use PostgreSQL in production
DATABASE_URL=postgresql://user:password@host/contri_share

# Run with gunicorn + uvicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
npm run build
# Serve dist/ folder with your web server
```

## Development

### Backend Tests
```bash
cd backend
pytest
```

### Code Quality
```bash
# Backend
black app/
ruff check app/

# Frontend
npm run type-check
```

## License

MIT
