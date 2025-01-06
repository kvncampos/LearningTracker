from typing import Any, Callable

import pytest
from django.contrib.auth.models import User
from learningtracker.models import DailyLearning, Tag


@pytest.fixture
def create_test_user(db) -> User:
    """
    Create a test user for the test suite.
    """
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )


@pytest.fixture
def create_learning_entry(create_test_user: User) -> Callable[..., DailyLearning]:
    """
    A factory function for creating `DailyLearning` instances dynamically.

    Args:
        test_user (User): The user associated with the learning instance.

    Returns:
        Callable[..., DailyLearning]: A factory function that creates `DailyLearning`
        instances.
    """

    def _create_daily_learning(**kwargs: Any) -> DailyLearning:
        defaults = {
            "user": create_test_user,
            "date": "2022-01-01",
            "learning_type": DailyLearning.Topics.PYTHON,
            "description": "This is a test learning.",
        }
        defaults.update(kwargs)
        return DailyLearning.objects.create(**defaults)

    return _create_daily_learning


@pytest.fixture
def create_tags(create_test_user):
    """
    Fixture to create multiple tags for testing.
    """
    user1 = create_test_user
    user2 = User.objects.create_user(
        username="testuser2", email="test2@example.com", password="password"
    )
    tags = [
        Tag.objects.create(user=user1, name="Python"),
        Tag.objects.create(user=user1, name="Docker"),
        Tag.objects.create(user=user2, name="Python"),
        Tag.objects.create(user=user2, name="React"),
    ]
    return tags
