from django.conf.urls import url, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', include(router.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^api/shops/$',
        views.ShopList.as_view(),
        name='shops-list'),
    url(r'^api/shops/(?P<pk>[0-9]+)/$',
        views.ShopDetail.as_view(),
        name='shop-detail'),

]
