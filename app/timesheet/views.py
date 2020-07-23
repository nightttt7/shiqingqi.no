from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from . import timesheet
from .forms import AddTodoForm
from .. import db
from ..models import Permission, Todo
from ..decorators import permission_required
from datetime import datetime


@timesheet.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form_add = AddTodoForm()
    if current_user.can(Permission.KEEP) and form_add.validate_on_submit():
        todo = Todo(item=form_add.item.data,
                    author=current_user._get_current_object())
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('timesheet.index'))
    todos = (current_user.todos.filter_by(statu=False).
             order_by(Todo.timestamp_start).all())
    archives = (current_user.todos.filter_by(statu=True).
                order_by(Todo.timestamp_start).all())
    return render_template('timesheet/index.html', form=form_add, todos=todos,
                           archives=archives)


@timesheet.route('/do/<int:id>')
@login_required
def do(id):
    todo = Todo.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == todo.author):
        todo.statu = True
        todo.timestamp_end = datetime.utcnow()
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('timesheet.index'))


@timesheet.route('/undo/<int:id>')
@login_required
def undo(id):
    todo = Todo.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == todo.author):
        todo.statu = False
        todo.timestamp_start = datetime.utcnow()
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('timesheet.index'))


@timesheet.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == todo.author):
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('timesheet.index'))
