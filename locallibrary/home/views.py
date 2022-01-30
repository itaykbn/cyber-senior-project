from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template


@login_required(login_url='/accounts/login')
def home(request):
    create_template()
    return render(request=request, template_name="home.html")


def create_template():
    shell = get_template("Entry.html")
    with open(shell) as file:
        print(file)



