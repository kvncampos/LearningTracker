from datetime import date, timedelta

import pytest
from learningtracker.models import DailyLearning, Tag
from learningtracker.serializers import DAILY_LEARNING_ERRORS, DailyLearningSerializer
from rest_framework.serializers import ValidationError


#################################################################
#                   VALIDATE VALID DATA
#################################################################
def test_dailylearning_serializer(create_learning_entry):
    # Create a DailyLearning instance using the factory
    instance = create_learning_entry()

    # Add tags to the instance
    tag_python = Tag.objects.create(user=instance.user, name="Python")
    instance.tags.add(tag_python)

    # Serialize the instance
    serializer = DailyLearningSerializer(instance)

    # Assertions
    assert isinstance(instance, DailyLearning)
    assert isinstance(tag_python, Tag)
    assert serializer.data["id"] == instance.id
    assert serializer.data["date"] == str(instance.date)
    assert serializer.data["learning_type"] == instance.learning_type
    assert serializer.data["description"] == instance.description
    assert "tags" in serializer.data
    assert serializer.data["tags"] == [{"id": tag_python.id, "name": "Python"}]


@pytest.mark.django_db
def test_dailylearning_serializer_is_valid_and_saves(create_test_user):
    data = {
        "date": date.today().isoformat(),
        "learning_type": "Python",
        "description": "Learned about Python serializers.",
        "tags": [{"name": "Python"}],
    }

    # Initialize the serializer with valid data
    serializer = DailyLearningSerializer(data=data, context={"request": None})

    # Ensure the serializer is valid
    assert serializer.is_valid(), serializer.errors

    # Save the validated data
    instance = serializer.save(user=create_test_user)

    # Assertions to ensure the instance is saved correctly
    assert instance.user == create_test_user
    assert instance.date.isoformat() == data["date"]
    assert instance.learning_type == data["learning_type"]
    assert instance.description == data["description"]
    assert DailyLearning.objects.filter(id=instance.id).exists()
    assert instance.tags.count() == 1
    assert instance.tags.first().name == "Python"


@pytest.mark.django_db
def test_dailylearning_serializer_updates_instance(create_learning_entry):
    instance = create_learning_entry()  # Create an initial instance

    # Add tags to the instance
    tag_python = Tag.objects.create(user=instance.user, name="Python")
    instance.tags.add(tag_python)

    update_data = {
        "date": instance.date,
        "learning_type": "Django",
        "description": "Updated learning entry.",
        "tags": [{"name": "Docker"}],  # Replace Python with Docker
    }

    serializer = DailyLearningSerializer(instance, data=update_data, partial=False)

    # Ensure the serializer is valid
    assert serializer.is_valid(), serializer.errors

    # Save the updated data
    updated_instance = serializer.save()

    # Assertions
    assert updated_instance.date == update_data["date"]
    assert updated_instance.learning_type == update_data["learning_type"]
    assert updated_instance.description == update_data["description"]
    assert updated_instance.tags.count() == 1
    assert updated_instance.tags.first().name == "Docker"


#################################################################
#                   VALIDATE INVALID DATA
#################################################################
def test_dailylearning_serializer_empty_object():
    data = {
        "id": 1,
        "date": None,
        "learning_type": None,
        "description": None,
        "tags": [],
    }
    serializer = DailyLearningSerializer(data=data)
    assert not serializer.is_valid()
    assert "date" in serializer.errors
    assert "learning_type" in serializer.errors
    assert "description" in serializer.errors
    assert len(serializer.errors) > 0


@pytest.mark.parametrize(
    "test_date, is_valid, expected_error",
    [
        # Valid dates
        (
            date.today().isoformat(),
            True,
            None,
        ),
        (
            (date.today() - timedelta(days=1)).isoformat(),
            True,
            None,
        ),
        # Future date
        (
            (date.today() + timedelta(days=1)).isoformat(),
            False,
            ["The date cannot be in the future."],
        ),
        # Invalid date format
        (
            "01-01-2022",
            False,
            ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."],
        ),
    ],
)
def test_dailylearning_serializer_date_validation(test_date, is_valid, expected_error):
    data = {
        "date": test_date,
        "learning_type": "Python",
        "description": "This is a test learning.",
        "tags": [{"name": "Python"}],
    }
    # Act: Initialize the serializer
    serializer = DailyLearningSerializer(data=data, context={"request": None})

    # Assert: Check if the serializer is valid or invalid
    if is_valid:
        assert serializer.is_valid()
    else:
        assert not serializer.is_valid()
        assert "date" in serializer.errors
        assert serializer.errors["date"] == expected_error


def test_dailylearning_serializer_invalid_learning_type():
    data = {
        "date": "2000-01-01",
        "learning_type": "Invalid",
        "description": "This is a test learning.",
        "tags": [{"name": "Python"}],
    }

    # Initialize the serializer with data
    serializer = DailyLearningSerializer(data=data)

    # Ensure the serializer is invalid
    assert not serializer.is_valid()
    assert "learning_type" in serializer.errors
    assert serializer.errors["learning_type"] == ['"Invalid" is not a valid choice.']


def test_dailylearning_serializer_invalid_short_description():
    data = {
        "date": "2000-01-01",
        "learning_type": "Python",
        "description": "ABC",  # Under 5 Characters
        "tags": [{"name": "Python"}],
    }

    serializer = DailyLearningSerializer(data=data)

    assert not serializer.is_valid()
    with pytest.raises(
        ValidationError, match=DAILY_LEARNING_ERRORS["invalid_description"]
    ):
        serializer.is_valid(raise_exception=True)
