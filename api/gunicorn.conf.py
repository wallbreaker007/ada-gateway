# -*- encoding: utf-8 -*-
'''
@Time : 2020/7/27 9:36 
@Author : qinhanluo
@File : gunicorn.conf.py 
@Software: PyCharm
@Description ： TODO
'''

workers = 5
worker_class = 'gevent'
bind = "0.0.0.0:5000"