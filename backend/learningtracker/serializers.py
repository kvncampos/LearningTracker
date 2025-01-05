from datetime import date

from rest_framework import serializers

from .models import DailyLearning, Tag
from .utils.error_const import DAILY_LEARNING_ERRORS


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class DailyLearningSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)  # Add tags as a nested serializer

    class Meta:
        model = DailyLearning
        fields = [
            "id",
            "date",
            "learning_type",
            "description",
            "tags",
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

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        daily_learning = DailyLearning.objects.create(**validated_data)

        # Add tags to the DailyLearning instance
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                user=daily_learning.user, **tag_data
            )
            daily_learning.tags.add(tag)

        return daily_learning

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)

        # Update fields of DailyLearning
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle tags if provided
        if tags_data is not None:
            instance.tags.clear()  # Clear existing tags
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(user=instance.user, **tag_data)
                instance.tags.add(tag)

        return instance
