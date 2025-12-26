# YTWL GPS Tracker - EC2 Deployment Guide

## Prerequisites
- AWS account with EC2 access
- Git repository with your code

## EC2 Setup Steps

### 1. Launch EC2 Instance
- Choose Amazon Linux 2 AMI
- Select t2.micro or t3.small (minimum)
- Configure security group:
  - Port 22 (SSH) - Your IP
  - Port 80 (HTTP) - 0.0.0.0/0
  - Port 8000 (App) - 0.0.0.0/0
  - Port 9000 (TCP Listener) - 0.0.0.0/0

### 2. Connect to EC2
```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```
ssh -i ytwlkey.pem ec2-user@98.88.254.163

### 3. Initial Setup
```bash
# Download and run setup script
curl https://raw.githubusercontent.com/eyoul/CBE-YTWL-TR/main/deploy-ec2.sh | bash

# Or manually:
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo usermod -a -G docker ec2-user
```

### 4. Deploy Application
```bash
# Clone your repository
cd /home/ec2-user
git clone https://github.com/eyoul/CBE-YTWL-TR.git
cd CBE-YTWL-TR

# Build and run
docker-compose up -d
```

### 5. Verify Deployment
```bash
# Check containers
docker-compose ps

# Check logs
docker-compose logs web

# Test locally
curl http://localhost:8000
```

### 6. Configure Nginx Reverse Proxy
```bash
# Create nginx config
sudo tee /etc/nginx/conf.d/ytwl.conf << 'EOF'
server {
    listen 80;
    server_name your-ec2-ip;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /socket.io/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
EOF

# Restart nginx
sudo systemctl restart nginx
```

## Updates
```bash
cd /home/ec2-user/CBE-YTWL-TR
git pull
docker-compose build
docker-compose up -d
```

## Access Your App
- HTTP: http://your-ec2-ip
- Direct: http://your-ec2-ip:8000

## Test YTWL Device Connection
```bash
# Test TCP listener
telnet your-ec2-ip 9000

# Expected response from YTWL device
# Device should send GPS data to port 9000
# Map will show real-time location updates
```

## Security Notes
- Change default SECRET_KEY in app.py
- Use HTTPS in production (Let's Encrypt)
- Configure firewall rules properly
- Set up database backups
- Monitor TCP port 9000 for unauthorized access

## Troubleshooting
```bash
# Check if ports are open
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :9000

# Check Docker logs
docker-compose logs web

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

## Current Configuration
- **App Port:** 8000 (Flask + SocketIO)
- **TCP Port:** 9000 (YTWL Device Listener)
- **Database:** SQLite with WAL mode
- **Real-time Updates:** Socket.IO
- **Map:** Leaflet.js with OpenStreetMap
- **IMEI for Testing:** 355442200991235
