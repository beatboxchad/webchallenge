from djoser.serializers import UserCreateSerializer \
    as BaseUserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from shops.models import Shop


User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    shops = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='shop-detail'
        )

    class Meta:
        model = User
        fields = ('url', 'email', 'shops', 'is_superuser')


class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = ('url', 'title')


class ShopLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('url', 'title', 'users')

    def update(self, instance, _):

        instance.users.add(self.context['request'].user)
        instance.save()
        return instance


class ShopUnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('url', 'title', 'users')

    def update(self, instance, _):
        instance.users.remove(self.context['request'].user)
        instance.save()
        return instance


class UserShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('shops',)


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('url',
                  'id',
                  'email',
                  'password',
                  'is_superuser')
