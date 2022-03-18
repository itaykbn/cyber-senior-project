from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import ResgistrationForm


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
        #print(form.errors)
        messages.error(request, "Unsuccessful registration. Invalid information.")
        form = AuthenticationForm()

    form_dict = {"form": form}

    return render(request=request, template_name="registration/login.html", context=form_dict)


def logout_request(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
