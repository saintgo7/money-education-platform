# Development Guide

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Git

### Local Development Setup

#### 1. Clone Repository

```bash
git clone <repository-url>
cd money-education-platform
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your local settings
# Make sure to set:
# - DATABASE_URL
# - REDIS_URL
# - ANTHROPIC_API_KEY

# Run migrations
cd src
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

The backend will be available at http://localhost:8000

#### 3. Start Celery (in separate terminals)

```bash
# Terminal 1: Celery Worker
cd backend/src
celery -A config worker -l info

# Terminal 2: Celery Beat
cd backend/src
celery -A config beat -l info
```

#### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Edit .env.local
# Set NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

The frontend will be available at http://localhost:3000

## Project Structure

```
money-education-platform/
├── backend/                 # Django backend
│   ├── src/
│   │   ├── config/         # Django settings
│   │   ├── users/          # User management
│   │   ├── courses/        # Course management
│   │   ├── ai/             # AI tutor system
│   │   ├── learning/       # Adaptive learning
│   │   ├── assessment/     # Quizzes & assignments
│   │   ├── payments/       # Payment processing
│   │   └── certificates/   # Certificate generation
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities & API client
│   │   ├── hooks/         # Custom React hooks
│   │   └── types/         # TypeScript types
│   └── package.json
│
├── docker/                # Docker configs
│   └── nginx/
│
└── docs/                  # Documentation
```

## Development Workflow

### Creating a New Feature

1. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes

3. Write tests
```bash
# Backend tests
cd backend/src
pytest

# Frontend tests
cd frontend
npm run test
```

4. Run linters
```bash
# Backend
black .
flake8
isort .

# Frontend
npm run lint
```

5. Commit and push
```bash
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
```

6. Create Pull Request

### Code Style

#### Backend (Python)

- Follow PEP 8
- Use Black for formatting
- Use type hints where possible
- Write docstrings for functions

```python
def calculate_mastery(student_id: int, topic: str) -> float:
    """
    Calculate student's mastery level for a topic.

    Args:
        student_id: ID of the student
        topic: Topic name

    Returns:
        Mastery level between 0.0 and 1.0
    """
    pass
```

#### Frontend (TypeScript)

- Use TypeScript strict mode
- Follow ESLint rules
- Use functional components
- Use custom hooks for logic

```typescript
interface CourseProps {
  course: Course
  onEnroll: () => void
}

export function CourseCard({ course, onEnroll }: CourseProps) {
  // Component code
}
```

## Database Management

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Seeding Data

```bash
python manage.py loaddata fixtures/courses.json
```

### Database Reset

```bash
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

## API Development

### Adding a New Endpoint

1. Define model in `models.py`
2. Create serializer in `serializers.py`
3. Create viewset in `views.py`
4. Register route in `urls.py`

Example:

```python
# models.py
class Resource(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

# serializers.py
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

# views.py
class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

# urls.py
router.register(r'resources', ResourceViewSet)
```

## Frontend Development

### Adding a New Page

```typescript
// src/app/courses/page.tsx
export default function CoursesPage() {
  return (
    <div>
      <h1>Courses</h1>
    </div>
  )
}
```

### Creating a Component

```typescript
// src/components/CourseCard.tsx
import { Course } from '@/types'

interface CourseCardProps {
  course: Course
}

export function CourseCard({ course }: CourseCardProps) {
  return (
    <div className="border rounded-lg p-4">
      <h3>{course.title}</h3>
      <p>{course.short_description}</p>
    </div>
  )
}
```

### Using the API

```typescript
import { coursesApi } from '@/lib/api'

// In a component or hook
const { data: courses, isLoading } = useQuery({
  queryKey: ['courses'],
  queryFn: () => coursesApi.list()
})
```

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_ai.py

# Run specific test
pytest tests/test_ai.py::test_tutor_answer
```

Writing tests:

```python
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username='test',
        email='test@example.com',
        password='testpass123'
    )
    assert user.username == 'test'
    assert user.check_password('testpass123')
```

### Frontend Tests

```bash
# Run tests
npm run test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

## Debugging

### Backend

Use Django Debug Toolbar:

```python
# In settings.py (development only)
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

### Frontend

Use React Developer Tools browser extension

## Common Issues

### Database Connection Error

```bash
# Check PostgreSQL is running
pg_isready

# Check connection settings in .env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping

# Should return PONG
```

### Module Import Error

```bash
# Make sure PYTHONPATH includes src
export PYTHONPATH=/path/to/backend/src:$PYTHONPATH
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

## VS Code Configuration

Recommended `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

## Resources

- Django Documentation: https://docs.djangoproject.com/
- Next.js Documentation: https://nextjs.org/docs
- Anthropic Claude API: https://docs.anthropic.com/
- TailwindCSS: https://tailwindcss.com/docs
