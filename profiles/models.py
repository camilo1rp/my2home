from django.contrib.auth.models import User
from django.db import models


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=30)
    phone = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Client(models.Model):
    # choices for gender
    MALE = 'MA'
    FEMALE = 'FE'
    OTHER = 'OT'
    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    nickname = models.CharField()
    gender = models.CharField(max_length=2, choices=GENDER, default=OTHER)
    city = models.CharField(max_length=30)
    photo = models.ImageField(upload_to="media/", default="media/default.png")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


