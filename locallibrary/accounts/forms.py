from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.apps import apps


# Create your forms here.

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
