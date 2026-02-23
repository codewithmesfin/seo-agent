# Production Deployment Guide

## Prerequisites
- Docker & Docker Compose
- Domain name and SSL certificates (handled by Nginx/Certbot)
- MongoDB Atlas (optional, for managed DB) or self-hosted MongoDB

## Steps to Deploy

### 1. Environment Setup
Clone the repository and create a `.env` file based on `.env-example`.

```bash
cp .env-example .env
# Edit .env with your production credentials
```

### 2. Docker Configuration
Update `docker-compose.yml` for production:
- Set `NODE_ENV=production` for the frontend.
- Disable `RELOAD` for FastAPI.
- Use secure passwords for MongoDB and Redis.

### 3. Build and Launch
```bash
make build
make up
```

### 4. Reverse Proxy (Nginx)
Configure Nginx to route traffic to the frontend (port 3000) and backend (port 8000).

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

### 5. Database Backups
Set up a cron job to run `mongodump` regularly to ensure data safety.

### 6. Monitoring
- Use **Sentry** for error tracking.
- Use **Prometheus/Grafana** for infrastructure monitoring.
- Use **Loguru** file rotation (configured in `backend/app/core/middleware.py`).
