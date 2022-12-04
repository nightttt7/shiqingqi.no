from flask import render_template, redirect, url_for, request, abort
from flask_login import current_user
from . import Blog
from .forms import PostForm, DeleteForm, CommentForm
from .. import db
from ..models import Permission, Role, User, Post, Comment
from ..decorators import permission_required


@Blog.route('/post', methods=['GET', 'POST'])
@permission_required(Permission.BLOG)
def post():
    form = PostForm()
    if current_user.can(Permission.BLOG) and form.validate_on_submit():
        post = Post(title=form.title.data,
                    tag=form.tag.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('Blog/post.html', form=form)


@Blog.route('/<int:id>', methods=['GET', 'POST'])
def read(id):
    post = Post.query.get_or_404(id)
    form_c = CommentForm()
    if form_c.validate_on_submit():
        is_user = False
        if current_user.is_authenticated:
            if form_c.name.data == current_user.username:
                is_user = True
            # indentation changed
            comment = Comment(name=form_c.name.data, body=form_c.body.data,
                              is_user=is_user, post=post)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('Blog.read', id=post.id, page=-1))
        else:
            abort(403)
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // 8 + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=8, error_out=False)
    comments = pagination.items
    if current_user.is_authenticated:
        form_c.name.data = current_user.username
    else:
        form_c.name.data = 'anonymous'
    return render_template('Blog/read.html',
                           current_user=current_user,
                           post=post,
                           form_c=form_c,
                           comments=comments,
                           pagination=pagination)


@Blog.route('/edit/<int:id>', methods=['GET', 'POST'])
@permission_required(Permission.BLOG)
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.tag = form.tag.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('Blog.read', id=post.id))
    form.title.data = post.title
    form.tag.data = post.tag
    form.body.data = post.body
    return render_template('Blog/edit.html', form=form)


@Blog.route('/delete/<int:id>', methods=['GET', 'POST'])
@permission_required(Permission.BLOG)
def delete(id):
    post = Post.query.get_or_404(id)
    if (not current_user.is_administrator()) and (current_user != post.author):
        abort(403)
    form_d = DeleteForm()
    if form_d.validate_on_submit():
        db.session.delete(post)
        for comment in Comment.query.filter_by(post=post):
            db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('main.index', id=post.id))
    return render_template('Blog/delete.html', form_d=form_d, post=post)


@Blog.route('<int:id>/deletecomment/<int:id_c>')
@permission_required(Permission.BLOG)
def deletecomment(id, id_c):
    post = Post.query.get_or_404(id)
    if (not current_user.is_administrator()) and (current_user != post.author):
        abort(403)
    comment = Comment.query.get_or_404(id_c)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('Blog.read', id=id))
