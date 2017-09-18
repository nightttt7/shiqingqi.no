from flask import render_template
from . import chop


@chop.route('/')
def chopindex():
    return render_template('chop/index.html')