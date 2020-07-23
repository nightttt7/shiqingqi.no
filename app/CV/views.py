from flask import render_template
from . import CV


@CV.route('/')
def index():
    return render_template('CV/index.html')


@CV.route('/timeline')
def timeline():
    return render_template('CV/timeline.html')
