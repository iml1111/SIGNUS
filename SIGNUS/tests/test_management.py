'''
Management API 관련 테스트 케이스
'''
import unittest
from json import loads
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

    def test_realtime(self):
        '''실시간 검색어'''
        resp = self.client.get(
            '/api/signus/v1/realtime',
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)

    def test_put_notice(self):
        '''공지 작성 API 검증 테스트'''
        resp = self.client.put(
            '/api/signus/v1/notice',
            headers=self.get_headers(),
            json={
                "title": "공지사항 테스트",
                "post": "공지사항 테스트"
            }
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_patch_notice(self):
        '''공지 수정 API 검증 테스트'''
        # 공지 추가
        resp = self.client.put(
            '/api/signus/v1/notice',
            headers=self.get_headers(),
            json={
                "title": "공지사항 테스트",
                "post": "공지사항 테스트"
            }
        )
        # 공지 전체 반환
        resp = self.client.get(
            '/api/signus/v1/notice',
            headers=self.get_headers(),
            json={}
        )
        notices = loads(loads(resp.data)['result'])
        notice_obi = notices[0]['_id']['$oid']
        # 공지 수정
        resp = self.client.patch(
            '/api/signus/v1/notice/' + notice_obi,
            headers=self.get_headers(),
            json={
                "title": "공지사항 수정 테스트",
                "post": "공지사항 수정 테스트"
            }
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_notice_many(self):
        '''공지 전체 반환 API 검증 테스트'''
        resp = self.client.get(
            '/api/signus/v1/notice',
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_notice_one(self):
        '''공지 단일 반환 API 검증 테스트'''
        # 공지 추가
        resp = self.client.put(
            '/api/signus/v1/notice',
            headers=self.get_headers(),
            json={
                "title": "공지사항 테스트",
                "post": "공지사항 테스트"
            }
        )
        # 공지 전체 반환
        resp = self.client.get(
            '/api/signus/v1/notice',
            headers=self.get_headers(),
            json={}
        )
        notices = loads(loads(resp.data)['result'])
        notice_obi = notices[0]['_id']['$oid']
        # 공지 단일 반환
        resp = self.client.get(
            '/api/signus/v1/notice/' + notice_obi,
            headers=self.get_headers(),
            json={}
        )
        self.assertEqual(resp.status_code, 200)
    
    def test_z_delete_notice(self):
        '''공지사항 삭제 API 검증 테스트'''
        # 공지 추가
        resp = self.client.put(
            '/api/signus/v1/notice',
            headers=self.get_headers(),
            json={
                "title": "공지사항 테스트",
                "post": "공지사항 테스트"
            }
        )
        # 공지 전체 반환
        resp = self.client.get(
            '/api/signus/v1/notice',
            headers=self.get_headers(),
            json={}
        )
        notices = loads(loads(resp.data)['result'])
        # 공지 삭제
        for notice in notices:
            resp = self.client.delete(
                '/api/signus/v1/notice/' + notice['_id']['$oid'],
                headers=self.get_headers(),
                json={}
            )
            self.assertEqual(resp.status_code, 200)
    