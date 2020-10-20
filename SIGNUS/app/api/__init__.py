'''
API rquest handler and util
'''
from flask import abort, g, current_app, request
from app.controllers.log import insert_log
from app.models.mongodb import open_mongo_cur, close_mongo_cur


def init_app(app):
    ''' api 초기 세팅'''

    @app.before_first_request
    def before_first_request():
        '''맨 처음 리퀘스트가 오기 전에'''

    @app.before_request
    def before_request():
        '''HTTP 요청이 들어올때 마다'''
        open_mongo_cur()

    @app.after_request
    def after_request(response):
        '''HTTP 요청이 끝나고 브라우저에 응답하기 전에'''

        # Slow API Tracking
        if 'process_time' in g and \
        g.process_time >= current_app.config['SLOW_API_TIME']:

            log_str = "\n!!! SLOW API DETECTED !!! \n" + \
                      "ip: " + request.remote_addr + "\n" + \
                      "url: " + request.full_path + "\n" + \
                      "input_json: " + str(request.get_json()) + "\n" + \
                      "slow time: " + str(g.process_time) + "\n"

            app.logger.warning(log_str)

        # User Action Tracking
        if 'user' in g and request.full_path != "/api/log/page?":
            insert_log(mongo_cur=g.mongo_cur,
                       user_id=g.user['user_id'],
                       url=request.full_path,
                       method=request.method,
                       params=str(request.data))

        return response

    @app.teardown_request
    def teardown_request(exception):
        '''HTTP 요청이 끝나고 브라우저에 응답하기 전에'''
        close_mongo_cur()

    @app.teardown_appcontext
    def teardown_appcontext(exception):
        '''app context가 종료되기 전에'''


def input_check(data, key, value_type, length=None):
    '''json input 파라미터 인자 검증 함수'''
    if key not in data:
        abort(400, description="'%s' not in data." % key)
    if not isinstance(data[key], value_type):
        abort(400, description="'%s' must be '%s' type." % (key, str(value_type)))
    if length and len(data[key]) > length:
        abort(400, description="'%s' is too long(longer than '%s')" % (key, str(length)))
