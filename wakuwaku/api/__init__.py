from flask import Blueprint

bp = Blueprint('api', __name__)

from wakuwaku.api import users
from wakuwaku.api import upload