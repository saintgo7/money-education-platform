from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LearningPath, TopicMastery
from .serializers import LearningPathSerializer, TopicMasterySerializer
from .adaptive import AdaptiveLearningEngine


class LearningPathViewSet(viewsets.ModelViewSet):
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LearningPath.objects.filter(student=self.request.user)

    @action(detail=True, methods=['get'])
    def next_lesson(self, request, pk=None):
        """Get recommended next lesson"""
        learning_path = self.get_object()
        engine = AdaptiveLearningEngine()

        recommendation = engine.get_next_content(
            student_id=request.user.id,
            course_id=learning_path.course_id
        )

        return Response(recommendation)


class TopicMasteryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TopicMasterySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TopicMastery.objects.filter(student=self.request.user)
