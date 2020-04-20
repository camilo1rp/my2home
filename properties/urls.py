from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.utils.translation import gettext_lazy as _

from .views import TemplateView

app_name = "property"
urlpatterns = [
    path('', views.ListProperty.as_view(), name='index'),
    path('template/', views.Template, name='template'),
    path('home/', views.homepage, name='home'),
    path('new_property/', views.CreateProperty.as_view(), name='create'),
    path('new_project/', views.CreateProject.as_view(), name='create-project'),
    path('contact_us/', views.contact_us, name='contact'),
    path('property/upload', views.property_upload, name='upload'),
    path('property/follow', views.property_following, name='follow'),
    path('new_address_col/<int:prop_id>/', views.create_address, name='create-address'),
    path('new_image/<int:prop_id>/', views.create_image, name='create-image'),
    path('update_property/<int:pk>/', views.UpdateProperty.as_view(), name='update'),
    path('pause_property/<int:prop_id>/', views.pause, name='pause'),
    path('property_detail/<int:prop_id>/', views.property_detail, name='detail'),
    path('whatsapp_connect/', views.whatsapp_contact, name='whatsapp'),
    path('address/', TemplateView.as_view(template_name="properties/address_auto.html")),
    path('testing/', TemplateView.as_view(template_name="properties2/base.html")),
]

