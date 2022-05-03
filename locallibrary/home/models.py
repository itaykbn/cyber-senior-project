from uuid import uuid4
import datetime
from django.db import models

from django.apps import apps


# Create your models here.
def create_id():
    now = datetime.datetime.now()
    return str(now.year) + str(now.month) + str(now.day) + str(uuid4())[:7]


def get_model(app, model_name):
    return apps.get_model(app, model_name)


# mysql models
class Post(models.Model):
    app_label = 'home'
    id = models.CharField(primary_key=True, default=create_id, editable=False, max_length=100)
    img = models.CharField(max_length=200, null=False)
    caption = models.CharField(max_length=1000, null=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    published = models.DateTimeField(default=datetime.datetime.now())


class Categories(models.Model):
    app_label = 'home'
    post = models.ForeignKey('home.Post', on_delete=models.CASCADE)
    categorie = models.CharField(max_length=200, null=True)
    id = models.CharField(primary_key=True, editable=False, max_length=100)


class HumanConnections(models.Model):
    app_label = 'home'
    follower = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='followed')
    id = models.CharField(primary_key=True, editable=False, max_length=100)


class Comments(models.Model):
    id = models.CharField(primary_key=True, default=create_id, editable=False, max_length=100)
    comment = models.CharField(max_length=1000, null=False)
    post = models.ForeignKey('home.Post', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)



