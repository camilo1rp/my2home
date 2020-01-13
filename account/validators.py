from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone(value):
    if len(str(value)) < 7:
        raise ValidationError("Phone number is too short. It must be between 7-10 digits")
    else:
        return value
