from flask import render_template, request
from . import main
from flask_login import current_user
from ..models import Post


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=8, error_out=False)
    posts = pagination.items
    return render_template('index_main.html', posts=posts, pagination=pagination)


@main.route('/tag/<string:tag>', methods=['GET', 'POST'])
def sametag(tag):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(tag=tag).order_by(Post.timestamp.desc()).paginate(
        page, per_page=8, error_out=False)
    posts = pagination.items
    tag_ = Post.query.filter_by(tag=tag).first_or_404().tag
    return render_template('index_sametag.html', posts=posts, pagination=pagination, tag_=tag_)


@main.route('/author/<int:author_id>', methods=['GET', 'POST'])
def sameauthor(author_id):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(author_id=author_id).order_by(Post.timestamp.desc()).paginate(
        page, per_page=8, error_out=False)
    posts = pagination.items
    author = Post.query.filter_by(author_id=author_id).first_or_404().author
    return render_template('index_sameauthor.html', posts=posts, pagination=pagination, author=author)
