from flask import render_template, url_for
from . import CV
from ..models import URL


@CV.route('/')
def index():
    return render_template('CV/index.html')


@CV.route('/timeline')
def timeline():
    return render_template('CV/timeline.html')
