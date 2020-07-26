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


class AddTimeLogForm(FlaskForm):
    project_added = StringField('Project:', validators=[DataRequired()])
    task_added = StringField('Task', validators=[DataRequired()])
    time_start_added = StringField('Start', validators=[DataRequired()])
    time_end_added = StringField('End', validators=[DataRequired()])
    submit_added = SubmitField('Add')
