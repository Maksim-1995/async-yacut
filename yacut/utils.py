import random
import string

from .models import URLMap

# Допустимые символы для короткой ссылки
ALPHABET = string.ascii_letters + string.digits

# Длина автоматически генерируемого short_id
SHORT_ID_LENGTH = 6


def get_unique_short_id():
    """Генерирует уникальный короткий идентификатор."""

    while True:
        short_id = ''.join(
            random.choices(ALPHABET, k=SHORT_ID_LENGTH)
        )

        if URLMap.get(short_id) is None:
            return short_id