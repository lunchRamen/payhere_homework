# Create your tests here.
from django.test import TestCase
# from rest_framework.response import Response
from rest_framework.test import APIClient

# from django.urls import reverse


class UserTestCase(TestCase):
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
