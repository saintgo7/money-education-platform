"""
Serializers for AI tutor models
"""
from rest_framework import serializers
from .models import Conversation, Message, PracticeQuestion, StudentAnswer


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message"""

    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'tokens_used', 'model_used', 'created_at']
        read_only_fields = ['tokens_used', 'model_used', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation"""

    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ['student']

    def get_message_count(self, obj):
        return obj.messages.count()


class PracticeQuestionSerializer(serializers.ModelSerializer):
    """Serializer for PracticeQuestion"""

    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = PracticeQuestion
        fields = '__all__'

    def get_success_rate(self, obj):
        if obj.times_used == 0:
            return 0
        return (obj.times_correct / obj.times_used) * 100


class StudentAnswerSerializer(serializers.ModelSerializer):
    """Serializer for StudentAnswer"""

    question_text = serializers.CharField(source='question.question', read_only=True)
    topic = serializers.CharField(source='question.topic', read_only=True)

    class Meta:
        model = StudentAnswer
        fields = '__all__'
        read_only_fields = ['student', 'is_correct', 'ai_feedback', 'score', 'evaluation_criteria']
