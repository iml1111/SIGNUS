'''
SIGNUS Database Models
'''
import sys
from app.models import mongodb


def init_app(config):
    '''
    db-init function
    '''
    mongodb.init_models(config)
    sys.stdout.write("MongoDB init ... OK\n")
