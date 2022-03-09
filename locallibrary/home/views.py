from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
from .forms import ImageForm


@login_required(login_url='/accounts/login')
def home(request):
    create_template()
    return render(request=request, template_name="home.html")


# create
@login_required(login_url='/accounts/login')
@api_view(['GET', 'POST'])
def select(request):
    if request.method == "POST":
        form = ImageForm(request.POST)
        if form.is_valid():
            uri = form.cleaned_data['uri']
            description = form.cleaned_data['description']

            print("content------------------" + description)

            return redirect("/")
    else:
        form = ImageForm()
    context = {
        'form': form
    }
    return render(request, "create.html", context)


def style(request):
    pass


# messenger

def create_template():
    post_shell = render_to_string("post_temp.html")

    #get data_from_db

    post = post_shell
    return post
