import uuid

from django.conf import settings


def base36_uuid(length: int = settings.SHORTEN_HEX_LEN) -> str:
    return f'{uuid.uuid4().int:x}'[:length]
