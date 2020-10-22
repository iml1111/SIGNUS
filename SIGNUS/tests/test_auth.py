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

    def test_sejong(self):
        '''세종대학교 구성원 인증 API 테스트'''
        resp = self.client.post(
            '/api/auth/sejong',
            headers=self.get_headers(),
            json={
                "sj_id": current_app.config['SEJONG_ID'],
                "sj_pw": current_app.config['SEJONG_PW']
            }
        )
        self.assertEqual(resp.status_code, 200)

    def test_signup_secession(self):
        '''회원 가입 API 테스트 (회원 탈퇴 API 테스트 로직도 이하 동일함)'''
        resp = self.client.post(
            '/api/auth/signup',
            headers=self.get_headers(),
            json={
                "sj_id": current_app.config['SEJONG_ID'],
                "sj_pw": current_app.config['SEJONG_PW'],
                "id": "test",
                "pw": "test",
                "nickname": "test"
            }
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(
            '/api/auth/secession',
            headers=self.get_headers("TEST"),
            json={"pw": "test"}
        )
        self.assertEqual(resp.status_code, 200)

    def test_signin(self):
        ''' 로그인 API 검증 테스트 '''
        resp = self.client.post(
            '/api/auth/signin',
            headers=self.get_headers(),
            json={
                "id": current_app.config['ADMIN_ID'],
                "pw": current_app.config['ADMIN_PW']
            }
        )
        self.assertEqual(resp.status_code, 200)

    def test_update_password(self):
        '''비밀번호 변경 API 테스트'''
        resp = self.client.post(
            '/api/auth/signup',
            headers=self.get_headers(),
            json={
                "sj_id": current_app.config['SEJONG_ID'],
                "sj_pw": current_app.config['SEJONG_PW'],
                "id": "test",
                "pw": "test",
                "nickname": "test"
            }
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.patch(
            '/api/auth/user/password',
            headers=self.get_headers("TEST"),
            json={
                "old_pw": "test",
                "new_pw": "test2",
                "check_pw": "test2"
            }
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(
            '/api/auth/secession',
            headers=self.get_headers("TEST"),
            json={"pw": "test2"}
        )
        self.assertEqual(resp.status_code, 200)
        
    def test_update_nickname(self):
        '''닉네임 변경 API 테스트'''
        resp = self.client.post(
            '/api/auth/signup',
            headers=self.get_headers(),
            json={
                "sj_id": current_app.config['SEJONG_ID'],
                "sj_pw": current_app.config['SEJONG_PW'],
                "id": "test",
                "pw": "test",
                "nickname": "test"
            }
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.patch(
            '/api/auth/user/nickname',
            headers=self.get_headers("TEST"),
            json={"nickname": "test2"}
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(
            '/api/auth/secession',
            headers=self.get_headers("TEST"),
            json={"pw": "test"}
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
