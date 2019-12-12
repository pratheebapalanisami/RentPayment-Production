from django.contrib.auth.models import AbstractUser
from django.db import models

from rent import settings
from rentapp.models import Property


class CustomUser(AbstractUser):
   pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.OneToOneField(Property, on_delete=models.CASCADE, null= True, blank= True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=50)
    is_tenant = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)





