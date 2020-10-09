'''
User API 관련 테스트 케이스
'''
import unittest
from json import loads
from flask import current_app
from app import create_app
from flask_jwt_extended import create_access_token


class UserAPITestCase(unittest.TestCase):
    '''User 테스트 케이스 클래스'''
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

    def test_a_signin(self):
        '''로그인 API 검증 테스트'''
        resp = self.client.post(
            '/api/user/signin',
            headers=self.get_headers(),
            json={
                "id":current_app.config['ADMIN_ID'],
                "pw":current_app.config['ADMIN_PW']
            }
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_b_fav_push(self):
        '''fav_list 추가 API 검증 테스트'''

        # 인기 뉴스피드 불러오기 (테스트 포스트 추출을 위함)
        resp = self.client.get(
            '/api/signus/v1/newsfeed/popular',
            headers=self.get_headers(),
            json={}
        )
        newsfeed = loads(loads(resp.data)['result'])
        post_obi = newsfeed[0]['_id']['$oid']

        # 본격 테스트
        resp = self.client.put(
            '/api/user/fav/push/' + post_obi,
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_c_fav_pull(self):
        '''fav_list 삭제 API 검증 테스트'''

        # 인기 뉴스피드 불러오기 (테스트 포스트 추출을 위함)
        resp = self.client.get(
            '/api/signus/v1/newsfeed/popular',
            headers=self.get_headers(),
            json={}
        )
        newsfeed = loads(loads(resp.data)['result'])
        post_obi = newsfeed[0]['_id']['$oid']

        # 본격 테스트
        resp = self.client.delete(
            '/api/user/fav/pull/' + post_obi,
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_d_view_push(self):
        '''view_list 추가 API 검증 테스트'''

        # 인기 뉴스피드 불러오기 (테스트 포스트 추출을 위함)
        resp = self.client.get(
            '/api/signus/v1/newsfeed/popular',
            headers=self.get_headers(),
            json={}
        )
        newsfeed = loads(loads(resp.data)['result'])
        post_obi = newsfeed[0]['_id']['$oid']

        # 본격 테스트
        resp = self.client.put(
            '/api/user/view/push/' + post_obi,
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)