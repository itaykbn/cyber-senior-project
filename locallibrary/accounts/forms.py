import datetime
import os

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.apps import apps
from django.contrib.auth.hashers import make_password

from django.conf import settings

from .models import User


# Create your forms here.

class UpdateUserData(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_pic = forms.FileField(required=False)

    class Meta:
        model = apps.get_model('accounts', 'User')
        fields = ("bio", "username", "first_name", "last_name", "email", "password1", "password2")

    def pre_save(self, prev_username, prev_email):
        self.values_dict = {}

        self.values_dict['prev_username'] = prev_username
        self.values_dict['prev_email'] = prev_email

    def save_img(self, file):

        print(f"file recruiter {file}")
        save_dir = str(settings.MEDIA_ROOT) + "/profile_pics"

        url_DB = str(settings.MEDIA_URL) + "profile_pics"

        name = f"sociocode_{str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))}{len(os.listdir(save_dir))}"
        with open(f'{save_dir}/{name}.png', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        print(f'{url_DB}/{name}.png')

        return f'{url_DB}/{name}.png'

    def clean(self, ):
        cleaned_data = super(UpdateUserData, self).clean()
        DB = self.Meta.model

        cleaned_data["bio"] = cleaned_data.get('bio').strip()

        raw_file = cleaned_data.get('profile_pic')
        if raw_file is not None:
            self.save_img(raw_file)
            cleaned_data["profile_pic"] = self.save_img(cleaned_data.get('profile_pic'))
        else:
            cleaned_data["profile_pic"] = None

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        user_exists = DB.objects.filter(username=username)
        email_exists = DB.objects.filter(email=email)

        prev_username = self.values_dict["prev_username"]
        prev_email = self.values_dict["prev_email"]

        if user_exists and username != prev_username:
            raise forms.ValidationError(f'Username "{username}" is already in use.')

        elif email_exists and email != prev_email:
            raise forms.ValidationError(f'Email "{email}" is already in use.')

        return cleaned_data

    def save(self, commit=True):
        user = super(UpdateUserData, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        print(user.first_name)
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"][:-1]
        user.profile_pic = self.cleaned_data["profile_pic"]
        user.bio = self.cleaned_data["bio"]

        prev_user = User.objects.get(username=self.values_dict["prev_username"])

        prev_user.username = user.username
        prev_user.email = user.email
        prev_user.first_name = user.first_name
        prev_user.last_name = user.last_name
        prev_user.password = user.password
        prev_user.bio = user.bio
        if user.profile_pic is not None:
            prev_user.profile_pic = user.profile_pic
        print(prev_user.last_name)

        if commit:
            prev_user.save()
        return prev_user


class ResgistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = apps.get_model('accounts', 'User')
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean(self, ):
        cleaned_data = super(ResgistrationForm, self).clean()
        DB = self.Meta.model

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        user_exists = DB.objects.filter(username=username)
        email_exists = DB.objects.filter(email=email)

        if user_exists:
            raise forms.ValidationError(f'Username "{username}" is already in use.')

        elif email_exists:
            raise forms.ValidationError(f'Email "{email}" is already in use.')

        return cleaned_data

    def save(self, commit=True):
        user = super(ResgistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]

        if commit:
            user.save()
        return user


'''
class UpdateUserData(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, data=None):
        super().__init__(data)
        self.values_dict = {}

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean(self, ):
        cleaned_data = super(UpdateUserData, self).clean()
        print(cleaned_data)
        DB = self.Meta.model
        prev_username = self.values_dict["prev_username"]
        print(f"*balls* prev : {prev_username}")
        prev_email = self.values_dict["prev_email"]

        username = self.values_dict["username"]
        print(f"*balls* curr : {username}")
        email = cleaned_data.get('email')

        password1 = self.values_dict["password1"]
        password2 = self.values_dict["password2"]

        user_exists = DB.objects.filter(username=username)
        email_exists = DB.objects.filter(email=email)

        cleaned_data["password"] = password1
        cleaned_data["username"] = username

        if password1 != password2:
            raise forms.ValidationError(f"passwords don't match")

        if user_exists and prev_username != username:
            raise forms.ValidationError(f'Username "{username}" is already in use ff.')

        elif email_exists and prev_email != email:
            raise forms.ValidationError(f'Email "{email}" is already in use.')

        return cleaned_data

    def pre_save(self, prev_username, prev_email, password1, password2, username):
        self.values_dict["username"] = username
        self.values_dict['prev_username'] = prev_username
        self.values_dict['prev_email'] = prev_email
        self.values_dict['password1'] = password1
        self.values_dict['password2'] = password2

    def save(self, commit=True):
        cleaned_data = super(UpdateUserData, self).clean()
        print("prev user")
        prev_username = self.values_dict['prev_username']

        prev_user = User.objects.get(username=prev_username)
        print(prev_user)

        user = super(UpdateUserData, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]
        user.password = self.cleaned_data["password"]
        print("============version2")
        print(cleaned_data)
        prev_user.email = user.email
        prev_user.first_name = user.first_name
        prev_user.last_name = user.last_name
        prev_user.username = user.username
        prev_user.password = make_password(user.password)

        if commit:
            prev_user.save()
'''
# class UpdateProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("uri", "description")
