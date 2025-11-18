"""
Serializers for course models
"""
from rest_framework import serializers
from .models import Course, Module, Lesson, Enrollment, LessonProgress, Review


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson"""

    class Meta:
        model = Lesson
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for Module"""

    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = '__all__'

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for Course list view"""

    instructor_name = serializers.CharField(
        source='instructor.get_full_name',
        read_only=True
    )
    module_count = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description',
            'instructor', 'instructor_name', 'thumbnail',
            'category', 'subcategory', 'tags', 'difficulty',
            'price_type', 'price', 'discount_price',
            'total_enrollments', 'average_rating', 'rating_count',
            'total_duration_minutes', 'module_count', 'lesson_count',
            'is_published', 'created_at'
        ]

    def get_module_count(self, obj):
        return obj.modules.count()

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(module__course=obj).count()


class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer for Course detail view"""

    instructor_name = serializers.CharField(
        source='instructor.get_full_name',
        read_only=True
    )
    modules = ModuleSerializer(many=True, read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(
                student=request.user,
                course=obj
            ).exists()
        return False


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment"""

    course_title = serializers.CharField(source='course.title', read_only=True)
    course_thumbnail = serializers.ImageField(source='course.thumbnail', read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['student', 'progress_percentage', 'is_completed']


class LessonProgressSerializer(serializers.ModelSerializer):
    """Serializer for LessonProgress"""

    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonProgress
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review"""

    student_name = serializers.CharField(
        source='student.get_full_name',
        read_only=True
    )
    student_avatar = serializers.ImageField(
        source='student.avatar',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['student', 'helpful_count']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
