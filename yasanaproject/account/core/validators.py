

from django.core.exceptions import ValidationError


def validate_user_phone_no(value):

    if value:
        if value.startswith('+') and value.count('+') == 1:
            temp_str = value[1:]
        else:
            temp_str = value
        try:
            int(temp_str)
        except ValueError:
            raise ValidationError('Phone number is invalid.')
        else:
            return value

    raise ValidationError('Phone number is invalid.')
