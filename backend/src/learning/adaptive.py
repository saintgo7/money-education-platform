"""
Adaptive learning engine implementation
"""
import numpy as np
from typing import Dict, List
from django.db.models import Avg, Count
from .models import TopicMastery, LearningPath
from courses.models import Lesson
from assessment.models import Quiz, QuizAttempt


class AdaptiveLearningEngine:
    """Adaptive learning engine using IRT-based algorithms"""

    def __init__(self, mastery_threshold: float = 0.8):
        self.mastery_threshold = mastery_threshold

    def calculate_mastery(self, student_id: int, course_id: int, topic: str) -> float:
        """
        Calculate mastery level for a topic using Item Response Theory

        Returns: float between 0.0 and 1.0
        """
        try:
            mastery = TopicMastery.objects.get(
                student_id=student_id,
                course_id=course_id,
                topic=topic
            )

            if mastery.attempts == 0:
                return 0.0

            # Simple IRT approximation
            base_mastery = mastery.successes / mastery.attempts

            # Get quiz performance for this topic
            quiz_attempts = QuizAttempt.objects.filter(
                student_id=student_id,
                quiz__course_id=course_id,
                quiz__topic=topic
            )

            if quiz_attempts.exists():
                avg_score = quiz_attempts.aggregate(Avg('score'))['score__avg']
                weighted_mastery = (base_mastery * 0.4) + (avg_score / 100 * 0.6)
            else:
                weighted_mastery = base_mastery

            return min(weighted_mastery, 1.0)

        except TopicMastery.DoesNotExist:
            return 0.0

    def get_next_content(self, student_id: int, course_id: int) -> Dict:
        """
        Recommend next content based on mastery levels

        Returns: Dict with recommended lesson and reasoning
        """
        # Get student's learning path
        try:
            learning_path = LearningPath.objects.get(
                student_id=student_id,
                course_id=course_id
            )
        except LearningPath.DoesNotExist:
            # Create new learning path
            learning_path = self._create_learning_path(student_id, course_id)

        # Get mastery levels for all topics
        masteries = TopicMastery.objects.filter(
            student_id=student_id,
            course_id=course_id
        )

        # Find topics that need more work
        weak_topics = [
            m for m in masteries
            if m.mastery_level < self.mastery_threshold
        ]

        if weak_topics:
            # Focus on weakest topic
            weakest = min(weak_topics, key=lambda x: x.mastery_level)
            next_lesson = self._find_lesson_for_topic(course_id, weakest.topic)

            return {
                'lesson': next_lesson,
                'reason': 'remedial',
                'topic': weakest.topic,
                'current_mastery': weakest.mastery_level
            }
        else:
            # Progress to next topic
            next_lesson = self._get_next_unlearned_lesson(learning_path)

            return {
                'lesson': next_lesson,
                'reason': 'progression',
                'topic': next_lesson.title if next_lesson else None,
                'current_mastery': 1.0
            }

    def _create_learning_path(self, student_id: int, course_id: int) -> LearningPath:
        """Create a new learning path for student"""
        lessons = Lesson.objects.filter(
            module__course_id=course_id
        ).order_by('module__order', 'order')

        recommended_lessons = [lesson.id for lesson in lessons]

        learning_path = LearningPath.objects.create(
            student_id=student_id,
            course_id=course_id,
            recommended_lessons=recommended_lessons,
            current_lesson=lessons.first() if lessons.exists() else None
        )

        return learning_path

    def _find_lesson_for_topic(self, course_id: int, topic: str) -> Lesson:
        """Find a lesson that covers the given topic"""
        # Search in lesson titles and content
        lessons = Lesson.objects.filter(
            module__course_id=course_id
        ).filter(
            models.Q(title__icontains=topic) |
            models.Q(content__icontains=topic)
        )

        return lessons.first()

    def _get_next_unlearned_lesson(self, learning_path: LearningPath) -> Lesson:
        """Get next lesson that hasn't been completed"""
        for lesson_id in learning_path.recommended_lessons:
            if lesson_id not in learning_path.completed_lessons:
                return Lesson.objects.get(id=lesson_id)

        return None

    def update_mastery(
        self,
        student_id: int,
        course_id: int,
        topic: str,
        success: bool
    ):
        """Update mastery level based on practice result"""
        mastery, created = TopicMastery.objects.get_or_create(
            student_id=student_id,
            course_id=course_id,
            topic=topic
        )

        mastery.attempts += 1
        if success:
            mastery.successes += 1

        # Recalculate mastery level
        mastery.mastery_level = self.calculate_mastery(student_id, course_id, topic)
        mastery.save()
