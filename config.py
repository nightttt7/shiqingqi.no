import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'key'
    # the variable name "SECRET_KEY" should not change
    # !!! in production environment
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_ADMIN = 'nightttt7@gmail.com'
    # !!! in production environment
    # FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'deve.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI =  \
        'sqlite:///' + os.path.join(basedir, 'data.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
