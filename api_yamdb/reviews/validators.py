import datetime
import re

from django.core.exceptions import ValidationError


def check_year(value):
    """Проверка соответствует ли год возможному"""
    current_year = datetime.date.today().year
    if value > current_year:
        raise ValidationError(
            f'Введеный год {value} не может быть позже'
            f'текущего {current_year} года. '
        )
    return value


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Имя me недоступно. Выберите другое.'
        )
    if re.search(r'^[\w.@+-]+\Z', value) is None:
        unmatch_symbols = ' '.join(set(
            symbol for symbol in value if not re.match(r'^[\w.@+-]+\Z', symbol)
        ))
        raise ValidationError(
            f'Данное имя недоступно.'
            f' Недопустимые символы: {unmatch_symbols}'
        )
    return value
