from django import template
from django.contrib.auth.models import User
from profiles.forms import ProfileEditForm
from profiles.models import Profile

register = template.Library()

@register.inclusion_tag('profiles/edit.html')
def edit_profile(id=None):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(id=user.profile.id)
    form = ProfileEditForm(instance=profile)
    return {'form': form}