import datetime
from uuid import uuid4

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt

from .forms import PostForm, CommentForm

from .click_house_link import ClickHouseService

PostDB = apps.get_model('home', 'Post')
UserDB = apps.get_model('accounts', 'User')
FollowDB = apps.get_model('home', 'HumanConnections')
CategoryDB = apps.get_model('home', 'Categories')
CommentsDB = apps.get_model('home', 'Comments')

click_db = ClickHouseService.instance()
post_chunk = 20


def create_post_list(index, posts, post_type):
    new_posts = [None] * 20

    n_objects = len(posts)

    for i in range(post_chunk):
        if index + i >= n_objects:
            if post_type == "home":
                overlapped_index = (index + i) % n_objects
                new_posts[i] = posts[overlapped_index]
        else:
            new_posts[i] = posts[index + i]

    return new_posts


def get_post_category(post):
    categories = CategoryDB.objects.filter(post=post)
    cat_string = ""
    for category in categories:
        cat_string += category.categorie
        cat_string += "#"
    return cat_string[:-1]


def click_execute(query):
    result = click_db.execute(query)
    return result


def shuffle_recommended(wanted, rest):
    recommended = []
    rest = list(rest)
    counter = 0
    for obj in wanted:
        recommended.append(obj.post)
        if counter % 3 == 0:
            recommended.append(rest.pop(0).post)
            recommended.append(rest.pop(0).post)
        counter += 1

    for obj in rest:
        recommended.append(obj.post)

    return recommended


def ajax_query(request):
    user = request.user

    if request.method == 'GET':
        try:
            user_prof = UserDB.objects.get(username=request.GET.get('username', None))
        except:
            user_prof = request.user
        index = request.GET.get('index', None)

        create_post = None
        posts = None
        finish = 0

        if request.GET.get('type', None) == "home":
            categories = user.categories.split("#")

            cat_num = len(categories)

            if cat_num == 1:
                wanted_objects = CategoryDB.objects.filter(categorie=categories[0])
                unwanted_objects = CategoryDB.objects.filter(~Q(categorie=categories[0]))
            elif cat_num == 2:
                wanted_objects = CategoryDB.objects.filter(Q(categorie=categories[0]) | Q(categorie=categories[1]))
                unwanted_objects = CategoryDB.objects.filter(~Q(categorie=categories[0]) & ~Q(categorie=categories[1]))

            else:
                wanted_objects = CategoryDB.objects.filter(
                    Q(categorie=categories[0]) | Q(categorie=categories[1]) | Q(categorie=categories[2]))
                unwanted_objects = CategoryDB.objects.filter(
                    ~Q(categorie=categories[0]) & ~Q(categorie=categories[1]) & ~Q(categorie=categories[2]))

            recommended = shuffle_recommended(wanted_objects, unwanted_objects)

            create_post = create_home_post
            posts = create_post_list(int(index), recommended, "home")

        elif request.GET.get('type', None) == "profile":
            create_post = create_user_post
            post_list = PostDB.objects.filter(user_id=user_prof.id).order_by('published')
            posts = create_post_list(int(index), post_list, "profile")

            if int(index) + post_chunk > post_list.count():
                finish = 1

        htmls = []
        for post in posts:
            if post is not None:
                htmls.append(create_post(post, request.user))

        context = {'HTMLS': htmls, 'finish': finish}

        return JsonResponse(context)

    elif request.method == 'POST':
        request_type = request.POST.get('type', None)

        if request_type == 'like':
            value = int(request.POST.get('value', None))
            post_id = request.POST.get('post_id', None)

            post = PostDB.objects.get(id=post_id)

            query_string = click_db.insert(user.id, post.id, get_post_category(post), value,
                                           0)
            click_execute(query_string)
            return HttpResponse()

        elif request_type == 'step_in':
            value = int(request.POST.get('value', None))
            post_id = request.POST.get('post_id', None)
            post = PostDB.objects.get(id=post_id)
            query_string = click_db.insert(user.id, post.id, get_post_category(post), 0, value)
            click_execute(query_string)

            return HttpResponse()

        elif request_type == 'follow':
            username = request.POST.get('username', None)
            value = request.POST.get('value', None)

            followed = UserDB.objects.get(username=username)

            if int(value) > 0:
                FollowDB.objects.create(id=create_id(), follower=user, followed=followed)
            elif int(value) < 0:
                FollowDB.objects.filter(follower=user, followed=followed).delete()

            return HttpResponse()


def autocomplete(request):
    username = request.GET.get('username')

    payload = []
    if username:
        matching_objs = UserDB.objects.filter(username__icontains=username)

        for obj in matching_objs:
            payload.append(obj.username)

    return JsonResponse({'status': 200, 'data': payload})


def save_into_categories(categories, post_id):
    CategoriesDB = apps.get_model('home', 'Categories')
    PostDB = apps.get_model('home', 'Post')

    categories = categories.split("#")
    categories = list(filter(lambda a: a != "", categories))

    for categorie in categories:
        post = PostDB.objects.get(id=post_id)
        CategoriesDB.objects.create(id=f"{post.id}|{categorie}", post=post, categorie=categorie)


# create
@login_required(login_url='/accounts/login')
def select(request):
    user = request.user

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            form.cleaned_data['user_id'] = request.user.id
            form.save()

            return redirect("/")
    else:
        form = PostForm()
    context = {
        'form': form,
        "profile_pic": user.profile_pic
    }
    return render(request, "create.html", context)


# home

@login_required(login_url='/accounts/login')
def home(request):
    user = request.user

    context = {
        "profile_pic": user.profile_pic
    }

    return render(request=request, template_name="home.html", context=context)


def redirect_to_post_page(request, post_id=None):
    if PostDB.objects.filter(id=post_id).exists():
        user = request.user
        post = PostDB.objects.get(id=post_id)
        post_html = create_home_post(post, user, post_id)

        context = {
            "profile_pic": user.profile_pic,
            "post": post_html,
        }
        return render(request=request, template_name="post_page.html", context=context)
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
    if request.user.username == username:
        user = request.user

        followers = FollowDB.objects.filter(followed=user).count
        following = FollowDB.objects.filter(follower=user).count
        posts = PostDB.objects.filter(user=user).count

        context = {
            "profile_pic": user.profile_pic,
            "username": user.username,
            "posts": posts,
            "followers": followers,
            "following": following,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio,
            "show": False
        }

        return render(request=request, template_name="profile.html", context=context)
    else:
        user = None
        try:
            user = UserDB.objects.get(username=username)
        except:
            redirect("/")
        if user:
            followers = FollowDB.objects.filter(followed=user).count
            following = FollowDB.objects.filter(follower=user).count
            posts = PostDB.objects.filter(user=user).count

            is_following = FollowDB.objects.filter(follower=request.user, followed=user).exists()

            context = {
                "profile_pic": request.user.profile_pic,
                "username": user.username,
                "posts": posts,
                "followers": followers,
                "following": following,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": user.bio,
                "show": True,
                "is_follow": is_following
            }

            return render(request=request, template_name="profile.html", context=context)
    return redirect("/")


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

    return render(request=request, template_name="edit_profile.html", context=context)


def get_likes(post_id):
    query_string = click_db.select("user_activity",
                                   where=f"(post_id = '{post_id}')",
                                   select_list=["sum(likes) AS likes"]
                                   )
    click_result = click_execute(query_string)

    if click_result:
        likes = click_result[0][0]
    else:
        likes = 0

    return likes


def am_i_like(user_id, post_id):
    query_string = click_db.select("user_activity",
                                   where=f"(post_id = '{post_id}') AND (user_id = '{user_id}')",
                                   select_list=["sum(likes) AS likes"]
                                   )

    click_result = click_execute(query_string)

    if click_result:
        likes = click_result[0][0]
    else:
        likes = 0

    if likes != 0:
        return True
    return False


def create_user_post(post_obj, user):
    post_id = post_obj.id
    image = post_obj.img
    likes = get_likes(post_id)

    comments = CommentsDB.objects.filter()
    comments = 0
    post_html = render_to_string("profile_post_temp.html")

    replace_array = [post_id, image, likes, comments]

    for item in replace_array:
        post_html = post_html.replace("{}", str(item), 1)

    return post_html


def create_home_post(post_obj, user, post_id=None):
    likes_svgs = [
        '<svg aria-label="Unlike" class="_8-yf5 " color="#ed4956" fill="#ed4956" height="24" role="img" viewBox="0 0 48 48" width="24"><path d="M34.6 3.1c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5s1.1-.2 1.6-.5c1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path></svg>',
        '<svg aria-label="Like" class="_8-yf5 " color="#262626" fill="#262626" height="24" role="img" viewBox="0 0 24 24" width="24"><path d="M16.792 3.904A4.989 4.989 0 0121.5 9.122c0 3.072-2.652 4.959-5.197 7.222-2.512 2.243-3.865 3.469-4.303 3.752-.477-.309-2.143-1.823-4.303-3.752C5.141 14.072 2.5 12.167 2.5 9.122a4.989 4.989 0 014.708-5.218 4.21 4.21 0 013.675 1.941c.84 1.175.98 1.763 1.12 1.763s.278-.588 1.11-1.766a4.17 4.17 0 013.679-1.938m0-2a6.04 6.04 0 00-4.797 2.127 6.052 6.052 0 00-4.787-2.127A6.985 6.985 0 00.5 9.122c0 3.61 2.55 5.827 5.015 7.97.283.246.569.494.853.747l1.027.918a44.998 44.998 0 003.518 3.018 2 2 0 002.174 0 45.263 45.263 0 003.626-3.115l.922-.824c.293-.26.59-.519.885-.774 2.334-2.025 4.98-4.32 4.98-7.94a6.985 6.985 0 00-6.708-7.218z"></path></svg>']

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

    likes = get_likes(post_obj.id)

    is_like = am_i_like(user.id, post_obj.id)

    if is_like:
        svg = likes_svgs[0]
    else:
        svg = likes_svgs[1]

    if post_id:
        comment_html = f"<iframe src='/{post_id}/comment'></iframe>"
    else:
        comment_html = ""
    replace_array = [post_obj.id, is_like, user_pfp_path, user_username, post_img_path, svg, likes, user_username,
                     post_caption,
                     post_uploaded, comment_html]

    for item in replace_array:
        post_html = post_html.replace("{}", str(item), 1)

    return post_html


@login_required(login_url='accounts/login')
@xframe_options_exempt
def comment(request, post_id):
    user = request.user

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.pre_save(user.id, post_id)
            form.save()
            return redirect(f"/{post_id}/comment")
    else:
        form = CommentForm()
    context = {
        'form': form,
        "post_id": post_id,
        "comments": get_comments(post_id)
    }
    return render(request=request, template_name="comments.html", context=context)


def get_comments(post_id):
    comments = CommentsDB.objects.filter(post=post_id)
    html = "<div class='wrapper'>"
    for _comment in comments:
        html += f"<p class='description'> <span>{_comment.user.username}</span>{_comment.comment}</p>"

    html += "</div>"

    return html
