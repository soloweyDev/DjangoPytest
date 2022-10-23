from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    image = models.FileField(upload_to='avatars', verbose_name='image')

    @property
    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/img/default.jpg'

    def __str__(self):
        return self.username


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='title')
    description = models.TextField(verbose_name='description')
    image = models.FileField(upload_to='products', verbose_name='image')

    @property
    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
