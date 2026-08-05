"""Конфигурация приложения сервиса YaCut."""

import os


class Config(object):
    """Класс конфигурации Flask-приложения.

    Значения берутся из переменных окружения:
        ``SQLALCHEMY_DATABASE_URI`` — URI подключения к базе данных;
        ``SECRET_KEY`` — секретный ключ Flask;
        ``DISK_TOKEN`` — токен для доступа к API Яндекс Диска.
    """

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
