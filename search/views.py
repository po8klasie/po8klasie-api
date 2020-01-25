from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from search.serializers import *


def index(request):
    return HttpResponse("Hello")


@api_view(['GET'])
def public_school_list(request):
    if request.method == 'GET':
        public_schools = PublicSchool.objects.all()
        serializer = PublicSchoolSerializer(public_schools, many=True)
        return JsonResponse(serializer.data, safe=False)
