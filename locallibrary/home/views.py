import datetime
from uuid import uuid4
from django.apps import apps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from rest_framework.decorators import api_view

from .forms import PostForm


@login_required(login_url='/accounts/login')
def home(request):
    create_template()
    return render(request=request, template_name="home.html")


# create
@login_required(login_url='/accounts/login')
@api_view(['GET', 'POST'])
def select(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            uri = form.cleaned_data['uri']
            description = form.cleaned_data['description']
            form.cleaned_data['user_id'] = request.user.id
            form.save()

            print("content------------------" + description)
            print("content------------------" + request.user.id)

            return redirect("/")
        print(form.errors)

    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, "create.html", context)


def style(request):
    pass


# messenger

def create_template():
    post_shell = render_to_string("post_temp.html")

    # get data_from_db

    post = post_shell
    return post


PostDB = apps.get_model('home', 'Post')
UserDB = apps.get_model('accounts', 'User')


def create_post_from_src(img_path, caption, published, ):
    PostDB.objects.create(id=create_id(), img=img_path, )


def create_id():
    now = datetime.datetime.now()
    return str(now.year) + str(now.month) + str(now.day) + str(uuid4())[:7]
