from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework import viewsets
from shops.models import Shop
from shops.serializers import (
    UserSerializer,
    GroupSerializer,
    ShopSerializer
)

User = get_user_model()


def index(request):
    return render(request, 'shops/index.html')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ShopViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
