# Create your tests here.
# from django.test import TestCase
from rest_framework.test import APITestCase,APITransactionTestCase
# from rest_framework.response import Response
from rest_framework.test import APIClient
from .models import User

from django.urls import reverse
from freezegun import freeze_time
import datetime


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

class UserTokenTestCase(APITestCase):
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
    
    def test_접근토큰_시간만료_전_성공(self):
        data = {
            "token": self.token
        }
        res = self.client.post('http://127.0.0.1/api/users/token/verify/', data)
        self. assertEqual(res.status_code , 200)
    
    def test_접근토큰_시간만료_후_실패(self):
        data = {
            "token": self.token
        }
        with freeze_time(datetime.datetime.now() + datetime.timedelta(hours=2)):
            res = self.client.post('http://127.0.0.1/api/users/token/verify/', data)
            self.assertEqual(res.status_code, 401)


class AccountBookTestCase(APITransactionTestCase):
    token = ""
    reset_sequences = True

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

    def do_유저_가계부_더미데이터_생성(self):
        data = {
            "money": 1000,
            "memo": "test",
        }
        res = self.client.post(reverse('accountbooks'),data)
        return res.data
    
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
        for _ in range(5):
            self.do_유저_가계부_더미데이터_생성()
        res = self.client.get(reverse('accountbooks'))
        self.assertEqual(res.status_code, 200)
    
    def test_유저_특정_가계부_조회_성공(self):
        self.do_유저_가계부_더미데이터_생성()
        res = self.client.get('http://127.0.0.1:8000/api/accountbook/',{"accountbook_id":1})
        self.assertEqual(res.status_code , 200)
    
    def test_유저_특정_가계부_조회_실패(self):
        self.do_유저_가계부_더미데이터_생성()
        res = self.client.get(reverse('accountbook',kwargs={"accountbook_id":2}))
        self.assertEqual(res.status_code , 400)
        self.assertEqual(res.data.get("detail"), "없는 가계부 조회는 불가합니다.")

    def test_유저_특정_가계부_업데이트_성공(self):
        self.do_유저_가계부_더미데이터_생성()
        data = {
            "money": 10000,
            "memo": "test2",
        }
        res = self.client.patch(reverse('accountbook',kwargs={"accountbook_id":1}), data = data)
        self.assertEqual(res.status_code, 200)
    
    def test_유저_특정_가계부_업데이트_실패_없는가계부(self):
        self.do_유저_가계부_더미데이터_생성()
        data = {
            "money": 10000,
            "memo": "test2",
        }
        res = self.client.patch(reverse('accountbook',kwargs={"accountbook_id":2}), data = data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data["detail"], "없는 가계부 조회는 불가합니다.")
    
    def test_유저_특정_가계부_삭제_성공(self):
        self.do_유저_가계부_더미데이터_생성()
        res = self.client.delete(reverse('accountbook', kwargs={'accountbook_id':1}))
        self.assertEqual(res.status_code, 200)