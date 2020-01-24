from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_phone(value):
    phone_length = len(str(value))
    if phone_length < 7:
        raise ValidationError(_("Phone number is too short. It must be between 7-10 digits"))
    elif phone_length > 10:
        raise ValidationError(_("Phone number is too long. It must be between 7-10 digits"))
    else:
        return value
