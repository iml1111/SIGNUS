'''
Newsfeed API 관련 테스트 케이스
'''
import unittest
from flask import current_app
from app import create_app
from flask_jwt_extended import create_access_token


class NewsfeedAPITestCase(unittest.TestCase):
    '''Newsfeed 테스트 케이스 클래스'''
    def setUp(self):
        '''전처리 메소드'''
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.access_token = create_access_token(
            identity=self.app.config['ADMIN_ID'],
            expires_delta=False
        )

    def tearDown(self):
        '''후처리 메소드'''
        self.app_context.pop()

    def get_headers(self):
        '''API Header 생성 메소드'''
        result = {
            'Accept': 'application/json',
            'Authorization': "Bearer " + self.access_token,
            #'Content-Type': 'application/json',
        }
        return result

    def test_newsfeed_recom(self):
        '''추천 뉴스피드 API 검증 테스트'''
        resp = self.client.get(
            '/api/signus/v1/newsfeed/recom',
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_newsfeed_popular(self):
        '''인기 뉴스피드 검증 테스트'''
        resp = self.client.get(
            '/api/signus/v1/newsfeed/popular',
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)

    def test_newsfeed_category(self):
        '''카테고리 뉴스피드 검증 테스트'''
        resp = self.client.get(
            '/api/signus/v1/newsfeed/대학교',
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)