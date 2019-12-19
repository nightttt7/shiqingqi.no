from flask import render_template, request
from . import main
from flask_login import current_user
from ..models import Post


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=5, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)
