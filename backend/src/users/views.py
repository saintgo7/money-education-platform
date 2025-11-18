"""
Views for user management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .models import StudentProfile, InstructorProfile
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    StudentProfileSerializer,
    InstructorProfileSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User operations"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class StudentProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for StudentProfile"""

    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter to only show current user's profile"""
        if self.request.user.is_student:
            return StudentProfile.objects.filter(user=self.request.user)
        return StudentProfile.objects.none()

    @action(detail=False, methods=['get'])
    def my_stats(self, request):
        """Get current student's learning statistics"""
        try:
            profile = request.user.student_profile
            return Response({
                'total_courses_enrolled': profile.total_courses_enrolled,
                'total_courses_completed': profile.total_courses_completed,
                'total_learning_hours': profile.total_learning_hours,
                'average_quiz_score': profile.average_quiz_score,
                'average_assignment_score': profile.average_assignment_score,
                'ai_questions_asked': profile.ai_questions_asked,
                'can_use_ai_tutor': profile.can_use_ai_tutor(),
            })
        except StudentProfile.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class InstructorProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for InstructorProfile"""

    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter based on user type"""
        if self.request.user.is_instructor:
            return InstructorProfile.objects.filter(user=self.request.user)
        # Allow viewing all instructor profiles for students
        return InstructorProfile.objects.all()

    @action(detail=False, methods=['get'])
    def my_earnings(self, request):
        """Get current instructor's earnings statistics"""
        if not request.user.is_instructor:
            return Response(
                {'error': 'Only instructors can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            profile = request.user.instructor_profile
            return Response({
                'total_revenue': profile.total_revenue,
                'commission_rate': profile.commission_rate,
                'net_earnings': float(profile.total_revenue) * (100 - float(profile.commission_rate)) / 100,
                'total_courses': profile.total_courses,
                'total_students': profile.total_students,
                'average_rating': profile.average_rating,
            })
        except InstructorProfile.DoesNotExist:
            return Response(
                {'error': 'Instructor profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
