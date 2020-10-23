'''
Template API
'''
import time
from flask import Blueprint, render_template, send_from_directory
from app.api.decorators import timer

template = Blueprint('template', __name__)


@template.route("/manifest.json")
def manifest():
    '''manifest.json'''
    return send_from_directory('/', 'manifest.json')


@template.route("/robots.txt")
def manifest_robot():
    '''robots.txt'''
    return send_from_directory('/', 'robots.txt')


@template.route("/")
@template.route("/best")
@template.route("/newsfeed/university")
@template.route("/newsfeed/award")
@template.route("/newsfeed/group")
@template.route("/newsfeed/job")
@template.route("/search")
@template.route("/notice")
@template.route("/notice/write")
def page():
    '''return client app'''
    return render_template('index.html')
