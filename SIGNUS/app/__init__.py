'''
Application Factory Module
'''
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
from app import api

from app.api.log import log as log_bp
from app.api.user import user as user_bp
from app.api.signus_v1 import signus_v1 as signus_v1_bp
from app.api.template import template as template_bp
from app.api.error_handler import error_handler as error_bp

jwt_manager = JWTManager()
cors = CORS()


def create_app(config_name):
    '''Applcation Object 생성 함수'''
    app = Flask(import_name=__name__,
                instance_relative_config=True,
                static_url_path="/",
                static_folder='client/',
                template_folder='client/')
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    jwt_manager.init_app(app)
    cors.init_app(app)
    api.init_app(app)

    app.register_blueprint(error_bp)
    app.register_blueprint(template_bp)
    app.register_blueprint(log_bp, url_prefix='/api/log')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(signus_v1_bp, url_prefix='/api/signus/v1')

    return app
