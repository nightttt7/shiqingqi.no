from flask import render_template
from . import translate


@translate.route('/')
def index():
    return render_template('translate/index.html')
