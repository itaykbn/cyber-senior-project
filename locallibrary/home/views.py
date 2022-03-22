import datetime
from uuid import uuid4

import pytz
from django.apps import apps
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from rest_framework.decorators import api_view

from .forms import PostForm

PostDB = apps.get_model('home', 'Post')
UserDB = apps.get_model('accounts', 'User')


def get_recommendation():
    return ["2022320f8c8ffd", "202232019390c2", "2022318bb8458a"]


def ajax_query(request):
    if request.method == 'GET':
        post_ids = get_recommendation()

        htmls = []

        for post_id in post_ids:
            # print(create_post_by_id(post_id))
            htmls.append(create_post_by_id(post_id))

        context = {'HTMLS': htmls}

        print(context, len(context['HTMLS']))

        return JsonResponse(context)


@login_required(login_url='/accounts/login')
def home(request):
    id1 = "2022318bb8458a"
    id2 = "2022320f8c8ffd"

    post_html = create_post_by_id(id2)

    return render(request=request, template_name="home.html")


# create
@login_required(login_url='/accounts/login')
@api_view(['GET', 'POST'])
def select(request):
    # naive = datetime.datetime(1999, 4, 6, 12, 4, 2)
    # get_delta_time(make_aware(naive, timezone=pytz.timezone("UTC")))
    # get_delta_time(PostDB.objects.get(id="2022318bb8458a").published)
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


def create_post_by_id(post_id):
    post_obj = PostDB.objects.get(id=post_id)
    # print("hooooooooooooooooooooood----------------------------------------------" + str(post_obj.user_id))
    user_obj = UserDB.objects.get(id=post_obj.user_id)

    # plant content
    # post_data
    post_img_path = post_obj.img
    post_caption = post_obj.caption
    post_uploaded = get_delta_time(post_obj.published)

    # user_data

    user_username = user_obj.username
    user_pfp_path = user_obj.profile_pic

    post_html = render_to_string("post_temp.html")

    replace_array = [user_pfp_path, user_username, post_img_path, 0, user_username, post_caption, post_uploaded]

    # print(replace_array)

    for item in replace_array:
        # print(item)
        post_html = post_html.replace("{}", str(item), 1)

        # print(post_html)

    return post_html


def get_delta_time(publish_time):
    time_delta = timezone.now() - publish_time

    delta_msg = ""

    days = time_delta.days
    seconds = time_delta.seconds
    minutes = int(seconds / 60)
    hours = int(minutes / 60)
    weeks = int(days / 7)
    months = int(weeks / 4)
    years = int(months / 12)

    if years > 0:
        delta_msg = f"posted {years} years ago"
    elif months > 0:
        delta_msg = f"posted {months} months ago"
    elif weeks > 0:
        delta_msg = f"posted {weeks} weeks ago"
    elif days > 0:
        delta_msg = f"posted {days} days ago"
    elif hours > 0:
        delta_msg = f"posted {hours} hours ago"
    elif minutes > 0:
        delta_msg = f"posted {minutes} minutes ago"
    else:
        delta_msg = "posted just now"

    return delta_msg


def create_id():
    now = datetime.datetime.now()
    return str(now.year) + str(now.month) + str(now.day) + str(uuid4())[:7]
