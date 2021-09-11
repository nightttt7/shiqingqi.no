from flask import render_template
from . import timeline


@timeline.route('/qs')
def qs():
    return render_template('timeline/qs.html')


@timeline.route('/lz')
def lz():
    return render_template('timeline/lz.html')
