from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from .forms import UserForm, ProfileForm, ProfileEditForm, ProfilePhotoForm
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

    def form_valid(self, form):
        form.save()
        return render(self.request, 'account/dashboard.html')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the profile id
        context['pro_id'] = self.kwargs['user_id']
        return context


class ProfileEdit(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "profiles/edit.html"
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile'

    def form_valid(self, form):
        print("valid****************")
        form.save()
        return render(self.request, 'profiles/details_list.html')


class ProtoEdit(UpdateView):
    model = Profile
    form_class = ProfilePhotoForm
    template_name = "profiles/photo_edit.html"
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile'

    def form_valid(self, form):
        print("valid****************")
        form.save()
        return HttpResponse(json.dumps(0), content_type='application/json')





# def edit_profile(request):
#     form = ProfileEditForm(request.POST or None)
#     if request.method == 'POST':
#         form = ProfileEditForm(request.POST)
#         if form.is_valid():
#             form.save()
#             HttpResponse(json.dumps(0), content_type='application/json')
#         else:
#             render(request, "properties/edit.html", {'form': form})
#     render(request, "properties/edit.html", {'form': form})


