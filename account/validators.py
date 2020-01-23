from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone(value):
    phone_length = len(str(value))
    if phone_length < 7 or phone_length > 10:
        raise ValidationError("Phone number is too short. It must be between 7-10 digits")
    else:
        return value
