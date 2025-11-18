"""
Tests for users app
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration"""

    def test_register_student(self):
        """Test student registration"""
        client = APIClient()

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'student'
        }

        response = client.post('/api/auth/users/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        user = User.objects.get(username='testuser')
        assert user.email == 'test@example.com'
        assert user.user_type == 'student'
        assert user.check_password('testpass123')

    def test_register_instructor(self):
        """Test instructor registration"""
        client = APIClient()

        data = {
            'username': 'instructor',
            'email': 'instructor@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'Instructor',
            'user_type': 'instructor'
        }

        response = client.post('/api/auth/users/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        user = User.objects.get(username='instructor')
        assert user.is_instructor


@pytest.mark.django_db
class TestUserAuthentication:
    """Test user authentication"""

    def test_login(self):
        """Test user login"""
        # Create user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        client = APIClient()
        response = client.post('/api/auth/token/', {
            'username': 'test@example.com',
            'password': 'testpass123'
        })

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        client = APIClient()
        response = client.post('/api/auth/token/', {
            'username': 'wrong@example.com',
            'password': 'wrongpass'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
