from shops.serializers import UserSerializer, ShopSerializer
from shops.permissions import IsSuperUserOrReadOnly
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets
from shops.models import Shop


User = get_user_model()


def index(request):
    return render(request, 'shops/index.html')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsSuperUserOrReadOnly,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
