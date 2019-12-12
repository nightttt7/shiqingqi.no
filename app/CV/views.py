from flask import render_template

@CV.route('/CV')
def CVindex():
    return render_template('CV/index.html')

from . import CV