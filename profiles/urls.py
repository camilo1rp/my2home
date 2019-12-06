from django.urls import path
from . import views


app_name = "profile"
urlpatterns = [
    path('create_user/', views.CreateUser.as_view(), name='create'),
    path('update_profile/<int:user_id>/', views.ProfileUpdate.as_view(), name='update'),
]
