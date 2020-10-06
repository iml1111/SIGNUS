'''
SIGNUS Application Config Setting
'''
import os
import sys
from datetime import datetime
from logging.config import dictConfig
from modules.tokenizer import Tokenizer
from modules.recommender.fasttext import Recommender

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    '''공통 Config'''
    # Authorization
    SECRET_KEY = os.environ['SIGNUS_SECRET_KEY']
    ADMIN_ID = os.environ['SIGNUS_ADMIN_ID']
    ADMIN_PW = os.environ['SIGNUS_ADMIN_PW']

    # Database
    MONGODB_URI = os.environ['SIGNUS_MONGODB_URI']
    MONGODB_DB_NAME = 'signus'

    # FastText
    FT = Recommender("../../model/ft/signus_ft_model")
    print("FastText Load Complete ...")

    # Tokenizer
    TK = Tokenizer()
    print("Tokenizer Load Complete ...")

    # Maximum API time
    SLOW_API_TIME = 0.5

    # master_config 기본 값
    DEFAULT_MASTER_CONFIG = [
        {
            "key": "updated_at",
            "value": datetime.now()
        },
        {
            "key": "highest_fav_cnt",
            "value": 1
        },
        {
            "key": "highest_view_cnt",
            "value": 1
        }
    ]

    # 실시간 검색어 초기 값
    DEFAULT_REALTIME = {
        "realtime": [
            ['세종대', 0.9],
            ['장학금', 0.9],
            ['학식', 0.9],
            ['공모전', 0.9],
            ['공결', 0.9],
            ['스터디', 0.9],
            ['세종사회봉사', 0.9],
            ['수강', 0.9],
            ['기초코딩', 0.9],
            ['학술정보원', 0.9],
            ['교양', 0.9],
            ['토익', 0.9],
            ['동아리', 0.9],
            ['야식행사', 0.9],
            ['기숙사', 0.9],
            ['대양AI센터', 0.9],
            ['어린이대공원', 0.9],
            ['카페', 0.9],
            ['맛집', 0.9],
            ['대동제', 0.9]
        ],
        "date": datetime.now()
    }

    # 각종 변수
    INDICATORS = {
        "FAS_WEIGHT": 1, # FAS 가중치
        "IS_WEIGHT": 1, # IS 가중치
        "RANDOM_WEIGHT": 1, # RANDOM 가중치
        "DEFAULT_DATE": 60, # POST 게시 날짜 Maximum (불러올 때)
        "CATEGORY_SET": ['대학교', '동아리-모임', '공모전-행사', '진로-구인'], # 사용중인 카테고리
        "POSTS_NUM_BY_CATEGORY": [60, 33, 33, 33, 18], # 카테고리 별 불러오는 개수
        "GET_POST_NUM": 500, # 최대 POST 불러오는 개수
        "RECOM_POST_WEIGHT": 150, # 추천 뉴스피드에서 사용하는 POST 개수 가중치
        "RECOM_POST_MINUS_WEIGHT": -75, # 추천 뉴스피드에서 사용하는 POST 가감 가중치

        # 관심사 측정에 필요한 지표
        "FAV_WEIGHT": 2,
        "VIEW_WEIGHT": 1,
        "SEARCH_WEIGHT": 1,
        "NEWSFEED_WEIGHT": 1,


        # 사용자 관련 지표
        "COLD_START": 10, # 사용자 Cold 기준
        "TAG_SUM_WEIGHT": 1.5,
        "FAV_TOPIC_WEIGHT": 35,
        "VIEW_TOPIC_WEIGHT": 30,
        "SEARCH_TOPIC_WEIGHT": 25,
        "NEWSFEED_TOPIC_WEIGHT": 10,

        # 개수 및 제한 관련 지표
        "RETURN_NUM": 150,
        "T_N_LIMIT": 2000,
        "REALTIME_LIMIT": 20, # 실시간 검색어 검색 제한 리미트
        "REALTIME_RETURN_NUM": 10 # 실시간 검색어 반환 개수
    }

    @staticmethod
    def init_app(app):
        '''전역 init_app 함수'''


class TestingConfig(Config):
    '''Test 전용 Config'''
    DEBUG = True
    TESTING = True


class DevelopmentConfig(Config):
    '''개발 환경 전용 Config'''
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    ''' 상용환경 전용 Config'''
    DEBUG = False
    TESTING = False

    @staticmethod
    def init_app(app):
        '''로거 등록 및 설정'''
        dictConfig({
            'version': 1,
            'formatters': {
                'default': {
                    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                }
            },
            'handlers': {
                'file': {
                    'level': 'WARNING',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.getenv('RAAS_ERROR_LOG_PATH') or './server.error.log',
                    'maxBytes': 1024 * 1024 * 5,
                    'backupCount': 5,
                    'formatter': 'default',
                },
            },
            'root': {
                'level': 'WARNING',
                'handlers': ['file']
            }
        })


config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestingConfig,
    'default':DevelopmentConfig,
}
