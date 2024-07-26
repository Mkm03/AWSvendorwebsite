from django.db import models
from django.contrib.auth.models import User


class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    pdf = models.FileField(upload_to='products/pdfs/', null=True, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    USER_ROLES = [
        ('vendor', 'Vendor'),
        ('user', 'User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_view = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
