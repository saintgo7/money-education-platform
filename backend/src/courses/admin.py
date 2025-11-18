"""
Admin configuration for courses app
"""
from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, LessonProgress, Review


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'difficulty', 'price_type', 'total_enrollments', 'is_published']
    list_filter = ['category', 'difficulty', 'price_type', 'is_published']
    search_fields = ['title', 'instructor__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'course__title']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'lesson_type', 'order', 'is_preview']
    list_filter = ['lesson_type', 'is_preview', 'is_mandatory']
    search_fields = ['title', 'module__title']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'progress_percentage', 'is_completed', 'enrolled_at']
    list_filter = ['is_completed', 'certificate_issued']
    search_fields = ['student__username', 'course__title']
    date_hierarchy = 'enrolled_at'


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'is_completed', 'completion_percentage']
    list_filter = ['is_completed']
    search_fields = ['enrollment__student__username', 'lesson__title']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['course__title', 'student__username', 'comment']
    date_hierarchy = 'created_at'
