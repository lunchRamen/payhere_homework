from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import AccountBook,User
from rest_framework.response import Response
from rest_framework import status,permissions,authentication
import jwt
from rest_framework.exceptions import APIException
from django.conf import settings
from .account_book_serializer import *
from .exceptions import *
# Create your views here.


class AccountBookViewSet(ModelViewSet):
    queryset = AccountBook.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'test':
            return AccountBookListSerializer
        elif self.action == 'retrieve':
            return AccountBookGetSerializer
        elif self.action == 'create':
            return AccountBookCreateSerializer
        elif self.action == 'update':
            return AccountBookUpdateSerializer
        elif self.action == 'destroy':
            return AccountBookDestroySerializer

    def get_user_id(self,request,*args,**kwargs):
        try:
            jwt_token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        except Exception:
            raise UnauthorizedUser
        decoded_jwt_token = jwt.decode(jwt_token,settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_jwt_token['user_id']


    def create(self,request,*args,**kwargs):
        if request.data.get('money') == '':
            raise MoneyNull
            
        user_id = self.get_user_id(request)
        data = {
            'money': request.data.get('money'),
            'memo': request.data.get('memo'),
            'user': user_id,
        }
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
        