from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# those attributes should have different names to avoid bugs
# attributes' name will be the id and name of element in html
class AddTodoForm(FlaskForm):
    todo_item = StringField('Add a todo', validators=[DataRequired()])
    submit_todo = SubmitField('Add')


class StartTimeLogForm(FlaskForm):
    project_start = StringField('Project', validators=[DataRequired()])
    task_start = StringField('Task', validators=[DataRequired()])
    time_start_start = StringField('Hidden element')
    submit_start = SubmitField('Start')


class AddTimeLogForm(FlaskForm):
    project_add = StringField('Project', validators=[DataRequired()])
    task_add = StringField('Task', validators=[DataRequired()])
    time_start_add = StringField('Start', validators=[DataRequired()])
    time_end_add = StringField('End', validators=[DataRequired()])
    utc_offset = StringField('Hidden element')
    submit_add = SubmitField('Add')
