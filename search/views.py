from django.http import JsonResponse
from rest_framework import viewsets
from django.contrib.postgres.search import TrigramSimilarity

from search.serializers import *


class HighSchoolViewSet(viewsets.ViewSet):

    def list(self, request, format=None):
        public_schools = PublicSchool.objects \
            .filter(school_type='liceum ogólnokształcące')
        private_schools = PrivateSchool.objects \
            .filter(school_type='liceum ogólnokształcące')
        if request.GET.get('name') is not None:
            name = request.GET.get('name')
            public_schools = public_schools \
                .annotate(similarity=TrigramSimilarity('school_name', name)) \
                .filter(similarity__gte=0.06) \
                .order_by('-similarity')
            private_schools = private_schools \
                .annotate(similarity=TrigramSimilarity('school_name', name)) \
                .filter(similarity__gte=0.06) \
                .order_by('-similarity')

        serializer_public = PublicSchoolSerializer(public_schools, many=True)
        serializer_private = PrivateSchoolSerializer(private_schools, many=True)
        return JsonResponse(serializer_public.data + serializer_private.data, safe=False)


class HighSchoolPublicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PublicSchool.objects.filter(school_type='liceum ogólnokształcące')
    serializer_class = PublicSchoolSerializer


class HighSchoolPrivateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PrivateSchool.objects.filter(school_type='liceum ogólnokształcące')
    serializer_class = PrivateSchoolSerializer


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
