# -*- encoding: utf-8 -*-
'''
@Time : 2020/7/13 14:13 
@Author : qinhanluo
@File : __init__.py 
@Software: PyCharm
@Description ： TODO
'''
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)