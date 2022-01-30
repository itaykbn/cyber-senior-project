from django.db import models
from datetime import date

from django.core.files.storage import FileSystemStorage


class Author(models.Model):
    user_name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.user_name


image_store = FileSystemStorage(location='/tmp/images')


class Entry(models.Model):
    username = models.TextField(Author)

    headline = models.CharField(max_length=255)
    image_path = models.ImageField(storage=image_store)
    body_text = models.TextField()

    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)

    commentors = models.ManyToManyField(Author)

    number_of_comments = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.headline

# Create your models here.
