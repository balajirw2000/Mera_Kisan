from django.db import models
from django.contrib.auth.models import User
import random
class Mobile(models.Model):

    username = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=10)


# Create your models here


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=12)
    otp = models.CharField(max_length=6)

class Type(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=12)
    type = models.CharField(max_length=40)
    username = models.CharField(max_length=1000,default="")
