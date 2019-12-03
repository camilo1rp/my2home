from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    MALE = 'MA'
    FEMALE = 'FE'
    OTHER = 'OT'
    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    nickname = models.CharField(max_length=20, default="none")
    gender = models.CharField(max_length=2, choices=GENDER, default=OTHER)
    city = models.CharField(max_length=30, null=True, blank=True)
    # photo = models.ImageField(upload_to="media/", default="media/default.png")
    company = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance).save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
