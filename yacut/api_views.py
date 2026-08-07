"""API для работы с сервисом YaCut."""

from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .models import URLMap
from .short_id import get_unique_short_id, SHORT_ID_PATTERN


@app.route('/api/id/', methods=('POST',))
def create_short_link():
    """Создание новой короткой ссылки."""
    body = request.get_json(silent=True)

    if not body:
        return (
            jsonify({'message': 'Отсутствует тело запроса'}),
            HTTPStatus.BAD_REQUEST
        )

    original = body.get('url')
    custom_id = body.get('custom_id')

    if not original:
        return (
            jsonify({'message': '"url" является обязательным полем!'}),
            HTTPStatus.BAD_REQUEST
        )

    if custom_id:
        # Проверка допустимого формата пользовательского идентификатора.
        if not SHORT_ID_PATTERN.match(custom_id):
            return (
                jsonify(
                    {'message': 'Указано недопустимое имя для короткой ссылки'}
                ),
                HTTPStatus.BAD_REQUEST
            )
        # Проверка, не занят ли предложенный вариант.
        if URLMap.get(custom_id):
            return (
                jsonify(
                    {'message': 'Предложенный вариант короткой ссылки уже '
                                'существует.'}
                ),
                HTTPStatus.BAD_REQUEST
            )
        short_id = custom_id
    else:
        # Автоматическая генерация уникального идентификатора.
        short_id = get_unique_short_id()

    url_map = URLMap.create(original=original, short=short_id)

    return (
        jsonify({
            'url': url_map.original,
            'short_link': url_for(
                'redirect_view', short_id=url_map.short, _external=True
            )
        }),
        HTTPStatus.CREATED
    )


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_link(short_id):
    """Получение оригинальной ссылки по короткому идентификатору."""
    url_map = URLMap.get(short_id)
    if url_map is None:
        return (
            jsonify({'message': 'Указанный id не найден'}),
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original})
