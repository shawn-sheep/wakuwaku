from flask import Blueprint

bp = Blueprint('api', __name__)

from wakuwaku.api import users