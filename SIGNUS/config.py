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
    FT = Recommender(os.environ['SIGNUS_FT_MODEL_PATH'])
    FT_VEC_SIZE = FT.model.vector_size
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
        }
    ]

    # 실시간 검색어 기본 값
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
        "GET_NF_POST_NUM": 500, # 뉴스피드용 POST 불러오는 최대 개수
        "RECOM_POST_WEIGHT": 150, # 추천 뉴스피드에서 사용하는 POST 개수 가중치
        "RECOM_POST_MINUS_WEIGHT": -75, # 추천 뉴스피드에서 사용하는 POST 가감 가중치

        # 관심사 측정에 필요한 지표
        "FAV_WEIGHT": 2, # 좋아요 가중치
        "VIEW_WEIGHT": 1, # 조회수 가중치
        "SEARCH_WEIGHT": 1, # 검색 가중치

        # 사용자 관련 지표
        "COLD_START": 10, # 사용자 Cold 기준

        # 검색 관련 지표
        "GET_SC_POST_NUM": 15000, # 검색용 POST 불러오는 최대 개수
        "TITLE_WEIGHT": 1.5, # TITLE TOKEN 가중치
        "TOKEN_WEIGHT": 1, # TOKEN 가중치
        "REGEX_WEIGHT": 1.5, # 제목 정규식 가중치
        "LOWEST_RANK": 1.5, # 최하위 랭크

        # 개수 및 제한 관련 지표
        "RETURN_NUM": 150, # 토탈 반환 개수
        "REALTIME_EFFECTIVE_DAY": 1, # 실시간 검색어 반영 기간
        "REALTIME_KEYWORD_LEN": 15, # 실시간 검색어 최대 길이
        "REALTIME_LIMIT": 20, # 실시간 검색어 검색 제한 리미트
        "REALTIME_RETURN_NUM": 10, # 실시간 검색어 반환 개수

        # 비속어 사전
        "BAD_LANGUAGE": {'페미', '냄져', '한남', '자댕이', '조팔', '씨발', '섹스', '개년', '개새끼', '씹', '셋스', '느개비', '좆', '노무현', "느개비", '느금마', '니애미', '빠구리', '시발년' ,'시발새끼', '느그앰', '느그미', '노무혐', '빠9리', '시발롬', '시발련', '창년', '보빨러', '사까시', '걸레년', '걸레련', '보빨', '4카시', '사카시', '봊', '보전깨', '니미', '오피누', '오피녀', '이기야', '놈딱', '북딱', '지잡', '십색기', '십색갸', '십색꺄', '일배', '일베', '일간베스트', 'ㅈ같', '보들', '자들', '섹종', '섺종', '땅끄', '땅크', '씹년', '훌짓', '섺끈', '세끈', '섹끈', '섻', '섹ㅅ', 'ㅂㅅ', 'ㅅ발', 'ㅈ밥', 'ㅂ신', '시팔', '색기', '니엄', '니앰', 'ㅆ발', 'ㅆㅂ', '무현', '부랄', '붕알', '족같', 'ㅈㄹ', 'ㅅㅂ', 'ㅈㄹ', '쎅스', '섻스', '갈보', '빙신', '병신', '걸레', '콘돔', '보빨', '걸레', '창년', '느금', '놈현', '응디', '딱좋', '틀딱', '엠창', '니미', '시팔', '씨팔', '빨통', '등신', '모텔', '잠지', '보지', '시발', '셋스', '후빨', '홍어', '창녀', '애비', '애미', '개년', '썅'}
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
                    'filename': os.getenv('SIGNUS_ERROR_LOG_PATH') or './server.error.log',
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
