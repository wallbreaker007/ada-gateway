# -*- encoding: utf-8 -*-
'''
@Time : 2020/7/13 14:17 
@Author : qinhanluo
@File : models.py 
@Software: PyCharm
@Description ： TODO
'''
from datetime import datetime

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class TaskState:
    UNDEFINED = 1
    PROCESSING = 2
    PROCESSED = 4
    ERROR = 8


