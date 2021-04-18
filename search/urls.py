from django.urls import path, include
from rest_framework.routers import DefaultRouter
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

from . import views

router = DefaultRouter()
router.register(
    r"highschool/class", views.HighSchoolClassViewSet, basename="highschoolclass"
)
router.register(r"language", views.LanguageViewSet, basename="language")
router.register(r"languages", views.AllLanguagesViewSet, basename="languages")
router.register(r"subject", views.ExtendedSubjectViewSet, basename="subject")
router.register(r"subjects", views.AllSubjectsViewSet, basename="subjects")
router.register(r"stats", views.StatisticsViewSet, basename="stats")
router.register(r"highschool", views.HighSchoolViewSet, basename="highschool")
router.register(r"school", views.SchoolViewSet, basename="school")
router.register(r"address", views.AddressViewSet, basename="address")
router.register(r"contact", views.ContactViewSet, basename="contactdata")
router.register(
    r"publicinstitution",
    views.PublicInstitutionDataViewSet,
    basename="publicinstitutiondata",
)
router.register(
    r"privateinstitution",
    views.PrivateInstitutionDataViewSet,
    basename="privateinstitutiondata",
)

urlpatterns = [
    path("", include(router.urls)),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
