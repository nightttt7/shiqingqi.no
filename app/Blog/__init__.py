from flask import Blueprint

chop = Blueprint('Blog', __name__)

from . import views
