# contri_share Frontend

React 18 + Vite + PWA application for the contri_share expense sharing platform.

## Architecture

### Feature-Sliced Design
- **features/**: Self-contained feature modules
  - dashboard/: Main overview and statistics
  - groups/: Group management and listing
  - expenses/: Expense tracking and management
- **components/**: Reusable UI components (Layout, Navbar)
- **hooks/**: Custom React hooks (useApi)
- **services/**: API client integration with axios
- **styles/**: Global CSS with CSS variables

### Key Features
- React 18 functional components with hooks
- Vite fast build tooling with HMR
- PWA support (offline capability, install prompts)
- Responsive design with CSS Grid/Flexbox
- Custom `useApi` hook for data fetching
- Axios interceptors for authentication tokens
- Environment-based API configuration

## Setup

```bash
npm install
cp .env.example .env
npm run dev
```

App runs on `http://localhost:5173`

## Build

```bash
npm run build
npm run preview
```

Production build output in `dist/`

## PWA Features

- Service worker registration for offline support
- Web app manifest for installability
- Workbox caching strategies for API responses
- Install prompts on supported browsers

## Environment Variables

```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=contri_share
VITE_APP_VERSION=0.1.0
```

## Performance

- Code splitting per feature
- Lazy loading of routes
- Caching of API responses
- Optimized CSS with variables
