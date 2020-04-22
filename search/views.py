from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from django.db.models import Q
from functools import reduce
from operator import or_
from search.serializers import *


class FilterWithBooleanMixin(ListModelMixin):
    OR = "|"

    def list(self, request, *args, **kwargs):
        if not self._is_request_with_booleans(request):
            return super().list(request, kwargs)

        queryset = self._query_with_boolean(request)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def _query_with_boolean(self, request):
        queries = self._parse_expressions(request.GET)
        queryset = self.get_queryset()
        # perform AND
        for q in queries:
            if not q:
                continue
            # perform OR
            query = reduce(or_, q)
            queryset = queryset.filter(query)
        return queryset

    def _parse_expressions(self, query_params):
        queries = []
        for field in query_params.keys():
            expressions = query_params.getlist(field)
            if not expressions or all(v == '' for v in expressions):
                continue
            for exp in expressions:
                values = exp.split(self.OR)
                queries.append([Q(**{field: val}) for val in values])
        return queries

    def _is_request_with_booleans(self, request):
        for key in request.GET.keys():
            values = request.GET.getlist(key)
            if not values or all(v == '' for v in values):
                continue
            if len(values) > 1 or any(self.OR in v for v in values):
                return True
        return False


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializers = SchoolSerializer
    serializer_class = SchoolSerializer
    filterset_fields = [f.name for f in School._meta.fields if
                        f.name not in ['specialised_divisions', 'data', 'school_name']]

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.GET.get('school_name') is not None:
            name = request.GET.get('school_name')
            queryset = queryset \
                .annotate(similarity=TrigramSimilarity('school_name', name)) \
                .filter(similarity__gte=0.05) \
                .order_by('-similarity')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HighSchoolViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.filter(school_type='liceum ogólnokształcące')
    serializer_class = SchoolSerializer
    filterset_fields = [f.name for f in School._meta.fields if f.name not in ['specialised_divisions', 'data']]
    search_fields = ['school_name', 'school_type']


class TechnikumViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.filter(school_type='technikum')
    serializer_class = SchoolSerializer
    filterset_fields = [f.name for f in School._meta.fields if f.name not in ['specialised_divisions', 'data']]


class AddressViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_fields = [f.name for f in Address._meta.fields]


class ContactViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ContactData.objects.all()
    serializer_class = ContactSerializer
    filterset_fields = [f.name for f in ContactData._meta.fields]


class PublicInstitutionDataViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = PublicInstitutionData.objects.all()
    serializer_class = PublicInstitutionDataSerializer
    filterset_fields = [f.name for f in PublicInstitutionData._meta.fields if f.name not in ['data']]


class PrivateInstitutionDataViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = PrivateInstitutionData.objects.all()
    serializer_class = PrivateInstitutionDataSerializer
    filterset_fields = [f.name for f in PrivateInstitutionData._meta.fields]


class HighSchoolClassViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = HighSchoolClass.objects.all()
    serializer_class = HighSchoolClassSerializer
    filterset_fields = [f.name for f in HighSchoolClass._meta.fields if f.name not in ['year']]


class ExtendedSubjectViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = ExtendedSubject.objects.all()
    serializer_class = ExtendedSubjectSerializer
    filterset_fields = [f.name for f in ExtendedSubject._meta.fields]


class LanguageViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filterset_fields = [f.name for f in Language._meta.fields]


class StatisticsViewSet(FilterWithBooleanMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    filterset_fields = [f.name for f in Statistics._meta.fields]
