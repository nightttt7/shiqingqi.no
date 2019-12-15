from flask import render_template
from . import Blog


@Blog.route('/')
def index():
    return render_template('Blog/index.html')