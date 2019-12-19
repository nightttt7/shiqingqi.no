from flask import render_template, redirect, url_for
from flask_login import current_user
from . import Blog
from .forms import PostForm
from .. import db
from ..models import Permission, Role, User, Post
from ..decorators import permission_required


@Blog.route('/post', methods=['GET', 'POST'])
@permission_required(Permission.BLOG)
def post():
    form = PostForm()
    if current_user.can(Permission.BLOG) and form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('Blog/post.html',  form=form)
