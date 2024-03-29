from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_login import LoginManager

login_manager = LoginManager()

from flasgger import Swagger

swagger = Swagger()

from flask_caching import Cache

cache = Cache()