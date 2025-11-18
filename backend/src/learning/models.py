"""
Models for adaptive learning engine
"""
from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

User = get_user_model()


class LearningPath(models.Model):
    """Personalized learning path for a student"""

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='learning_paths')

    recommended_lessons = models.JSONField(default=list)
    completed_lessons = models.JSONField(default=list)
    current_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)

    estimated_completion_days = models.IntegerField(default=30)
    actual_completion_days = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'learning_paths'
        unique_together = ['student', 'course']


class TopicMastery(models.Model):
    """Track student's mastery of topics"""

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_mastery')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    topic = models.CharField(max_length=200)
    mastery_level = models.FloatField(default=0.0)  # 0.0 to 1.0
    attempts = models.IntegerField(default=0)
    successes = models.IntegerField(default=0)

    last_practiced = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'topic_mastery'
        unique_together = ['student', 'course', 'topic']
