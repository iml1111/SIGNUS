'''
Post API 관련 테스트 케이스
'''
import unittest
from json import loads
from flask import current_app
from app import create_app
from flask_jwt_extended import create_access_token


class PostAPITestCase(unittest.TestCase):
    '''Post 테스트 케이스 클래스'''
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

    def test_1_post_like(self):
        '''Post 좋아요 API 검증 테스트'''

        # 인기 뉴스피드 불러오기 (테스트 포스트 추출을 위함)
        resp = self.client.get(
            '/api/signus/v1/newsfeed/popular',
            headers=self.get_headers(),
            json={}
        )
        newsfeed = loads(loads(resp.data)['result'])
        post_obi = newsfeed[0]['_id']['$oid']

        # Post 좋아요
        resp = self.client.patch(
            '/api/signus/v1/post/like/' + post_obi,
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_2_post_unlike(self):
        '''Post 좋아요 취소 검증 테스트'''

        # 인기 뉴스피드 불러오기 (테스트 포스트 추출을 위함)
        resp = self.client.get(
            '/api/signus/v1/newsfeed/popular',
            headers=self.get_headers(),
            json={}
        )
        newsfeed = loads(loads(resp.data)['result'])
        post_obi = newsfeed[0]['_id']['$oid']

        # Post 좋아요 취소
        resp = self.client.patch(
            '/api/signus/v1/post/unlike/' + post_obi,
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)

    def test_view(self):
        '''Post 조회수 검증 테스트'''

        # 인기 뉴스피드 불러오기 (테스트 포스트 추출을 위함)
        resp = self.client.get(
            '/api/signus/v1/newsfeed/popular',
            headers=self.get_headers(),
            json={}
        )
        newsfeed = loads(loads(resp.data)['result'])
        post_obi = newsfeed[0]['_id']['$oid']

        # Post 조회수
        resp = self.client.patch(
            '/api/signus/v1/post/view/' + post_obi,
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)