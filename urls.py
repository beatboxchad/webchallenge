from django.urls import include, path
from django.contrib import admin
from shops import urls

urlpatterns = [
    path('/shops/', include('shops.urls')),
    path('admin/', admin.site.urls),
]
