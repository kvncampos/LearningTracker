import django_filters

from .models import DailyLearning, Tag


class DailyLearningFilter(django_filters.FilterSet):
    # Filters with descriptions
    date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="exact",
        label="Exact Date",
        help_text="Filter entries by an exact date (YYYY-MM-DD).",
    )
    from_date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="gte",
        label="From Date",
        help_text="Filter entries on or after this date (YYYY-MM-DD).",
    )
    to_date = django_filters.DateFilter(
        field_name="date",
        lookup_expr="lte",
        label="To Date",
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
        fields = ["date", "from_date", "to_date", "learning_type", "description"]


class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="name",
        lookup_expr="icontains",
        help_text="Filter entries by words in the tags. (case-insensitive match).",
    )
    user = django_filters.NumberFilter(
        field_name="user__id",
        help_text="Filter entries by user id.",
    )

    class Meta:
        model = Tag
        fields = ["name", "user"]
