from flask import render_template
from . import Blog


@Blog.route('/Blog')
def Blogindex():
    return render_template('Blog/index.html')