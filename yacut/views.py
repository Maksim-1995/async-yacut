"""View-функции веб-интерфейса сервиса YaCut."""

from http import HTTPStatus

from flask import (
    abort, current_app, flash, redirect, render_template
)

from . import app
from .forms import FileForm, URLMapForm
from .models import URLMap
from .short_id import get_unique_short_id, is_short_id_available
from .yandex_disk import upload_files_to_disk


@app.route('/', methods=('GET', 'POST'))
def index_view():
    """Главная страница: преобразование длинных ссылок в короткие.

    Обрабатывает форму с оригинальной ссылкой и необязательным
    пользовательским вариантом короткой ссылки. При успешном создании
    отображает результат на странице.
    """
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('add_urls.html', form=form)

    original_link = form.original_link.data
    custom_id = form.custom_id.data

    if custom_id:
        if not is_short_id_available(custom_id):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('add_urls.html', form=form)
    else:
        custom_id = get_unique_short_id()

    url_map = URLMap.create(original=original_link, short=custom_id)
    return render_template('add_urls.html', form=form, url_map=url_map)


@app.route('/files', methods=('GET', 'POST'))
async def files_view():
    """Страница асинхронной загрузки файлов на Яндекс Диск.

    Обрабатывает форму с несколькими файлами, асинхронно загружает их
    на Яндекс Диск и для каждого файла создаёт короткую ссылку.
    Результаты отображаются в таблице под формой.
    """
    form = FileForm()
    uploaded_files = []

    if form.validate_on_submit():
        files = form.files.data
        token = current_app.config.get('DISK_TOKEN')

        results = await upload_files_to_disk(files, token)

        for filename, download_link in results:
            short_id = get_unique_short_id()
            url_map = URLMap.create(
                original=download_link, short=short_id
            )
            uploaded_files.append((filename, url_map.short))

    return render_template(
        'files.html', form=form, uploaded_files=uploaded_files
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    """Переадресация на исходный адрес по короткой ссылке.

    Если короткий идентификатор не найден в базе данных,
    возвращается ошибка 404.
    """
    url_map = URLMap.get(short_id)
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)