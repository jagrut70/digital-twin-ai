# 🚀 Digital Twin System - Production Deployment Guide

## 📋 Prerequisites

- Python 3.11+
- Virtual environment
- Docker (optional, for containerized deployment)
- Git

## 🏗️ Deployment Options

### Option 1: Direct Python Deployment (Recommended for Development/Testing)

#### 1. Setup Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd Digi-twin

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Production Settings
```bash
# Copy production config
cp config.production.env .env

# Edit .env file with your production settings
nano .env
```

#### 3. Start Production Server
```bash
# Make startup script executable
chmod +x start_production.sh

# Start the application
./start_production.sh
```

### Option 2: Docker Deployment (Recommended for Production)

#### 1. Build and Run with Docker Compose
```bash
# Build and start services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f digital-twin
```

#### 2. Manual Docker Build
```bash
# Build image
docker build -t digital-twin:latest .

# Run container
docker run -d \
  --name digital-twin-app \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/models:/app/models \
  digital-twin:latest
```

## 🔧 Production Configuration

### Environment Variables
```bash
# Required
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-super-secret-key

# Optional
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./digital_twin_production.db
MODEL_DEVICE=cpu
```

### Security Considerations
1. **Change Default Secret Key**: Update `SECRET_KEY` in `.env`
2. **Enable HTTPS**: Use reverse proxy (nginx) with SSL certificates
3. **Firewall Rules**: Restrict access to necessary ports only
4. **Database Security**: Use strong database passwords if switching from SQLite

## 📊 Monitoring and Health Checks

### Health Endpoint
```bash
# Check application health
curl http://localhost:8000/health

# Expected response: {"status": "healthy", "timestamp": "..."}
```

### Log Monitoring
```bash
# View application logs
tail -f logs/production.log

# Docker logs
docker-compose logs -f digital-twin
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill process or change port in .env
```

#### 2. Permission Issues
```bash
# Fix directory permissions
sudo chown -R $USER:$USER data/ logs/ models/
chmod -R 755 data/ logs/ models/
```

#### 3. Memory Issues
```bash
# Check memory usage
docker stats digital-twin-app

# Increase memory limits in docker-compose.yml
```

### Performance Optimization

#### 1. Database Optimization
```bash
# Enable database logging for debugging
DATABASE_ECHO=true

# Use connection pooling
DATABASE_POOL_SIZE=20
```

#### 2. AI Model Optimization
```bash
# Use GPU if available
USE_GPU=true
MODEL_DEVICE=cuda

# Enable model caching
MODEL_CACHE_ENABLED=true
```

## 🔄 Updates and Maintenance

### Application Updates
```bash
# Pull latest code
git pull origin main

# Restart application
docker-compose restart digital-twin

# Or for direct deployment
pkill -f "python main.py"
./start_production.sh
```

### Database Migrations
```bash
# Run migrations
alembic upgrade head

# Check migration status
alembic current
```

## 📈 Scaling Considerations

### Horizontal Scaling
1. **Load Balancer**: Use nginx or HAProxy
2. **Multiple Instances**: Run multiple containers
3. **Database**: Consider PostgreSQL for production

### Vertical Scaling
1. **Resource Limits**: Adjust Docker memory/CPU limits
2. **Worker Processes**: Increase uvicorn workers
3. **Caching**: Add Redis for session/data caching

## 🛡️ Backup and Recovery

### Data Backup
```bash
# Backup database
cp digital_twin_production.db backup_$(date +%Y%m%d_%H%M%S).db

# Backup synthetic data
tar -czf data_backup_$(date +%Y%m%d_%H%M%S).tar.gz data/
```

### Recovery
```bash
# Restore database
cp backup_*.db digital_twin_production.db

# Restore data
tar -xzf data_backup_*.tar.gz
```

## 📞 Support

For deployment issues:
1. Check logs: `tail -f logs/production.log`
2. Verify configuration: `.env` file settings
3. Test endpoints: `curl http://localhost:8000/health`
4. Check system resources: `docker stats` or `htop`

## ✅ Deployment Checklist

- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Logs directory created
- [ ] Health endpoint responding
- [ ] UI accessible
- [ ] Security settings applied
- [ ] Monitoring configured
- [ ] Backup strategy in place

---

**🎉 Your Digital Twin System is now production-ready!**
