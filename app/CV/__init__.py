from flask import Blueprint

chop = Blueprint('CV', __name__)

from . import views
