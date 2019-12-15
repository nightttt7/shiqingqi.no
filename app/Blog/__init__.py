from flask import Blueprint

Blog = Blueprint('Blog', __name__)

from . import views
