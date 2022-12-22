from rest_framework import serializers

from .models import AccountBook


class AccountBookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBook
        fields = '__all__'

class AccountBookGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBook
        fields = '__all__'
class AccountBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBook
        fields = '__all__'

class AccountBookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBook
        fields = '__all__'
class AccountBookDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBook
        fields = '__all__'
    
    