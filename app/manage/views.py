from flask import render_template, request, redirect, url_for
from . import manage
from .. import db
from ..models import Permission, User, Post
from ..decorators import permission_required


@manage.route('/')
@permission_required(Permission.ADMIN)
def index():
    return render_template('manage/index.html')


@manage.route('/comments')
@permission_required(Permission.ADMIN)
def comments():
    post_and_comment_s = []
    for post in Post.query:
        user = User.query.filter_by(id=post.author_id)[0]
        for comment in post.comments:
            post_and_comment_s.append({'post': post, 'comment': comment, 'user': user})
    post_and_comment_s.sort(key=lambda x: x['comment'].timestamp, reverse=True)
    return render_template('manage/comments.html',
                           post_and_comment_s=post_and_comment_s
                           )


@manage.route('/users')
@permission_required(Permission.ADMIN)
def users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id.desc()).paginate(page, per_page=8, error_out=False)
    users = pagination.items
    return render_template('manage/users.html',
                           users=users
                           )


@manage.route('/set_permision/<int:id>/<string:role_name>')
@permission_required(Permission.ADMIN)
def set_permision(id, role_name):
    user = User.query.get_or_404(id)
    user.set_permision(role_name)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('manage.users'))
