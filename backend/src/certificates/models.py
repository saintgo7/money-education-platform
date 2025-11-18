"""
Certificate models
"""
from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
import uuid

User = get_user_model()


class Certificate(models.Model):
    """Course completion certificate"""

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')

    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    pdf_url = models.URLField(blank=True)

    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificates'
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
