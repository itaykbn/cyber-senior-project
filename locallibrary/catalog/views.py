from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def log_in(request):
    return HttpResponse("login please")
