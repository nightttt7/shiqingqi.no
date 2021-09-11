from flask import Blueprint

timeline = Blueprint('timeline', __name__)

from . import views
