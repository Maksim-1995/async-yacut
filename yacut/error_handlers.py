"""Обработчики ошибок для веб-интерфейса сервиса YaCut."""

from flask import render_template

from . import app, db


@app.errorhandler(404)
def page_not_found(error):
    """Обработчик ошибки 404 — страница не найдена."""

    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработчик внутренней ошибки сервера 500.

    Откатывает текущую транзакцию базы данных и возвращает
    шаблон страницы ошибки.
    """

    db.session.rollback()
    return render_template('500.html'), 500
