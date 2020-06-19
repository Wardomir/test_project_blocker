from django.contrib.auth.models import AbstractUser
from django.db import models


class Administrator(AbstractUser):
    username = models.CharField(max_length=345, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Inquiry(models.Model):
    url = models.URLField()
    reason = models.TextField()
    email = models.EmailField()
    issuer_ip = models.GenericIPAddressField(default='0.0.0.0')
    open_for_review = models.BooleanField(default=True)
    website_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.url

