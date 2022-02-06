from django import forms


class ImageForm(forms.Form):
    description = forms.CharField(max_length=2200)
    uri = forms.CharField(widget=forms.HiddenInput())
