from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login')
def home(request):
    return render(request=request, template_name="home.html")


