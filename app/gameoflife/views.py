from flask import render_template
from . import gameoflife


@gameoflife.route('/')
def index():
    return render_template('gameoflife/index.html')
