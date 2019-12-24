from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext_lazy as _

app_name = "property"
urlpatterns = [
    path('', views.ListProperty.as_view(), name='index'),
    path('new_property/', views.CreateProperty.as_view(), name='create'),
    path('new_address_col/<int:prop_id>/', views.create_address, name='create-address'),
    path('new_image/<int:prop_id>/', views.create_image, name='create-image'),
    path('update_property/<int:pk>/', views.UpdateProperty.as_view(), name='update'),
]

