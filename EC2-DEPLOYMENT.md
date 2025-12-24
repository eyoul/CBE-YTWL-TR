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

### 2. Connect to EC2
```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```

### 3. Initial Setup
```bash
# Download and run setup script
curl https://raw.githubusercontent.com/your-repo/deploy-ec2.sh | bash

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
git clone https://github.com/yourusername/CBE-YTWL-TR.git
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

## Security Notes
- Change default SECRET_KEY
- Use HTTPS in production
- Configure firewall rules
- Set up backups
