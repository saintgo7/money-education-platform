# Deployment Guide

This guide covers deploying the Money Education Platform to production.

## Prerequisites

- Docker and Docker Compose installed
- Domain name configured
- SSL certificate (Let's Encrypt recommended)
- PostgreSQL database
- Redis instance
- S3 or similar object storage for media files

## Quick Deploy with Docker

### 1. Clone the Repository

```bash
git clone <repository-url>
cd money-education-platform
```

### 2. Configure Environment Variables

**Backend (.env)**
```bash
cd backend
cp .env.example .env
# Edit .env with your production values
```

**Frontend (.env.local)**
```bash
cd frontend
cp .env.example .env.local
# Edit .env.local with your production values
```

### 3. Build and Start Services

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### 4. Initialize Database

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Load initial data (optional)
docker-compose exec backend python manage.py loaddata initial_data.json
```

### 5. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin Panel: http://localhost:8000/admin

## Production Deployment (AWS)

### Architecture

```
┌─────────────┐
│   Route 53  │  DNS
└──────┬──────┘
       │
┌──────▼──────┐
│     ALB     │  Load Balancer
└──────┬──────┘
       │
┌──────▼──────┐
│     ECS     │  Container Service
│  (Fargate)  │
└──────┬──────┘
       │
┌──────▼──────┐
│     RDS     │  PostgreSQL
└─────────────┘
       │
┌──────▼──────┐
│ ElastiCache │  Redis
└─────────────┘
       │
┌──────▼──────┐
│      S3     │  Media Storage
└─────────────┘
```

### Step-by-Step AWS Deployment

#### 1. Create RDS PostgreSQL Instance

```bash
aws rds create-db-instance \
    --db-instance-identifier education-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password <password> \
    --allocated-storage 20
```

#### 2. Create ElastiCache Redis

```bash
aws elasticache create-cache-cluster \
    --cache-cluster-id education-redis \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1
```

#### 3. Create S3 Bucket

```bash
aws s3 mb s3://education-platform-media
aws s3 mb s3://education-platform-static
```

#### 4. Push Docker Images to ECR

```bash
# Create ECR repositories
aws ecr create-repository --repository-name education-backend
aws ecr create-repository --repository-name education-frontend

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
docker build -t education-backend ./backend
docker tag education-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/education-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/education-backend:latest

# Build and push frontend
docker build -t education-frontend ./frontend
docker tag education-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/education-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/education-frontend:latest
```

#### 5. Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name education-cluster
```

#### 6. Create Task Definitions

See `aws/ecs-task-definition.json` for complete task definition.

#### 7. Create ECS Services

```bash
aws ecs create-service \
    --cluster education-cluster \
    --service-name education-backend \
    --task-definition education-backend \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

## SSL Certificate Setup

### Using Let's Encrypt

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Get certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
certbot renew --dry-run
```

## Monitoring Setup

### Prometheus & Grafana

```yaml
# Add to docker-compose.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3001:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Sentry for Error Tracking

```python
# In settings.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=0.1,
)
```

## Backup Strategy

### Database Backup

```bash
# Automated daily backup
0 2 * * * docker-compose exec -T postgres pg_dump -U education_user education_db | gzip > /backups/db_$(date +\%Y\%m\%d).sql.gz
```

### Media Files Backup

```bash
# S3 sync
aws s3 sync /path/to/media s3://education-platform-media-backup/
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend workers
docker-compose up -d --scale backend=3 --scale celery_worker=5
```

### Auto-scaling with AWS

Configure ECS auto-scaling policies based on:
- CPU utilization > 70%
- Memory utilization > 80%
- Request count

## Health Checks

```bash
# Backend health
curl http://localhost:8000/api/health/

# Frontend health
curl http://localhost:3000/

# Database connection
docker-compose exec backend python manage.py check --database default
```

## Troubleshooting

### Container not starting

```bash
docker-compose logs backend
docker-compose logs frontend
```

### Database connection issues

```bash
docker-compose exec backend python manage.py dbshell
```

### Redis connection issues

```bash
docker-compose exec redis redis-cli ping
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Set DEBUG=False in production
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS only
- [ ] Set up CORS properly
- [ ] Configure firewall rules
- [ ] Enable database encryption
- [ ] Set up regular backups
- [ ] Configure rate limiting
- [ ] Enable security headers

## Performance Optimization

### Backend

- Enable database query caching
- Use Redis for session storage
- Configure Celery for async tasks
- Optimize database indexes

### Frontend

- Enable Next.js static optimization
- Use CDN for static assets
- Implement code splitting
- Enable image optimization

## Support

For deployment issues, contact the development team or check the documentation at `/docs/`.
