from flask import render_template, url_for
from . import CV
from ..models import URL


@CV.route('/')
def index():
    CV_url = URL.query.filter_by(urlname='CV_url').first().url
    return render_template('CV/index.html', CV_url=CV_url)
