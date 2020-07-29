# -*- encoding: utf-8 -*-
'''
@Time : 2020/7/17 11:29 
@Author : qinhanluo
@File : worker.py 
@Software: PyCharm
@Description ： TODO
'''
import os
from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)
