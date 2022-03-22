import datetime
import os
import time
from django.utils import timezone

from django import forms
from django.apps import apps

from django.conf import settings


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

        if commit:
            post.save()
        return post


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
