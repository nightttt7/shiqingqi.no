from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from . import timesheet
from .forms import (AddTodoForm, StartTimeLogForm,
                    AddTimeLogForm)
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
    # FIXME: the timestamp_start is not the current time, but of last load
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
    # FIXME: the input time will be parsed as UTC time but not local time
    form_add_timelog = AddTimeLogForm()
    if current_user.can(Permission.KEEP) and form_add_timelog.validate_on_submit():
        timestamp_start = datetime.strptime(
            form_add_timelog.time_start_added.data, '%Y-%m-%d %H:%M')
        timestamp_end = datetime.strptime(
            form_add_timelog.time_end_added.data, '%Y-%m-%d %H:%M')
        if (datetime.utcnow() < timestamp_end):
            statu_code = 0
        else:
            statu_code = 2
        timelog = TimeLog(project=form_add_timelog.project_added.data,
                          task=form_add_timelog.task_added.data,
                          timestamp_start=timestamp_start,
                          timestamp_end=timestamp_end,
                          time_delta_seconds=(timestamp_end-timestamp_start).seconds,
                          statu_code=statu_code,
                          author=current_user._get_current_object())
        db.session.add(timelog)
        db.session.commit()
        current_user.time_statu = False
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('timesheet.index'))
    form_add_timelog.time_start_added.data = (
        datetime.utcnow().strftime('%Y-%m-%d 14:00'))
    form_add_timelog.time_end_added.data = (
        datetime.utcnow().strftime('%Y-%m-%d 18:00'))
    # passing variables
    todos = (current_user.todos.filter_by(statu=False).
             order_by(Todo.timestamp_start.desc()).all())
    archives = (current_user.todos.filter_by(statu=True).
                order_by(Todo.timestamp_start.desc()).all())
    timelog_plan = (current_user.timelogs.filter_by(statu_code=0).
                    order_by(TimeLog.timestamp_start.desc()).limit(8).all())
    timelog_current = (current_user.timelogs.filter_by(statu_code=1).
                       first())
    timelog_finished = (current_user.timelogs.filter_by(statu_code=2).
                        order_by(TimeLog.timestamp_start.desc()).limit(8).
                        all())
    # for testing
    # current_user.time_statu = True
    return render_template('timesheet/index.html',
                           form_add_todo=form_add_todo,
                           todos=todos, archives=archives,
                           form_start_timelog=form_start_timelog,
                           form_add_timelog=form_add_timelog,
                           time_statu=current_user.time_statu,
                           timelog_plan=timelog_plan,
                           timelog_current=timelog_current,
                           timelog_finished=timelog_finished,
                           datetime=datetime
                           )


@timesheet.route('/do/<int:id>')
@login_required
def do(id):
    todo = Todo.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == todo.author):
        todo.statu = True
        todo.timestamp_end = datetime.utcnow()
        todo.time_delta_seconds = (
            (todo.timestamp_end-todo.timestamp_start).seconds)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('timesheet.index'))


@timesheet.route('/undo/<int:id>')
@login_required
def undo(id):
    todo = Todo.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == todo.author):
        todo.statu = False
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
        timelog.time_delta_seconds = (
            (timelog.timestamp_end-timelog.timestamp_start).seconds)
        db.session.add(timelog)
        current_user.time_statu = False
        db.session.add(current_user)
        db.session.commit()
    return redirect(url_for('timesheet.index'))


@timesheet.route('/finish_plan/<int:id>')
@login_required
def finish_plan(id):
    timelog = TimeLog.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == timelog.author):
        timelog.statu_code = 2
        db.session.add(timelog)
        db.session.commit()
    return redirect(url_for('timesheet.index'))


@timesheet.route('/start_finished/<int:id>')
@login_required
def start_finished(id):
    timelog_old = TimeLog.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == timelog_old.author) and (not current_user.time_statu):
        timelog = TimeLog(project=timelog_old.project,
                          task=timelog_old.task,
                          statu_code=1,
                          author=current_user._get_current_object())
        db.session.add(timelog)
        current_user.time_statu = True
        db.session.add(current_user)
        db.session.commit()
    return redirect(url_for('timesheet.index'))


@timesheet.route('/start_planed/<int:id>')
@login_required
def start_planed(id):
    timelog = TimeLog.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == timelog.author) and (not current_user.time_statu):
        timelog.statu_code = 1
        timelog.timestamp_start = datetime.utcnow()
        db.session.add(timelog)
        current_user.time_statu = True
        db.session.add(current_user)
        db.session.commit()
    return redirect(url_for('timesheet.index'))


@timesheet.route('/start_planed_keep/<int:id>')
@login_required
def start_planed_keep(id):
    timelog_old = TimeLog.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == timelog_old.author) and (not current_user.time_statu):
        timelog = TimeLog(project=timelog_old.project,
                          task=timelog_old.task,
                          statu_code=1,
                          timestamp_end=timelog_old.timestamp_end,
                          author=current_user._get_current_object())
        db.session.add(timelog)
        current_user.time_statu = True
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
