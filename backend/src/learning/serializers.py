from rest_framework import serializers
from .models import LearningPath, TopicMastery


class LearningPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPath
        fields = '__all__'


class TopicMasterySerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicMastery
        fields = '__all__'
