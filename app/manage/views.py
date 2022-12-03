from flask import render_template
from . import manage
from ..models import Permission, Role, User, Post
from ..decorators import permission_required


@manage.route('/')
@permission_required(Permission.ADMIN)
def index():
    post_and_comment_s = []
    for post in Post.query:
        user = User.query.filter_by(id=post.author_id)[0]
        for comment in post.comments:
            post_and_comment_s.append({'post': post, 'comment': comment, 'user': user})
    post_and_comment_s.sort(key=lambda x: x['comment'].timestamp, reverse=True)

    return render_template('manage/index.html',
                           post_and_comment_s=post_and_comment_s)
