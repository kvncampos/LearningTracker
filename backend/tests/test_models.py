import pytest
from django.db.utils import IntegrityError


def test_dailylearning_creation(daily_learning):
    learning = daily_learning(date="2023-01-01", description="Learning Django")
    assert learning.date == "2023-01-01"
    assert learning.description == "Learning Django"


def test_dailylearning_unique_date(daily_learning):
    daily_learning(date="2022-01-01")
    with pytest.raises(IntegrityError):
        daily_learning(date="2022-01-01")


def test_str_representation(daily_learning):
    learning_instance = (
        daily_learning()
    )  # Call the factory function to create an instance
    assert str(learning_instance) == "testuser's Learning on 2022-01-01"
