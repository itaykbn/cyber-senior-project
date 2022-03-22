from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
import datetime
from django import forms

from django.conf import settings

default_pfp = str(settings.MEDIA_URL) + "profile_pics/default.png"


def create_id():
    now = datetime.datetime.now()
    return str(now.year) + str(now.month) + str(now.day) + str(uuid4())[:7]


# Create your models here.
class User(AbstractUser):
    app_label = 'accounts'
    id = models.CharField(primary_key=True, default=create_id, editable=False, max_length=100)
    profile_pic = models.CharField(max_length=200, default=default_pfp)
    bio = models.CharField(max_length=800)
