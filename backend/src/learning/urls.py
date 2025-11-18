from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LearningPathViewSet, TopicMasteryViewSet

router = DefaultRouter()
router.register(r'learning-paths', LearningPathViewSet, basename='learning-path')
router.register(r'topic-mastery', TopicMasteryViewSet, basename='topic-mastery')

urlpatterns = [
    path('', include(router.urls)),
]
