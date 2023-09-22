from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if '@' not in field.data:
            raise ValidationError(f"Please include an '@' in the email address. '{field.data}' is missing an '@'.")
        elif not field.data.endswith('@mail.utoronto.ca'):
            raise ValidationError('Please use a valid UofT email address in the format: username@mail.utoronto.ca.')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.is_submitted():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
            session['name'] = form.name.data
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        if form.validate():
            session['name'] = form.name.data
            session['email'] = form.email.data
            return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))
