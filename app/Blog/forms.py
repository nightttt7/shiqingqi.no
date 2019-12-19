from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Blog", validators=[DataRequired()],
                         render_kw={"rows": "15"})
    submit = SubmitField('Post')
