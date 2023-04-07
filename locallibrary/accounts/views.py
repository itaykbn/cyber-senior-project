from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import ResgistrationForm, UpdateUserData


def register_request(request):
    if request.method == "POST":
        form = ResgistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, "Registration successful.")
            return redirect("/accounts/login/")
    else:
        form = ResgistrationForm()
        # messages.error(request, "Unsuccessful registration. Invalid information.")
    form_dict = {"form": form}
    return render(request=request, template_name="registration/register.html", context=form_dict)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "Login successful.")
            print("hello")
            return redirect("/")
    else:
        messages.error(request, "Unsuccessful registration. Invalid information.")
        form = AuthenticationForm()

    form_dict = {"form": form}

    return render(request=request, template_name="registration/login.html", context=form_dict)


def logout_request(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')


@login_required(login_url='/accounts/login')
def user_settings(request, username=None):
    prev_user = request.user

    if username == prev_user.username:

        if request.method == "POST":
            post_data = request.POST
            post_data._mutable = True
            post_data['username'] = post_data['username'] + "@"

            form = UpdateUserData(post_data, request.FILES)
            form.pre_save(prev_user.username, prev_user.email)

            if form.is_valid():
                updated_user = form.save()
                login(request, updated_user)
                return redirect("/")
        else:
            form = UpdateUserData()
            # messages.error(request, "Unsuccessful registration. Invalid information.")
        prev_pfp = prev_user.profile_pic
        prev_pfp = prev_pfp.replace("\\", "/")
        form_dict = {
            "profile_pic": prev_pfp,
            "prev_bio": prev_user.bio,
            "prev_pfp": prev_pfp,
            "form": form,
            "prev_last_name": prev_user.last_name,
            "prev_first_name": prev_user.first_name,
            "prev_username": prev_user.username,
            "prev_email": prev_user.email
        }
        return render(request=request, template_name="registration/update_user_data.html", context=form_dict)
    return redirect("/")
