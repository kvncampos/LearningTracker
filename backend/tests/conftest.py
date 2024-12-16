from typing import Any, Callable

import pytest
from django.contrib.auth.models import User
from learningtracker.models import DailyLearning


@pytest.fixture
def test_user(db) -> User:
    """
    Create a test user for the test suite.
    """
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )


@pytest.fixture
def daily_learning(test_user: User) -> Callable[..., DailyLearning]:
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
            "user": test_user,
            "date": "2022-01-01",
            "learning_type": DailyLearning.Topics.PYTHON,
            "description": "This is a test learning.",
        }
        defaults.update(kwargs)
        return DailyLearning.objects.create(**defaults)

    return _create_daily_learning
