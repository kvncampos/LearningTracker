# backend/learningtracker/serializers.py
from rest_framework import serializers
from .models import DailyLearning


class DailyLearningSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLearning
        fields = ["id", "date", "description"]
