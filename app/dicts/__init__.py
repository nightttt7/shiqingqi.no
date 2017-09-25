from flask import Blueprint

dicts = Blueprint('dicts',  __name__)

from . import views
