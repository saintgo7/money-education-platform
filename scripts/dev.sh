#!/bin/bash

# Development script for local development without Docker

echo "🚀 Starting development servers..."
echo ""

# Start backend
echo "Starting Django backend..."
cd backend/src
python manage.py runserver &
BACKEND_PID=$!

# Start Celery worker
echo "Starting Celery worker..."
celery -A config worker -l info &
CELERY_PID=$!

# Start Redis (assumes Redis is installed)
echo "Checking Redis..."
if ! pgrep -x "redis-server" > /dev/null; then
    echo "Starting Redis..."
    redis-server &
    REDIS_PID=$!
fi

# Start frontend
echo "Starting Next.js frontend..."
cd ../../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "✅ All services started!"
echo "=========================================="
echo ""
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/api/docs/"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "echo 'Stopping services...'; kill $BACKEND_PID $CELERY_PID $FRONTEND_PID $REDIS_PID 2>/dev/null; exit" INT
wait
