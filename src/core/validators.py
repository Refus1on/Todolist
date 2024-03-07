from django.core.exceptions import ValidationError


def validate_password_length(value):
    min_length = 8
    if len(value) < min_length:
        raise ValidationError(
            message=f'Пароль должен быть не меньше {min_length} символов.',
            code='Пароль слишком короткий.',
            params={'min_length': min_length}
        )
