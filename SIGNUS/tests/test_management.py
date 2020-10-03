'''
Management API 관련 테스트 케이스
'''
import unittest
from flask import current_app
from app import create_app
from flask_jwt_extended import create_access_token


class ManagementAPITestCase(unittest.TestCase):
    '''Management 테스트 케이스 클래스'''
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
    
    def test_put_notice(self):
        '''공지사항 작성 API 검증 테스트'''
        resp = self.client.put(
            '/api/signus/v1/notice',
            headers=self.get_headers(),
            json={
                "title": "공지사항 테스트",
                "post": "공지사항 테스트"
            }
        )
        self.assertEqual(resp.status_code, 200)
    
    
    