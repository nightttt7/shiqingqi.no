from flask import render_template
from flask_login import current_user
from . import account
from .. import db
from ..models import Permission, Role, User, Post, Comment


@account.route('/')
def index():
    post_and_comment_s = []
    for post in Post.query.filter_by(author_id=current_user.id):
        for comment in post.comments:
            post_and_comment_s.append({'post': post, 'comment': comment})
    return render_template('account/index.html',
                           post_and_comment_s=post_and_comment_s)
