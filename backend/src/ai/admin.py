"""
Admin configuration for AI app
"""
from django.contrib import admin
from .models import Conversation, Message, PracticeQuestion, StudentAnswer


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'course', 'lesson', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'student__username', 'course__title']
    inlines = [MessageInline]
    date_hierarchy = 'created_at'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'content_preview', 'tokens_used', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content', 'conversation__title']

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'


@admin.register(PracticeQuestion)
class PracticeQuestionAdmin(admin.ModelAdmin):
    list_display = ['topic', 'difficulty', 'course', 'times_used', 'success_rate', 'created_at']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['topic', 'question', 'course__title']

    def success_rate(self, obj):
        if obj.times_used == 0:
            return '0%'
        return f"{(obj.times_correct / obj.times_used) * 100:.1f}%"
    success_rate.short_description = 'Success Rate'


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['student', 'question_topic', 'score', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']
    search_fields = ['student__username', 'question__topic', 'answer']
    date_hierarchy = 'answered_at'

    def question_topic(self, obj):
        return obj.question.topic
    question_topic.short_description = 'Topic'
