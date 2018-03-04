from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from shops.models import Shop

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'shops')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = ('url', 'title')
