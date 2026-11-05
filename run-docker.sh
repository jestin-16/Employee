#!/usr/bin/env bash
set -e

echo "==============================================================================="
echo "  Employee Management Dashboard - Launching Docker Stack"
echo "==============================================================================="

echo "1. Building images and starting containers via Docker Compose..."
docker compose up -d --build

echo ""
echo "2. Checking container status..."
docker compose ps

echo ""
echo "==============================================================================="
echo "  Employee Management Dashboard is live!"
echo "  - Open in Browser:   http://localhost:8088"
echo "  - Direct Web Port:   http://localhost:8000"
echo "  - Health Check:      http://localhost:8088/api/health/"
echo ""
echo "  Login Credentials:"
echo "    Admin: admin / admin123"
echo "    HR:    hrmanager / Password@123"
echo "==============================================================================="
