from flask import Flask

from wakuwaku.api import bp as api_bp

from wakuwaku.extensions import db, login_manager, swagger, cache

def create_app(config_class=None):
    '''Factory Pattern: Create Flask app.'''
    app = Flask(__name__)

    configure_app(app)

    configure_blueprints(app)

    configure_extensions(app)

    return app

def configure_app(app : Flask):
    '''Configure Flask app.'''

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:GaussdbPassword%40123@119.3.126.0:5432/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    app.config["SECRET_KEY"] = 'ImageDB_secret_key'

    app.config['SWAGGER'] = {
        'title': 'Wakuwaku API',
        'doc_dir': './wakuwaku/docs/'
    }

    app.config['CACHE_TYPE'] = 'simple'

    app.config['UPLOAD_FOLDER'] = './wakuwaku/static/upload/'

def configure_blueprints(app : Flask):
    '''Configure Flask blueprints.'''
    app.register_blueprint(api_bp, url_prefix='/api')

def configure_extensions(app : Flask):
    '''Configure Flask extensions.'''
    db.init_app(app)
    login_manager.init_app(app)
    swagger.init_app(app)
    cache.init_app(app)