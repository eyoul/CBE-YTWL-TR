#!/bin/bash

# EC2 Deployment Script for YTWL GPS Tracker
echo "Starting EC2 deployment..."

# Stop existing services
docker-compose down

# Pull latest code
git pull origin main

# Build new containers
docker-compose build

# Start services
docker-compose up -d

# Check status
sleep 10
docker-compose ps

echo "Deployment complete!"
