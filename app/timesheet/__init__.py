from flask import Blueprint

timesheet = Blueprint('timesheet', __name__)

from . import views
