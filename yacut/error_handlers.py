"""Обработчики ошибок для веб-интерфейса сервиса YaCut."""

from http import HTTPStatus

from flask import render_template

from . import app, db


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Обработчик ошибки 404 — страница не найдена."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Обработчик внутренней ошибки сервера 500.

    Откатывает текущую транзакцию базы данных и возвращает
    шаблон страницы ошибки.
    """
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
