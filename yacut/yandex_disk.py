"""Асинхронное взаимодействие с API Яндекс Диска."""

import asyncio
import urllib.parse

import aiohttp

# Хост API Яндекс Диска.
API_HOST = 'https://cloud-api.yandex.net/'

# Версия API Яндекс Диска.
API_VERSION = 'v1'

# Эндпоинт для получения URL загрузки файла на Диск.
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'

# Эндпоинт для получения ссылки на скачивание файла с Диска.
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def _upload_single_file(session, file_storage, auth_headers):
    """Загружает один файл на Яндекс Диск.

    Выполняет три запроса к API Диска:
    1. GET-запрос для получения URL загрузки файла.
    2. PUT-запрос для загрузки файла по полученному URL.
    3. GET-запрос для получения ссылки на скачивание файла.

    Аргументы:
        session: Экземпляр ``aiohttp.ClientSession``.
        file_storage: Объект загружаемого файла (``FileStorage``).
        auth_headers: Словарь с заголовком авторизации.

    Возвращает кортеж ``(имя файла, ссылка на скачивание)``.
    """
    filename = file_storage.filename
    path = 'app:/{}'.format(filename)

    params = {'path': path, 'overwrite': 'True'}
    async with session.get(
        REQUEST_UPLOAD_URL, headers=auth_headers, params=params
    ) as response:
        upload_link = (await response.json())['href']

    file_data = file_storage.read()
    async with session.put(upload_link, data=file_data) as response:
        location = response.headers.get('Location', '')

    location = urllib.parse.unquote(location)
    file_path = location.replace('/disk', '')

    async with session.get(
        DOWNLOAD_LINK_URL, headers=auth_headers, params={'path': file_path}
    ) as response:
        download_link = (await response.json())['href']

    return filename, download_link


async def upload_files_to_disk(file_storages, token):
    """Асинхронно загружает несколько файлов на Яндекс Диск.

    Аргументы:
        file_storages: Итерируемый объект с загружаемыми файлами.
        token: Токен авторизации Яндекс Диска.

    Возвращает список кортежей ``(имя файла, ссылка на скачивание)``.
    """
    auth_headers = {'Authorization': f'OAuth {token}'}
    async with aiohttp.ClientSession() as session:
        tasks = (
            _upload_single_file(session, file_storage, auth_headers)
            for file_storage in file_storages
        )
        return await asyncio.gather(*tasks)
