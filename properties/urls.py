from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext_lazy as _

app_name = "property"
urlpatterns = [
    path('', views.CreateProperty.as_view(), name='index'),
]
