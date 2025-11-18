"""
Admin configuration for users app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, InstructorProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'subscription_tier', 'is_active']
    list_filter = ['user_type', 'subscription_tier', 'is_active', 'verified_instructor']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {
            'fields': ('user_type', 'avatar', 'bio', 'phone')
        }),
        ('Learning', {
            'fields': ('learning_style', 'learning_level', 'interests')
        }),
        ('Instructor', {
            'fields': ('expertise', 'verified_instructor', 'instructor_rating')
        }),
        ('Subscription', {
            'fields': ('subscription_tier', 'subscription_expires')
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_courses_enrolled', 'total_courses_completed', 'average_quiz_score']
    search_fields = ['user__username', 'user__email']
    list_filter = ['preferred_language', 'notification_enabled']


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_courses', 'total_students', 'total_revenue', 'average_rating']
    search_fields = ['user__username', 'user__email', 'organization']
    list_filter = ['commission_rate']
