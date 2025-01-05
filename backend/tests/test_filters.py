# backend/learningtracker/tests/test_filters.py

import pytest
from learningtracker.filters import DailyLearningFilter
from learningtracker.models import DailyLearning


#################################################################
#                   VALIDATE FILTER VALID DATA
#################################################################
@pytest.mark.parametrize(
    "filter_data, expected_count",
    [
        ({"date": "2022-01-01"}, 1),  # Exact date
        ({"from_date": "2022-01-01"}, 1),  # Date >= 2022-01-01
        ({"to_date": "2022-01-01"}, 1),  # Date <= 2022-01-01
        ({"learning_type": "python"}, 1),  # Case-insensitive match
        ({"description": "test"}, 1),  # Case-insensitive substring match
    ],
)
@pytest.mark.django_db
def test_filter_with_valid_data(create_learning_entry, filter_data, expected_count):
    """
    Test that the filters return the correct number of entries.
    """
    create_learning_entry()
    filter_set = DailyLearningFilter(
        data=filter_data, queryset=DailyLearning.objects.all()
    )
    filtered_qs = filter_set.qs
    assert filtered_qs.count() == expected_count


#################################################################
#                   VALIDATE FILTER INVALID DATA
#################################################################
@pytest.mark.parametrize(
    "filter_data, expected_count",
    [
        ({"date": "2030-01-01"}, 0),  # Invalid Exact date
        ({"from_date": "2030-01-01"}, 0),  # Invalid Date >= 2030-01-01
        ({"to_date": "2000-01-01"}, 0),  # Invalid Date <= 2000-01-01
        ({"learning_type": "test"}, 0),  # Invalid Case-insensitive match
        ({"description": "invalid"}, 0),  # Invalid Case-insensitive substring match
    ],
)
@pytest.mark.django_db
def test_filter_with_invalid_data(create_learning_entry, filter_data, expected_count):
    """
    Test that the filters return the correct number of entries.
    """
    create_learning_entry()
    filter_set = DailyLearningFilter(
        data=filter_data, queryset=DailyLearning.objects.all()
    )
    filtered_qs = filter_set.qs
    assert filtered_qs.count() == expected_count


#################################################################
#                   VALIDATE FILTER META DATA
#################################################################
@pytest.mark.parametrize(
    "field_name, expected_label, expected_lookup, expected_help_text",
    [
        (
            "date",
            "Exact Date",
            "exact",
            "Filter entries by an exact date (YYYY-MM-DD).",
        ),
        (
            "from_date",
            "From Date",
            "gte",
            "Filter entries on or after this date (YYYY-MM-DD).",
        ),
        (
            "to_date",
            "To Date",
            "lte",
            "Filter entries on or before this date (YYYY-MM-DD).",
        ),
        (
            "learning_type",
            "Learning Topic",
            "icontains",
            "Filter entries by a learning topic (case-insensitive match).",
        ),
        (
            "description",
            "Description",
            "icontains",
            "Filter entries by words in the desc. (case-insensitive match).",
        ),
    ],
)
def test_filter_metadata(
    field_name, expected_label, expected_lookup, expected_help_text
):
    """
    Test that filter field metadata matches the expected values.
    """
    filter_set = DailyLearningFilter(queryset=DailyLearning.objects.all())
    field = filter_set.filters[field_name]
    assert field.label == expected_label
    assert field.lookup_expr == expected_lookup
    assert field.extra.get("help_text") == expected_help_text
