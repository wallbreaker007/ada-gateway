# -*- encoding: utf-8 -*-
'''
@Time : 2020/7/10 13:38 
@Author : qinhanluo
@File : adaGateway.py 
@Software: PyCharm
@Description ： TODO
'''
import os
import click
from app import create_app
from app.models import Permission, TaskState

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return dict(Permission=Permission, TaskState=TaskState)

@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    '''Run the unit tests.'''
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromName(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)