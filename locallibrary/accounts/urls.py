from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path("register/", views.register_request, name="register"),
                  path("login/", views.login_request, name="login"),
                  path("logout/", views.logout_request, name="logout"),
                  path("<username>/", views.user_settings, name="user"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
