from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext_lazy as _

app_name = "city"
urlpatterns = [
    path('cities/', views.city, name='cities'),
    path('states/', views.state, name='states'),
    path('all_cities/', views.all_cities, name='all-cities'),
]
