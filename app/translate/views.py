from flask import render_template
from . import translate
from ..models import URL


@translate.route('/')
def index():
    return render_template('translate/index.html')
