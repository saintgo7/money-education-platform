"""
Models for assessment system
"""
from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

User = get_user_model()


class Quiz(models.Model):
    """Quiz model"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    topic = models.CharField(max_length=200, blank=True)

    passing_score = models.IntegerField(default=70)
    time_limit_minutes = models.IntegerField(default=30)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quizzes'


class QuizQuestion(models.Model):
    """Quiz question"""

    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    question_text = models.TextField()
    options = models.JSONField(null=True, blank=True)
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True)
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'quiz_questions'
        ordering = ['order']


class QuizAttempt(models.Model):
    """Student's quiz attempt"""

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')

    score = models.FloatField(default=0.0)
    passed = models.BooleanField(default=False)
    answers = models.JSONField(default=dict)

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'quiz_attempts'


class Assignment(models.Model):
    """Assignment model"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments', null=True, blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()

    max_score = models.IntegerField(default=100)
    due_date = models.DateTimeField(null=True, blank=True)

    rubric = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'assignments'


class Submission(models.Model):
    """Student assignment submission"""

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('grading', 'Grading'),
        ('graded', 'Graded'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')

    content = models.TextField()
    attachments = models.JSONField(default=list)

    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'submissions'
