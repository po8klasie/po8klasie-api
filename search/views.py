from django.http import JsonResponse
from rest_framework import viewsets
from django.contrib.postgres.search import TrigramSimilarity
from django_filters import rest_framework as filters

from search.serializers import *


# class HighSchoolViewSet(viewsets.ViewSet):
#
#     def list(self, request, format=None):
#         if request.GET.get('name') is not None:
#             name = request.GET.get('name')
#             schools = School.objects \
#                 .filter(school_type='liceum ogólnokształcące') \
#                 .annotate(similarity=TrigramSimilarity('school_name', name)) \
#                 .filter(similarity__gte=0.06) \
#                 .order_by('-similarity')
#         else:
#             schools = School.objects \
#                 .filter(school_type='liceum ogólnokształcące')
#
#         serializer = SchoolSerializer(schools, many=True)
#         return JsonResponse(serializer.data, safe=False)

class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializers = SchoolSerializer
    serializer_class = SchoolSerializer


class HighSchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.filter(school_type='liceum ogólnokształcące')
    serializer_class = SchoolSerializer
    filterset_fields = ['is_public']
    search_fields = ['school_name']


class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactData.objects.all()
    serializer_class = ContactSerializer


class PublicInstitutionDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PublicInstitutionData.objects.all()
    serializer_class = PublicInstitutionDataSerializer


class PrivateInstitutionDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PrivateInstitutionData.objects.all()
    serializer_class = PrivateInstitutionDataSerializer


class HighSchoolClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HighSchoolClass.objects.all()
    serializer_class = HighSchoolClassSerializer


class ExtendedSubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExtendedSubject.objects.all()
    serializer_class = ExtendedSubjectSerializer


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class StatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
