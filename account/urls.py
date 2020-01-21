from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext_lazy as _
app_name = 'account'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('property_card/', views.card, name='card'),
]
