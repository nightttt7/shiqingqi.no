from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Blog", validators=[DataRequired()],
                         render_kw={"rows": "15"})
    submit = SubmitField('Post')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
