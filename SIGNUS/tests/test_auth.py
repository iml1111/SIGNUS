'''
Auth API 관련 테스트 케이스
'''
import unittest
from json import loads
from flask import current_app
from app import create_app
from flask_jwt_extended import create_access_token


class AuthAPITestCase(unittest.TestCase):
    ''' Auth 테스트 케이스 클래스 '''
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
        ''' 후처리 메소드 '''
        self.app_context.pop()

    def get_headers(self):
        '''API Header 생성 메소드'''
        result = {
            'Accept': 'application/json',
            'Authorization': "Bearer " + self.access_token,
            #'Content-Type': 'application/json',
        }
        return result

    def test_signin(self):
        ''' 로그인 API 검증 테스트 '''
        resp = self.client.post(
            '/api/auth/signin',
            headers=self.get_headers(),
            json={
                "id":current_app.config['ADMIN_ID'],
                "pw":current_app.config['ADMIN_PW']
            }
        )
        self.assertEqual(resp.status_code, 200)

    def test_get_user(self):
        ''' 회원 정보 반환 API 검증 테스트 '''
        resp = self.client.get(
            '/api/auth/user',
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)
