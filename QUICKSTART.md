# Quick Start Guide

Get contri_share running in minutes.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Git

## Local Development (Separate Terminals)

### Terminal 1: Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Create environment file
cp .env.example .env

# Run development server
python main.py
```

Visit: `http://localhost:8000`  
API Docs: `http://localhost:8000/api/v1/docs`

### Terminal 2: Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Run development server
npm run dev
```

Visit: `http://localhost:5173`

## Docker Compose (Single Command)

```bash
# Start all services (backend, frontend, PostgreSQL)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- API Docs: `http://localhost:8000/api/v1/docs`

## First API Calls

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Create User
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "john_doe",
    "full_name": "John Doe",
    "password": "secure_password_123"
  }'
```

### Create Group
```bash
curl -X POST http://localhost:8000/api/v1/groups \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weekend Trip",
    "description": "Expenses for weekend trip",
    "currency": "USD"
  }'
```

### Create Expense
```bash
curl -X POST http://localhost:8000/api/v1/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "group_id": 1,
    "paid_by_id": 1,
    "description": "Dinner",
    "amount": 45.50,
    "category": "Food"
  }'
```

## Project Structure

```
contri_share/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── core/        # Config, database, security
│   │   ├── models/      # Data models
│   │   ├── schemas/     # Validation schemas
│   │   ├── services/    # Business logic
│   │   └── api/         # Route handlers
│   ├── main.py          # Application entry point
│   └── pyproject.toml   # Python dependencies
│
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── features/    # Feature modules
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # API client
│   │   ├── App.jsx      # Root component
│   │   └── App.css      # Global styles
│   ├── public/          # Static assets
│   ├── vite.config.js   # Vite configuration
│   └── package.json     # Node dependencies
│
├── docker-compose.yml   # Multi-service orchestration
├── README.md            # Project documentation
├── CONTRIBUTING.md      # Contribution guidelines
├── ARCHITECTURE.md      # Architecture guide
└── context.md           # Project context
```

## Available Scripts

### Backend

```bash
# Development
python main.py
python -m uvicorn main:app --reload

# Testing
pytest
pytest --cov=app

# Code quality
black app/
ruff check app/
mypy app/
```

### Frontend

```bash
# Development
npm run dev

# Production build
npm run build
npm run preview

# Code quality
npm run type-check
```

## Environment Variables

### Backend `.env`
```
DATABASE_URL=sqlite:///./contri_share.db
DEBUG=True
BACKEND_CORS_ORIGINS=http://localhost:5173
SECRET_KEY=dev-secret-key
```

### Frontend `.env`
```
VITE_API_BASE_URL=http://localhost:8000
```

## Database

### SQLite (Development)
- Automatically created at `backend/contri_share.db`
- No setup needed

### PostgreSQL (Production)
```bash
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost/contri_share

# Create database
createdb contri_share

# With Docker Compose, PostgreSQL is automatically set up
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in main.py (backend)
uvicorn.run(..., port=8001)

# Change port in vite.config.js (frontend)
server: { port: 5174 }
```

### Module Not Found
```bash
# Backend: reinstall dependencies
pip install -e .

# Frontend: reinstall dependencies
npm install
```

### CORS Error
- Ensure `BACKEND_CORS_ORIGINS` includes your frontend URL
- Check that both services are running

### Database Connection Error
- Check `DATABASE_URL` in `.env`
- Ensure database service is running (PostgreSQL with Docker)
- Check database credentials

## Next Steps

1. **Explore the API:** Visit `http://localhost:8000/api/v1/docs`
2. **Create sample data:** Use the API endpoints or cURL commands
3. **Build features:** Check `ARCHITECTURE.md` for patterns
4. **Write tests:** See `CONTRIBUTING.md` for testing guidelines
5. **Deploy:** Follow `DEPLOYMENT.md` for production setup

## Support

- Check `README.md` for detailed documentation
- Review `ARCHITECTURE.md` for design patterns
- See `CONTRIBUTING.md` for coding standards
- Read `context.md` for project overview

## Quick Reference

| Component | URL | Default Port |
|-----------|-----|--------------|
| Backend API | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/api/v1/docs | 8000 |
| Frontend | http://localhost:5173 | 5173 |
| PostgreSQL | localhost | 5432 |

Happy coding! 🚀
