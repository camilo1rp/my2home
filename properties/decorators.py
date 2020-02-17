from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.translation import gettext

from .models import Property


def user_is_propertys_manager(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            try:
                obj = Property.objects.get(id=kwargs['pk'])
            except ObjectDoesNotExist:
                return HttpResponse(gettext("Property does not exist"))
            if request.user not in [obj.manager, obj.owner]:
                return HttpResponseRedirect(reverse('property:index'))
            return function(request, *args, **kwargs)
        return _wrapped_view
    return decorator(function)