from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register(r'highschool/public', views.HighSchoolPublicViewSet, basename='highschool-public')
router.register(r'highschool/private', views.HighSchoolPrivateViewSet, basename='highschool-private')
router.register(r'highschool/class', views.HighSchoolClassViewSet, basename='highschoolclass')
router.register(r'language', views.LanguageViewSet, basename='language')
router.register(r'subject', views.ExtendedSubjectViewSet, basename='subject')
router.register(r'stats', views.StatisticsViewSet, basename='stats')
router.register(r'highschool', views.HighSchoolViewSet, basename='highschool')

urlpatterns = [
    path('', include(router.urls)),
]
