from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import Required
class chopForm(FlaskForm):
    money_int = StringField('$', validators=[Required(), NumberRange(min=1,max=100000000)])
    submit = SubmitField('submit')