from rest_framework import viewsets
from search.serializers import *


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializers = SchoolSerializer
    serializer_class = SchoolSerializer
    filterset_fields = [f.name for f in School._meta.fields if f.name not in ['specialised_divisions', 'data']]


class HighSchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.filter(school_type='liceum ogólnokształcące')
    serializer_class = SchoolSerializer
    filterset_fields = [f.name for f in School._meta.fields if f.name not in ['specialised_divisions', 'data']]
    search_fields = ['school_name', 'school_type']


class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_fields = [f.name for f in Address._meta.fields]


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactData.objects.all()
    serializer_class = ContactSerializer
    filterset_fields = [f.name for f in ContactData._meta.fields]


class PublicInstitutionDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PublicInstitutionData.objects.all()
    serializer_class = PublicInstitutionDataSerializer
    filterset_fields = [f.name for f in PublicInstitutionData._meta.fields if f.name not in ['data']]


class PrivateInstitutionDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PrivateInstitutionData.objects.all()
    serializer_class = PrivateInstitutionDataSerializer
    filterset_fields = [f.name for f in PrivateInstitutionData._meta.fields]


class HighSchoolClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HighSchoolClass.objects.all()
    serializer_class = HighSchoolClassSerializer
    filterset_fields = [f.name for f in HighSchoolClass._meta.fields if f.name not in ['year']]


class ExtendedSubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExtendedSubject.objects.all()
    serializer_class = ExtendedSubjectSerializer
    filterset_fields = [f.name for f in ExtendedSubject._meta.fields]


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filterset_fields = [f.name for f in Language._meta.fields]


class StatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    filterset_fields = [f.name for f in Statistics._meta.fields]
