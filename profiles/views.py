from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from .forms import UserForm, ProfileForm
from .models import Profile


class CreateUser(CreateView):
    form_class = UserForm
    template_name = "profiles/new_user.html"


class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/profile.html"
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile'


