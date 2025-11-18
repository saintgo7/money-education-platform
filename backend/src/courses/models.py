"""
Course models for the education platform
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Course(models.Model):
    """Main course model"""

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    PRICE_TYPE_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('subscription', 'Subscription Only'),
    ]

    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)

    # Instructor
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses_teaching'
    )

    # Content
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    trailer_video_url = models.URLField(blank=True)

    # Categories & Tags
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list)

    # Difficulty & Prerequisites
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    prerequisites = models.TextField(blank=True)
    learning_objectives = models.JSONField(default=list)

    # Pricing
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Stats
    total_enrollments = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rating_count = models.IntegerField(default=0)
    total_duration_minutes = models.IntegerField(default=0)

    # Status
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Module(models.Model):
    """Course module/section"""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_modules'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    """Individual lesson within a module"""

    LESSON_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text/Article'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('live', 'Live Session'),
    ]

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES)
    order = models.IntegerField(default=0)

    # Content
    content = models.TextField(blank=True)  # For text lessons
    video_url = models.URLField(blank=True)  # Mux video URL
    video_duration = models.IntegerField(default=0)  # in seconds

    # Resources
    attachments = models.JSONField(default=list)  # List of file URLs

    # Settings
    is_preview = models.BooleanField(default=False)  # Can be viewed without enrollment
    is_mandatory = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lessons'
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Enrollment(models.Model):
    """Student course enrollment"""

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    # Progress
    progress_percentage = models.FloatField(default=0.0)
    completed_lessons = models.JSONField(default=list)  # List of lesson IDs
    last_accessed_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='last_accessed_by'
    )

    # Completion
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Certificate
    certificate_issued = models.BooleanField(default=False)

    # Metadata
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'enrollments'
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class LessonProgress(models.Model):
    """Track individual lesson progress"""

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='lesson_progress'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )

    # Progress
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.FloatField(default=0.0)
    time_spent_seconds = models.IntegerField(default=0)

    # Video Progress
    video_progress_seconds = models.IntegerField(default=0)

    # Metadata
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lesson_progress'
        unique_together = ['enrollment', 'lesson']

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.lesson.title}"


class Review(models.Model):
    """Course review"""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.IntegerField()  # 1-5
    comment = models.TextField(blank=True)

    # Helpful votes
    helpful_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        unique_together = ['course', 'student']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.rating}/5)"
