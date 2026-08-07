"""Генерация и проверка коротких идентификаторов для сервиса YaCut."""

import random
import re
import string

from .models import SHORT_ID_MAX_LENGTH, URLMap

# Допустимые символы для короткой ссылки.
ALPHABET = string.ascii_letters + string.digits

# Длина автоматически генерируемого short_id.
SHORT_ID_LENGTH = 6

# Допустимый формат короткого идентификатора:
# латинские буквы (верхнего и нижнего регистра) и цифры.
SHORT_ID_REGEX = r'^[a-zA-Z0-9]+$'

# Скомпилированный шаблон для проверки короткого идентификатора
# (используется в API).
SHORT_ID_PATTERN = re.compile(
    r'^[a-zA-Z0-9]{1,%d}$' % SHORT_ID_MAX_LENGTH
)

# Идентификаторы, которые нельзя использовать как короткую ссылку,
# так как они заняты маршрутами приложения.
RESERVED_SHORT_IDS = ('files',)


def get_unique_short_id():
    """Генерирует уникальный короткий идентификатор.

    Возвращает строку из ``SHORT_ID_LENGTH`` случайных символов.
    Если сгенерированный идентификатор уже существует в базе данных,
    генерация повторяется.
    """
    while True:
        short_id = ''.join(
            random.choices(ALPHABET, k=SHORT_ID_LENGTH)
        )
        if URLMap.get(short_id) is None:
            return short_id


def is_short_id_available(short_id):
    """Проверяет, доступен ли короткий идентификатор для использования.

    Идентификатор считается недоступным, если он зарезервирован
    (совпадает с маршрутом приложения) или уже существует в базе данных.
    """
    return (
        short_id not in RESERVED_SHORT_IDS
        and URLMap.get(short_id) is None
    )
