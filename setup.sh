#!/bin/bash

echo "🚀 Money Education Platform - Setup Script"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker가 설치되어 있지 않습니다."
    echo "   Docker를 먼저 설치해주세요: https://www.docker.com/get-started"
    exit 1
fi

echo "✅ Docker found"

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose가 설치되어 있지 않습니다."
    echo "   Docker Compose를 먼저 설치해주세요"
    exit 1
fi

echo "✅ Docker Compose found"
echo ""

# Setup environment files
echo "📝 Setting up environment files..."

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env"
else
    echo "⚠️  backend/.env already exists, skipping..."
fi

if [ ! -f frontend/.env.local ]; then
    cp frontend/.env.example frontend/.env.local
    echo "✅ Created frontend/.env.local"
else
    echo "⚠️  frontend/.env.local already exists, skipping..."
fi

echo ""
echo "⚙️  Please edit the following files and add your API keys:"
echo "   - backend/.env (ANTHROPIC_API_KEY, etc.)"
echo "   - frontend/.env.local"
echo ""
read -p "Press Enter when you're ready to continue..."

# Build and start Docker containers
echo ""
echo "🐳 Building Docker containers..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Run migrations
echo ""
echo "📦 Running database migrations..."
docker-compose exec backend python manage.py migrate

# Create sample data
echo ""
read -p "Would you like to create sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose exec backend python manage.py create_sample_data
    echo "✅ Sample data created"
fi

# Create superuser
echo ""
read -p "Would you like to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose exec backend python manage.py createsuperuser
fi

echo ""
echo "=========================================="
echo "🎉 Setup complete!"
echo "=========================================="
echo ""
echo "Your services are running at:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/api/docs/"
echo "  Admin:     http://localhost:8000/admin/"
echo ""
echo "Sample credentials (if you created sample data):"
echo "  Student:    student@example.com / student123"
echo "  Instructor: instructor@example.com / instructor123"
echo "  Admin:      admin@example.com / admin123"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop:      docker-compose down"
echo ""
