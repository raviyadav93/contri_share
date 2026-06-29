# Contributing to contri_share

Thank you for your interest in contributing to contri_share! Here are some guidelines to help you get started.

## Development Environment

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+ (for production builds)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Frontend Setup
```bash
cd frontend
npm install
```

## Code Standards

### Backend
- **Type Hints:** All functions must have explicit type annotations
- **Docstrings:** Use Google-style docstrings
- **Line Length:** Maximum 88 characters (enforced by Black)
- **Imports:** Organized with isort
- **Testing:** Minimum 80% code coverage

```python
async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    """Get user by their ID.
    
    Args:
        db: Database session
        user_id: User ID to fetch
        
    Returns:
        User instance
        
    Raises:
        ResourceNotFoundError: If user doesn't exist
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise ResourceNotFoundError("User", user_id)
    return user
```

### Frontend
- **Components:** Functional components with hooks only
- **Naming:** PascalCase for components, camelCase for functions/variables
- **Props:** Destructured and typed with JSDoc
- **Files:** One component per file (optional for small utils)

```jsx
/**
 * UserCard component displaying user information
 * @param {Object} props - Component props
 * @param {number} props.userId - User ID to display
 * @param {string} props.className - Optional CSS class
 * @returns {JSX.Element} Rendered component
 */
function UserCard({ userId, className = '' }) {
  const { get } = useApi()
  const [user, setUser] = useState(null)
  
  // Implementation
  return <div className={className}>{/* ... */}</div>
}

export default UserCard
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
npm run type-check
```

## Commit Guidelines

Use conventional commits:
```
feat: Add user authentication endpoint
fix: Resolve CORS headers in health check
docs: Update API documentation
test: Add user service tests
refactor: Simplify database session management
chore: Update dependencies
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/feature-name`
3. Make your changes with meaningful commits
4. Add tests for new functionality
5. Ensure all tests pass: `pytest` / `npm test`
6. Update documentation as needed
7. Submit PR with clear description

## Issues & Bug Reports

When reporting issues:
1. Provide clear reproduction steps
2. Include relevant error messages/logs
3. Specify OS and version information
4. Include screenshots for UI issues

## Architecture Decisions

Before making significant changes:
1. Check existing issues/PRs for context
2. Open an issue to discuss approach
3. Follow established patterns (services, hooks, etc.)
4. Update documentation and context.md

## Performance

- Profile database queries with `EXPLAIN ANALYZE`
- Use React DevTools Profiler for frontend performance
- Monitor API response times
- Test with realistic data volumes

## Security

- Never commit secrets (use `.env.example`)
- Validate all user inputs
- Use parameterized queries (ORM handles this)
- Follow OWASP guidelines
- Keep dependencies updated

## Documentation

- Update README for new features
- Add docstrings to public functions
- Update context.md for architecture changes
- Include examples for complex features

## Questions?

Open an issue or start a discussion. We're happy to help!

## License

By contributing, you agree your code will be licensed under the MIT License.
