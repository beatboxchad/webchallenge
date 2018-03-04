from django.contrib.auth.models import AbstractUser
from django.db import models


class Shop(models.Model):
    title = models.CharField('name of shop', max_length=200)


class User(AbstractUser):
    shops = models.ManyToManyField(Shop)
