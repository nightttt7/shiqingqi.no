from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required
from . import timesheet
from .forms import (AddTodoForm, StartTimeLogForm,
                    AddTimeLogForm, StatTimeLogFormBase)
from wtforms import SelectMultipleField
from .. import db
from sqlalchemy.sql import func
from ..models import Permission, Todo, TimeLog
from ..decorators import permission_required
from datetime import datetime, timedelta


@timesheet.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form_add_todo = AddTodoForm()
    if current_user.can(Permission.KEEP) and form_add_todo.validate_on_submit():
        todo = Todo(item=form_add_todo.todo_item.data,
                    author=current_user._get_current_object())
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('timesheet.index'))
    form_start_timelog = StartTimeLogForm()
    if current_user.can(Permission.KEEP) and form_start_timelog.validate_on_submit():
        time_start_start = (
            datetime.strptime(form_start_timelog.time_start_start.data,
                              '%Y-%m-%d %H:%M:%S'))
        timelog = TimeLog(project=form_start_timelog.project_start.data,
                          task=form_start_timelog.task_start.data,
                          timestamp_start=time_start_start,
                          statu_code=1,
                          author=current_user._get_current_object())
        db.session.add(timelog)
        current_user.time_statu = True
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('timesheet.index'))
    form_add_timelog = AddTimeLogForm()
    if current_user.can(Permission.KEEP) and form_add_timelog.validate_on_submit():
        utc_offset = int(form_add_timelog.utc_offset.data)
        timestamp_start = (datetime.strptime(
            form_add_timelog.time_start_add.data, '%Y-%m-%d %H:%M') -
            timedelta(minutes=utc_offset))
        timestamp_end = (datetime.strptime(
            form_add_timelog.time_end_add.data, '%Y-%m-%d %H:%M') -
            timedelta(minutes=utc_offset))
        if (datetime.utcnow() < timestamp_end):
            statu_code = 0
        else:
            statu_code = 2
        timelog = TimeLog(project=form_add_timelog.project_add.data,
                          task=form_add_timelog.task_add.data,
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
    todos = (current_user.todos.filter_by(statu=False).
             order_by(Todo.timestamp_start.desc()).all())
    archives = (current_user.todos.filter_by(statu=True).
                order_by(Todo.timestamp_start.desc()).limit(8).all())
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
                           todos=todos,
                           archives=archives,
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
    target = request.args.get('next')
    if target is None or not target.startswith('/'):
        target = request.referrer
        if target is None:
            target = url_for('timesheet.index')
    return redirect(target)


@timesheet.route('/undo/<int:id>')
@login_required
def undo(id):
    todo = Todo.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == todo.author):
        todo.statu = False
        db.session.add(todo)
        db.session.commit()
    target = request.args.get('next')
    if target is None or not target.startswith('/'):
        target = request.referrer
        if target is None:
            target = url_for('timesheet.index')
    return redirect(target)


@timesheet.route('/delete_todo/<int:id>')
@login_required
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == todo.author):
        db.session.delete(todo)
        db.session.commit()
    target = request.args.get('next')
    if target is None or not target.startswith('/'):
        target = request.referrer
        if target is None:
            target = url_for('timesheet.index')
    return redirect(target)


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
    target = request.args.get('next')
    if target is None or not target.startswith('/'):
        target = request.referrer
        if target is None:
            target = url_for('timesheet.index')
    return redirect(target)


@timesheet.route('/finish_plan/<int:id>')
@login_required
def finish_plan(id):
    timelog = TimeLog.query.get_or_404(id)
    if current_user.can(Permission.KEEP) and (current_user == timelog.author):
        timelog.statu_code = 2
        db.session.add(timelog)
        db.session.commit()
    target = request.args.get('next')
    if target is None or not target.startswith('/'):
        target = request.referrer
        if target is None:
            target = url_for('timesheet.index')
    return redirect(target)


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
    target = request.args.get('next')
    if target is None or not target.startswith('/'):
        target = request.referrer
        if target is None:
            target = url_for('timesheet.index')
    return redirect(target)


@timesheet.route('/archives')
@login_required
def archives():
    archives = (current_user.todos.filter_by(statu=True).
                order_by(Todo.timestamp_start.desc()).all())
    return render_template('timesheet/archives.html',
                           archives=archives
                           )


@timesheet.route('/timelog_finished', methods=['GET'])
@login_required
def timelog_finished():
    if request.args.get('task'):
        timelog_finished = (
            current_user.timelogs.filter_by(
                statu_code=2,
                project=request.args.get('project'),
                task=request.args.get('task')).
            order_by(TimeLog.timestamp_start.desc()).all())
        highlight = 'task'
        duration_sum = (
            TimeLog.query.
            with_entities(func.sum(TimeLog.time_delta_seconds).label("sum")).
            filter_by(statu_code=2,
                      author_id=current_user.id,
                      project=request.args.get('project'),
                      task=request.args.get('task')
                      ).first()).sum
    elif request.args.get('project'):
        timelog_finished = (
            current_user.timelogs.filter_by(
                statu_code=2,
                project=request.args.get('project')).
            order_by(TimeLog.timestamp_start.desc()).all())
        highlight = 'project'
        duration_sum = (
            TimeLog.query.
            with_entities(func.sum(TimeLog.time_delta_seconds).label("sum")).
            filter_by(statu_code=2,
                      author_id=current_user.id,
                      project=request.args.get('project')
                      ).first()).sum
    elif request.args.get('date'):
        timelog_finished = (
            current_user.timelogs.filter(
                TimeLog.timestamp_start >=
                datetime.strptime(request.args.get('date'), '%Y-%m-%d'),
                TimeLog.timestamp_start <
                (datetime.strptime(request.args.get('date'), '%Y-%m-%d') +
                 timedelta(days=1)),
                TimeLog.statu_code == 2).
            order_by(TimeLog.timestamp_start.desc()).all())
        highlight = 'date'
        duration_sum = (
            TimeLog.query.
            with_entities(func.sum(TimeLog.time_delta_seconds).label("sum")).
            filter(TimeLog.statu_code == 2,
                   TimeLog.author_id == current_user.id,
                   TimeLog.timestamp_start >=
                   datetime.strptime(request.args.get('date'), '%Y-%m-%d'),
                   TimeLog.timestamp_start <
                   (datetime.strptime(request.args.get('date'), '%Y-%m-%d') +
                    timedelta(days=1))
                   ).first()).sum
    else:
        timelog_finished = (current_user.timelogs.filter_by(statu_code=2).
                            order_by(TimeLog.timestamp_start.desc()).
                            all())
        highlight = 'all'
        duration_sum = (
            # why SQLAlchemy so complex?
            TimeLog.query.
            with_entities(func.sum(TimeLog.time_delta_seconds).label("sum")).
            filter_by(statu_code=2, author_id=current_user.id).first()).sum
    return render_template('timesheet/timelog_finished.html',
                           timelog_finished=timelog_finished,
                           highlight=highlight,
                           duration_sum=duration_sum
                           )


@timesheet.route('/timelog_stat', methods=['GET', 'POST'])
@login_required
def timelog_stat():
    project_list = set([log.project for log in (
        current_user.timelogs.filter_by(statu_code=2).
        order_by(TimeLog.timestamp_start.desc()).all())])
    # add 1 for choice "all"
    num_project = len(project_list) + 1
    # to avoid the word to be used as the project name
    choices = [('longrandomwordiueldkfifj', 'all')]
    for project in project_list:
        choices.append((project, project))

    class StatTimeLogForm(StatTimeLogFormBase):
        project_stat = SelectMultipleField('Project', choices=choices)

    form_stat_timelog = StatTimeLogForm()
    if current_user.can(Permission.KEEP) and form_stat_timelog.validate_on_submit():
        utc_offset = int(form_stat_timelog.utc_offset.data)
        stat_start = (datetime.strptime(
            form_stat_timelog.stat_start.data, '%Y-%m-%d') -
            timedelta(minutes=utc_offset))
        stat_end = (datetime.strptime(
            form_stat_timelog.stat_end.data, '%Y-%m-%d') -
            timedelta(minutes=utc_offset))
        # TODO: 1 whether sum different date 2 show sum duration for each group
        if 'longrandomwordiueldkfifj' in form_stat_timelog.project_stat.data:
            result = (
                current_user.timelogs.filter(
                    TimeLog.timestamp_start >=
                    datetime.strptime(form_stat_timelog.stat_start.data,
                                      '%Y-%m-%d'),
                    TimeLog.timestamp_start <
                    (datetime.strptime(form_stat_timelog.stat_end.data,
                                       '%Y-%m-%d') + timedelta(days=1)),
                    # TimeLog.project.in_(form_stat_timelog.project_stat.data),
                    TimeLog.statu_code == 2).
                order_by(TimeLog.timestamp_start.desc()).all())
        else:
            result = (
                current_user.timelogs.filter(
                    TimeLog.timestamp_start >=
                    datetime.strptime(form_stat_timelog.stat_start.data,
                                      '%Y-%m-%d'),
                    TimeLog.timestamp_start <
                    (datetime.strptime(form_stat_timelog.stat_end.data,
                                       '%Y-%m-%d') + timedelta(days=1)),
                    TimeLog.project.in_(form_stat_timelog.project_stat.data),
                    TimeLog.statu_code == 2).
                order_by(TimeLog.timestamp_start.desc()).all())
        return render_template('timesheet/timelog_stat.html',
                               form_stat_timelog=form_stat_timelog,
                               num_project=num_project,
                               # whether have stat result
                               result_mode=True,
                               result=result,
                               )
    return render_template('timesheet/timelog_stat.html',
                           form_stat_timelog=form_stat_timelog,
                           num_project=num_project,
                           result_mode=False,
                           )


@timesheet.route('/timelog_plan')
@login_required
def timelog_plan():
    timelog_plan = (current_user.timelogs.filter_by(statu_code=0).
                    order_by(TimeLog.timestamp_start.desc()).all())
    return render_template('timesheet/timelog_plan.html',
                           timelog_plan=timelog_plan
                           )
