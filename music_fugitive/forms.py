from flask_wtf import FlaskForm
from .last import artist_exists
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import ValidationError


def artist_validate(form, field):
    if not field.data:
        return
    if not artist_exists(field.data):
        raise ValidationError('Artist not found')


class artist_form(FlaskForm):
    style = {'class': 'form-control ask-input'}
    artist_1 = StringField('Artist', validators=[DataRequired(),
                           artist_validate], render_kw=style)
    artist_2 = StringField('Artist', validators=[artist_validate],
                           render_kw=style)
    artist_3 = StringField('Artist', validators=[artist_validate],
                           render_kw=style)
