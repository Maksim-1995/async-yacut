from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap

@app.route('/')
def index_view():
    quantity = URLMap.query.count()
    if not quantity:
        abort(500)
    offset_value = randrange(quantity)
    url_map = URLMap.query.offset(offset_value).first()
    return render_template('url_map.html', url_map=url_map)
    

@app.route('/add', methods=['GET', 'POST'])
def add_url_map_view():
    form = URLMapForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data, 
            text=text, 
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)

@app.route('/opinions/<int:id>')
def opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion) 