from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='listings/', blank=True, null=True)
    price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)