from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Property


def user_is_propertys_manager(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            obj = Property.objects.get(id=kwargs['pk'])
            if obj.manager != request.user:
                return HttpResponseRedirect(reverse('property:index'))
            return function(request, *args, **kwargs)
        return _wrapped_view
    return decorator(function)