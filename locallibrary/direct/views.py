from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.template.loader import render_to_string


@login_required(login_url='/accounts/login')
def inbox(request):
    context = {"user": "balls user"}
    return render(request=request, template_name="inbox.html", context=context)
