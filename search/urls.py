from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/publiczne/', views.public_school_list),
    path('search/', views.high_school_list_by_name),
]
