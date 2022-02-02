from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


@login_required(login_url='/accounts/login')
def home(request):
    create_template()
    return render(request=request, template_name="home.html")


@login_required(login_url='/accounts/login')
def create(request):
    create_template()
    return render(request=request, template_name="create.html")


@login_required(login_url='/accounts/login')
def messenger(request):
    create_template()
    return render(request=request, template_name="messenger.html")


def create_template():
    post_shell = render_to_string("post_temp.html")
    print(post_shell)
