from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from settings import Config

# Загрузить переменные окружения из файла .env.
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Создать таблицы в базе данных, если они ещё не существуют.
with app.app_context():
    db.create_all()

from . import api_views, short_id, error_handlers, views
