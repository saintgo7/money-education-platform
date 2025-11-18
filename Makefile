.PHONY: help setup dev test clean docker-up docker-down migrate

help:
	@echo "Money Education Platform - Commands"
	@echo ""
	@echo "  setup             - Initial setup (create env files)"
	@echo "  dev               - Start development servers"
	@echo "  test              - Run tests"
	@echo "  clean             - Clean up cache files"
	@echo "  docker-up         - Start Docker containers"
	@echo "  docker-down       - Stop Docker containers"
	@echo "  migrate           - Run database migrations"
	@echo "  sample-data       - Create sample data"
	@echo "  english-courses   - Create English education courses"
	@echo "  detailed-modules  - Add detailed modules to all courses"
	@echo "  create-50-more    - Create 50 additional diverse courses"
	@echo "  add-50-modules    - Add 50 modules to each course"
	@echo ""

setup:
	@echo "Setting up environment files..."
	@cp -n backend/.env.example backend/.env || true
	@cp -n frontend/.env.example frontend/.env.local || true
	@echo "✅ Environment files created"
	@echo "Please edit backend/.env and frontend/.env.local with your configuration"

dev:
	@echo "Starting development servers..."
	@chmod +x scripts/dev.sh
	@./scripts/dev.sh

test:
	@echo "Running backend tests..."
	@cd backend/src && pytest
	@echo "Running frontend tests..."
	@cd frontend && npm run test

clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete"

docker-up:
	@echo "Starting Docker containers..."
	@docker-compose up -d
	@echo "✅ Containers started"

docker-down:
	@echo "Stopping Docker containers..."
	@docker-compose down
	@echo "✅ Containers stopped"

migrate:
	@echo "Running migrations..."
	@docker-compose exec backend python manage.py migrate
	@echo "✅ Migrations complete"

sample-data:
	@echo "Creating sample data..."
	@docker-compose exec backend python manage.py create_sample_data
	@echo "✅ Sample data created"

english-courses:
	@echo "Creating English education courses..."
	@docker-compose exec backend python manage.py create_english_courses
	@echo "✅ English courses created"

detailed-modules:
	@echo "Adding detailed modules to all courses..."
	@docker-compose exec backend python manage.py add_detailed_modules
	@echo "✅ Detailed modules added"

create-50-more:
	@echo "Creating 50 additional courses..."
	@docker-compose exec backend python manage.py create_50_more_courses
	@echo "✅ 50 more courses created"

add-50-modules:
	@echo "Adding 50 modules to each course..."
	@docker-compose exec backend python manage.py add_50_modules_per_course
	@echo "✅ 50 modules added to each course"
