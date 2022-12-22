# Create your tests here.
# from django.test import TestCase
from rest_framework.test import APITestCase
# from rest_framework.response import Response
from rest_framework.test import APIClient
from .models import User

from django.urls import reverse


class UserSignupTestCase(APITestCase):
    client_calss = APIClient

    def test_유저_생성_성공(self):
        data = {
            "email": "test@gmail.com",
            "password1": "asdff1234",
            "password2": "asdff1234"
        }
        res = self.client.post('http://127.0.0.1:8000/api/users/signup/', data)
        self.assertEqual(res.status_code, 201)

    def test_유저_생성_실패_정보부족(self):
        res = self.client.post('http://127.0.0.1:8000/api/users/signup/')
        self.assertEqual(res.status_code, 400)

    def test_유저_생성_실패_이메일형식(self):
        data = {
            "email": "test",
            "password1": "asdff1234",
            "password2": "asdff1234"
        }
        res = self.client.post('http://127.0.0.1:8000/api/users/signup/',data)
        self.assertEqual(res.status_code, 400)
    
    def test_유저_생성_실패_비밀번호형식(self):
        data = {
            "email": "test@gmail.com",
            "password1": "1234",
            "password2": "1234"
        }
        res = self.client.post('http://127.0.0.1:8000/api/users/signup/',data)
        self.assertEqual(res.status_code, 400)

    
class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email = "test@gmail.com"
        )
        self.user.set_password("asdff1234")
        self.user.save()

    def test_유저_로그인_성공(self):
        data = {
            "email": "test@gmail.com",
            "password": "asdff1234"
        }
        res = self.client.post('http://127.0.0.1:8000/api/users/login/',data)
        self.assertEqual(res.status_code , 200)
    
    def test_유저_로그인_실패_이메일(self):
        data = {
            "email": "test2@gmail.com",
            "password": "asdff1234"
        }
        res = self.client.post('http://127.0.0.1:8000/api/users/login/',data)
        self.assertEqual(res.status_code , 400)
    
    def test_유저_로그인_실패_비밀번호(self):
        data = {
            "email": "test2@gmail.com",
            "password": "asdf234"
        }
        res = self.client.post('http://127.0.0.1:8000/api/users/login/',data)
        self.assertEqual(res.status_code , 400)

class UserLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email = "test@gmail.com"
        )
        self.user.set_password("asdff1234")
        self.user.save()
    
    def test_유저_로그아웃_성공(self):
        res = self.client.post('http://127.0.0.1:8000/api/users/logout/')
        self.assertEqual(res.status_code, 200)


class AccountBookTestCase(APITestCase):
    token = ""

    def setUp(self):
        self.user = User.objects.create(
            email = "test@gmail.com"
        )
        self.user.set_password("asdff1234")
        self.user.save()

        data = {
            "email":"test@gmail.com",
            "password":"asdff1234"
        }

        res = self.client.post('http://127.0.0.1:8000/api/users/login/',data)
        self.token = res.json()["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION = "Bearer " + self.token)
    
    def test_유저_가계부_생성_성공(self):
        data = {
            "money": 1000,
            "memo": "test",
        }
        res = self.client.post(reverse('accountbooks'),data)
        self.assertEqual(res.status_code, 201)
    
    def test_유저_가계부_생성_실패_돈미입력(self):
        data = {
            "money":'',
            "memo": "test",
        }
        res = self.client.post(reverse('accountbooks'),data)
        self.assertEqual(res.status_code, 400)
    
    def test_유저_가계부_생성_실패_돈_숫자X(self):
        data = {
            "money":'1q',
            "memo": "test",
        }
        res = self.client.post(reverse('accountbooks'),data)
        self.assertEqual(res.status_code, 400)
    
    def test_유저_가계부_생성_실패_돈0원(self):
        data = {
            "money":0,
            "memo": "test",
        }
        res = self.client.post(reverse('accountbooks'),data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data.get("detail"), "가계부의 생성,수정은 0원이 넘어야 가능합니다.")
    
    def test_유저_가계부_리스트_성공(self):
        res = self.client.get(reverse('accountbooks'))
        self.assertEqual(res.status_code, 200)
    
    def test_유저_특정_가계부_조회_성공(self):
        def do_유저_가계부_더미데이터_생성():
            data = {
                "money": 1000,
                "memo": "test",
            }
            res = self.client.post(reverse('accountbooks'),data)
            return res.data
        do_유저_가계부_더미데이터_생성()
        res = self.client.get('http://127.0.0.1:8000/api/accountbook/',{"accountbook_id":1})
        self.assertEqual(res.status_code , 200)
    
    def test_유저_특정_가계부_조회_실패(self):
        def do_유저_가계부_더미데이터_생성():
            data = {
                "money": 1000,
                "memo": "test",
            }
            res = self.client.post(reverse('accountbooks'),data)
            return res.data
        do_유저_가계부_더미데이터_생성()
        res = self.client.get(reverse('accountbook',kwargs={"accountbook_id":2}))
        self.assertEqual(res.status_code , 400)
        self.assertEqual(res.data.get("detail"), "없는 가계부 조회는 불가합니다.")