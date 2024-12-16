# backend/learningtracker/serializers.py
from datetime import date
from typing import TypedDict

from rest_framework import serializers

from .models import DailyLearning


class DailyLearningErrorDefinitions(TypedDict):
    invalid_date: str
    invalid_description: str


DAILY_LEARNING_ERRORS: DailyLearningErrorDefinitions = {
    "invalid_date": "The date cannot be in the future.",
    "invalid_description": "Description must be at least 5 characters.",
}


class DailyLearningSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLearning
        fields = [
            "id",
            "date",
            "learning_type",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError(DAILY_LEARNING_ERRORS["invalid_date"])
        return value

    def validate_description(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                DAILY_LEARNING_ERRORS["invalid_description"]
            )
        return value
