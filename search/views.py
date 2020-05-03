from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import viewsets
from rest_framework.response import Response

from search.serializers import *
from search.mixins import FilterWithBooleanMixin, FilterWithBooleanAndSearchMixin


class SchoolViewSet(FilterWithBooleanAndSearchMixin, viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializers = SchoolSerializer
    serializer_class = SchoolSerializer
    filterset_fields = [f.name for f in School._meta.fields if
                        f.name not in ['specialised_divisions', 'data', 'school_name']]


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
