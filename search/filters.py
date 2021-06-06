from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.forms import BooleanField
from django_filters import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    MultipleChoiceFilter,
    NumberFilter,
)
from search.models import (
    School,
    SchoolType,
    HighSchoolClass,
    Address,
    ExtendedSubject,
)


def is_regon(id):
    return len(id) in [9, 14]


def get_available_values_from_model(selected_model, key):
    return [
        (value, value)
        for value in selected_model.objects.values_list(key, flat=True).distinct()
    ]


class BooleanDefaultField(BooleanField):
    def clean(self, value):
        if value is None:
            return False
        return super(BooleanDefaultField, self).clean(value)


class BooleanDefaultFilter(BooleanFilter):
    field_class = BooleanDefaultField


class SchoolClassFilter(FilterSet):
    class Meta:
        model = HighSchoolClass
        fields = "__all__"

    year = NumberFilter(field_name="year", method="filter_year")

    def filter_year(self, queryset, _name, value):
        return queryset.filter(year__startswith=value)


class SchoolFilter(FilterSet):
    CURRENT_RECRUITMENT_YEAR = 2020
    SUPPORTED_SCHOOL_TYPES = [SchoolType.LO, SchoolType.TECH, SchoolType.BRAN]
    QUERY_FIELD = "school_name"
    MIN_QUERY_SIMILARITY = 0.05

    class Meta:
        model = School
        fields = ["school_name", "is_public"]

    include_unsupported = BooleanDefaultFilter(
        field_name="school_type", method="include_unsupported_filter"
    )

    school_ids = MultipleChoiceFilter(
        field_name="id",
        choices=get_available_values_from_model(School, "id"),
        method="school_ids_filter",
    )

    query = CharFilter(field_name="school_name", method="query_filter")

    extended_subjects = MultipleChoiceFilter(
        field_name="highschoolclass__extendedsubject__name",
        choices=get_available_values_from_model(ExtendedSubject, "name"),
        method="extended_subjects_filter",
    )

    districts = MultipleChoiceFilter(
        field_name="address__district",
        choices=get_available_values_from_model(Address, "district"),
    )

    def include_unsupported_filter(self, queryset, _name, value):
        print(value)
        if value is True:
            return queryset

        return queryset.filter(school_type__in=self.SUPPORTED_SCHOOL_TYPES)

    def school_ids_filter(self, queryset, name, value):
        regons = [regon for regon in value if is_regon(value)]
        ids = [school_id for school_id in value if school_id not in regons]

        return queryset.filter(
            Q(id__in=ids) | Q(public_institution_data__regon__in=regons)
        )

    def query_filter(self, queryset, name, value):
        return queryset.annotate(
            similarity=TrigramSimilarity(self.QUERY_FIELD, value)
        ).filter(similarity__gte=self.MIN_QUERY_SIMILARITY)

    def extended_subjects_filter(self, queryset, _name, value):
        return queryset.filter(
            highschoolclass__extendedsubject__name__in=value,
            highschoolclass__year__startswith=self.CURRENT_RECRUITMENT_YEAR,
        ).distinct()
