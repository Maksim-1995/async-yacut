from flask_wtf import FlaskForm
from wtforms import MultipleFileField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class URLMapForm(FlaskForm):
    """Форма для главной страницы: сокращение длинных ссылок."""

    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Введите корректный URL')
        ]
    )

    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=16, message='Не более 16 символов'),
            Regexp(
                r'^[a-zA-Z0-9]+$',
                message='Указано недопустимое имя для короткой ссылки'
            )
        ]
    )

    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    """Форма для страницы загрузки файлов на Яндекс Диск."""

    files = MultipleFileField(
        'Загрузите файлы',
        validators=[DataRequired(message='Обязательное поле')]
    )

    submit = SubmitField('Загрузить')
