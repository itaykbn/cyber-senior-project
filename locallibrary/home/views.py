import datetime
from uuid import uuid4

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from .forms import PostForm
from .process_image import process_image

PostDB = apps.get_model('home', 'Post')
UserDB = apps.get_model('accounts', 'User')

post_chunk = 20


def create_post_list(index, posts, post_type):
    new_posts = [None] * 20

    n_objects = posts.count()

    print("--------------------objects " + str(post_type))
    for i in range(post_chunk):
        if index + i >= n_objects:
            if post_type == "home":
                print("--------------------index in " + str(i))
                overlapped_index = (index + i) % n_objects
                new_posts[i] = posts[overlapped_index]
        else:
            print("--------------------index out " + str(i))
            new_posts[i] = posts[index + i]

    return new_posts


def ajax_query(request):
    if request.method == 'GET':
        index = request.GET.get('index', None)
        print("------------------index_number - - - - " + index)

        create_post = None
        posts = None
        finish = 0

        if request.GET.get('type', None) == "home":

            create_post = create_home_post
            posts = create_post_list(int(index), PostDB.objects.all(), "home")

        elif request.GET.get('type', None) == "profile":
            create_post = create_user_post
            post_list = PostDB.objects.filter(user_id=request.user.id).order_by('published')
            posts = create_post_list(int(index), post_list, "profile")

            if int(index) + post_chunk > post_list.count():
                finish = 1

        htmls = []

        for post in posts:
            if post is not None:
                htmls.append(create_post(post))

        context = {'HTMLS': htmls, 'finish': finish}

        # print(context, len(context['HTMLS']))

        return JsonResponse(context)


def cum_on_all():
    path_root = "C:\\Users\\ItayK\\Documents\\dev\\python\\cyber-senior-project\\locallibrary\\"
    PostDB = apps.get_model('home', 'Post')
    for post in PostDB.objects.all():
        img_path = post.img
        categories = process_image(path_root + img_path.replace("/", "\\"))
        save_into_categories(categories, post.id)


def save_into_categories(categories, post_id):
    CategoriesDB = apps.get_model('home', 'Categories')
    PostDB = apps.get_model('home', 'Post')

    categories = categories.split("#")
    categories = list(filter(lambda a: a != "", categories))
    print(categories)

    for categorie in categories:
        post = PostDB.objects.get(id=post_id)
        CategoriesDB.objects.create(id=f"{post.id}|{categorie}", post=post, categorie=categorie)


# create
@login_required(login_url='/accounts/login')
def select(request):
    user = request.user
    # naive = datetime.datetime(1999, 4, 6, 12, 4, 2)
    # get_delta_time(make_aware(naive, timezone=pytz.timezone("UTC")))
    # get_delta_time(PostDB.objects.get(id="2022318bb8458a").published)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
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
        'form': form,
        "profile_pic": user.profile_pic
    }
    return render(request, "create.html", context)


# home

def hood():
    from .click_house_link import ClickHouseService

    click_service = ClickHouseService.instance()

    click_service.execute('CREATE TABLE user_activity ('
                          'likes UInt8,'
                          'step_in UInt8, '
                          'category String, '
                          'post_id String, '
                          'user_id String) ENGINE = MergeTree '
                          'PARTITION BY tuple() ORDER BY (user_id,post_id,step_in)')


@login_required(login_url='/accounts/login')
def home(request):
    user = request.user

    # hood()

    context = {
        "profile_pic": user.profile_pic
    }

    return render(request=request, template_name="home.html", context=context)


def redirect_to_post_page(request, post_id=None):
    if PostDB.objects.filter(id=post_id).exists():
        user = request.user
        print("im in redirect_to_post_page ")
        print(request.user.profile_pic)
        base_html = render_to_string("post_preview.html")

        html = create_home_post(PostDB.objects.get(id=post_id))

        div_code_1 = '''<div class="profile-img">
                <!-- Profile icon start  -->
                <div> <span style="width:22px;height:22px; border: 1px solid #fafafa;">
                            <img style="width:22px;height:22px;border-radius: 100%;" src=""
                                 alt="">
                        </span>
                </div>'''

        replace_div_code_1 = f'''<div class="profile-img">
                <!-- Profile icon start  -->
                <div> <span style="width:22px;height:22px; border: 1px solid #fafafa;">
                            <img style="width:22px;height:22px;border-radius: 100%;" src="{user.profile_pic}"
                                 alt="">
                        </span>
                </div>'''

        div_code_2 = '''<a href="/profile/">Profile</a>'''

        replace_div_code_2 = f'''<a href="/profile/{user.username}">Profile</a>'''

        print(f"\n\n\n helllllo {replace_div_code_2} \n\n\n")

        base_html = base_html.replace("{post stuff}", html)
        base_html = base_html.replace(div_code_1, replace_div_code_1)
        base_html = base_html.replace(div_code_2, replace_div_code_2)

        print(base_html)

        # print(base_html)

        return HttpResponse(base_html)
    return redirect('/')


def get_delta_time(publish_time):
    time_delta = timezone.now() - publish_time

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


# profile

@login_required(login_url='/accounts/login')
def profile(request, username=None):
    user = request.user
    if request.user.username == username:
        context = {
            "profile_pic": user.profile_pic,
            "username": user.username,
            "posts": 0,
            "followers": 0,
            "following": 0,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio
        }

        return render(request=request, template_name="profile.html", context=context)

    return redirect('/')


@login_required(login_url='/accounts/login')
def edit_profile(request, username=None):
    user = request.user
    context = {
        "profile_pic": user.profile_pic,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user.bio
    }
    if request.method == "POST":
        form = ResgistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            return redirect("/accounts/login/")
    else:
        form = ResgistrationForm()
        # messages.error(request, "Unsuccessful registration. Invalid information.")
    form_dict = {"form": form}
    return render(request=request, template_name="edit_profile.html", context=context)



def create_user_post(user_obj):
    image = user_obj.img
    likes = 0
    comments = 0

    post_html = render_to_string("profile_post_temp.html")

    replace_array = [image, likes, comments]

    for item in replace_array:
        # print(item)
        post_html = post_html.replace("{}", str(item), 1)

    return post_html


def create_home_post(post_obj):
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

    replace_array = [post_obj.id, user_pfp_path, user_username, post_img_path, 0, user_username, post_caption,
                     post_uploaded]

    # print(replace_array)

    for item in replace_array:
        # print(item)
        post_html = post_html.replace("{}", str(item), 1)

        # print(post_html)

    return post_html
