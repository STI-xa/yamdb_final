import random

from django.conf import settings


def generate_code():
    return ''.join(random.sample(
        settings.CODE_GEN_SYMBOLS, settings.CODE_LEN
    ))
