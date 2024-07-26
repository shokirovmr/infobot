# apps/infobot/utils.py
import json

from django.utils.functional import Promise


def _normalize(value):
    if isinstance(value, Promise):
        return str(value)
    return value


def dumps(data):
    normalized_data = _normalize(data)
    return json.dumps(normalized_data, ensure_ascii=False)
