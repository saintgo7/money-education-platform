"""
Views for course management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Course, Module, Lesson, Enrollment, LessonProgress, Review
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    ModuleSerializer,
    LessonSerializer,
    EnrollmentSerializer,
    LessonProgressSerializer,
    ReviewSerializer
)


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course CRUD operations"""

    queryset = Course.objects.filter(is_published=True)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # Sort
        sort_by = self.request.query_params.get('sort_by', '-created_at')
        queryset = queryset.order_by(sort_by)

        return queryset

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll student in a course"""
        course = self.get_object()
        student = request.user

        if not student.is_student:
            return Response(
                {'error': 'Only students can enroll in courses'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response(
                {'error': 'Already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check subscription/payment (simplified)
        if course.price_type == 'paid' and not student.has_active_subscription:
            return Response(
                {'error': 'Payment required'},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )

        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student,
            course=course
        )

        # Update course stats
        course.total_enrollments += 1
        course.save()

        # Update student stats
        if hasattr(student, 'student_profile'):
            profile = student.student_profile
            profile.total_courses_enrolled += 1
            profile.save()

        return Response(
            EnrollmentSerializer(enrollment).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def curriculum(self, request, pk=None):
        """Get course curriculum with modules and lessons"""
        course = self.get_object()
        modules = course.modules.all().prefetch_related('lessons')
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """Get courses the user is teaching (instructor) or enrolled in (student)"""
        user = request.user

        if user.is_instructor:
            courses = Course.objects.filter(instructor=user)
            serializer = CourseListSerializer(courses, many=True)
        else:
            enrollments = Enrollment.objects.filter(student=user)
            serializer = EnrollmentSerializer(enrollments, many=True)

        return Response(serializer.data)


class ModuleViewSet(viewsets.ModelViewSet):
    """ViewSet for Module CRUD operations"""

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Only course instructor can create modules"""
        course = serializer.validated_data['course']
        if course.instructor != self.request.user:
            return Response(
                {'error': 'Only course instructor can create modules'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for Lesson CRUD operations"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        """Mark lesson as completed"""
        lesson = self.get_object()
        student = request.user

        # Get enrollment
        try:
            enrollment = Enrollment.objects.get(
                student=student,
                course=lesson.module.course
            )
        except Enrollment.DoesNotExist:
            return Response(
                {'error': 'Not enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update or create lesson progress
        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson
        )

        progress.is_completed = True
        progress.completion_percentage = 100.0
        progress.completed_at = timezone.now()
        progress.save()

        # Update enrollment progress
        total_lessons = Lesson.objects.filter(
            module__course=enrollment.course
        ).count()
        completed_lessons = LessonProgress.objects.filter(
            enrollment=enrollment,
            is_completed=True
        ).count()

        enrollment.progress_percentage = (completed_lessons / total_lessons) * 100
        enrollment.save()

        return Response({'status': 'Lesson marked as complete'})


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing enrollments"""

    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Students see their own enrollments"""
        return Enrollment.objects.filter(student=self.request.user)

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get detailed progress for an enrollment"""
        enrollment = self.get_object()
        progress_records = LessonProgress.objects.filter(enrollment=enrollment)
        serializer = LessonProgressSerializer(progress_records, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for course reviews"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter reviews by course if specified"""
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def perform_create(self, serializer):
        """Create review and update course rating"""
        review = serializer.save(student=self.request.user)

        # Update course rating
        course = review.course
        reviews = Review.objects.filter(course=course)
        course.rating_count = reviews.count()
        course.average_rating = sum(r.rating for r in reviews) / course.rating_count
        course.save()
