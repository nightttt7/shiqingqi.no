from flask import render_template
from . import main
from flask_login import current_user
from ..models import Permission

@main.route('/')
def index():
    if current_user.is_administrator():
        return render_template('indexforadmin.html')
    elif current_user.can(Permission.BLOG):
        return render_template('indexforblog.html')
    else:
        return render_template('index.html')
