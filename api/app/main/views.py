# -*- encoding: utf-8 -*-
'''
@Time : 2020/7/13 14:26 
@Author : qinhanluo
@File : views.py 
@Software: PyCharm
@Description ： TODO
'''
from flask import request, jsonify
from . import main

from ..worker import celery
import celery.states as states

'''
TODO
'''
@main.route('/v1/check/<string:id>')
def check_task(id):
    res = celery.AsyncResult(id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)

'''
TODO,
1. 获取区域
2. 生成uuid
3. 定义任务，区域，传递给服务端
4. 维护UUID的状态信息
'''
@main.route('/v1/enhance/district', methods=['GET'])
def generate_enhance_district():
    getArgs = request.args

    left_top_x = int(getArgs.get('left_top_x'))
    left_top_y = int(getArgs.get('left_top_y'))

    right_bottom_x = int(getArgs.get('right_bottom_x'))
    right_bottom_y = int(getArgs.get('right_bottom_y'))

    z = int(getArgs.get('level'))

    #TODO, qualify the params
    task = celery.send_task('mytasks.process', args=[left_top_y, left_top_x, right_bottom_y, right_bottom_x, z], kwargs={})
    return jsonify({'taskID': str(task.id)})
