from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddTodoForm(FlaskForm):
    item = StringField('Add a todo:', validators=[DataRequired()])
    submit = SubmitField('Add')


class StartTimeLogForm(FlaskForm):
    project = StringField('Project:', validators=[DataRequired()])
    task = StringField('Task', validators=[DataRequired()])
    submit = SubmitField('Start')


# TODO:
class EditUnfinishedTimeLogForm(FlaskForm):
    item = StringField('Add a todo:', validators=[DataRequired()])
    submit = SubmitField('Edit')


# TODO:
class AddTimeLogForm(FlaskForm):
    project = StringField('Add a todo:', validators=[DataRequired()])
    task = SubmitField('Add')


# TODO:
class EditFinishedTimeLogForm(FlaskForm):
    item = StringField('Add a todo:', validators=[DataRequired()])
    submit = SubmitField('Edit')
