"""
Tests for courses app
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Module, Lesson, Enrollment

User = get_user_model()


@pytest.mark.django_db
class TestCourseCreation:
    """Test course creation"""

    def test_create_course(self):
        """Test creating a course"""
        instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='pass123',
            user_type='instructor'
        )

        course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            description='Test description',
            short_description='Short desc',
            instructor=instructor,
            category='programming',
            difficulty='beginner',
            price_type='free'
        )

        assert course.title == 'Test Course'
        assert course.instructor == instructor
        assert course.is_published == False


@pytest.mark.django_db
class TestCourseEnrollment:
    """Test course enrollment"""

    def test_enroll_in_course(self):
        """Test student enrolling in a course"""
        # Create instructor and course
        instructor = User.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='pass123',
            user_type='instructor'
        )

        course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            description='Test',
            short_description='Test',
            instructor=instructor,
            category='programming',
            difficulty='beginner',
            price_type='free',
            is_published=True
        )

        # Create student
        student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='pass123',
            user_type='student'
        )

        # Enroll
        client = APIClient()
        client.force_authenticate(user=student)

        response = client.post(f'/api/courses/courses/{course.id}/enroll/')
        assert response.status_code == status.HTTP_201_CREATED

        enrollment = Enrollment.objects.get(student=student, course=course)
        assert enrollment.progress_percentage == 0.0
