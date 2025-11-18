# API Documentation

## Base URL

```
Development: http://localhost:8000/api
Production: https://api.yourdomain.com/api
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Obtain Token

```http
POST /auth/token/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token

```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Users API

### Register User

```http
POST /auth/users/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "student"
}
```

### Get Current User

```http
GET /auth/users/me/
Authorization: Bearer <token>
```

## Courses API

### List Courses

```http
GET /courses/courses/?category=programming&difficulty=beginner&search=python
```

Response:
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/courses/courses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python for Beginners",
      "slug": "python-for-beginners",
      "short_description": "Learn Python from scratch",
      "instructor_name": "John Doe",
      "category": "programming",
      "difficulty": "beginner",
      "price": "49000.00",
      "average_rating": "4.5",
      "total_enrollments": 1250
    }
  ]
}
```

### Get Course Detail

```http
GET /courses/courses/{id}/
```

### Enroll in Course

```http
POST /courses/courses/{id}/enroll/
Authorization: Bearer <token>
```

### Get My Courses

```http
GET /courses/courses/my_courses/
Authorization: Bearer <token>
```

## AI Tutor API

### Start Conversation

```http
POST /ai/conversations/start_conversation/
Authorization: Bearer <token>
Content-Type: application/json

{
  "course_id": 1,
  "lesson_id": 5
}
```

### Ask Question

```http
POST /ai/conversations/{conversation_id}/ask/
Authorization: Bearer <token>
Content-Type: application/json

{
  "question": "Python에서 리스트와 튜플의 차이점이 뭔가요?"
}
```

Response:
```json
{
  "question": {
    "id": 123,
    "role": "user",
    "content": "Python에서 리스트와 튜플의 차이점이 뭔가요?",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "answer": {
    "id": 124,
    "role": "assistant",
    "content": "리스트와 튜플의 주요 차이점은...",
    "created_at": "2024-01-15T10:30:02Z"
  }
}
```

### Generate Practice Questions

```http
POST /ai/practice-questions/generate/
Authorization: Bearer <token>
Content-Type: application/json

{
  "topic": "Python Lists",
  "difficulty": "medium",
  "count": 5,
  "course_id": 1
}
```

### Submit Answer

```http
POST /ai/student-answers/submit/
Authorization: Bearer <token>
Content-Type: application/json

{
  "question_id": 10,
  "answer": "Your answer here"
}
```

## Learning API

### Get Learning Path

```http
GET /learning/learning-paths/{id}/
Authorization: Bearer <token>
```

### Get Next Recommended Lesson

```http
GET /learning/learning-paths/{id}/next_lesson/
Authorization: Bearer <token>
```

Response:
```json
{
  "lesson": {
    "id": 15,
    "title": "Functions in Python",
    "lesson_type": "video"
  },
  "reason": "progression",
  "topic": "Functions",
  "current_mastery": 0.85
}
```

### Get Topic Mastery

```http
GET /learning/topic-mastery/
Authorization: Bearer <token>
```

## Assessment API

### Get Quiz

```http
GET /assessment/quizzes/{id}/
Authorization: Bearer <token>
```

### Submit Quiz Attempt

```http
POST /assessment/quiz-attempts/
Authorization: Bearer <token>
Content-Type: application/json

{
  "quiz": 1,
  "answers": {
    "1": "answer A",
    "2": "answer C"
  }
}
```

### Submit Assignment

```http
POST /assessment/submissions/
Authorization: Bearer <token>
Content-Type: application/json

{
  "assignment": 1,
  "content": "My submission content",
  "attachments": ["url1", "url2"]
}
```

## Payments API

### Create Payment

```http
POST /payments/payments/
Authorization: Bearer <token>
Content-Type: application/json

{
  "course": 1,
  "amount": "49000.00",
  "payment_method": "stripe"
}
```

### Get Payment History

```http
GET /payments/payments/
Authorization: Bearer <token>
```

### Get Subscription Status

```http
GET /payments/subscriptions/
Authorization: Bearer <token>
```

## Certificates API

### Get My Certificates

```http
GET /certificates/certificates/
Authorization: Bearer <token>
```

Response:
```json
[
  {
    "id": 1,
    "student_name": "John Doe",
    "course_title": "Python for Beginners",
    "certificate_id": "550e8400-e29b-41d4-a716-446655440000",
    "pdf_url": "https://cdn.example.com/certificates/...",
    "issued_at": "2024-01-15T10:00:00Z"
  }
]
```

## Error Responses

All API endpoints return standardized error responses:

```json
{
  "error": "Error message",
  "detail": "Detailed error information",
  "code": "ERROR_CODE"
}
```

### HTTP Status Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

- Free tier: 100 requests/hour
- Pro tier: 1000 requests/hour
- Team tier: 10000 requests/hour

## Pagination

All list endpoints support pagination:

```
GET /api/courses/courses/?page=2&page_size=20
```

## Filtering & Sorting

Most list endpoints support filtering and sorting:

```
GET /api/courses/courses/?category=programming&sort_by=-created_at
```

## Interactive API Documentation

Visit these URLs for interactive API documentation:

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
