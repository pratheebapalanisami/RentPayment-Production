from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
from rent import settings


class Property(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    apt_no = models.CharField(max_length=10)
    property_name = models.CharField(max_length=50)
    rent_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return str(self.apt_no)

class Payment(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=9, decimal_places=2)
    paid_date = models.DateField()

    def __str__(self):
        return str(self.amount_paid)


class MaintenanceRequest(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    priority = models.CharField(max_length=50)
    problem = models.TextField()
    status = models.CharField(max_length=50, default="New")
    resolved_by = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.problem)

