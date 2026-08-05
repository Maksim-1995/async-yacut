import asyncio
import urllib.parse

import aiohttp

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def _upload_single_file(session, file_storage, auth_headers):
    """Загружает один файл на Яндекс Диск и возвращает ссылку на скачивание."""
    filename = file_storage.filename
    path = 'app:/' + filename

    # 1. Запрашиваем URL для загрузки файла.
    params = {'path': path, 'overwrite': 'True'}
    async with session.get(
        REQUEST_UPLOAD_URL, headers=auth_headers, params=params
    ) as response:
        upload_link = (await response.json())['href']

    # 2. Загружаем файл PUT-запросом по полученному URL.
    file_data = file_storage.read()
    async with session.put(upload_link, data=file_data) as response:
        location = response.headers.get('Location', '')

    # Декодируем строку URL и убираем префикс /disk.
    location = urllib.parse.unquote(location)
    file_path = location.replace('/disk', '')

    # 3. Запрашиваем ссылку на скачивание файла.
    async with session.get(
        DOWNLOAD_LINK_URL, headers=auth_headers, params={'path': file_path}
    ) as response:
        download_link = (await response.json())['href']

    return filename, download_link


async def upload_files_to_disk(file_storages, token):
    """Асинхронно загружает несколько файлов на Яндекс Диск.

    Возвращает список кортежей (имя файла, ссылка на скачивание).
    """
    auth_headers = {'Authorization': f'OAuth {token}'}
    async with aiohttp.ClientSession() as session:
        tasks = [
            _upload_single_file(session, file_storage, auth_headers)
            for file_storage in file_storages
        ]
        return await asyncio.gather(*tasks)