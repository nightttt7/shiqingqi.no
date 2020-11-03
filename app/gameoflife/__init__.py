from flask import Blueprint

gameoflife = Blueprint('gameoflife', __name__)

from . import views
