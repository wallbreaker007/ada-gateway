# -*- encoding: utf-8 -*-
'''
@Time : 2020/7/10 13:48 
@Author : qinhanluo
@File : __init__.py 
@Software: PyCharm
@Description ： TODO
'''
from flask import Flask
from config import config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
