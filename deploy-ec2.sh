#!/bin/bash

# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create app directory
mkdir -p /home/ec2-user/app
cd /home/ec2-user/app

# Clone your repository (replace with your repo URL)
# git clone https://github.com/yourusername/CBE-YTWL-TR.git .

# Build and run containers
docker-compose up -d

# Setup auto-restart on reboot
sudo systemctl enable docker
