from djoser.serializers import UserCreateSerializer \
    as BaseUserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from shops.models import Shop


User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'email', 'shops', 'is_superuser')


class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = ('url', 'title')


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('url',
                  'id',
                  'email',
                  'password',
                  'is_superuser')
