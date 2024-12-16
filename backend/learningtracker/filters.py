import django_filters

from .models import DailyLearning


class DailyLearningFilter(django_filters.FilterSet):
    # Filters with descriptions
    date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="exact",
        label="Exact Date",
        help_text="Filter entries by an exact date (YYYY-MM-DD).",
    )
    start_date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="gte",
        label="Start Date",
        help_text="Filter entries on or after this date (YYYY-MM-DD).",
    )
    end_date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="lte",
        label="End Date",
        help_text="Filter entries on or before this date (YYYY-MM-DD).",
    )
    learning_type = django_filters.CharFilter(
        field_name="learning_type",
        lookup_expr="icontains",
        label="Learning Topic",
        help_text="Filter entries by a learning topic (case-insensitive match).",
    )
    description = django_filters.CharFilter(
        field_name="description",
        lookup_expr="icontains",
        label="Description",
        help_text="Filter entries by words in the desc. (case-insensitive match).",
    )

    class Meta:
        model = DailyLearning
        fields = ["date", "start_date", "end_date", "learning_type", "description"]
