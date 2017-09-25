from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import Required


class DictsForm(FlaskForm):
    englishword = StringField('English', validators=[Required()])
    dictname = RadioField('dictname', choices=[('https://www.vocabulary.com/dictionary/', 'voca'), \
                                               ('2', 'youdao'), \
                                               ('https://dict.eudic.net/dicts/en/', 'eudic'), \
                                               ('4', 'oxford'), \
                                               ('http://fanyi.baidu.com/?aldtype=16047#en/zh/', 'baidu'), \
                                               ('https://translate.google.cn/#en/zh-CN/', 'google')],\
                          default='2'
                          )
    submit = SubmitField('translate')
