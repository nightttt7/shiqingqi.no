from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddTodoForm(FlaskForm):
    item = StringField('Add a todo:', validators=[DataRequired()])
    submit = SubmitField('Add')
