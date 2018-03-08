from shops.serializers import UserSerializer, ShopSerializer
from shops.mixins import ClobberShopListModelMixin
from shops.permissions import IsSuperUserOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, mixins
from django.shortcuts import render
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


class ShopList(ClobberShopListModelMixin,
               mixins.CreateModelMixin,
               mixins.ListModelMixin,
               generics.GenericAPIView):
    permission_classes = (IsSuperUserOrReadOnly,)
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ShopDetail(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
