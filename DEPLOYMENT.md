# Production Deployment

## Backend Build

```bash
docker build -t contri-share-api:latest ./backend
docker run -d \
  --name contri-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db-host/contri_share \
  -e SECRET_KEY=$SECRET_KEY \
  contri-share-api:latest
```

## Frontend Build

```bash
docker build -t contri-share-web:latest ./frontend
docker run -d \
  --name contri-web \
  -p 80:80 \
  -e VITE_API_BASE_URL=https://api.example.com \
  contri-share-web:latest
```

## Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Kubernetes Deployment

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: contri-config
data:
  DATABASE_URL: postgresql://user:pass@postgres:5432/contri_share
  BACKEND_CORS_ORIGINS: https://app.example.com

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: contri-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: contri-api
  template:
    metadata:
      labels:
        app: contri-api
    spec:
      containers:
      - name: api
        image: contri-share-api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: contri-config
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Environment Variables

### Backend Production
```
DATABASE_URL=postgresql://user:securepass@prod-db.example.com/contri_share
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
BACKEND_CORS_ORIGINS=https://app.example.com
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Production
```
VITE_API_BASE_URL=https://api.example.com
VITE_APP_NAME=contri_share
VITE_APP_VERSION=1.0.0
```

## Nginx Configuration

```nginx
upstream api {
  server backend:8000;
}

server {
  listen 80;
  server_name api.example.com;
  
  location / {
    proxy_pass http://api;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}

server {
  listen 80;
  server_name app.example.com;
  
  root /usr/share/nginx/html;
  index index.html;
  
  location / {
    try_files $uri $uri/ /index.html;
  }
  
  location /api/ {
    proxy_pass http://api;
  }
}
```

## SSL/TLS (Let's Encrypt)

```bash
# Using Certbot with Nginx
docker run -it --rm --name certbot \
  -v /etc/letsencrypt:/etc/letsencrypt \
  certbot/certbot certonly \
  --standalone \
  -d api.example.com \
  -d app.example.com
```

## Database Backup

```bash
# PostgreSQL backup
pg_dump -h prod-db.example.com -U user contri_share > backup.sql

# Restore
psql -h new-db.example.com -U user contri_share < backup.sql
```

## Monitoring

- Backend: Prometheus + Grafana for metrics
- Frontend: Sentry for error tracking
- Database: CloudWatch or DataDog monitoring
- Logs: ELK stack or CloudWatch Logs

## Scaling Considerations

1. **Horizontal Scaling:** Run multiple API replicas behind load balancer
2. **Caching:** Redis for session management and API response caching
3. **Database:** Connection pooling with PgBouncer
4. **CDN:** CloudFront or Cloudflare for frontend assets
5. **Rate Limiting:** Implement per IP/user rate limiting
