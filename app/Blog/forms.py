from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    body = TextAreaField('Blog', validators=[DataRequired()],
                         render_kw={'rows': '15'})
    submit = SubmitField('Post')


class DeleteForm(FlaskForm):
    submit = SubmitField('Confirm and delete')


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    body = TextAreaField('Comment', validators=[DataRequired()],
                         render_kw={'rows': '3'})
    submit = SubmitField('Comment')
