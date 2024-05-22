from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=12, null=True)
    is_new = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    username = None
   
    is_admin = models.BooleanField('Is Admin', default=False)
    is_comercial = models.BooleanField('Is Comercial', default=False)
    is_client_particulier = models.BooleanField('Is Partner', default=False)
    is_client_groupe = models.BooleanField('Is Partner', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


