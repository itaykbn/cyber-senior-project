import datetime
import os
import time
from django.utils import timezone

from .process_image import process_image

from django import forms
from django.apps import apps

from django.conf import settings


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('home', 'User')
        fields = ("uri", "description")


class PostForm(forms.ModelForm):
    description = forms.CharField(max_length=2200)
    uri = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = apps.get_model('home', 'Post')
        fields = ("uri", "description")

    def save(self, commit=True):
        UserDB = apps.get_model('accounts', 'User')

        post = super(PostForm, self).save(commit=False)

        img_path = save_img(self.cleaned_data["uri"])

        post.img = img_path
        post.caption = self.cleaned_data["description"]

        # print("-------------user" + post.user)
        post.published = timezone.now()
        post.user = UserDB.objects.get(id=self.cleaned_data["user_id"])

        path_root = settings.MEDIA_ROOT[:-12]
        categories = process_image(path_root + img_path.replace("/", "\\"))

        # add categories

        if commit:
            post.save()
            save_into_categories(categories, post.id)
        return post


def save_into_categories(categories, post_id):
    CategoriesDB = apps.get_model('home', 'Categories')
    PostDB = apps.get_model('home', 'Post')

    categories = categories.split("#")
    categories = list(filter(lambda a: a != "", categories))
    print(categories)

    for categorie in categories:
        post = PostDB.objects.get(id=post_id)
        CategoriesDB.objects.create(id=f"{post.id}|{categorie}", post=post, categorie=categorie)


def save_img(uri):
    from binascii import a2b_base64

    save_dir = str(settings.MEDIA_ROOT) + "/imgs"

    url_DB = str(settings.MEDIA_URL) + "imgs"

    binary_data = a2b_base64(uri)

    name = f"sociocode_{str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))}{len(os.listdir(save_dir))}"

    fd = open(f'{save_dir}/{name}.png', 'wb')
    fd.write(binary_data)
    fd.close()

    return f'{url_DB}/{name}.png'
