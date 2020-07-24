from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from . import timesheet
from .forms import AddTodoForm, StartTimeLogForm
from .. import db
from ..models import Permission, Todo, TimeLog
from ..decorators import permission_required
from datetime import datetime


@timesheet.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form_add_todo = AddTodoForm()
    if current_user.can(Permission.KEEP) and form_add_todo.validate_on_submit():
        todo = Todo(item=form_add_todo.item.data,
                    author=current_user._get_current_object())
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('timesheet.index'))
    form_start_timelog = StartTimeLogForm()
    if current_user.can(Permission.KEEP) and form_start_timelog.validate_on_submit():
        timelog = TimeLog(project=form_start_timelog.project.data,
                          task=form_start_timelog.task.data,
                          statu_code=1,
                          author=current_user._get_current_object())
        db.session.add(timelog)
        current_user.time_statu = True
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('timesheet.index'))
    todos = (current_user.todos.filter_by(statu=False).
             order_by(Todo.timestamp_start).all())
    archives = (current_user.todos.filter_by(statu=True).
                order_by(Todo.timestamp_start).all())
    timelog_plan = (current_user.timelogs.filter_by(statu_code=0).all())
    timelog_current = (current_user.timelogs.filter_by(statu_code=1).first())
    timelog_finished = (current_user.timelogs.filter_by(statu_code=2).all())
    return render_template('timesheet/index.html',
                           form_add_todo=form_add_todo,
                           todos=todos, archives=archives,
                           form_start_timelog=form_start_timelog,
                           time_statu=current_user.time_statu,
                           # TODO:
                           timelog_plan=timelog_plan,
                           timelog_current=timelog_current,
                           timelog_finished=timelog_finished
                           )


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


@timesheet.route('/delete_todo/<int:id>')
@login_required
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == todo.author):
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('timesheet.index'))


@timesheet.route('/finish/<int:id>')
@login_required
def finish(id):
    timelog = TimeLog.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == timelog.author):
        timelog.statu_code = 2
        timelog.timestamp_end = datetime.utcnow()
        db.session.add(timelog)
        current_user.time_statu = False
        db.session.add(current_user)
        db.session.commit()
    return redirect(url_for('timesheet.index'))


@timesheet.route('/delete_timelog/<int:id>')
@login_required
def delete_timelog(id):
    timelog = TimeLog.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == timelog.author):
        db.session.delete(timelog)
        db.session.commit()
    return redirect(url_for('timesheet.index'))
