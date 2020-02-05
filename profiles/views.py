from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserForm, ProfileForm
from .models import Profile


class CreateUser(CreateView):
    form_class = UserForm
    template_name = "profiles/create.html"


class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/profile.html"
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the profile id
        context['pro_id'] = self.kwargs['user_id']
        return context





