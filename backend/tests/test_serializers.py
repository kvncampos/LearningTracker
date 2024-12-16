from datetime import date, timedelta

import pytest
from learningtracker.models import DailyLearning
from learningtracker.serializers import DAILY_LEARNING_ERRORS, DailyLearningSerializer
from rest_framework.serializers import ValidationError


def test_dailylearning_serializer(daily_learning):
    # Create a DailyLearning instance using the factory
    instance = daily_learning()

    # Serialize the instance
    serializer = DailyLearningSerializer(instance)

    # Assertions
    assert isinstance(instance, DailyLearning)
    assert serializer.data["id"] == instance.id
    assert serializer.data["date"] == str(instance.date)
    assert serializer.data["learning_type"] == instance.learning_type
    assert serializer.data["description"] == instance.description


#################################################################
#                   VALIDATE INVALID DATA
#################################################################
def test_dailylearning_serializer_empty_object():
    data = {
        "id": 1,
        "date": None,
        "learning_type": None,
        "description": None,
    }
    serializer = DailyLearningSerializer(data=data)
    assert not serializer.is_valid()
    assert "date" in serializer.errors
    assert "learning_type" in serializer.errors
    assert "description" in serializer.errors


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
            "invalid-date",
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
    # Data with an invalid date
    data = {
        "id": 1,
        "date": "2000-01-01",  # Incorrect format
        "learning_type": "Invalid",
        "description": "This is a test learning.",
    }

    # Initialize the serializer with data
    serializer = DailyLearningSerializer(data=data)

    # Ensure the serializer is invalid
    assert not serializer.is_valid()

    # Check that the correct error message is raised for the date field
    assert "learning_type" in serializer.errors
    assert serializer.errors["learning_type"] == ['"Invalid" is not a valid choice.']


def test_dailylearning_serializer_invalid_short_description():
    # Arrange: Data with a future date
    data = {
        "id": 1,
        "date": "2000-01-01",
        "learning_type": "Python",
        "description": "ABC",  # Under 5 Characters
    }

    # Act: Initialize the serializer
    serializer = DailyLearningSerializer(data=data)

    # Assertions
    assert not serializer.is_valid()

    # Assert: ValidationError is raised for future date
    with pytest.raises(
        ValidationError, match=DAILY_LEARNING_ERRORS["invalid_description"]
    ):
        serializer.is_valid(raise_exception=True)


def test_dailylearning_serializer_validation_errors():
    data = {
        "id": 1,
        "date": None,
        "short_description": "",
        "description": "",
    }
    serializer = DailyLearningSerializer(data=data)
    serializer.is_valid()
    validation_errors = serializer.errors
    assert len(validation_errors) > 0


# @pytest.mark.django_db
# def test_dailylearning_serializer_save(daily_learning):
#     serializer = DailyLearningSerializer(daily_learning)
#     serializer.save()
#     assert DailyLearning.objects.count() == 1


# def test_dailylearning_serializer_update():
#     daily_learning = DailyLearning.objects.create(
#         user="testuser",
#         date="2022-01-01",
#         learning_type="Test Learning",
#         description="This is a test learning.",
#     )
#     serializer = DailyLearningSerializer(daily_learning)
#     serializer.data["learning_type"] = "SQL"
#     serializer.save()
#     assert daily_learning.learning_type == "SQL"
