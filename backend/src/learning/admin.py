from django.contrib import admin
from .models import LearningPath, TopicMastery


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'current_lesson', 'created_at']
    search_fields = ['student__username', 'course__title']


@admin.register(TopicMastery)
class TopicMasteryAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'topic', 'mastery_level', 'attempts', 'successes']
    list_filter = ['mastery_level']
    search_fields = ['student__username', 'topic']
