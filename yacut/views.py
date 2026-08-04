import asyncio

from flask import (
    abort, current_app, flash, redirect, render_template, request
)

from . import app, db
from .forms import FileForm, URLMapForm
from .models import URLMap
from .utils import get_unique_short_id
from .yandex_disk import upload_files_to_disk

# Идентификаторы, которые нельзя использовать как короткую ссылку,
# так как они заняты маршрутами приложения.
RESERVED_SHORT_IDS = ('files',)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница: преобразование длинных ссылок в короткие."""
    form = URLMapForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id:
            # Если предложенный вариант уже занят или зарезервирован —
            # сообщаем пользователю и не создаём запись.
            if (
                custom_id in RESERVED_SHORT_IDS
                or URLMap.get(custom_id) is not None
            ):
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('add_urls.html', form=form)
        else:
            # Если вариант не предложен — генерируем автоматически.
            custom_id = get_unique_short_id()

        url_map = URLMap(original=original_link, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return render_template('add_urls.html', form=form, url_map=url_map)

    return render_template('add_urls.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    """Страница асинхронной загрузки файлов на Яндекс Диск."""
    form = FileForm()
    uploaded_files = []

    if form.validate_on_submit():
        files = request.files.getlist('files')
        token = current_app.config.get('DISK_TOKEN')

        # Асинхронно загружаем файлы на Яндекс Диск.
        results = asyncio.run(upload_files_to_disk(files, token))

        for filename, download_link in results:
            # Для каждого файла генерируем собственную короткую ссылку.
            short_id = get_unique_short_id()
            url_map = URLMap(original=download_link, short=short_id)
            db.session.add(url_map)
            db.session.commit()
            uploaded_files.append((filename, url_map.short))

    return render_template(
        'files.html', form=form, uploaded_files=uploaded_files
    )


@app.route('/<short_id>')
def redirect_view(short_id):
    """Переадресация на исходный адрес по короткой ссылке."""
    url_map = URLMap.get(short_id)
    if url_map is None:
        abort(404)
    return redirect(url_map.original)