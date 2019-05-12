from flask import Blueprint

api = Blueprint('api', __name__)

from . import user, movie, token, movlist, comment, recommend
