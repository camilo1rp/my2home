from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Property


# def user_is_propertys_manager(function):
#     def wrap(request, *args, **kwargs):
#         prop = Property.objects.get(pk=kwargs['pk_url_kwarg'])
#         if prop.manager == request.user:
#             return function(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap


def user_is_propertys_manager(function):
    def decorator(function):
        def _wrapped_view(request, *args, **kwargs):
            obj = Property.objects.get(id=kwargs['pk'])
            print("got in")
            print(obj.manager)
            print(request.user)
            if obj.manager != request.user:
                return HttpResponseRedirect(reverse('property:index'))
            return function(request, *args, **kwargs)
        return _wrapped_view
    return decorator(function)