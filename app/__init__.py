import os

from flask import Flask
from flask_assets import Environment
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect


from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_ckeditor import CKEditor

from app.assets import app_css, app_js, vendor_css, vendor_js
from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()
images = UploadSet('images', IMAGES)
docs = UploadSet('docs', ('rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'pdf', 'css'))

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'account.login'


def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    Config[config_name].init_app(app)

    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Set up extensions
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)
    configure_uploads(app, images)
    configure_uploads(app, docs)
    CKEditor(app)

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    from .blueprints.public import public as public_blueprint
    app.register_blueprint(public_blueprint)


    from .blueprints.content_manager import content_manager as content_manager_blueprint
    app.register_blueprint(content_manager_blueprint)


    from .blueprints.profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/profile')


    from .blueprints.seeking import seeking as seeking_blueprint
    app.register_blueprint(seeking_blueprint, url_prefix='/preferences')

    from .blueprints.page_manager import page_manager as page_manager_blueprint
    app.register_blueprint(page_manager_blueprint)

    from .blueprints.messaging_manager import messaging_manager as messaging_manager_blueprint
    app.register_blueprint(messaging_manager_blueprint, url_prefix='/message')

    from .blueprints.notification import notification as notification_blueprint
    app.register_blueprint(notification_blueprint, url_prefix='/notification')
    
    from .blueprints.account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .blueprints.photo import photo as photo_blueprint
    app.register_blueprint(photo_blueprint, url_prefix='/photo')

    from .blueprints.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
