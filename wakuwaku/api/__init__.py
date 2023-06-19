from flask import Blueprint

bp = Blueprint('api', __name__)

from wakuwaku.api import users
from wakuwaku.api import upload
from wakuwaku.api import posts
from wakuwaku.api import tags
from wakuwaku.api import votes
from wakuwaku.api import comments
from wakuwaku.api import favorite