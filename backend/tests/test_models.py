from datetime import date, timedelta

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from learningtracker.models import DailyLearning, Tag
from learningtracker.utils.error_const import DAILY_LEARNING_ERRORS, TAG_ERRORS


#################################################################
#                   VALIDATE DAILYLEARNING CRUD OPERATIONS
#################################################################
@pytest.mark.django_db
def test_dailylearning_create(create_learning_entry):
    instance = create_learning_entry()
    assert DailyLearning.objects.filter(id=instance.id).exists()


@pytest.mark.django_db
def test_dailylearning_update(create_learning_entry):
    # Arrange: Create an instance
    instance: DailyLearning = create_learning_entry()

    # Act: Update the instance
    instance.description = "new description"
    instance.save()

    # Assert: Ensure the change is reflected in the database
    instance.refresh_from_db()
    assert instance.description == "new description"


@pytest.mark.django_db
def test_dailylearning_user_cascade_delete(create_learning_entry):
    # Arrange: Create a learning instance associated with the user
    instance = create_learning_entry()

    # Act: Delete the user
    instance.user.delete()

    # Assert: Ensure the learning instance is also deleted
    assert not DailyLearning.objects.filter(id=instance.id).exists()
    assert not User.objects.filter(id=instance.user.id)


@pytest.mark.django_db
def test_dailylearning_user_unique_together(create_learning_entry):
    # Arrange: Create the first DailyLearning instance
    instance = create_learning_entry()

    # Act: Attempt to create a second DailyLearning instance with the same user and date
    with pytest.raises(ValidationError):
        create_learning_entry(date=instance.date)

    # Assert: Ensure the first instance still exists
    assert DailyLearning.objects.filter(id=instance.id).exists()


@pytest.mark.django_db
def test_dailylearning_different_users_same_date(create_learning_entry):
    # Arrange: Create a learning instance for the first user
    instance = create_learning_entry()

    # Act: Create a second user and a learning instance with the same date
    user2 = User.objects.create_user(
        username="testuser2", email="test2@example.com", password="password"
    )
    instance2 = create_learning_entry(user=user2, date=instance.date)

    # Assert: Both instances exist
    assert DailyLearning.objects.filter(id=instance.id).exists()
    assert DailyLearning.objects.filter(id=instance2.id).exists()


#################################################################
#                   VALIDATE INVALID DAILYLEARNING DATA
#################################################################
def test_dailylearning_future_date(create_learning_entry):
    # Arrange: Set a future date
    future_date = date.today() + timedelta(days=1)

    # Assert: ValidationError is raised during save()
    with pytest.raises(ValidationError) as exc_info:
        # Act: Create an instance with a future date
        instance = create_learning_entry(date=future_date)
        instance.save()

    # Assert: Validate the error details
    assert exc_info.value.message_dict["date"] == [
        DAILY_LEARNING_ERRORS["invalid_date"]
    ]


def test_dailylearning_short_description(create_learning_entry):
    # Arrange: Set an invalid short description
    short_description = "test"

    # Assert: ValidationError is raised during save()
    with pytest.raises(ValidationError) as exc_info:
        # Act: Create an instance with an invalid description
        instance = create_learning_entry(description=short_description)
        instance.save()

    # Assert: Validate the error details
    assert exc_info.value.message_dict["description"] == [
        DAILY_LEARNING_ERRORS["invalid_description"]
    ]


def test_dailylearning_unique_date(create_learning_entry):
    # Arrange: Create a valid entry
    create_learning_entry()

    with pytest.raises(ValidationError):
        # Act: Create another entry with the same date. (not unique)
        create_learning_entry()

    # Assert: Validate the error details and that one entry exists.
    assert DailyLearning.objects.all().count() == 1


def test_dailylearning_invalid_learning_type(create_learning_entry):
    # Arrange: Create a valid entry with an invalid learning type
    invalid_learning_type = {"learning_type": "Invalid"}

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        # Create an entry with an invalid learning type
        entry = create_learning_entry(**invalid_learning_type)
        entry.full_clean()  # Triggers validation for `choices`

    # Assert: Ensure the ValidationError is raised and has the expected message
    assert "learning_type" in exc_info.value.message_dict
    assert exc_info.value.message_dict["learning_type"] == [
        "Value 'Invalid' is not a valid choice."
    ]


#################################################################
#                   VALIDATE TAG MODEL VALID DATA
#################################################################
@pytest.mark.django_db
def test_tag_creation(create_test_user):
    # Arrange: Create a tag for the user
    tag = Tag.objects.create(user=create_test_user, name="Python")

    # Assert: Tag exists and is associated with the user
    assert Tag.objects.filter(id=tag.id).exists()
    assert tag.user == create_test_user


@pytest.mark.django_db
def test_tag_different_users_same_name(create_test_user):
    # Arrange: Create a tag for the first user
    tag1 = Tag.objects.create(user=create_test_user, name="Python")

    # Act: Create another user and a tag with the same name
    user2 = User.objects.create_user(
        username="testuser2", email="test2@example.com", password="password"
    )
    tag2 = Tag.objects.create(user=user2, name="Python")

    # Assert: Both tags exist independently
    assert Tag.objects.filter(id=tag1.id).exists()
    assert Tag.objects.filter(id=tag2.id).exists()
    assert tag1.user != tag2.user


@pytest.mark.django_db
def test_tag_cascade_delete(create_test_user):
    # Arrange: Create a tag for the user
    tag = Tag.objects.create(user=create_test_user, name="Python")

    # Act: Delete the user
    create_test_user.delete()

    # Assert: Ensure the tag is also deleted
    assert not Tag.objects.filter(id=tag.id).exists()


#################################################################
#                   VALIDATE TAG MODEL INVALID DATA
#################################################################
@pytest.mark.django_db
def test_tag_uniqueness_per_user_with_error_message(create_test_user):
    # Arrange: Create a tag for the user
    Tag.objects.create(user=create_test_user, name="Python")

    # Act & Assert: Attempt to create a duplicate tag for the same user
    with pytest.raises(ValidationError) as exc_info:
        duplicate_tag = Tag(user=create_test_user, name="Python")
        duplicate_tag.full_clean()  # Triggers validation

    # Assert: Check the error message
    assert (
        exc_info.value.message_dict["duplicate_name"][0] == TAG_ERRORS["duplicate_name"]
    )


@pytest.mark.django_db
def test_tag_max_len(create_test_user):
    # Arrange: Create a tag for the user
    invalid_tag_name = "SuperLongTitleThatExceedsLimits"

    # Act & Assert: Attempt to create a duplicate tag for the same user
    with pytest.raises(ValidationError) as exc_info:
        exceed_char_max = Tag(user=create_test_user, name=invalid_tag_name)
        exceed_char_max.full_clean()  # Triggers validation

    # Assert: Check the error message
    assert (
        exc_info.value.message_dict["name"][0]
        == "Ensure this value has at most 30 characters (it has 31)."
    )


#################################################################
#                   VALIDATE STR FOR MODELS
#################################################################
def test_str_representations(create_learning_entry):
    learning_instance = create_learning_entry()
    tag = Tag.objects.create(user=learning_instance.user, name="Python")

    assert str(learning_instance) == "testuser's Python Learning on Jan 01, 2022"
    assert str(tag) == "Python (testuser)"
