'''
Flask Application Error Handler
'''
from flask import Blueprint, render_template, jsonify, request

error_handler = Blueprint('error_handler', __name__)


@error_handler.app_errorhandler(404)
def not_found(error):
    '''404 error handler'''
    if request.accept_mimetypes.accept_json:
        return jsonify(msg=str(error)), 404
    return render_template('index.html'), 404


@error_handler.app_errorhandler(500)
def internal_server_error(error):
    '''500 error handler'''
    if request.accept_mimetypes.accept_json:
        return jsonify(msg=str(error)), 500
    return render_template('index.html'), 500
