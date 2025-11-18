"""
Serializers for user models
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile, InstructorProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'avatar', 'bio', 'phone',
            'learning_style', 'learning_level', 'interests',
            'expertise', 'verified_instructor', 'instructor_rating',
            'subscription_tier', 'subscription_expires',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'user_type'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create profile based on user type
        if user.user_type == 'student':
            StudentProfile.objects.create(user=user)
        elif user.user_type == 'instructor':
            InstructorProfile.objects.create(user=user)

        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for StudentProfile"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'


class InstructorProfileSerializer(serializers.ModelSerializer):
    """Serializer for InstructorProfile"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = InstructorProfile
        fields = '__all__'
        read_only_fields = [
            'total_courses', 'total_students', 'total_revenue',
            'rating_count', 'average_rating'
        ]
