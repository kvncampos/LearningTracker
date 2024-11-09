from django.db.utils import IntegrityError
import pytest
from django.core.exceptions import ValidationError
from learningtracker.models import DailyLearning

@pytest.mark.django_db
def test_daily_learning_creation():
    """Test creating a daily learning instance"""
    daily_learning = DailyLearning.objects.create(date='2022-01-01', description='Test Description')
    assert str(daily_learning.date) == '2022-01-01'
    assert daily_learning.description == 'Test Description'

@pytest.mark.django_db
def test_daily_learning_unique_date():
    """Test creating a new instance with an existing date"""
    DailyLearning.objects.create(date='2022-01-01', description='Test Description')
    duplicate_learning = DailyLearning(date='2022-01-01', description='New Description')
    with pytest.raises(ValidationError):
        duplicate_learning.full_clean()  # Trigger validation manually

@pytest.mark.django_db
def test_daily_learning_str_representation():
    """Test the string representation of a daily learning instance"""
    daily_learning = DailyLearning.objects.create(date='2022-01-01', description='Test Description')
    assert str(daily_learning) == 'Learning on 2022-01-01'

@pytest.mark.django_db
def test_daily_learning_none_date():
    """Test that creating a DailyLearning instance with a None date raises an IntegrityError"""
    with pytest.raises(IntegrityError):
        DailyLearning.objects.create(date=None, description='Test Description')
