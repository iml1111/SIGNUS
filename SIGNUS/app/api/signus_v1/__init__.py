'''
SIGNUS V1 API Module Package
'''
from flask import Blueprint

signus_v1 = Blueprint('signus_v1', __name__)

from . import *
