'''
SIGNUS Application Main Manage Module
'''
import os
import unittest
import click
from config import config
from app import create_app
from app import models
from app.models.mongodb import get_mongo_cur
from modules import bg_process

application = create_app(os.getenv('FLASK_CONFIG') or 'default')


@application.shell_context_processor
def make_shell_context():
    '''Init shell context'''
    return dict(mongo_cur=get_mongo_cur())

@application.cli.command()
def bg_interest():
    """User interest score measurement."""
    bg_process.user_interest(config[os.getenv('FLASK_CONFIG') or 'default'])

@application.cli.command()
def bg_realtime():
    """Realtime update."""
    bg_process.realtime(config[os.getenv('FLASK_CONFIG') or 'default'])

@application.cli.command()
def db_init():
    """First, run the Database init modules."""
    models.init_app(config[os.getenv('FLASK_CONFIG') or 'default'])


@application.cli.command()
def log_delete():
    """log table remove command, please be carefully"""
    mongo_cur = get_mongo_cur()
    col = mongo_cur[config[os.getenv('FLASK_CONFIG') or 'default'].MONGODB_DB_NAME]['log']
    col.delete_many({})


@application.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
