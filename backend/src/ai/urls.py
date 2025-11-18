"""
URL patterns for AI app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, PracticeQuestionViewSet, StudentAnswerViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'practice-questions', PracticeQuestionViewSet, basename='practice-question')
router.register(r'student-answers', StudentAnswerViewSet, basename='student-answer')

urlpatterns = [
    path('', include(router.urls)),
]
