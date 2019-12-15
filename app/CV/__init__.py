from flask import Blueprint

CV = Blueprint('CV', __name__)

from . import views
