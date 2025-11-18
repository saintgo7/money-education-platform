"""
Models for AI tutor system
"""
from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

User = get_user_model()


class Conversation(models.Model):
    """AI tutor conversation session"""

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ai_conversations'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='ai_conversations',
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='ai_conversations',
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ai_conversations'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.student.username} - {self.title or 'Conversation'}"


class Message(models.Model):
    """Individual message in a conversation"""

    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()

    # Metadata
    tokens_used = models.IntegerField(default=0)
    model_used = models.CharField(max_length=100, default='claude-sonnet-4')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class PracticeQuestion(models.Model):
    """AI-generated practice questions"""

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='practice_questions'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='practice_questions',
        null=True,
        blank=True
    )

    topic = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)

    question = models.TextField()
    options = models.JSONField(null=True, blank=True)  # For multiple choice
    correct_answer = models.TextField()
    explanation = models.TextField()

    # Usage stats
    times_used = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'practice_questions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.topic} - {self.difficulty}"


class StudentAnswer(models.Model):
    """Student's answer to practice questions"""

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='practice_answers'
    )
    question = models.ForeignKey(
        PracticeQuestion,
        on_delete=models.CASCADE,
        related_name='student_answers'
    )

    answer = models.TextField()
    is_correct = models.BooleanField()
    ai_feedback = models.TextField()

    # Evaluation details
    score = models.FloatField(default=0.0)  # 0-100
    evaluation_criteria = models.JSONField(default=dict)

    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student_answers'
        ordering = ['-answered_at']

    def __str__(self):
        return f"{self.student.username} - {self.question.topic}"
