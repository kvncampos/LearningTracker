# backend/learningtracker/tests/test_filters.py

import pytest
from learningtracker.filters import DailyLearningFilter, TagFilter
from learningtracker.models import DailyLearning, Tag


#################################################################
#                   VALIDATE DAILYLEARNINGFILTER VALID DATA
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
def test_dailylearningfilter_with_valid_data(
    create_learning_entry, filter_data, expected_count
):
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
#                   VALIDATE DAILYLEARNINGFILTER INVALID DATA
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
def test_dailylearningfilter_with_invalid_data(
    create_learning_entry, filter_data, expected_count
):
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
#                   VALIDATE DAILYLEARNINGFILTER META DATA
#################################################################
def test_dailylearningfilter_metadata():
    filter_set = DailyLearningFilter(queryset=DailyLearning.objects.all())
    for field_name, field in filter_set.filters.items():
        assert field.label
        assert field.lookup_expr
        assert field.extra.get("help_text")


#################################################################
#                   VALIDATE TAGFILTER DATA
#################################################################


@pytest.mark.django_db
def test_tag_filter_with_valid_data(create_tags):
    """
    Test filtering tags by name (case-insensitive match).
    """
    tags = Tag.objects.all()
    filter_data = {"name": "python"}
    filtered_tags = TagFilter(filter_data, queryset=tags).qs

    # Assert: Only tags with name containing "python" are returned
    assert filtered_tags.count() == 2
    assert all("python" in tag.name.lower() for tag in filtered_tags)


@pytest.mark.django_db
def test_tag_filter_by_user(create_tags, create_test_user):
    """
    Test filtering tags by user.
    """
    tags = Tag.objects.all()
    filter_data = {"user": create_test_user.id}
    filtered_tags = TagFilter(filter_data, queryset=tags).qs

    # Assert: Only tags belonging to the specified user are returned
    assert filtered_tags.count() == 2
    assert all(tag.user == create_test_user for tag in filtered_tags)


@pytest.mark.django_db
def test_tag_filter_by_name_and_user(create_tags, create_test_user):
    """
    Test filtering tags by name and user simultaneously.
    """
    tags = Tag.objects.all()
    filter_data = {"name": "python", "user": create_test_user.id}
    filtered_tags = TagFilter(filter_data, queryset=tags).qs

    # Assert: Only tags matching the name and user are returned
    assert filtered_tags.count() == 1
    assert all(tag.user == create_test_user for tag in filtered_tags)
    assert all("python" in tag.name.lower() for tag in filtered_tags)


@pytest.mark.django_db
def test_tag_filter_no_results(create_tags):
    """
    Test filtering with criteria that yield no results.
    """
    tags = Tag.objects.all()
    filter_data = {"name": "nonexistent", "user": 9999}  # Invalid user ID
    filtered_tags = TagFilter(filter_data, queryset=tags).qs

    # Assert: No tags are returned
    assert filtered_tags.count() == 0


def test_tagfiltered_metadata():
    filter_set = TagFilter(queryset=Tag.objects.all())
    for field_name, field in filter_set.filters.items():
        assert field.label
        if field_name == "name":
            assert field.lookup_expr
        assert field.extra.get("help_text")
