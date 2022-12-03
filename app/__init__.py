from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    # register blueprints here

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .Blog import Blog as Blog_blueprint
    app.register_blueprint(Blog_blueprint, url_prefix='/blog')

    from .timeline import timeline as timeline_blueprint
    app.register_blueprint(timeline_blueprint, url_prefix='/timeline')

    from .timesheet import timesheet as timesheet_blueprint
    app.register_blueprint(timesheet_blueprint, url_prefix='/t')

    from .gameoflife import gameoflife as gameoflife_blueprint
    app.register_blueprint(gameoflife_blueprint, url_prefix='/g')

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .manage import manage as manage_blueprint
    app.register_blueprint(manage_blueprint, url_prefix='/manage')

    return app
