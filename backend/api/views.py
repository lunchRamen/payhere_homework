import jwt
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView

from .serializers import *
from .exceptions import *
from .models import AccountBook

# Create your views here.


class AccountBookViewSet(ModelViewSet):
    queryset = AccountBook.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field='accountbook_id'

    def get_serializer_class(self):
        if self.action == 'list':
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
        elif request.data.get('money') == '0':
            raise MoneyZero
            
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
    
    def list(self,request,*args,**kwargs):
        user_id = self.get_user_id(request)
        queryset = AccountBook.objects.filter(user__id = user_id)
        serializer = self.get_serializer(queryset, many = True)
        
        return Response(serializer.data, status = status.HTTP_200_OK)

    def get_object(self):
        try:
            obj = AccountBook.objects.get(pk = self.kwargs["accountbook_id"])
        except Exception:
            raise NoAccountBook
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        user_id = self.get_user_id(request)
        if request.data["money"] == "0":
            raise MoneyZero
        data = {
            "money":request.data["money"],
            "memo":request.data["memo"],
            "user":user_id
        }
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

class AccountBookCopyCreateAPIView(CreateAPIView):
    queryset = AccountBook.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field='accountbook_id'
    serializer_class = AccountBookCreateSerializer

    def get_object(self):
        try:
            obj = AccountBook.objects.get(pk = self.kwargs["accountbook_id"])
        except Exception:
            raise NoAccountBook
        return obj

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            "money": instance.money,
            "memo": instance.memo,
            "user": instance.user.id
        }
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        

    
        