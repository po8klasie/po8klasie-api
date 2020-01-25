from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('publiczne/', views.public_school_list),
]
