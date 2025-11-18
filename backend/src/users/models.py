"""
User models for the education platform
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model"""

    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]

    LEARNING_STYLE_CHOICES = [
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('kinesthetic', 'Kinesthetic'),
        ('reading', 'Reading/Writing'),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='student'
    )

    # Profile
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Learning Profile (for students)
    learning_style = models.CharField(
        max_length=20,
        choices=LEARNING_STYLE_CHOICES,
        blank=True
    )
    learning_level = models.CharField(max_length=50, blank=True)
    interests = models.JSONField(default=list, blank=True)

    # Instructor Profile
    expertise = models.JSONField(default=list, blank=True)
    verified_instructor = models.BooleanField(default=False)
    instructor_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Subscription
    subscription_tier = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('pro', 'Pro'),
            ('team', 'Team'),
        ],
        default='free'
    )
    subscription_expires = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    @property
    def is_student(self):
        return self.user_type == 'student'

    @property
    def is_instructor(self):
        return self.user_type == 'instructor'

    @property
    def has_active_subscription(self):
        if self.subscription_tier == 'free':
            return True
        if self.subscription_expires:
            from django.utils import timezone
            return self.subscription_expires > timezone.now()
        return False


class StudentProfile(models.Model):
    """Extended student profile with learning analytics"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    # Learning Analytics
    total_courses_enrolled = models.IntegerField(default=0)
    total_courses_completed = models.IntegerField(default=0)
    total_learning_hours = models.FloatField(default=0.0)

    # Performance Metrics
    average_quiz_score = models.FloatField(default=0.0)
    average_assignment_score = models.FloatField(default=0.0)

    # AI Tutor Usage
    ai_questions_asked = models.IntegerField(default=0)
    ai_questions_limit = models.IntegerField(default=10)  # Per month for free tier

    # Weak Areas (stored as JSON)
    weak_topics = models.JSONField(default=list)

    # Preferences
    preferred_language = models.CharField(max_length=10, default='ko')
    notification_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_profiles'

    def __str__(self):
        return f"{self.user.username}'s profile"

    def can_use_ai_tutor(self):
        """Check if student can use AI tutor based on their plan"""
        if self.user.subscription_tier == 'free':
            return self.ai_questions_asked < self.ai_questions_limit
        return True  # Pro and Team tiers have unlimited access


class InstructorProfile(models.Model):
    """Extended instructor profile"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='instructor_profile'
    )

    # Professional Info
    title = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    # Teaching Stats
    total_courses = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Ratings
    rating_count = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    # Commission Rate
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=30.00,
        help_text="Platform commission percentage"
    )

    # Bank Info for Payouts
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    account_holder = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'instructor_profiles'

    def __str__(self):
        return f"{self.user.username}'s instructor profile"
