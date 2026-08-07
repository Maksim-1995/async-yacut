"""Модель сервиса YaCut."""

from datetime import datetime

from yacut import db

# Максимальная длина короткого идентификатора.
SHORT_ID_MAX_LENGTH = 16


class URLMap(db.Model):
    """Модель соответствия между оригинальной и короткой ссылкой."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(SHORT_ID_MAX_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @classmethod
    def get(cls, short):
        return cls.query.filter_by(short=short).first()

    @classmethod
    def create(cls, original, short):
        instance = cls(
            original=original,
            short=short
        )
        db.session.add(instance)
        db.session.commit()
        return instance
