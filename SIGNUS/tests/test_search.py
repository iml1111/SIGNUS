'''
Search API 관련 테스트 케이스
'''
import unittest
from json import loads
from flask import current_app
from app import create_app
from flask_jwt_extended import create_access_token


class SearchAPITestCase(unittest.TestCase):
    '''Search 테스트 케이스 클래스'''
    def setUp(self):
        '''전처리 메소드'''
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.access_token = {
            'ADMIN': create_access_token(
                     identity=self.app.config['ADMIN_ID'],
                     expires_delta=False),
            'TEST': create_access_token(
                     identity="test",
                     expires_delta=False)}

    def tearDown(self):
        '''후처리 메소드'''
        self.app_context.pop()

    def get_headers(self, user_type="ADMIN"):
        '''API Header 생성 메소드'''
        result = {
            'Accept': 'application/json',
            'Authorization': "Bearer " + self.access_token[user_type],
            #'Content-Type': 'application/json',
        }
        return result

    def test_Search(self):
        '''Search API 검증 테스트'''
        # 검색
        resp = self.client.post(
            '/api/signus/v1/search',
            headers=self.get_headers(),
            json={
                "keywords": "공모전",
                "order": 1,
            }
        )
        self.assertEqual(resp.status_code, 200)
